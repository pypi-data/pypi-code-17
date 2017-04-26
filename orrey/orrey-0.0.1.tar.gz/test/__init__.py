import glob
import orrey
import os
import pandas as pd
from unittest import TestCase

filepath = os.path.abspath(__file__)
basedir = os.path.dirname(filepath)

class TestModelCorr(TestCase):
    def test_builds_df_with_one_design_file(self):
        fixtures = glob.glob(os.path.join(basedir, 'fixtures/*design.csv'))[:1]
        mod = orrey.model.ModelWrapper(fixtures)
        self.assertTrue(isinstance(mod.designDf, pd.DataFrame))
        self.assertEqual(mod.design.shape[0], 120)

    def test_builds_df_with_two_design_files(self):
        fixtures = glob.glob(os.path.join(basedir, 'fixtures/*design.csv'))
        mod = orrey.model.ModelWrapper(fixtures)
        self.assertEqual(mod.design.shape[0], 240)

    def test_saves_design(self):
        fixtures = glob.glob(os.path.join(basedir, 'fixtures/*design.csv'))[:1]
        mod = orrey.model.ModelWrapper(fixtures)
        outfile = 'tmp.csv'
        mod._saveDesign(outfile=outfile)
        self.assertTrue(os.path.exists(outfile))

    def test_saves_png(self):
        fixtures = glob.glob(os.path.join(basedir, 'fixtures/*design.csv'))[:1]
        mod = orrey.model.ModelWrapper(fixtures)
        outfile = 'tmp.png'
        mod._saveFigure(outfile=outfile)
        self.assertTrue(os.path.exists(outfile))

    def tearDown(self):
        'called multiple times, after every test method'
        if os.path.exists('tmp.png'):
            os.remove('tmp.png')

        if os.path.exists('tmp.csv'):
            os.remove('tmp.csv')
