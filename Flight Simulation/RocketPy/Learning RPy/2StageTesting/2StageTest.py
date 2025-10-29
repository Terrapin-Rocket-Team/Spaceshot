import os

import numpy
# Import four rocketpy classes
from rocketpy import Environment, SolidMotor, Rocket, Flight
import datetime
workingDir = os.getcwd()

# Environment and time Fields
latitude = 32.990254
longitude = -106.974998
elevation = 1400
days_out = 1
time_utc = 12

# Launch Details
rail_length = 5.2
inclination = 85
heading = 0
# Test data apogee time was 16.094684676597385
separation_time = 14

# Stage 1 Motor
stage1_thrust_curve = workingDir + "/data/motors/cesaroni/Cesaroni_M1670.eng"
stage1_dry_mass = 1.815
stage1_dry_inertia = (0.125, 0.125, 0.002)
stage1_nozzle_radius = 33 / 1000
stage1_grain_number = 5
stage1_grain_density = 1815
stage1_grain_outer_radius = 33 / 1000
stage1_grain_initial_inner_radius = 15 / 1000
stage1_grain_initial_height = 120 / 1000
stage1_grain_separation = 5 / 1000
stage1_grains_center_of_mass_position = 0.397
stage1_center_of_dry_mass_position = 0.317
stage1_nozzle_position = 0
stage1_burn_time = 3.9
stage1_throat_radius = 11 / 1000
stage1_motor_position = -1.255

# Stage 2 Motor
stage2_thrust_curve = workingDir + "/data/motors/cesaroni/Cesaroni_M1670.eng"
stage2_dry_mass = 1.815
stage2_dry_inertia = (0.125, 0.125, 0.002)
stage2_nozzle_radius = 33 / 1000
stage2_grain_number = 5
stage2_grain_density = 1815
stage2_grain_outer_radius = 33 / 1000
stage2_grain_initial_inner_radius = 15 / 1000
stage2_grain_initial_height = 120 / 1000
stage2_grain_separation = 5 / 1000
stage2_grains_center_of_mass_position = 0.397
stage2_center_of_dry_mass_position = 0.317
stage2_nozzle_position = 0
stage2_burn_time = 3.9
stage2_throat_radius = 11 / 1000
stage2_motor_position = -.1

# Specify the latitude, longitude, and elevation of the launch site
env = Environment(latitude=latitude, longitude=longitude, elevation=elevation)

# Create a datetime object to store the launch date
tomorrow = datetime.date.today() + datetime.timedelta(days=days_out)

# Set the date of the launch using the datetime object
env.set_date(
    (tomorrow.year, tomorrow.month, tomorrow.day, time_utc) # Hour given in UTC time
)

# Sets the atmosphere to the latest forecast from the Global Forecast System (GFS)
env.set_atmospheric_model(type="Forecast", file="GFS")

Stage1Motor = SolidMotor(
    thrust_source=stage1_thrust_curve,
    dry_mass=stage1_dry_mass,
    dry_inertia=stage1_dry_inertia,
    nozzle_radius=stage1_nozzle_radius,
    grain_number=stage1_grain_number,
    grain_density=stage1_grain_density,
    grain_outer_radius=stage1_grain_outer_radius,
    grain_initial_inner_radius=stage1_grain_initial_inner_radius,
    grain_initial_height=stage1_grain_initial_height,
    grain_separation=stage1_grain_separation,
    grains_center_of_mass_position=stage1_grains_center_of_mass_position,
    center_of_dry_mass_position=stage1_center_of_dry_mass_position,
    nozzle_position=stage1_nozzle_position,
    burn_time=stage1_burn_time,
    throat_radius=stage1_throat_radius,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

Stage2Motor = SolidMotor(
    thrust_source=stage2_thrust_curve,
    dry_mass=stage2_dry_mass,
    dry_inertia=stage2_dry_inertia,
    nozzle_radius=stage2_nozzle_radius,
    grain_number=stage2_grain_number,
    grain_density=stage2_grain_density,
    grain_outer_radius=stage2_grain_outer_radius,
    grain_initial_inner_radius=stage2_grain_initial_inner_radius,
    grain_initial_height=stage2_grain_initial_height,
    grain_separation=stage2_grain_separation,
    grains_center_of_mass_position=stage2_grains_center_of_mass_position,
    center_of_dry_mass_position=stage2_center_of_dry_mass_position,
    nozzle_position=stage2_nozzle_position,
    burn_time=stage2_burn_time,
    throat_radius=stage2_throat_radius,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

# Booster Rocket
stage1_rocket_radius = 127 / 2000
stage1_rocket_mass = 14.426 * 2 + Stage2Motor.dry_mass + Stage2Motor.propellant_initial_mass
stage1_rocket_inertia = (6.321, 6.321, 0.034)
stage1_rocket_power_off_drag = workingDir + "/data/rockets/calisto/powerOffDragCurve.csv"
stage1_rocket_power_on_drag = workingDir + "/data/rockets/calisto/powerOnDragCurve.csv"
stage1_rocket_center_of_mass_without_motor = 0

# Sustainer Rocket
stage2_rocket_radius = 127 / 2000
stage2_rocket_mass = 14.426
stage2_rocket_inertia = (6.321, 6.321, 0.034)
stage2_rocket_power_off_drag = workingDir + "/data/rockets/calisto/powerOffDragCurve.csv"
stage2_rocket_power_on_drag = workingDir + "/data/rockets/calisto/powerOnDragCurve.csv"
stage2_rocket_center_of_mass_without_motor = 0

# Rail Buttons
upper_button_position = 0.0818
lower_button_position = -0.6182
angular_position = 45

# Nose Cone
nose_length = 0.55829
nose_kind = "von karman"
nose_position = 1.478

# Lower Fins
num_lower_fins = 4
lower_fin_root_chord = 0.120
lower_fin_tip_chord = 0.060
lower_fin_span = 0.110
lower_fin_position = -1.04956
lower_fin_cant_angle = 0.5
lower_fin_airfoil = (workingDir + "/data/airfoils/NACA0012-radians.txt", "radians")

# Upper Fins
num_upper_fins = 4
upper_fin_root_chord = 0.120
upper_fin_tip_chord = 0.060
upper_fin_span = 0.110
upper_fin_position = .1
upper_fin_cant_angle = 0.5
upper_fin_airfoil = (workingDir + "/data/airfoils/NACA0012-radians.txt", "radians")

# Booster Tail
booster_tail_top_radius = 0.0635
booster_tail_bottom_radius = 0.0435
booster_tail_length = 0.060
booster_tail_position = -1.194656

# Sustainer Tail
sustainer_tail_top_radius = 0.0635
sustainer_tail_bottom_radius = 0.0435
sustainer_tail_length = 0.060
sustainer_tail_position = -.04

# Booster Main Parachute
booster_main_name = "booster main"
booster_main_drag_coefficient = 10.0
booster_main_trigger = 800
booster_main_sampling_rate = 105
booster_main_lag = 1.5
booster_main_noise = (0, 8.3, 0.5)

# Booster Drogue Parachute
booster_drogue_name = "booster drogue"
booster_drogue_drag_coefficient = 1.0
booster_drogue_trigger = 1200
booster_drogue_sampling_rate = 105
booster_drogue_lag = 1.5
booster_drogue_noise = (0, 8.3, 0.5)

# Sustainer Main Parachute
sustainer_main_name = "sustainer main"
sustainer_main_drag_coefficient = 10.0
sustainer_main_trigger = 800
sustainer_main_sampling_rate = 105
sustainer_main_lag = 1.5
sustainer_main_noise = (0, 8.3, 0.5)

# Sustainer Drogue Parachute
sustainer_drogue_name = "sustainer drogue"
sustainer_drogue_drag_coefficient = 1.0
sustainer_drogue_trigger = 1200
sustainer_drogue_sampling_rate = 105
sustainer_drogue_lag = 1.5
sustainer_drogue_noise = (0, 8.3, 0.5)

booster_rocket = Rocket(
    radius=stage1_rocket_radius,
    mass=stage1_rocket_mass,
    inertia=stage1_rocket_inertia,
    power_off_drag=stage1_rocket_power_off_drag,
    power_on_drag=stage1_rocket_power_on_drag,
    center_of_mass_without_motor=stage1_rocket_center_of_mass_without_motor,
    coordinate_system_orientation="tail_to_nose"
)

booster_rocket.add_motor(Stage1Motor, position=stage1_motor_position)

booster_rail_buttons = booster_rocket.set_rail_buttons(
    upper_button_position=upper_button_position,
    lower_button_position=lower_button_position,
    angular_position=angular_position,
)

booster_nose_cone = booster_rocket.add_nose(
    length=nose_length,
    kind=nose_kind,
    position=nose_position
)

booster_lower_fin_set = booster_rocket.add_trapezoidal_fins(
    n=num_lower_fins,
    root_chord=lower_fin_root_chord,
    tip_chord=lower_fin_tip_chord,
    span=lower_fin_span,
    position=lower_fin_position,
    cant_angle=lower_fin_cant_angle,
    airfoil=lower_fin_airfoil,
)

booster_upper_fin_set = booster_rocket.add_trapezoidal_fins(
    n=num_upper_fins,
    root_chord=upper_fin_root_chord,
    tip_chord=upper_fin_tip_chord,
    span=upper_fin_span,
    position=upper_fin_position,
    cant_angle=upper_fin_cant_angle,
    airfoil=upper_fin_airfoil,
)

booster_tail = booster_rocket.add_tail(
    top_radius=booster_tail_top_radius,
    bottom_radius=booster_tail_bottom_radius,
    length=booster_tail_length,
    position=booster_tail_position
)

booster_main = booster_rocket.add_parachute(
    name=booster_main_name,
    cd_s=booster_main_drag_coefficient,
    trigger=booster_main_trigger,
    sampling_rate=booster_main_sampling_rate,
    lag=booster_main_lag,
    noise=booster_main_noise,
)

booster_drogue = booster_rocket.add_parachute(
    name=booster_drogue_name,
    cd_s=booster_drogue_drag_coefficient,
    trigger=booster_drogue_trigger,
    sampling_rate=booster_drogue_sampling_rate,
    lag=booster_drogue_lag,
    noise=booster_drogue_noise,
)

# booster_rocket.draw()

sustainer_rocket = Rocket(
    radius=stage2_rocket_radius,
    mass=stage2_rocket_mass,
    inertia=stage2_rocket_inertia,
    power_off_drag=stage2_rocket_power_off_drag,
    power_on_drag=stage2_rocket_power_on_drag,
    center_of_mass_without_motor=stage2_rocket_center_of_mass_without_motor,
    coordinate_system_orientation="tail_to_nose"
)

sustainer_rocket.add_motor(Stage2Motor, position=stage2_motor_position)

sustainer_nose_cone = sustainer_rocket.add_nose(
    length=nose_length,
    kind=nose_kind,
    position=nose_position
)

sustainer_fin_set = sustainer_rocket.add_trapezoidal_fins(
    n=num_upper_fins,
    root_chord=upper_fin_root_chord,
    tip_chord=upper_fin_tip_chord,
    span=upper_fin_span,
    position=upper_fin_position,
    cant_angle=upper_fin_cant_angle,
    airfoil=upper_fin_airfoil,
)

sustainer_tail = sustainer_rocket.add_tail(
    top_radius=sustainer_tail_top_radius,
    bottom_radius=sustainer_tail_bottom_radius,
    length=sustainer_tail_length,
    position=sustainer_tail_position
)

# sustainer_rocket.draw()

stage1_flight = Flight(
    rocket=booster_rocket,
    environment=env,
    rail_length=rail_length,
    inclination=inclination,
    heading=heading,
    max_time=separation_time,
    max_time_step=1
)

#stage1_flight.plots.trajectory_3d()

stage1_end = stage1_flight.solution[-1]

init = numpy.concatenate(([0], stage1_end[1:6], [1,0,0,0], stage1_end[11:])).flatten()

stage2_flight = Flight(
    rocket=sustainer_rocket,
    environment=env,
    rail_length=1,
    initial_solution=init,
    max_time=100,
    min_time_step=.01,
    max_time_step=1
)



stage2_flight.plots.trajectory_3d()


"""
                      [0,
                      stage1_flight.x(separation_time),
                      stage1_flight.y[-1],
                      stage1_flight.z(separation_time),
                      stage1_flight.vx(separation_time),
                      stage1_flight.vy(separation_time),
                      stage1_flight.vz(separation_time),
                      stage1_flight.e0(separation_time),
                      stage1_flight.e1(separation_time),
                      stage1_flight.e2(separation_time),
                      stage1_flight.e3(separation_time),
                      stage1_flight.w1(separation_time),
                      stage1_flight.w2(separation_time),
                      stage1_flight.w3(separation_time)]
                      ^ Gives error about array having an inhomogeneous shape
                      
                      [0] + stage1_end[1:]
                      ^ Created flight, gave error when creating 3D trajectory that there were infinite/NaN values
                      
                      [0] + stage1_end[1:6] + [1,0,0,0] + stage1_end[11:]
                      numpy.concatenate(([0], stage1_end[1:6], [1,0,0,0], stage1_end[11:]))
                      ^ Both gave error when creating flight that "atol has wrong shape"
                      """