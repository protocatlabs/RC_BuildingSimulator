# This comoponent allows the user to override the default zone parameters to create a zone with their preferred level of customization
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
Use this component to define a customized thermal zone. Parameters left blank will be filled with default values.
-
Provided by Oasys 0.0.1
    
    Args:
        window_area: Window area used to calculate losses.
        external_envelope_area: Area of all envelope surfaces, including windows in contact with the outside
        room_depth: Depth of the modelled room [m]
        room_width: Width of the modelled room [m] 
        room_height: Height of the modelled room [m]
        lighting_load: Lighting Load [W/m2] 
        lighting_control: Lux threshold at which the lights turn on [Lx]
        u_walls: U value of opaque surfaces  [W/m2K]
        u_windows: U value of glazed surfaces [W/m2K]
        ach_vent: Air changes per hour through ventilation [Air Changes Per Hour]
        ach_infl: Air changes per hour through infiltration [Air Changes Per Hour]
        ventilation_efficiency: The efficiency of the heat recovery system for ventilation. Set to 0 if there is no heat 
            recovery []
        thermal_capacitance_per_floor_area: Thermal capacitance of the room per floor area [J/m2K]
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
        Zone: A Zone object described by the args.
        local_and_global_variables: a list of tuples seperated by a colon which can be used to export and quickly reproduce the zone properties in a Python-based testing environment.
        
"""

ghenv.Component.Name = "Zone"
ghenv.Component.NickName = 'Zone'
ghenv.Component.Message = 'VER 0.0.1\nFEB_21_2018'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Oasys"
ghenv.Component.SubCategory = " 1 | Zone"
#compatibleOasysVersion = VER 0.0.1\nFEB_21_2018
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import Grasshopper.Kernel as gh
import scriptcontext as sc

#  Initialize default values if no input is detected
zone_attributes = ['window_area','external_envelope_area','room_depth',
                  'room_width', 'room_height','lighting_load','lighting_control',
                  'lighting_utilisation_factor',  'lighting_maintenance_factor',
                  'u_walls', 'u_windows', 'g_windows', 'ach_vent', 'ach_infl',
                  'ventilation_efficiency','thermal_capacitance_per_floor_area',
                  't_set_heating', 't_set_cooling', 'max_cooling_energy_per_floor_area',
                  'max_heating_energy_per_floor_area', 'heating_supply_system',  
                  'cooling_supply_system', 'heating_emission_system',
                  'cooling_emission_system']

initial_values = ['4.0','15.0','7.0','5.0','3.0','11.7','300.0','0.455','0.9',
                  '0.2','1.1','0.6','1.5','0.5','0.6','165000','20.0','26.0',
                  '-float("inf")','float("inf")','sc.sticky["OilBoilerNew"]',
                  'sc.sticky["HeatPumpAir"]', 'sc.sticky["OldRadiators"]',
                  'sc.sticky["AirConditioning"]']

default_attributes = {}
for a,v in zip(zone_attributes,initial_values):
    default_attributes[a] = v

#Create a list of zone inputs for testing and debugging in Python
local_and_global_variables = ['Key:Value']

# Check namespace for variables provided as inputs
local_keys = list(locals())
local_values = list(locals().values())

for key,value in zip(local_keys,local_values):
    
    if key in zone_attributes and 'supply' not in key and 'emission' not in key:
            if value is not None:
                local_and_global_variables.append(key+':'+str(value))
            else:
                # Assign default values
                exec('%s = %s'%(key,default_attributes[key]))
                local_and_global_variables.append(key+':'+default_attributes[key])
    
    elif key in zone_attributes and 'supply' in key:
        local_and_global_variables.append(a+': supply_system.'+v[22:-2])
        exec('%s = %s'%(key,default_attributes[key]))
    
    elif key in zone_attributes and 'emission' in key:
        local_and_global_variables.append(a+': emission_system.'+v[22:-2])
        exec('%s = %s'%(key,default_attributes[key]))


#Initialise zone object
Zone = sc.sticky["RC_Zone"](
     window_area=window_area,
     external_envelope_area=external_envelope_area,
     room_depth=room_depth,
     room_width=room_width,
     room_height=room_width,
     lighting_load=lighting_load,
     lighting_control=lighting_control,
     lighting_utilisation_factor=lighting_utilisation_factor,
     lighting_maintenance_factor=lighting_maintenance_factor,
     u_walls=u_walls,
     u_windows=u_windows,
     g_windows=g_windows,
     ach_vent=ach_vent,
     ach_infl=ach_infl,
     ventilation_efficiency=ventilation_efficiency,
     thermal_capacitance_per_floor_area=thermal_capacitance_per_floor_area,
     t_set_heating=t_set_heating,
     t_set_cooling=t_set_cooling,
     max_cooling_energy_per_floor_area=max_cooling_energy_per_floor_area,
     max_heating_energy_per_floor_area=max_heating_energy_per_floor_area,
     heating_supply_system=heating_supply_system,  
     cooling_supply_system=cooling_supply_system,
     heating_emission_system=heating_emission_system,
     cooling_emission_system=cooling_emission_system)

#  Add obect attributes to local_and_global_variables
attrs = vars(Zone)
for item in attrs.items():
    local_and_global_variables.append("%s: %s" % item)

