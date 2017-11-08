
""" Not sure exactly but I think this should go here...
ghenv.Component.Name = "A/S RC Building Simulator"
ghenv.Component.NickName = 'buildingSimulator'
ghenv.Component.Message = 'VER 0.0.1'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
#ghenv.Component.Category = "Ladybug"
#ghenv.Component.SubCategory = "3 | EnvironmentalAnalysis"
"""

import Grasshopper.Kernel as gh
import scriptcontext

# Initialise parameters

if outdoor_air_temperature == None:
    warning = "outdoor_air_temperature not specified. Assumed to be 10C"
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, warning)
    t_air = 10
else:
    t_air = outdoor_air_temperature
    
if previous_mass_temperature == None:
    warning = "previous_mass_temperature not specified. Assumed to be 20C"
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, warning)
    t_m_prev = 22
else:
    t_m_prev = previous_mass_temperature

if internal_gains == None:
    warning = "internal_gains not specified. Assumed to be 10W"
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, warning)
    internal_gains = 10  # Watts

if solar_irradiation == None:
    warning = "solar_irradiation not specified. Assumed to be 2000W"
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, warning)
    solar_irradiation = 2000 # Watts. Requires adjustment to account for window losses

if illuminance == None:
    warning = "illuminance not specified. Assumed to be 44000W"
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, warning)
    ill = 44000  # Illuminance after transmitting through the window [Lumens]

if occupancy == None:
    warning = "Occupancy assumed to be 0.1"
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, warning)
    occupancy = 0.1  # Occupancy for the timestep [people/hour/square_meter]


Zone = scriptcontext.sticky["RC_Zone"]()

#For now assume glass solar transmittance = 0.6
solar_gains = solar_irradiation * 0.6

Zone.solve_building_energy(internal_gains, solar_gains, t_air, t_m_prev)
Zone.solve_building_lighting(ill, occupancy)

indoor_air_temperature = Zone.t_air
mass_temperature = Zone.t_m  # Printing Room Temperature of the medium
lighting_demand =  Zone.lighting_demand  # Print Lighting Demand
energy_demand = Zone.energy_demand  # Print heating/cooling loads
heating_demand = Zone.heating_demand
cooling_demand = Zone.cooling_demand