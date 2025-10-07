import csv # to work with CSV inputs
from dataclasses import dataclass, field # for dataclass holding CSV data
import matplotlib.pyplot as plt # for plotting data

@dataclass
class CSVdata():
    flight_time: list[float] = field(default_factory=list)
    baro_alt_AGL: list[float] = field(default_factory=list)

    def pull(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                self.flight_time.append(float(row[4]))
                self.baro_alt_AGL.append(float(row[9]))

class main:
    dataRaw = CSVdata() 
    filename = input("Enter the CSV file path: ") # replace with your actual file path
    dataRaw.pull(filename) # replace 'your_filename.csv' with your actual file path

    plt.plot(dataRaw.flight_time, dataRaw.baro_alt_AGL)
    plt.title('Barometric Altitude AGL over Flight Time')
    plt.xlabel('Flight Time')
    plt.ylabel('Barometric Altitude AGL')
    plt.show()

if __name__ == "__main__":
    main()