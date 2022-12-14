import argparse


class CommandLineInterfaceHandler:
    """CLI input reader class for the AIS analyzer application

    <docs here>

    """

    def __init__(self, args=None):

        # Create the parser
        ais_parser = argparse.ArgumentParser(prog='ais',
                                             description='AIS analyzer application')

        # Add the positional arguments
        ais_parser.add_argument('--input-file',
                                action='store',
                                type=str,
                                help='the path to the input ais csv file(s)')

        ais_parser.add_argument('command',
                                metavar='<COMMAND>',
                                action='store',
                                type=str,
                                choices={'statistics', 'portcalls'},
                                help='a command to call on the input data')

        ais_parser.add_argument('--full',
                                action='store_true',
                                default=False,
                                help='enables the full statistic output')

        ais_parser.add_argument('--mmsi',
                                action='store_true',
                                default=False,
                                help='enables the mmsi statistic output')

        ais_parser.add_argument('--country',
                                action='store_true',
                                default=False,
                                help='enables the country of ships statistic output')
                        
        ais_parser.add_argument('--complete',
                                action='store_true',
                                default=False,
                                help='enables the statistics for the whole dataset in one row as output')

        ais_parser.add_argument('--lat',
                                action='store',
                                default=None,
                                help='latitude in degrees, use decimal degrees not minutes & seconds')

        ais_parser.add_argument('--lon',
                                action='store',
                                default=None,
                                help='longitude in degrees, use decimal degrees not minutes & seconds')

        ais_parser.add_argument('--radius',
                                action='store',
                                default=None,
                                type=float,
                                help='radius from latlong point in meters')

        ais_parser.add_argument('--polygon',
                                action='store',
                                default=None,
                                type=float,
                                nargs="*",
                                help='list of coordinate tuple pairs (lat, lon), (lat, lon)... MINIMUM 3')

        ais_parser.add_argument('--output-file',
                                action='store',
                                type=str,
                                help='output path and name of output csv')

        ais_parser.add_argument('--log',
                                action='store',
                                default='info',
                                choices=["debug", "info", "warning", "critical", "fatal", "error"],
                                help='logging level when running commands. Defaults to \"info\"')

        ais_parser.add_argument('--log-cli',
                                action='store',
                                default="false",
                                choices=["true", "false", "cli", "file"],
                                type=str,
                                help='whether logging should be done to file or cmd. Defaults to file (False)')

        if args:
            # Args can be sent in as a list from functon call
            self.args = ais_parser.parse_args(args=args)
        else:
            # Execute the parse_args() method to get arguments from command line
            self.args = ais_parser.parse_args()

        if self.args.polygon:
            self.args.__setattr__("polygon", self.pair_polygons(self.args.polygon))

    def pair_polygons(self, coords: list):
        return [(coords[i], coords[i+1]) for i, c in enumerate(coords) if i % 2 == 0]

    def get_args(self, asdict=False):
        """ Return the args either as namespace or as dict """
        if asdict:
            return vars(self.args)

        return self.args
