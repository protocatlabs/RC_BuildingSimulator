
""" Not sure exactly but I think this should go here...
ghenv.Component.Name = "AS_simulate_period"
ghenv.Component.NickName = 'sim_period'
ghenv.Component.Message = 'VER 0.0.1'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
#ghenv.Component.Category = "Ladybug"
#ghenv.Component.SubCategory = "3 | EnvironmentalAnalysis"
"""

import Grasshopper.Kernel as gh
import scriptcontext

hours = 23

#Initialise zone object
#TODO: Use detected inputs in the RC_Zone initialisation
Zone = scriptcontext.sticky["RC_Zone"](
    window_area=window_area,
    external_envelope_area=external_envelope_area,
#    room_depth=room_depth,
#    room_width=room_width,
#    room_height=room_height,
#    lighting_load=lighting_load,
#    lighting_control=lighting_control,
    ach_vent=0.1,
    ach_infl=0.1)

# Initialise simulation parameters
# TODO: Check that all inputs are of the same length
if outdoor_air_temperature == []:
    t_air = [20]*hours
else:
    t_air = outdoor_air_temperature

if previous_mass_temperature == []:
    t_m_prev = 20
else:
    t_m_prev = previous_mass_temperature

if internal_gains == []:
    internal_gains = [10]*hours  # Watts

if solar_irradiation == []:
    solar_irradiation = [2000]*hours # Watts. Requires adjustment to account for window losses

if occupancy == []:
    occupancy = [0.1]*hours  # Occupancy for the timestep [people/hour/square_meter]


#Initialise result lists
indoor_air_temperature = []
mass_temperature = []
energy_demand = []
heating_demand = []
cooling_demand = []
lighting_demand = []

#Start simulation
for hour in range(0,hours):
    #Set parameters for his hour
    #For now assume glass solar transmittance = 0.6
    solar_gains = solar_irradiation[hour] * 0.6
    #Spectral luminous efficacy (108)- can be calculated from the weather file https://en.wikipedia.org/wiki/Luminous_efficacy
    ill = solar_irradiation[hour] * 108
    ig = internal_gains[hour]
    ta = t_air[hour]
    occ = occupancy[hour]

    #Solve
    Zone.solve_building_energy(ig, solar_gains, ta, t_m_prev)    
    Zone.solve_building_lighting(ill, occupancy)
    
    #Set T_m as t_m_prev for next timestep
    t_m_prev = Zone.t_m

    #Record Results
    indoor_air_temperature.append(Zone.t_air)
    mass_temperature.append(Zone.t_m)  # Printing Room Temperature of the medium
    lighting_demand.append(Zone.lighting_demand)  # Print Lighting Demand
    energy_demand.append(Zone.energy_demand)  # Print heating/cooling loads
    heating_demand.append(Zone.heating_demand)
    cooling_demand.append(Zone.cooling_demand)