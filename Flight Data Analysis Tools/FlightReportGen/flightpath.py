from dataclasses import dataclass, field # for dataclass holding CSV data
from typing import List, Tuple # for defining dataclass values
import copy # for creating copies of rocket states

@dataclass
class rocket():
    time: float
    pos: tuple[float, float, float] # pos in 3 dimensions
    vel: tuple[float, float, float] # velocity vector
    accel: tuple[float, float, float] # acceleration vector
    att: tuple[float,float, float, float] # quaternion describing attitude

    def update(self, time, pos, vel, accel, att):
        self.time = time
        self.pos = pos
        self.vel = vel
        self.accel = accel
        self.att = att
        
class stateGen():
    def att(data, timestep):
        raw = data.quat(timestep)
        scaled = ()
        for val in raw:
            scaled.append(val/30000) # BR high rate quternion data scaled by 30000
        return scaled
    
    def pos():
        pass

    def vel():
        pass

    def accel():
        pass

    
def generateFlight(data):
    # flight history storage
    flight_history = list[rocket] = []
    state = rocket()
    timestep = 0

    for time in data.flight_time:
        state.update(time, stateGen.pos, stateGen.vel, stateGen.accel, stateGen.att)
        flight_history.append(copy.deepcopy(state))
        timestep += 1

    return flight_history