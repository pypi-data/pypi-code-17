""" (Deep) Deterministic Policy Gradient (DDPG) implementation

Papers:
Deterministic policy gradient algorithms
http://www.jmlr.org/proceedings/papers/v32/silver14.pdf

Continuous control with deep reinforcement learning
https://arxiv.org/abs/1509.02971
"""

import tensorflow as tf
from tensorflow.python.layers.utils import smart_cond
from tensorflow.python.ops.variable_scope import get_local_variable
import chi
from chi import Function
from chi import experiment, model, Experiment, Model
from tensorflow.contrib import layers
import gym
from gym import spaces
from gym import wrappers
import numpy as np
from tensorflow.contrib.framework import arg_scope
from chi.rl import ReplayMemory


def ornstein_uhlenbeck_noise(a, t_decay=100000):
  noise_var = get_local_variable("nm", initializer=tf.zeros(a.get_shape()[1:]))
  ou_theta = get_local_variable("ou_theta", initializer=0.2)
  ou_sigma = get_local_variable("ou_sigma", initializer=0.15)
  # ou_theta = tf.Print(ou_theta, [noise_var], 'noise: ', first_n=2000)
  ou_sigma = tf.train.exponential_decay(ou_sigma, chi.function.step(), t_decay, 1e-6)
  n = noise_var.assign_sub(ou_theta * noise_var - tf.random_normal(a.get_shape()[1:], stddev=ou_sigma))
  return a + n


class Ddpg:
  def __init__(self, env: gym.Env, actor: Model, critic: Model, preprocess: Model = None, memory=None,
               noise: callable = ornstein_uhlenbeck_noise):

    assert isinstance(env.action_space, spaces.Box), "The environment's action space has to be continuous"

    acsp = env.action_space
    obsp = env.observation_space

    self.memory = memory or ReplayMemory(1000000, obsp.shape, acsp.shape)
    self.env = env

    preprocess = preprocess or Model(lambda x: x,
                                     optimizer=tf.train.AdamOptimizer(.001),
                                     tracker=tf.train.ExponentialMovingAverage(1 - 0.001))

    def act(o: [obsp.shape], noisy=True):
      with arg_scope([layers.batch_norm], is_training=False):
        s = preprocess(o)
        a = actor(s, noise=noisy)
        a = smart_cond(noisy, lambda: noise(a), lambda: a)
        q = critic(s, a)
        layers.summarize_tensors([s, a, q])
        return a

    self.act = Function(act)

    def train_actor(o: [obsp.shape]):
      s = preprocess(o)
      a0 = actor(s)
      q = critic(s, a0)
      loss = - tf.reduce_mean(q, axis=0)
      return actor.minimize(loss), preprocess.minimize(loss)

    self.train_actor = Function(train_actor)

    def train_critic(o: [obsp.shape], a: [acsp.shape], r, t: tf.bool, o2: [obsp.shape]):
      s = preprocess(o)
      q2 = critic(s, a)
      s2 = preprocess.tracked(o2)
      qt = critic.tracked(s2, actor.tracked(s2))
      qtt = tf.where(t, r, r + 0.99 * qt)
      mse = tf.reduce_mean(tf.square(q2 - qtt), axis=0)
      return critic.minimize(mse), preprocess.minimize(mse)

    self.train_critic = Function(train_critic)

    def log_return(r: []):
      layers.summarize_tensor(r, 'Return')

    self.log_return = Function(log_return)

    self.t = 0

  def play_episode(self):
    ob = self.env.reset()
    done = False
    R = 0
    self.act.initialize_local()  # reset local variables (e.g. the noise state)
    while not done:
      # a = act(ob, False) if np.random.rand() > .1 else acsp.sample()
      a = self.act(ob)
      ob2, r, done, _ = self.env.step(a)
      self.memory.enqueue(ob, a, r, done)

      ob = ob2
      R += r

      debug_training = self.t == 100
      if self.t > 2000 or debug_training:
        mbs = 64
        for i in range(1):
          mb = self.memory.sample_batch(mbs)[:-1]
          self.train_critic(*mb)

        mb = self.memory.sample_batch(mbs)[:-1]
        self.train_actor(mb[0])

      self.t += 1

    self.log_return(R)
    return R, {}


def test_ddpg():
  import gym_mix
  env = gym.make('ContinuousCopyRand-v0')
  env = wrappers.TimeLimit(env, max_episode_steps=0)

  @model(optimizer=tf.train.AdamOptimizer(0.0001),
         tracker=tf.train.ExponentialMovingAverage(1 - 0.001))
  def actor(x):
    x = layers.fully_connected(x, 50, biases_initializer=layers.xavier_initializer())
    a = layers.fully_connected(x, env.action_space.shape[0], None,
                               weights_initializer=tf.random_normal_initializer(0, 1e-4))
    return a

  @model(optimizer=tf.train.AdamOptimizer(.001),
         tracker=tf.train.ExponentialMovingAverage(1 - 0.001))
  def critic(x, a):
    x = layers.fully_connected(x, 300, biases_initializer=layers.xavier_initializer())
    x = tf.concat([x, a], axis=1)
    x = layers.fully_connected(x, 300, biases_initializer=layers.xavier_initializer())
    x = layers.fully_connected(x, 300, biases_initializer=layers.xavier_initializer())
    q = layers.fully_connected(x, 1, None, weights_initializer=tf.random_normal_initializer(0, 1e-4))
    return tf.squeeze(q, 1)

  agent = Ddpg(env, actor, critic)

  for ep in range(10000):
    R, _ = agent.play_episode()

    if ep % 100 == 0:
      print(f'Return after episode {ep} is {R}')
