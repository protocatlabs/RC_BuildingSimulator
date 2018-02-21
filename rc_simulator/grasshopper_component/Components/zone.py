import Grasshopper.Kernel as gh
import scriptcontext

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
                  '-float("inf")','float("inf")','scriptcontext.sticky["OilBoilerNew"]',
                  'scriptcontext.sticky["HeatPumpAir"]', 'scriptcontext.sticky["OldRadiators"]',
                  'scriptcontext.sticky["AirConditioning"]']

default_attributes = {}
for a,v in zip(zone_attributes,initial_values):
    default_attributes[a] = v

#Create a list of zone inputs for testing and debugging in Python
local_and_global_variables = ['Key:Value']

# Check namespace for variables provided as inputs
loc = locals()
for key,value in loc.iteritems():
    
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
Zone = scriptcontext.sticky["RC_Zone"](
     window_area=4.0,
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

print Zone.cooling_emission_system