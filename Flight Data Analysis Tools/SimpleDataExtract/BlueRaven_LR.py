import csv # to work with CSV inputs
from dataclasses import dataclass, field # for dataclass holding CSV data
import matplotlib.pyplot as plt # for plotting data

@dataclass
class CSVdata():
    flight_time: list[float] = field(default_factory=list)
    baro_alt_AGL: list[float] = field(default_factory=list)
    apo_signal: list[int] = field(default_factory=list)
    main_signal: list[int] = field(default_factory=list)
    motor_signal: list[int] = field(default_factory=list)

    def pull(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                self.flight_time.append(float(row[4]))
                self.baro_alt_AGL.append(float(row[9]))
                self.apo_signal.append(int(row[36]))
                self.main_signal.append(int(row[37]))
                self.motor_signal.append(int(row[38]))
                

class main:
    dataRaw = CSVdata() 
    filename = input("Enter the CSV file path: ") # replace with your actual file path
    dataRaw.pull(filename) # load data from CSV
    
    # Baro Apogee
    apogee = max(dataRaw.baro_alt_AGL)
    apogee_time = dataRaw.flight_time[dataRaw.baro_alt_AGL.index(apogee)]
    print(f"Apogee (Max Barometric Altitude AGL): {apogee} @ {apogee_time} seconds")

    # Apogee Signal Time
    apo_signal_time = dataRaw.flight_time[next((i for i, x in enumerate(dataRaw.apo_signal) if x == 1), None)]
    if apo_signal_time:
        apo_signal_alt = dataRaw.baro_alt_AGL[dataRaw.flight_time.index(apo_signal_time)]
        print(f"Apogee Signal Detected at: {apo_signal_time} seconds, Altitude: {apo_signal_alt}")
    # Main Signal Time
    main_signal_time = dataRaw.flight_time[next((i for i, x in enumerate(dataRaw.main_signal) if x == 1), None)]
    if main_signal_time:
        main_signal_alt = dataRaw.baro_alt_AGL[dataRaw.flight_time.index(main_signal_time)]
        print(f"Main Signal Detected at: {main_signal_time} seconds, Altitude: {main_signal_alt}")
    # Motor Signal Time
    motor_signal_time = dataRaw.flight_time[next((i for i, x in enumerate(dataRaw.motor_signal) if x == 1), None)]
    if motor_signal_time:
        motor_signal_alt = dataRaw.baro_alt_AGL[dataRaw.flight_time.index(motor_signal_time)]
        print(f"Motor Signal Detected at: {motor_signal_time} seconds, Altitude: {motor_signal_alt}")
    
    # Plot: Barometric Altitude AGL over Flight Time
    plt.plot(dataRaw.flight_time, dataRaw.baro_alt_AGL) # plot barometric altitude AGL over flight time
    plt.axvline(apogee_time, color='red', label='Apogee', linestyle='-') # vertical line at apogee time
    plt.axhline(y=0, color='green', label='Ground', linestyle='-') # horizontal line at ground level
    # additional lines for signals if they exist
    if apo_signal_time:
        plt.scatter(apo_signal_time, apo_signal_alt, color='orange', label='Apo Signal', zorder=5)
    if main_signal_time:
        plt.scatter(main_signal_time, main_signal_alt, color='blue', label='Main Signal', zorder=5)
    if motor_signal_time:
        plt.scatter(motor_signal_time, motor_signal_alt, color='purple', label='Motor Signal', zorder=5)
    # plot settings
    plt.title('Barometric Altitude AGL over Flight Time')
    plt.xlabel('Flight Time')
    plt.ylabel('Barometric Altitude AGL')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()