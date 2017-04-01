"""Tests for visualsearch pipeline.
"""

import unittest

from owl.pipelines.visualsearch import visualsearch


class VisualSearchTester(unittest.TestCase):
  res_dir = "/mnt/DataHouse/Fashion/EyeStyle/cnn_test/pipeline/test1/res_test/"
  pipe = visualsearch.VisualSearchPipeline("vs_test", res_dir)

  def test_file_loading(self):
    img_dir = "/mnt/DataHouse/Fashion/EyeStyle/cnn_test/pipeline/test1/data/"
    self.pipe.read_data_from_files(img_dir, ["*.jpg"])

  def test_db_loading(self):
    self.pipe.load_items_from_db()


if __name__ == "__main__":
  unittest.main()
