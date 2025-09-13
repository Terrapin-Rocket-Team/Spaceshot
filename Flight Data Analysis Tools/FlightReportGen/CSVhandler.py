import csv # to work with CSV inputs
from dataclasses import dataclass, field # for dataclass holding CSV data
from typing import List, Tuple # for defining dataclass values

# add filetype error handling #

@dataclass
class CSVdata():
    time: list[tuple[int, int, int, str]] = field(default_factory=list)
    flight_time: list[float] = field(default_factory=list)
    sync: list[int] = field(default_factory=list)
    gyro: list[tuple[float, float, float]] = field(default_factory=list)
    accel: list[tuple[float, float, float]] = field(default_factory=list)
    quat: list[tuple[float, float, float, float]] = field(default_factory=list)
    aux_V: list[float] = field(default_factory=list)
    current: list[float] = field(default_factory=list)

    def pull(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                self.time.append((int(row[0]), int(row[1]), int(row[2]), row[3]))
                self.flight_time.append(float(row[4]))
                self.sync.append(int(row[5]))
                self.gyro.append((float(row[6]), float(row[7]), float(row[8])))
                self.accel.append((float(row[9]), float(row[10]), float(row[11])))
                self.quat.append((float(row[12]), float(row[13]), float(row[14]), float(row[15])))
                self.aux_V.append(float(row[16]))
                self.current.append(float(row[17]))