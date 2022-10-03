import unittest
import src.ais_analyzer.ais_data_container as adc


class MyTestCase(unittest.TestCase):



    def test_create_container(self):
        nordata = adc.AisDataContainer()
        nordata.initialize_data('tests/data/ais_test_data_10_rader_mongstad.csv')
        self.assertEqual(nordata.get_nr_rows(), 10)


if __name__ == '__main__':
    unittest.main()
