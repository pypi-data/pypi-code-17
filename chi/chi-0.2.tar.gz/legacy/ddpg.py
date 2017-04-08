""" This script implements the DDPG algorithm
"""
import tensorflow as tf
from tensorflow.python.ops.variable_scope import get_local_variable

import chi
from chi import experiment, model
from chi.rl import ReplayMemory


@experiment
def simple_ddpg(logdir=None):
  from tensorflow.contrib import layers
  import gym
  from gym import spaces
  from gym import wrappers

  chi.set_loglevel('debug')

  e = 1

  if e == 0:
    from gym_mix import envs
    env = envs.ContinuousCopyRandEnv()
    env = wrappers.TimeLimit(env, max_episode_steps=0)
  elif e == 1:
    # env = gym.make('Pendulum-v0')
    env = gym.make('MountainCarContinuous-v0')
    class Obw(gym.ObservationWrapper):
      def _observation(self, o):
        return 

    env = wrappers.Monitor(env, logdir + '/monitor')
  elif e == 2:
    from rlunity import envs
    # print(rlunity.__file__)
    env = gym.make('unityenv-v0')
    env.configure(w=32, h=32, batchmode=True)
    # env = wrappers.Monitor(env, logdir + '/monitor')

  assert isinstance(env, gym.Env)
  assert isinstance(env.action_space, spaces.Box)
  acsp = env.action_space.shape
  obsp = env.observation_space.shape

  m = ReplayMemory(100000, obsp, acsp)

  def noise(a):
    noise_var = get_local_variable("nm", initializer=tf.zeros(a.get_shape()[1:]))
    ou_theta = get_local_variable("ou_theta", initializer=0.2)
    ou_sigma = get_local_variable("ou_sigma", initializer=0.15)
    n = noise_var.assign_sub(ou_theta * noise_var - tf.random_normal(a.get_shape()[1:], stddev=ou_sigma))
    return a + n

  @model(optimizer=tf.train.AdamOptimizer(.0001),
         tracker=tf.train.ExponentialMovingAverage(1-0.0001))
  def pp(x: [obsp]):
    # x = tf.reshape(o, [tf.shape(o)[0], 32*32*3])
    x = layers.fully_connected(x, 300)
    x = layers.fully_connected(x, 300)
    return x

  @model(optimizer=tf.train.AdamOptimizer(0.0001),
         tracker=tf.train.ExponentialMovingAverage(1-0.0001))
  def actor(x):

    a = layers.fully_connected(x, acsp[0], None)
    a = a + tf.random_normal(tf.shape(a), mean=0, stddev=.15)
    # a = tf.cond(is_training, lambda: noise(a), lambda: a)
    return a

  @model(optimizer=tf.train.AdamOptimizer(.001),
         tracker=tf.train.ExponentialMovingAverage(1-0.001))
  def critic(x, a: [acsp]):
    x = layers.fully_connected(x, 1, None)
    q = x + layers.fully_connected(a, 1, None)
    return tf.squeeze(q, 1)

  @chi.function
  def act(o: [obsp]):
    s = pp(o)
    a = actor(s, is_training=False)
    return a

  @chi.function
  def train(o, a, r, t: tf.bool, o2):
    s = pp(o)
    a0 = actor(s)
    q = critic(s, a0)

    q2 = critic(s, a)
    s2 = pp.tracked(o2)
    qt = critic.tracked(s2, actor.tracked(s2))
    qtt = tf.where(t, r, r + 0.99 * qt)
    mse = tf.reduce_mean(tf.square(q2 - qtt))

    return (
      actor.minimize(-q),
      critic.minimize(mse),
      pp.minimize([-q, mse])
    )

  t = 0
  for ep in range(1000000):
    ob = env.reset()
    done = False
    R = 0
    while not done:
      a = act(ob)
      ob, r, done, _ = env.step(a)
      m.enqueue(ob, a, r, done)
      R += r
      if t > 100:
        mb = m.sample_batch(32)[:-1]

        # print(mb)
        # exit()
        train(*mb)

      if t % 1000 == 0:
        print('a', a, 'ob', ob, 'r', r, 'done', done)
        print(m)
        print(f'Return in after episode {ep}: {R}')

      t += 1



