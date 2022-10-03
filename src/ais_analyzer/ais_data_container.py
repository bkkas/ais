import pandas as pd
import numpy as np


class AisDataContainer:
    """ Container / wrapper class for our ais data in pandas DataFrames """
    def __init__(self, data=None):
        self.data = data

    def initialize_data(self, input_path):
        """ Function to pass data to the container """
        self.data = pd.read_csv(input_path, sep=';')

    def get_representation(self):
        """ Output the container object type """
        print("AIS data representation:", type(self.data))

    def print_head(self):
        """ Print the first rows of the AIS data """
        print(self.data.head())

    def get_nr_rows(self):
        return np.shape(self.data)[0]
