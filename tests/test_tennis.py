import shutil
import unittest
import tempfile

from src.tennis import predict
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

    def testPredict(self):
        predict('Jared Donaldson', 'Karen Khachanov')