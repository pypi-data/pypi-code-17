import unittest

from owl.data import common


class CommonToolsTester(unittest.TestCase):
  def test_split_data(self):
    img_folder = "/mnt/DataHouse/Fashion/EyeStyle/cnn_test/pipeline/test1/data/"
    img_fns, img_labels, label_names = common.list_img_files(img_folder)
    self.assertEqual(len(img_fns), len(img_labels))
    db_ids, _, query_ids = common.split_train_val_test(
        img_labels, train_ratio=0.8, test_ratio=0.2)
    self.assertAlmostEqual(len(db_ids), 0.8 * len(img_labels))


if __name__ == "__main__":
  unittest.main()