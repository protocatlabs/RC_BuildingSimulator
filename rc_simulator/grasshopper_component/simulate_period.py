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

hours = len(outdoor_air_temperature)

#  Initialize default values if no input is detected

zone_attributes = ['window_area','external_envelope_area','room_depth',
                  'room_width', 'room_height','lighting_load','lighting_control',
                  'lighting_utilisation_factor',  'lighting_maintenance_factor',
                  'u_walls', 'u_windows', 'ach_vent', 'ach_infl',
                  'ventilation_efficiency','thermal_capacitance_per_floor_area',
                  't_set_heating', 't_set_cooling', 'max_cooling_energy_per_floor_area',
                  'max_heating_energy_per_floor_area', 'heating_supply_system',  
                  'cooling_supply_system', 'heating_emission_system',
                  'cooling_emission_system']

initial_values = ['4.0','15.0','7.0','5.0','3.0','11.7','300.0','0.455','0.9',
                  '0.2','1.1','1.5','0.5','0.6','165000','20.0','26.0',
                  '-float("inf")','float("inf")','scriptcontext.sticky["OilBoilerNew"]',
                  'scriptcontext.sticky["HeatPumpAir"]', 'scriptcontext.sticky["OldRadiators"]',
                  'scriptcontext.sticky["AirConditioning"]']

local_and_global_variables = ['Key:Value']

for a,v in zip(zone_attributes,initial_values):
    exec('%s = %s if %s is None else %s'%(a,v,a,a))
    if 'supply' not in a and 'emission' not in a:
        local_and_global_variables.append(a+':'+v)
    elif 'supply' in a:
        local_and_global_variables.append(a+': supply_system.'+v[22:-2])
    elif 'emission' in a:
        local_and_global_variables.append(a+': emission_system.'+v[22:-2])


#Initialise zone object
Zone = scriptcontext.sticky["RC_Zone"](
    window_area=window_area,
    external_envelope_area=external_envelope_area,
    room_depth=room_depth,
    room_width=room_width,
    room_height=room_height,
    lighting_load=lighting_load,
    lighting_control=lighting_control,
    ach_vent=ach_vent,
    ach_infl=ach_infl,
    thermal_capacitance_per_floor_area=thermal_capacitance_per_floor_area)


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

solar_gains = [x * g_windows for x in solar_irradiation]

#Spectral luminous efficacy (108)- can be calculated from the weather file https://en.wikipedia.org/wiki/Luminous_efficacy
ill = [s * 108 for s in solar_irradiation]

if occupancy == []:
    occupancy = [0.1]*hours  # Occupancy for the timestep [people/hour/square_meter]

"""
#  Export obect attributes for testing and debugging
attrs = vars(Zone)
for item in attrs.items():
    local_and_global_variables.append("%s: %s" % item)
"""

#Initialise result lists
indoor_air_temperature = []
mass_temperature = []
energy_demand = []
heating_demand = []
cooling_demand = []
lighting_demand = []

#Start simulation
for hour in range(0,hours):
    il = ill[hour]
    ig = internal_gains[hour]
    ta = t_air[hour]
    sg = solar_gains[hour]
    oc = occupancy[hour]

    #Solve
    Zone.solve_building_energy(ig, sg, ta, t_m_prev)    
    Zone.solve_building_lighting(il, oc)
    
    #Set T_m as t_m_prev for next timestep
    t_m_prev = Zone.t_m

    #Record Results
    indoor_air_temperature.append(Zone.t_air)
    mass_temperature.append(Zone.t_m)  # Printing Room Temperature of the medium
    lighting_demand.append(Zone.lighting_demand)  # Print Lighting Demand
    energy_demand.append(Zone.energy_demand)  # Print heating/cooling loads
    heating_demand.append(Zone.heating_demand)
    cooling_demand.append(Zone.cooling_demand)