import chi
import os
chi.set_loglevel('debug')


@chi.experiment
def wgan_conv(self: chi.Experiment, alpha=.00005, c=.01, m=64, n_critic=5, logdir=None, slim=True):
  """ Wasserstein GAN with convolutional nets
  Paper: https://arxiv.org/abs/1701.07875
  """
  import tensorflow as tf
  import numpy as np
  from tensorflow.contrib import layers
  from tensorflow.contrib import learn
  from chi.util import ClippingOptimizer

  if slim:
    tf.InteractiveSession(config=tf.ConfigProto(inter_op_parallelism_threads=4,
                                                intra_op_parallelism_threads=2))
  nch = 200

  @chi.model(optimizer=tf.train.AdamOptimizer(alpha),
             initializer=layers.xavier_initializer(False))
  def generator(z):
    zp = layers.fully_connected(z, nch*14*14)
    x = tf.reshape(zp, [m, 14, 14, nch])
    x = layers.conv2d_transpose(x, nch//2, 5, 2)
    x = layers.conv2d_transpose(x, nch//4, 5, 1)
    x = layers.conv2d_transpose(x, nch//4, 5, 1)
    x = layers.conv2d_transpose(x, 1, 1, 1, activation_fn=tf.nn.sigmoid)
    return x  # 28x28x1

  @chi.model(optimizer=ClippingOptimizer(tf.train.AdamOptimizer(alpha), -c, c),
             initializer=layers.xavier_initializer(False))
  def critic(x: [[28, 28, 1]]):
    x = layers.conv2d(x, 256, 5, 2)
    x = layers.conv2d(x, 512, 5, 2)
    x = layers.fully_connected(x, 256)
    y = layers.fully_connected(x, 1, None)  # linear
    return y

  @chi.function
  def train_critic(x):
    z = tf.random_normal([m, 100])
    loss = critic(generator(z)) - critic(x)
    return critic.minimize(loss)

  @chi.function
  def train_generator():
    z = tf.random_normal([m, 100])
    x = generator(z)
    tf.summary.image('x', x, max_outputs=16)  # save generated images
    loss = - critic(x)
    return generator.minimize(loss)

  # download and pre process mnist
  datapath = os.path.join(os.path.expanduser('~'), '.chi', 'datasets', 'mnist')
  dataset = learn.datasets.mnist.read_data_sets(datapath, reshape=False, validation_size=0)

  print('Starting training')
  for i in range(100000):
    for j in range(n_critic):
      images, _ = dataset.train.next_batch(m)
      train_critic(images)

    train_generator()
