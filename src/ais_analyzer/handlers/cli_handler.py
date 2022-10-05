import argparse


class AISCLI:

    def __init__(self, args=None):
        self.args = args

        # Create the parser
        ais_parser = argparse.ArgumentParser(prog='ais',
                                             description='AIS analyzer application')

        # Add the positional arguments
        ais_parser.add_argument('path',
                                metavar='<PATH>',
                                action='store',
                                type=str,
                                help='the path to the input ais csv file(s)')

        ais_parser.add_argument('command',
                                metavar='<COMMAND>',
                                action='store',
                                type=str,
                                choices={'statistics', 'print'},
                                help='a command to call on the input data')

        ais_parser.add_argument('--full',
                                action='store_true',
                                default=True,
                                help='enables the full statistic output')

        ais_parser.add_argument('--output',
                                action='store',
                                type=str,
                                help='output and name result of command as csv')

        # Execute the parse_args() method
        self.args = ais_parser.parse_args()

    def get_args(self, asdict=False):
        """ Return the args either as namespace or as dict """
        if asdict:
            return vars(self.args)

        return self.args
