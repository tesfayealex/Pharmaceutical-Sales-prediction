

import unittest
from bleach import Cleaner
import pandas as pd
import numpy as np
import sys
import os
from pprint import pprint
import json
# sys.path.append(os.path.abspath(os.path.join('../Pharmaceutical-Sales-prediction/scripts')))
sys.path.append('../scripts')
from cleaner import CleanDataFrame



class TestCleanerModule(unittest.TestCase):

    def setUp(self) -> pd.DataFrame:
        self.cleaner = CleanDataFrame()

    def test_get_numerical_columns(self):
        df = pd.DataFrame([[1, "a", "b", 4], [5, "c", "d", 8]])
        self.assertEqual(self.cleaner.get_numerical_columns(df), [0, 3])
    def test_get_categorical_columns(self):
        df = pd.DataFrame([[1, "a", "b", 4], [5, "c", "d", 8]])
        self.assertEqual(self.cleaner.get_categorical_columns(df), [1, 2])


if __name__ == '__main__':
    unittest.main()
