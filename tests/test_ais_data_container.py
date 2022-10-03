import unittest
import src.ais_analyzer.ais_data_container as adc


class MyTestCase(unittest.TestCase):


    def test_read_csv(self):
        nordata = adc.AisDataContainer()
        nordata.read_csv('tests/data/ais_test_data_10_rader_mongstad.csv', sep=';')
        self.assertEqual(nordata.shape()[0], 10)

    def test_shape(self):
        # TODO
        pass


    def test_append(self):
        # TODO
        pass


    def test_get_representation(self):
        # TODO
        pass


    def test_head(self):
        #TODO
        pass


if __name__ == '__main__':
    unittest.main()
