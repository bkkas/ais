import argparse
import csv

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
                       choices={'statistics', 'print'},
                       type=str,
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

if (output_path != '') and (output_path[-4:] == '.csv'):
    out = ["Wow", "it", "works", "eviny"]



    with open('output.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(out)
