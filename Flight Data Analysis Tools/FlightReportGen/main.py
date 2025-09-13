from argparse import ArgumentParser # to function in CMD environment
import CSVhandler

# parses CMD input
parser = ArgumentParser()
parser.add_argument('--file', '-f', required=True, help='')
args = parser.parse_args()
filename =  args.file

# creates/loads a data object to hold flight data
dataRaw = CSVhandler.CSVdata()
dataRaw.pull(filename)

