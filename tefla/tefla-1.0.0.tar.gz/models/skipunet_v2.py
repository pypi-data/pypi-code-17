from __future__ import division, print_function, absolute_import
import tensorflow as tf

from tefla.core import initializers as initz
from tefla.core.layer_arg_ops import common_layer_args, make_args, end_points
from tefla.core.layers import dropout, rms_pool_2d, feature_max_pool_2d
from tefla.core.layers import conv2d, upsample2d, max_pool, relu, prelu, softmax, register_to_collections

image_size = (512, 512)
crop_size = (448, 448)


def model(inputs, is_training, reuse, num_classes=15, batch_size=1, input_size=image_size[0]):
    common_args = common_layer_args(is_training, reuse)
    conv_args = make_args(batch_norm=True, activation=prelu, w_init=initz.he_normal(
        scale=1), untie_biases=True, **common_args)
    upsample_args = make_args(
        batch_norm=None, activation=relu, filter_size=2, stride=2, use_bias=False, **common_args)
    fc_args = make_args(
        activation=prelu, w_init=initz.he_normal(scale=1), **common_args)
    logit_args = make_args(
        activation=None, w_init=initz.he_normal(scale=1), **common_args)
    pred_args = make_args(
        activation=prelu, w_init=initz.he_normal(scale=1), **common_args)
    pool_args = make_args(padding='SAME', filter_size=2, **common_args)
    common_args = common_layer_args(is_training, reuse)

    x1 = conv2d(inputs, 32, name="conv1_1", **conv_args)
    x = max_pool(x1, name='pool1', **pool_args)
    x = conv2d(x, 32, name="conv1_2", **conv_args)
    x2 = conv2d(x, 64, name="conv2_1", **conv_args)
    x = max_pool(x2, name='pool2', **pool_args)
    # 128
    x = conv2d(x, 64, name="conv3_1", **conv_args)
    x = conv2d(x, 64, name="conv3_2", **conv_args)
    x3 = conv2d(x, 64, name="conv3_3", **conv_args)
    x = max_pool(x3, name='pool3', **pool_args)
    # 64
    x = conv2d(x, 128, name="conv4_1", **conv_args)
    x = conv2d(x, 128, name="conv4_2", **conv_args)
    x4 = conv2d(x, 128, name="conv4_3", **conv_args)
    x = max_pool(x4, name='pool4', **pool_args)
    # 32
    x = conv2d(x, 256, name="conv5_1", **conv_args)
    x4_shape = x4.get_shape().as_list()
    up1 = upsample2d(x, [batch_size, x4_shape[1], x4_shape[2], 256],
                     name="up1", **upsample_args)
    x = tf.concat([x4, up1], axis=3)
    x = conv2d(x, 128, name="upconv4_1", **conv_args)
    # x = conv2d(x, 128, name="upconv4_2", **conv_args)
    # 56
    x3_shape = x3.get_shape().as_list()
    up2 = upsample2d(x, [batch_size, x3_shape[1], x3_shape[2], 128],
                     name="up2", **upsample_args)
    x = tf.concat([x3, up2], axis=3)
    x = conv2d(x, 64, name="upconv3_1", **conv_args)
    # x = conv2d(x, 64, name="upconv3_2", **conv_args)
    # 112
    x2_shape = x2.get_shape().as_list()
    up3 = upsample2d(x, [batch_size, x2_shape[1], x2_shape[2], 128],
                     name="up3", **upsample_args)
    x = tf.concat([x2, up3], axis=3)
    x = conv2d(x, 64, name="upconv2_1", **conv_args)
    # x = conv2d(x, 64, name="upconv2_2", **conv_args)
    # 224
    x1_shape = x1.get_shape().as_list()
    up4 = upsample2d(x, [batch_size, x1_shape[1], x1_shape[2], 64],
                     name="up4", **upsample_args)
    x = tf.concat([x1, up4], axis=3)
    x = conv2d(x, 32, name="upconv1_1", **conv_args)
    # x = conv2d(x, 32, name="upconv1_2", **conv_args)
    # 448
    final_x = conv2d(x, num_classes, filter_size=1, stride=1,
                     name="final_map_logits", **logit_args)
    logits = register_to_collections(tf.reshape(
        final_x, shape=(-1, num_classes)), name='logits', **common_args)
    pred_up = tf.argmax(final_x, axis=3)
    pred_up = register_to_collections(
        pred_up, name='final_prediction_map', **common_args)
    predictions = register_to_collections(
        pred_up, name='predictions', **common_args)
    return end_points(is_training)
