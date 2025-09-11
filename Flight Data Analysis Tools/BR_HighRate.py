import csv
from argparse import ArgumentParser
from dataclasses import dataclass

parser = ArgumentParser()
parser.add_argument('--file', '-f', required=True, help='')
file = parser.parse_args()

# add filetype error handling #

@dataclass
class CSVdata:
    year: int #4 digit year
    month: int #1-2 digit month
    day: int #1-2 digit month
    time: str #<2 digit>:<2 digit>:<2 digit>
    flight_time: float
    sync: int #(what is this?)
    gyro: tuple
    accel: tuple
    quat: tuple
    aux_volts: float
    current: float

class BR_CSV():
    def parse(file):
        csv = CSVdata()
        with open(file, 'r') as f:
            for row in f:



    