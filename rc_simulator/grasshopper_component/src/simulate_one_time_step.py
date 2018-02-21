# This component can be used to simulate a single timestep, which is mostly useful for testing and debugging.
#
# Oasys: A energy simulation plugin developed by the A/S chair at ETH Zurich
# This component is based on examples\hourSimulation.py in the RC_BuildingSimulator Github repository
# https://github.com/architecture-building-systems/RC_BuildingSimulator
# Extensive documentation is available on the project wiki.
#
# Author: Justin Zarb <zarbj@student.ethz.ch>
#
# This file is part of Oasys
#
# Licensing/Copyright and liability comments go here.
# <Copyright 2018, Architecture and Building Systems - ETH Zurich>
# <Licence: MIT>

"""
Use this component to simulate a single timestep. You may add a custom zone or leave the Zone arg blank for the default zone.
-
Provided by Oasys 0.0.1
    
    Args:
        Zone: Input a customized Zone from the Zone component.
        outdoor_air_temperature: The outdoor air temperature for the hour being simulated
        previous_mass_temperature: The temperature of the mass node during the previous hour. This temperature represents the average temperature of the building envelope itself.
        internal_gains: internal heat gains for the hour being simulated in [Watts]
        solar_irradiation: Solar irradiation gains for the hour being simulated in [Watts]. Does not account for losses through window!
        illuminance: Illuminance after transmitting through the window [Lumens]
        occupancy: Occupancy for the timestep [people/hour/square_meter]
    Returns:
        readMe!: ...
        indoor_air_temperature: Indoor air temperature for the given time step
        lighting_demand: lighting energy demand for the given time step
        heating_demand: heating energy demand required to maintain the heating setpoint temperature defined in the Zone.
        cooling_demand: cooling energy demand required to maintain the cooling setpoint temperature defined in the Zone.
        energy_demand: Sum of heating, cooling and lighting demand for the given timestep.
 
"""

ghenv.Component.Name = "Simulate a Single Time Step"
ghenv.Component.NickName = 'SimulateOneTimeStep'
ghenv.Component.Message = 'VER 0.0.1\nFEB_21_2018'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Oasys"
ghenv.Component.SubCategory = "Simulation"
#compatibleOasysVersion = VER 0.0.1\nFEB_21_2018
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import Grasshopper.Kernel as gh
import scriptcontext as sc

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

if Zone == None:
    Zone = sc.sticky["RC_Zone"]()
    warning = """No zone definition has been detected. The default zone will be
    applied."""
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, warning)
else:
    Zone = Zone

solar_gains = solar_irradiation * Zone.g_windows

Zone.solve_building_energy(internal_gains, solar_gains, t_air, t_m_prev)
Zone.solve_building_lighting(ill, occupancy)

indoor_air_temperature = Zone.t_air
mass_temperature = Zone.t_m  # Printing Room Temperature of the medium
lighting_demand =  Zone.lighting_demand  # Print Lighting Demand
energy_demand = Zone.energy_demand  # Print heating/cooling loads
heating_demand = Zone.heating_demand
cooling_demand = Zone.cooling_demand