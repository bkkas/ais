import pandas as pd


class MyAISHandler:

    def __init__(self, data=None):
        self.data = data

    def eval_args(self, args):
        """ Evaluate the dict of arguments passed from the CLI """
        print("AIS handler is passed these arguments:\n")
        for argkey, arg in args.items():
            print(f"{argkey}: {arg}")

        # TODO: Handle the arguments in a proper manner

        # Input from cli
        input_path = args['path']
        output_path = args['output']
        command = args['command']
        param = args['full']

        # Only support for norwegian AIS data per now
        self.read_csv(input_path, sep=';')
        self.output_data(output_path)

    def read_csv(self, path, sep=','):
        ''' This function will be focus of alot of optimization'''
        self.data = pd.read_csv(path, sep)

    def get_data(self):
        return self.data

    def shape(self):
        return self.data.shape

    def get_statistics(self, full=True):
        if full:
            return self.data.describe(include='all')
        return self.data.describe()

    def output_data(self, path, sep=',', statistics=False):

        df = self.data
        if statistics:
            df = self.get_statistics

        df.to_csv(path, sep)
