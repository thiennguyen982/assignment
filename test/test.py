# test/test_is_date.py
import unittest
import pandas as pd
from src.main import is_date, is_valid_numeric

class TestIsDate(unittest.TestCase):
    def test_all_valid_dates(self):
        series = pd.Series(['2023-05-25', '2024-01-01', '1999-12-31'])
        self.assertTrue(is_date(series))
    
    def test_all_invalid_dates(self):
        series = pd.Series(['not a date', 'another invalid', '12345'])
        self.assertFalse(is_date(series))
    
    def test_mixed_valid_and_invalid_dates(self):
        series = pd.Series(['2023-05-25', 'not a date', '1999-12-31'])
        self.assertTrue(is_date(series))
    
    def test_empty_series(self):
        series = pd.Series([])
        self.assertFalse(is_date(series))
    
    def test_non_date_values(self):
        series = pd.Series([123, 456.789, True])
        self.assertFalse(is_date(series))
    
    def test_none_values(self):
        series = pd.Series([None, None, None])
        self.assertFalse(is_date(series))

class TestIsValidNumeric(unittest.TestCase):
    def test_all_invalid_numeric(self):
        series = pd.Series(['123', 'abc', '456.789'])
        self.assertFalse(is_valid_numeric(series))
    
    def test_mixed_valid_and_invalid_numeric(self):
        series = pd.Series([' 123 ', 'abc', ' 789 '])
        self.assertFalse(is_valid_numeric(series))
    
    def test_non_numeric_values(self):
        series = pd.Series(['123', '456.789', 'True'])
        self.assertFalse(is_valid_numeric(series))
    
if __name__ == '__main__':
    unittest.main()