"""Test dm models.
"""

import tensorflow as tf

from ... import commons

import dm_vgg
import dm_inception


class DMModelTest(tf.test.TestCase):
  def test_vgg16(self):
    vgg16 = dm_vgg.VGGDM(commons.ModelTypes.VGG16)
    self.assertIsNotNone(vgg16.get_label_names())
    self.assertIsNotNone(vgg16.get_preprocess_fn())
    with self.assertRaises(ValueError) as context:
     dm_vgg.VGGDM(commons.ModelTypes.INCEPTION_V1)

  def test_vgg19(self):
    vgg19 = dm_vgg.VGGDM(commons.ModelTypes.VGG19)
    self.assertIsNotNone(vgg19.get_label_names())
    self.assertIsNotNone(vgg19.get_preprocess_fn())


if __name__ == "__main__":
  tf.test.main()
