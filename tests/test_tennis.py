import shutil
import unittest
import tempfile

from src.tennis import get_database_from_csv
from src.csv_helper import csv_to_lists
from src.constants import LAST_RANKS_CSV

class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestDB, cls).setUpClass()
        cls.test_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)
        super(TestDB, cls).tearDownClass()

    def test_db_creation(self):
        db = get_database_from_csv()

class TestCSV(unittest.TestCase):
    def test_csv_to_lists(self):
        result = csv_to_lists(LAST_RANKS_CSV)
        self.assertTrue(len(result) > 0)