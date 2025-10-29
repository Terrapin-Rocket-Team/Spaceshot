import os

# Import four rocketpy classes
from rocketpy import Environment, SolidMotor, Rocket, Flight
import datetime
workingDir = os.getcwd()

# Specify the latitude, longitude, and elevation of the launch site
env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)

# Create a datetime object to store the launch date
tomorrow = datetime.date.today() + datetime.timedelta(days=1)

# Set the date of the launch using the datetime object
env.set_date(
    (tomorrow.year, tomorrow.month, tomorrow.day, 12) # Hour given in UTC time
)

# Sets the atmosphere to the latest forecast from the Global Forecast System (GFS)
env.set_atmospheric_model(type="Forecast", file="GFS")

# Displays information about the environment forecast
# TODO: Uncomment to see output
# env.info()

# Create a solid motor with the given characteristics
Pro75M1670 = SolidMotor(
    thrust_source=workingDir+"/data/motors/cesaroni/Cesaroni_M1670.eng",
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=33 / 1000,
    grain_number=5,
    grain_density=1815,
    grain_outer_radius=33 / 1000,
    grain_initial_inner_radius=15 / 1000,
    grain_initial_height=120 / 1000,
    grain_separation=5 / 1000,
    grains_center_of_mass_position=0.397,
    center_of_dry_mass_position=0.317,
    nozzle_position=0,
    burn_time=3.9,
    throat_radius=11 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

# Displays information about the motor
# TODO: Uncomment to see output
# Pro75M1670.info()

# Creates a rocket object with the given characteristics
calisto = Rocket(
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag=workingDir+"/data/rockets/calisto/powerOffDragCurve.csv",
    power_on_drag=workingDir+"/data/rockets/calisto/powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

# Adds the previously created motor to the rocket
calisto.add_motor(Pro75M1670, position=-1.255)

# Adds rail guides to the rocket object
rail_buttons = calisto.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.6182,
    angular_position=45,
)

# Adds a nose cone to the rocket object
nose_cone = calisto.add_nose(
    length=0.55829,
    kind="von karman",
    position=1.278
)

# Adds a fin set to the rocket object
fin_set = calisto.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    position=-1.04956,
    cant_angle=0.5,
    airfoil=(workingDir+"/data/airfoils/NACA0012-radians.txt","radians"),
)

# Adds a tail to the rocket
tail = calisto.add_tail(
    top_radius=0.0635,
    bottom_radius=0.0435,
    length=0.060,
    position=-1.194656
)

# Any number of parachutes can be added
main = calisto.add_parachute(
    name="main",
    cd_s=10.0,
    trigger=800,      # ejection altitude in meters
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

drogue = calisto.add_parachute(
    name="drogue",
    cd_s=1.0,
    trigger="apogee",  # ejection at apogee
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

# Displays the static margin of the rocket
# Negative or extremely high numbers are bad
# TODO: Uncomment to see output
# calisto.plots.static_margin()

# Draws a diagram of the rocket you have created
# TODO: Uncomment to see output
# calisto.draw()

# Creates a flight object which runs the simulation and stores data
test_flight = Flight(
    rocket=calisto, environment=env, rail_length=5.2, inclination=85, heading=0, max_time=60
    )

# Displays all plots created by test_flight
# TODO: Uncomment to see outputs
test_flight.all_info()

# Prints the rocket conditions at ignition
test_flight.prints.initial_conditions()

# Prints the wind conditions at the surface
test_flight.prints.surface_wind_conditions()

# Prints the launch rail conditions
test_flight.prints.launch_rail_conditions()

# Prints the conditions of the rocket as soon as it leaves the launch rail
test_flight.prints.out_of_rail_conditions()

# Prints the conditions of the rocket as soon as the motor burns out
test_flight.prints.burn_out_conditions()

# Prints the rocket conditions at the apex of the flight
test_flight.prints.apogee_conditions()

# Prints the ejection data of parachutes
test_flight.prints.events_registered()

# Prints the conditions of the rocket at impact
test_flight.prints.impact_conditions()

# Prints maximum recorded values
test_flight.prints.maximum_values()