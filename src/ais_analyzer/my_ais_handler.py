import pandas as pd


class MyAISHandler:

    def __init__(self, data=None):
        self.data = data

    def eval_args(self, args):
        for argkey, arg in args.items():
            print("AIS handler is passed these arguments:\n")
            print(f"{argkey}: {arg}")

    def read_csv(self, path, sep=','):
        self.data = pd.read_csv(path, sep)


    def get_data(self):
        return self.data

    def to_csv(self, path, sep=','):
        self.data.to_csv(path, sep)

    def statistics(self, full=True):
        if full:
            return self.data.describe(include='all')
        else:
            return self.data.describe()

    def shape(self):
        return self.data.shape
