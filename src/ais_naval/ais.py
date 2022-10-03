import argparse
import csv

import pandas as pd

# Create the parser
my_parser = argparse.ArgumentParser(prog='ais',
                                    description='AIS analyzer application')

# Add the positional arguments
my_parser.add_argument('Path',
                       metavar='<PATH>',
                       action='store',
                       type=str,
                       help='the path to the input ais csv file(s)')

my_parser.add_argument('Command',
                       metavar='<COMMAND>',
                       action='store',
                       type=str,
                       choices={'statistics', 'print'},
                       help='a command to call on the input data')

my_parser.add_argument('--full',
                       action='store_true',
                       default=True,
                       help='enables the full statistic output')

my_parser.add_argument('--output',
                       action='store',
                       type=str,
                       help='output and name result of command as csv')

# Execute the parse_args() method
args = my_parser.parse_args()

input_path = args.Path
command = args.Command
full = args.full
output_path = args.output


def is_valid_filename(filename):
    return filename[-4:] == '.csv'


# Loading input

data_df = pd.read_csv(input_path, sep=';')

with open(input_path, 'r') as csv_file:
    reader = csv.reader(csv_file)

    if command == 'statistics':
        counter = 0
        for row in reader:
            counter += 1
        print("Nr of rows: ", counter)

    if command == 'print':
        for row in reader:
            print(row)

    csv_file.close()



# Output
# Validating output file name
if is_valid_filename(output_path):

    # writing some arbitrary list to the csv
    with open(output_path, 'w') as file:
        out = ["Wow", "it", "works", "eviny"]
        writer = csv.writer(file)
        writer.writerow(out)

    # Testing output with pandas
    # Storing input as a dataframe
    stats = data_df.describe()
    stats.to_csv(output_path)
