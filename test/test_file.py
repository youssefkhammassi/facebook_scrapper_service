import unittest

from src.get_data import FbDataLoader
import sqlite3 as sl

db = sl.connect('src/my-test.db')


class TestWriteDataBRToOS(unittest.TestCase):
    def test_getData(self):
        url = f'https://www.facebook.com/youssef.khammassi'
        fb_loader = FbDataLoader(url, db)
        data = fb_loader.get_data()
        self.assertNotEqual(data, None)


if __name__ == '__main__':
    unittest.main()
