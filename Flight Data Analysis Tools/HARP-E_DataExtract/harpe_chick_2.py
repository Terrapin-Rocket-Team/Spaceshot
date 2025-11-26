import csv # to work with CSV inputs
from dataclasses import dataclass, field # for dataclass holding CSV data
import matplotlib.pyplot as plt # for plotting data

@dataclass
class CSVdata():
    flight_time: list[float] = field(default_factory=list)
    stage: list[int] = field(default_factory=list)
    baro_alt: list[float] = field(default_factory=list)
    baro_pressure: list[float] = field(default_factory=list)
    gps_alt: list[float] = field(default_factory=list)
    gps_lat: list[float] = field(default_factory=list)
    gps_lon: list[float] = field(default_factory=list)
    gps_vel: list[float] = field(default_factory=list)
    gps_fix: list[int] = field(default_factory=list)

    def pull(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                self.flight_time.append(float(row[0]))
                self.stage.append(int(row[1]))
                self.baro_alt.append(float(row[2]))
                self.baro_pressure.append(float(row[3]))
                self.gps_alt.append(float(row[4]))
                self.gps_lat.append(float(row[5]))
                self.gps_lon.append(float(row[6]))
                self.gps_vel.append(float(row[7]))
                self.gps_fix.append(int(row[8]))

class main:
    dataRaw = CSVdata() 
    filename = input("Enter the CSV file path: ") # replace with your actual file path
    dataRaw.pull(filename) # load data from CSV
    
    # Baro Apogee
    apogee = max(dataRaw.baro_alt)
    apogee_time = dataRaw.flight_time[dataRaw.baro_alt.index(apogee)]
    print(f"Apogee (Max Barometric Altitude AGL): {apogee} @ {apogee_time} seconds")

    # GPS Apogee
    gps_apogee = max(dataRaw.gps_alt)
    gps_apogee_time = dataRaw.flight_time[dataRaw.gps_alt.index(gps_apogee)]
    print(f"GPS Apogee (Max GPS Altitude): {gps_apogee} @ {gps_apogee_time} seconds")

    # Stage change timestamp
    stage_changes = []
    for i in range(1, len(dataRaw.stage)):
        if dataRaw.stage[i] != dataRaw.stage[i-1]:
            stage_changes.append((dataRaw.flight_time[i], dataRaw.stage[i]))
    for change in stage_changes:
        print(f"Time: {change[0]} seconds, New Stage: {change[1]}")

    # # Apogee Signal Time
    # apo_signal_time = dataRaw.flight_time[next((i for i, x in enumerate(dataRaw.apo_signal) if x == 1), None)]
    # if apo_signal_time:
    #     apo_signal_alt = dataRaw.baro_alt_AGL[dataRaw.flight_time.index(apo_signal_time)]
    #     print(f"Apogee Signal Detected at: {apo_signal_time} seconds, Altitude: {apo_signal_alt}")
    # # Main Signal Time
    # main_signal_time = dataRaw.flight_time[next((i for i, x in enumerate(dataRaw.main_signal) if x == 1), None)]
    # if main_signal_time:
    #     main_signal_alt = dataRaw.baro_alt_AGL[dataRaw.flight_time.index(main_signal_time)]
    #     print(f"Main Signal Detected at: {main_signal_time} seconds, Altitude: {main_signal_alt}")
    # # Motor Signal Time
    # motor_signal_time = dataRaw.flight_time[next((i for i, x in enumerate(dataRaw.motor_signal) if x == 1), None)]
    # if motor_signal_time:
    #     motor_signal_alt = dataRaw.baro_alt_AGL[dataRaw.flight_time.index(motor_signal_time)]
    #     print(f"Motor Signal Detected at: {motor_signal_time} seconds, Altitude: {motor_signal_alt}")

    # Plot: Barometric Altitude AGL over Flight Time  
    plt.plot(dataRaw.flight_time, dataRaw.baro_alt) # plot barometric altitude AGL over flight time
    plt.title('Barometric Altitude AGL over Flight Time')
    plt.xlabel('Flight Time')
    plt.ylabel('Barometric Altitude AGL')
    plt.legend()
    plt.show()

    # Plot: GPS Altitude over Flight Time
    plt.plot(dataRaw.flight_time, dataRaw.gps_alt) # plot GPS altitude over flight time
    plt.title('GPS Altitude over Flight Time')  
    plt.xlabel('Flight Time')
    plt.ylabel('GPS Altitude')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()