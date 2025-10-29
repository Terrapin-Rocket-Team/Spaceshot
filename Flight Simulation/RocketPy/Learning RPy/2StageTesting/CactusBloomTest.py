import datetime
import os

from rocketpy import Environment, Flight, Function, MonteCarlo, Rocket, SolidMotor
from rocketpy.stochastic import (
    StochasticEnvironment,
    StochasticFlight,
    StochasticNoseCone,
    StochasticParachute,
    StochasticRailButtons,
    StochasticRocket,
    StochasticSolidMotor,
    StochasticTail,
    StochasticTrapezoidalFins,
)

workingDir = os.getcwd()

# Specify the latitude, longitude, and elevation of the launch site
# TODO: Set launch coordinates to correct location
env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)

# Create a datetime object to store the launch date
tomorrow = datetime.date.today() + datetime.timedelta(days=1)

# Set the date of the launch using the datetime object
env.set_date(
    (tomorrow.year, tomorrow.month, tomorrow.day, 18) # Hour given in UTC time, EST = UST - 4
)

# Sets the atmosphere to the latest forecast from the Global Forecast System (GFS)
env.set_atmospheric_model(type="Forecast", file="GFS")

# L1040DM-P
stage1Motor = SolidMotor(
    thrust_source=workingDir+"/data/motors/CactusBloom/CactusBloomStage1Thrust.csv", # DONE
    dry_mass=2.115, # DONE
    dry_inertia=(0.125, 0.125, 0.002), # TODO: Figure out how to measure this
    nozzle_radius=37 / 1000, # DONE
    grain_number=1, # DONE
    grain_density=1815,
    grain_outer_radius=33 / 1000,
    grain_initial_inner_radius=15 / 1000,
    grain_initial_height=120 / 1000,
    grain_separation=5 / 1000,
    grains_center_of_mass_position=0.397,
    center_of_dry_mass_position=0.317,
    nozzle_position=0, # DONE
    burn_time=4.114, # DONE
    throat_radius=11 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber", # DONE
)

# K250
stage2Motor = SolidMotor(
    thrust_source=workingDir+"/data/motors/CactusBloom/CactusBloomStage2Thrust.csv", # DONE
    dry_mass=.777, # DONE
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=25 / 1000, # DONE
    grain_number=1, # DONE
    grain_density=1820, # DONE
    grain_outer_radius=33 / 1000,
    grain_initial_inner_radius=15 / 1000,
    grain_initial_height=120 / 1000,
    grain_separation=5 / 1000,
    grains_center_of_mass_position=0.397,
    center_of_dry_mass_position=0.317,
    nozzle_position=0, # DONE
    burn_time=1.373, # DONE
    throat_radius=11 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber", # DONE
)

stage1Motor.draw()

booster = Rocket(
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag=workingDir+"/data/rockets/calisto/powerOffDragCurve.csv",
    power_on_drag=workingDir+"/data/rockets/calisto/powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose", # DONE
)

sustainer = Rocket(
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag=workingDir+"/data/rockets/calisto/powerOffDragCurve.csv",
    power_on_drag=workingDir+"/data/rockets/calisto/powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose", # DONE
)