import chi
import numpy as np
import gym
import tensorflow as tf
from tensorflow.contrib import layers
from chi import Function


class Dqn:
  def __init__(self, env: gym.Env, q_network: chi.Model, memory=None):
    oshape = env.observation_space.shape

    self.env = env
    self.memory = memory or chi.rl.ReplayMemory(1000000, oshape, 1)

    def act(x: [oshape]):
      qs = q_network(x)
      a = tf.argmax(qs, axis=1)
      qm = tf.reduce_max(qs, axis=1)
      layers.summarize_tensor(a)
      return a, qm

    self.act = Function(act)

    def train(o, a: (tf.int32, (None, 1)), r: (None,), t: (tf.bool, (None,)), o2):
      asq = tf.squeeze(a, axis=1)

      q = q_network(o)
      # ac = tf.argmax(q, axis=1)

      # compute targets
      q2 = q_network.tracked(o2)
      q_target = tf.where(t, r, r + 0.99 * tf.reduce_max(q2, axis=1))
      q_target = tf.stop_gradient(q_target)

      # compute loss
      oh = tf.one_hot(asq, env.action_space.n, 1.0, 0.0, axis=1)
      qs = tf.reduce_sum(q * oh, axis=1, name='q_max')
      td = tf.subtract(q_target, qs, name='td')
      # td = tf.clip_by_value(td, -10, 10)
      mse = tf.reduce_mean(tf.abs(td), axis=0, name='mae')
      # mse = tf.where(tf.abs(td) < 1.0, 0.5 * tf.square(td), tf.abs(td) - 0.5, name='mse_huber')
      # mse = tf.reduce_mean(tf.square(td), axis=0, name='mse')

      loss = q_network.minimize(mse)

      # logging
      layers.summarize_tensors([td, mse, r, o, a,
                                tf.subtract(o2, o, name='state_dif'),
                                tf.reduce_mean(tf.cast(t, tf.float32), name='frac_terminal'),
                                tf.subtract(tf.reduce_max(q, 1, True), q, name='av_advantage')])
      layers.summarize_tensors(chi.activations())
      layers.summarize_tensors(chi.gradients())
      return loss

    self.train = Function(train)

    def log_weigths():
      v = q_network.trainable_variables()
      print(f'log weights {v}')

      f = q_network.tracker_variables
      print(f'log weights EMA {f}')

      difs = []
      for g in v:
        a = q_network.tracker.average(g)
        difs.append(tf.subtract(g, a, name=f'ema/dif{g.name[:-2]}'))

      layers.summarize_tensors(v+f+difs)

    self.log_weights = Function(log_weigths)

    def log_returns(R, qs):
      layers.summarize_tensors([R, qs, tf.subtract(R, qs, name='R-Q')])

    self.log_returns = Function(log_returns)

    self.t = 0

  def play_episode(self):
    ob = self.env.reset()
    done = False
    R = 0
    annealing_time = 1000000
    value_estimates = []
    while not done:
      # select actions according to epsilon-greedy policy
      epsilon = 1 - self.t / annealing_time
      if np.random.rand() < .05 * epsilon:
        a = np.random.randint(0, self.env.action_space.n)
      else:
        a, value = self.act(ob)
        value_estimates.append(value)

      ob2, r, done, info = self.env.step(a)
      r = r
      self.memory.enqueue(ob, a, r, done, info)

      ob = ob2
      R += r

      if self.t > 1000:
        self.train(*self.memory.sample_batch()[:-1])

      if self.t % 20000 == 0:
        self.log_weights()

        self.t += 1

    self.log_returns(R, value_estimates)
