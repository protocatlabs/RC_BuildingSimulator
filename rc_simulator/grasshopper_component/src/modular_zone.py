# This comoponent creates a zone made of elements: the user is allowed 
# to override the default attributes and customize it.
#
# Oasys: A energy simulation plugin developed by the A/S chair at ETH Zurich
# This component is based on building_physics.py in the RC_BuildingSimulator Github repository
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
Create a customized zone using elements as inputs.
Parameters left blank will be filled with default values.
-
Provided by Oasys 0.0.1
    
    Args:
        glazed_elements: Element objects with additional glazing properties
        opaque_elements: Element objects
        thermal_bridges: Linear thermal bridge objects
        floor_area: The conditioned floor area within the zone
        zone_volume: Volume of the zone being simulated [m^2]
        thermal_capacitance_per_floor_area: Thermal capacitance of the room per 
            floor area [J/m2K]
        lighting_load: Lighting Load [W/m2] 
        lighting_control: Lux threshold at which the lights turn on [Lx]
        lighting_utilization_factor: How the light entering the window is 
            transmitted to the working plane []
        lighting_maintenance_factor: How dirty the window is[]
        ach_vent: Air changes per hour through ventilation [Air Changes Per Hour]
        ach_infl: Air changes per hour through infiltration [Air Changes Per Hour]
        ventilation_efficiency: The efficiency of the heat recovery system for ventilation. Set to 0 if there is no heat 
            recovery []
        t_set_heating : Thermal heating set point [C]
        t_set_cooling: Thermal cooling set point [C]
        max_cooling_energy_per_floor_area: Maximum cooling load. Set to -np.inf for unrestricted cooling [C]
        max_heating_energy_per_floor_area: Maximum heating load per floor area. Set to no.inf for unrestricted heating [C]
        heating_supply_system: The type of heating system. Choices are DirectHeater, ResistiveHeater, HeatPumpHeater. 
            Direct heater has no changes to the heating demand load, a resistive heater takes an efficiency into account, 
            HeatPumpHeatercalculates a COP based on the outdoor and system supply temperature 
        cooling_supply_system: The type of cooling system. Choices are DirectCooler HeatPumpCooler. 
            DirectCooler has no changes to the cooling demand load, 
            HeatPumpCooler calculates a COP based on the outdoor and system supply temperature 
        heating_emission_system: How the heat is distributed to the building
        cooling_emission_system: How the cooling energy is distributed to the building
    Returns:
        readMe!: ...
        Zone: ModularRCZone object
        local_and_global_variables: a list of tuples seperated by a colon which 
            can be used to export and quickly reproduce the zone properties in 
            a Python-based testing environment.
        
"""

ghenv.Component.Name = "Zone2"
ghenv.Component.NickName = 'Zone2'
ghenv.Component.Message = 'VER 0.0.1\nFEB_28_2018'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Oasys"
ghenv.Component.SubCategory = " 1 | Zone"
#compatibleOasysVersion = VER 0.0.1\nFEB_21_2018
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import scriptcontext as sc

#  Initialize default values if no input is detected
attributes = {"elements":None,
              "thermal_bridges":None,
              "floor_area":34.3,
              "volume":106.33,
              "thermal_capacitance_per_floor_area":165000,
              "ach_vent":1.5,
              "ach_infl":0.5,
              "ventilation_efficiency":1,
              "t_set_heating":20,
              "t_set_cooling":26,
              "max_heating_energy_per_floor_area":12,
              "max_cooling_energy_per_floor_area":-12,
              "heating_supply_system":sc.sticky["DirectHeater"],
              "cooling_supply_system":sc.sticky["DirectCooler"],
              "heating_emission_system":sc.sticky["AirConditioning"],
              "cooling_emission_system":sc.sticky["AirConditioning"]
              }

#Create a list of zone inputs for testing and debugging in Python
local_and_global_variables = ['Key:Value']


#def build_zone(glazed_elements,opaque_elements,thermal_bridges,zone_volume,
#    thermal_capacitance_per_floor_area, lighting_load, lighting_control,
#    lighting_utilisation_factor, lighting_maintenance_factor, ach_vent, ach_infl,
#    ventilation_efficiency, t_set_heating, t_set_cooling,
#    max_cooling_energy_per_floor_area, max_heating_energy_per_floor_area, 
#    heating_supply_system, cooling_supply_system, heating_emission_system,
#    cooling_emission_system):
#    
#    
#    
#
#    Zone = sc.sticky['ModularRCZone']()
#    


summary = []

# keep valid element objects and combine them into a single list.
g = [x for x in glazed_elements if x is sc.sticky['Element']]
o = [x for x in opaque_elements if x is sc.sticky['Element']]
if len(g) != len(glazed_elements):
    warning = "Invalid glazed element detected"
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, warning)
if len(o) != len(opaque_elements):
    warning = "Invalid opaque element detected"
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, warning)    
elements = g + o
message = '%i glazed and %i opaque elements detected'%(len(g),len(o))
summary.append(message)
if len(elements) == 0:
    elements = None

# keep valid thermal bridge objects
t = [x for x in thermal_bridges if x is sc.sticky['ThermalBridge']]
if len(t) != len(thermal_bridges):
    warning = "Invalid thermal bridge detected"
    w = gh.GH_RuntimeMessageLevel.Warning
    ghenv.Component.AddRuntimeMessage(w, warning)
message = '%i thermal bridges detected'%len(t)
summary.append(message)
if len(t) == 0:
    thermal_bridges = None


for a in attributes.keys():
    if locals()[a] is not None:
        attributes[a] = locals()[a]
        message = a+'='+str(locals()[a])
        summary.append(message)

#Declare zone
ThermalZone = sc.sticky['Zone'](elements = elements,
                         thermal_bridges = thermal_bridges,
                         floor_area = attributes['floor_area'],
                         volume = attributes['volume'],
                         thermal_capacitance_per_floor_area=attributes['thermal_capacitance_per_floor_area'],
                         ach_vent=attributes['ach_vent'],
                         ach_infl=attributes['ach_infl'],
                         ventilation_efficiency=attributes['ventilation_efficiency'],
                         t_set_heating = attributes['t_set_heating'],
                         t_set_cooling = attributes['t_set_cooling'],
                         max_heating_energy_per_floor_area = attributes['max_heating_energy_per_floor_area'],
                         max_cooling_energy_per_floor_area = attributes['max_cooling_energy_per_floor_area'],
                         heating_supply_system=attributes['heating_supply_system'],
                         cooling_supply_system=attributes['cooling_supply_system'],
                         heating_emission_system=attributes['heating_emission_system'],
                         cooling_emission_system=attributes['cooling_emission_system'],
                         )

#TODO: add value errors for inputs.
