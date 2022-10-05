import unittest
import src.ais_analyzer.my_ais_handler as handler


class MyTestCase(unittest.TestCase):

    def test_read_csv(self):
        nordata = handler.MyAISHandler()
        nordata.read_csv('tests/data/ais_test_data_10_rader_mongstad.csv', sep=';')
        self.assertEqual(nordata.shape()[0], 10)


if __name__ == '__main__':
    unittest.main()
