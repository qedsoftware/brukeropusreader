import unittest
from brukeropusreader.utils import find_all


class MyTestCase(unittest.TestCase):

    def test_find_existing(self):
        self.assertEqual(list(find_all('test', 'somelongtestwie')), [8])

    def test_not_existing(self):
        self.assertEqual(list(find_all('test', 'nothinghere')), [])

    def test_three(self):
        self.assertEqual(list(find_all('txt', 'txtxttxtastxt')), [0, 5, 10])


if __name__ == '__main__':
    unittest.main()
