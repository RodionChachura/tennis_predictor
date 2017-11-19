import shutil
import unittest
import tempfile

from data_keeper import DataKeeper

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
        DataKeeper(self.test_dir)