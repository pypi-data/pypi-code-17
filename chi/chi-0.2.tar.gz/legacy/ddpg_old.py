import tensorflow as tf
import numpy as np
from flow.memory import ReplayMemory
from flow.agent import Agent
import flow.tensorfun as fn
from tensorflow.contrib import layers

# TODO: make command line options
discount = .99
pl2 = .0
ql2 = .01
lrp = .0001
lrq = .001
rm_size = 1000000
rm_dtype = 'float32'


from tensorflow.train import AdamOptimizer

@chi.model(optimizer=MAO(AdamOptimizer(.001), 1-0.001))
def pp(o):
  h1 = layers.fully_connected(o, 300)
  h2 = layers.fully_connected(h1, 300)
  h3 = layers.fully_connected(h2, 300)
  tf.train.AdamOptimizer(0.001)

  return h3

@chi.model(optimizer=MAO(AdamOptimizer(.001), 1-0.001))
def actor(s, noisevar):
  a = layers.fully_connected(s, dima)
  n = tf.get_local_variable()
  an = noise(a, n, noisevar)

@chi.model(optimizer=MAO(AdamOptimizer(.0001), 1-0.001))
def critic(s, a):
  q = layers.fully_connected(s, 1, tf.identity)
  q = q + layers.fully_connected(a, 1, tf.identity)
  return q

class DdpgBaseAgent(Agent):
  """
  Args:
    **kwargs:
      env: an gym.Env
      session: a tf.Session
  """

  flags = Agent.flags.get_child()
  flags.async = False, 'update policy and q function concurrently'
  flags.tau = .001, 'target network'
  flags.bsize = 32, 'batch size'
  flags.warmup = 10000
  flags.async = False


  def __init__(self, pp, ac, cr):
    from chi import Model, function
    from tensorflow.contrib.opt import MovingAverageOptimizer as MAO
    from tensorflow.train import AdamOptimizer

    pp = Model(pp, optimizer=MAO(AdamOptimizer(.001), 1-0.001))
    ac = Model(ac, optimizer=MAO(AdamOptimizer(.001), 1-0.001))
    cr = Model(cr, optimizer=MAO(AdamOptimizer(.001), 1-0.001))
    self.ac = fun(ac(pp, noisevar=.5))

    @function(logdir='')
    def train(o:(-1,),a,r,t:bool,o2):
      s = pp(o)
      q = cr(s, ac(s, noisevar=0.))

      q = cr(s, a)
      s2 = ppt(o2)
      q2 = crt(s2, act(s))
      qt = tf.cond(t, lambda: r, lambda: r + 0.99 * q2)
      mse = tf.square(q-qt)

      return ac.minimize(-q), cr.minimize(mse), pp.minimize([-q, mse])

    self.train = fun(train)
    # pl = ac.losses + [-q]  # ac.losses should give REGULARIZATION_LOSSES put into ac.apply

  @fun
  def act(self, o):
    s = self.pp(o)
    a = self.ac(s, noisevar=.5)
    return a


  def act(self, obs):

    a = self.net(obs, noise=0)


  def _build(self):
    # init replay memory
    dim_a = list(self.env.action_space.shape)
    dim_o = list(self.env.observation_space.shape)
    self.rm = ReplayMemory(rm_size, dim_o, dim_a, dtype=np.__dict__[rm_dtype])

    fn.configure(logging_path=self.flags.outdir)

    # create computational graph
    self.actor = fn.Module('actor')
    with fn.module(self.actor):
      state = tf.placeholder(tf.float32, [1] + dim_o)
      action = self.build_actor(state, mode='act')
      # exploration noise
      noise = self.build_noise()
      self.actor_mode = m = get_local_var('mode', 'test')
      action = tf.cond(tf.equal(m, 'test'), lambda: action, lambda: action + noise)
      self.actor.output = action

    self.actor_ema = fn.ExponentialMovingAverage(self.actor.trainable_variables_dict, self.flags.tau)

    self.critic = fn.Module('critic')
    with fn.module(self.critic):
      q = self.build_critic(state, action, mode='act')
      self.critic_ema = fn.ExponentialMovingAverage(self.critic.trainable_variables_dict, self.flags.tau)

    self.train_actor = fn.Module('train_actor')
    with fn.module(self.train_actor):
      self.actor_ema.update()

      state = tf.placeholder(tf.float32)
      with fn.module('actor', reuse_vars=self.actor.trainable_variables_dict):
        action = self.build_actor(state, mode='train')

      with fn.module('critic', reuse_vars=self.critic.trainable_variables_dict):
        q = self.build_critic(state, action, mode='train')

      # training
      # policy loss
      mean_q = tf.reduce_mean(q, 0)
      # TODO: realize weight decay via tf metrics
      wd_p = tf.add_n([pl2 * tf.nn.l2_loss(var) for var in self.actor.trainable_variables])  # weight decay
      loss_p = -mean_q + wd_p

      # policy optimization
      optim_p = tf.train.AdamOptimizer(learning_rate=lrp)
      grads_and_vars_p = optim_p.compute_gradients(loss_p, var_list=self.actor.trainable_variables)
      optimize_p = optim_p.apply_gradients(grads_and_vars_p)
      with tf.control_dependencies([optimize_p]):
        self.train_actor.output = self.actor.update_ops

    self.train_critic = fn.Module('train_critic')
    with fn.module(self.train_critic):
      # q optimization
      state = tf.placeholder(tf.float32)
      action = tf.placeholder(tf.float32, [self.flags.bsize] + dim_a, "act_train")
      rew = tf.placeholder(tf.float32, [self.flags.bsize], "rew")
      term = tf.placeholder(tf.bool, [self.flags.bsize], "term")
      state2 = tf.placeholder(tf.float32, [self.flags.bsize] + dim_o, "state2")
      # q
      with fn.module('critic', reuse_vars=self.critic.trainable_variables_dict):
        q_train = self.build_critic(state, action, mode='train')
        self.critic_ema.update()

      # q targets
      with fn.module('actor_target', reuse_vars=self.actor_ema.averages):
        act2 = self.build_actor(state2, mode='target')

      with fn.module('critic_target', reuse_vars=self.critic_ema.averages):
        q2 = self.build_critic(state2, act2, mode='target')

      q_target = tf.stop_gradient(tf.select(term, rew, rew + discount * q2))
      # q_target = tf.stop_gradient(rew + discount * q2)
      # q loss
      td_error = q_train - q_target
      ms_td_error = tf.reduce_mean(tf.square(td_error), 0)
      # TODO: realize weight decay via tf metrics
      wd_q = tf.add_n([ql2 * tf.nn.l2_loss(var) for var in self.critic.trainable_variables])  # weight decay
      loss_q = ms_td_error + wd_q
      # q optimization
      optim_q = tf.train.AdamOptimizer(learning_rate=lrq)
      grads_and_vars_q = optim_q.compute_gradients(loss_q, var_list=self.critic.trainable_variables)
      optimize_q = optim_q.apply_gradients(grads_and_vars_q)
      with tf.control_dependencies([optimize_q]):
        self.train_critic.output = self.critic.update_ops

  def _reset_(self, **kwargs):
    Agent._reset_(self, **kwargs)
    self.actor.reset()
    fn.set_value(self.actor_mode, kwargs.get("mode", "test"))

  def _act(self, state):
    state = state[np.newaxis, ...]  # add batch dimension
    action = self.actor.run(state)
    return action[0, ...]  # remove batch dimension

  def _perceive(self, state, action, rew, term, next_state):
    if self.mode == "train":
      self.rm.enqueue(state, action, rew, term)

      if self.t_train > self.flags.warmup:

        obs, act, rew, ob2, term2, info = self.rm.sample_batch(size=self.flags.bsize)

        if self.flags.async:
          # TODO: async training
          assert False
        else:
          self.train_critic.run(obs, act, rew, ob2, term2)
          self.train_actor.run(obs)

  def build_actor(self, state, **kwargs):
    """layout for the actor network

    Args:
      state: the agent's state (tf.Tensor)
      **kwargs: further build information e.g. "mode": "act" or "train"

    Returns:
      an action
    """
    raise NotImplementedError()

  def build_critic(self, state, action, **kwargs):
    """layout for the critic network

    Args:
      state: the agent's state (tf.Tensor)
      action: (tf.Tensor)
      **kwargs: further build information

    Returns:
      a value estimate (tf.Tensor)
    """
    raise NotImplementedError()

  def build_noise(self, **kwargs):
    """ ops for additive exploration noise

    Args:

    Returns:
      noise with shape = [batch] + action_shape
    """
    return tf.zeros([None]+self.env.action_space.shape)


class DdpgAgent(DdpgBaseAgent):
  flags = DdpgBaseAgent.flags.get_child()
  flags.noise_sigma = 0.2, ''
  flags.noise_theta = 0.15, ''

  # def _reset_(self, **kwargs):
  #   DdpgBaseAgent._reset_(self, **kwargs)
  #
  #   # set noise variance
  #   val = 0. if kwargs.get('mode') is 'test' else self.flags.noise_sigma
  #   if not hasattr(self, 'noise_sigma_var'):
  #     self.noise_sigma_var = self.actor.get_var('noise_sigma')
  #   fn.set_value(self.noise_sigma_var, val)

  def build_actor(self, state, **kwargs):
    """layout for the actor network

    Args:
      state: the agent's state (tf.Tensor with shape [batch_size, action_size])
      **kwargs: further build information e.g. "explore": True

    Returns:
      an action
    """
    do = self.env.observation_space.shape[0]
    da = self.env.action_space.shape[0]
    l1 = 400  # dm 400
    l2 = 300  # dm 300

    xavier = tf.contrib.layers.xavier_initializer()

    W = tf.get_variable('1w', [do, l1], initializer=xavier)
    b = tf.get_variable('1b', initializer=tf.zeros(l1))
    x = tf.nn.relu(tf.matmul(state, W) + b)

    W = tf.get_variable('2w', [l1, l2], initializer=tf.contrib.layers.xavier_initializer())
    b = tf.get_variable('2b', initializer=tf.zeros(l2))
    x = tf.nn.relu(tf.matmul(x, W) + b)

    uni = tf.random_uniform_initializer(-3e-4, 3e-4)

    W = tf.get_variable('3w', [l2, da], initializer=uni)
    b = tf.get_variable('3b', da, initializer=uni)
    z = tf.matmul(x, W) + b
    action = tf.nn.tanh(z, name='h4-action')
    return action

  def build_noise(self, **kwargs):
    da = self.env.action_space.shape[0]
    noise_init = tf.zeros([1, da])
    noise_var = get_local_var("nm", noise_init)
    # local variables are automatically reset by fn.Module.reset

    ou_theta = get_local_var("ou_theta", self.flags.noise_theta)
    ou_sigma = get_local_var("ou_sigma", self.flags.noise_sigma)

    noise = noise_var.assign_sub(ou_theta * noise_var - tf.random_normal([1, da], stddev=ou_sigma))

    return noise

  def build_critic(self, state, action, **kwargs):
    """layout for the critic network

    Args:
      state: the agent's state (tf.Tensor)
      action: (tf.Tensor)
      **kwargs: further build information

    Returns:
      a value estimate (tf.Tensor)
    """
    dimO = self.env.observation_space.shape[0]
    dimA = self.env.action_space.shape[0]

    l1 = 400  # dm 400
    l2 = 300  # dm 300

    xavier = tf.contrib.layers.xavier_initializer()

    W = tf.get_variable('1w', [dimO, l1], initializer=xavier)
    b = tf.get_variable('1b', initializer=tf.zeros(l1))
    x = tf.nn.relu(tf.matmul(state, W) + b)
    x = tf.concat(1, [x, action])

    W = tf.get_variable('2w', [l1 + dimA, l2], initializer=xavier)
    b = tf.get_variable('2b', initializer=tf.zeros(l2))
    x = tf.nn.relu(tf.matmul(x, W) + b)

    uni = tf.random_uniform_initializer(-3e-4, 3e-4)

    W = tf.get_variable('3w', [l2, 1], initializer=uni)
    b = tf.get_variable('3b', initializer=0.)
    qs = tf.matmul(x, W) + b
    q = tf.squeeze(qs, [1], name='h3-q')

    return q


class DdpgConvAgent(DdpgAgent):
  """

  """

  # TODO: make convolutional version
  def __init__(self):
    assert False


def conv(x, W, b, stride=4):
  c = tf.contrib.layers.conv2d(x_image, filter=W, strides=[1, stride, stride, 1], padding='VALID')
  z = c + b
  y = tf.nn.relu(z)
  return y


if __name__ == "__main__":
  pass
