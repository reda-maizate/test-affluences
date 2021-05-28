import sys
sys.path.append('..')

import unittest
import pandas as pd
from detection_missing_data import *

class TestDetectingMissingData(unittest.TestCase):

    def tests_import_data_correct(self):
        """
        Classic usage
        """
        sensor_data = "../data/data.csv"
        timetables = "../data/timetables.csv"

        d = DetectMissingData(sensor_data, timetables)
        sensor_df, tt_df = d.import_data()
        self.assertEqual((type(sensor_df), type(tt_df)), (pd.core.frame.DataFrame, pd.core.frame.DataFrame))

    def test_import_data_incorrect_path(self):
        """
        Check that the paths inserted are correct.
        """
        sensor_data = "data/incorrect.csv"
        timetables = "data/oups.csv"

        d = DetectMissingData(sensor_data, timetables)
        with self.assertRaises(FileNotFoundError):
            d.import_data()

    def test_import_data_incorrect_type(self):
        """
        Check that the type of the paths are string.
        """
        sensor_data = 5
        timetables = 42

        d = DetectMissingData(sensor_data, timetables)
        with self.assertRaises(ValueError):
            d.import_data()


if __name__ == "__main__":
    unittest.main()
