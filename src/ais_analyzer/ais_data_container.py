import pandas as pd
import numpy as np


class AisDataContainer:
    """ Container class for our ais data in pandas DataFrames """

    def __init__(self, data=None):
        self.data = data

    def read_csv(self, *args, **kwargs):
        """ Function to pass data to the container given a path to a csv """
        self.data = pd.read_csv(*args, **kwargs)

    def append(self, data_to_append):
        data_to_append = pd.DataFrame(data_to_append)
        self.data.append(data_to_append)

    def get_representation(self):
        """ Output the container object type """
        print("AIS data representation:", type(self.data))

    def head(self, *args, **kwargs):
        """ Print the first rows of the AIS data """
        print(self.data.head(*args,**kwargs))

    def shape(self):
        return self.data.shape
