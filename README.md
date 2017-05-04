##5R1C Building Simulation Model
First commit 
Second commit
Third commit

* `buildingPhysics.py`: Is the RC model class
* `supplySystem.py`: Is a builder pattern class to define the building system 
* `emissionSystem.py`: Is a builder pattern class to define the emission system of the building (work in progress)
* `examples` : Folder containing two examples
* `tests` : Is the unittest folder. 


The equations presented here is this code are derived from ISO 13790 Annex C, Methods are listed in order of apperance in the Annex 

###HOW TO USE
See RCsimulator/examples/
```python
from buildingPhysics import Building #Importing Building Class
Office=Building() #Set an instance of the class
Office.solve_building_energy(phi_int, internal_gains, solar_gains,T_out, T_m_prev) #Solve for Energy Demand
Office.solve_building_lighting(ill, occupancy) #Solve for Lighting
```


###VARIABLE DEFINITION

	internal_gains: Internal Heat Gains [W]
	solar_gains: Solar Heat Gains [W]
	T_out: Outdoor air temperature [C]
	T_m_prev: Thermal mass temperature from the previous time step 
	ill: Illuminance in contact with the total outdoor window surface [lumens]
	occupancy: Occupancy [people]

	T_m_next: Medium temperature of the enxt time step [C]
	T_m: Some wierd average between the previous and current timestep of the medium  [C] #TODO: Check this 

	Inputs to the 5R1C model:
	c_m: Thermal Capacitance of the medium [J/K]
	h_tr_is: Heat transfer coefficient between the air and the inside surface [W/K]
	h_tr_w: Heat transfer from the outside through windows, doors [W/K]
	H_tr_ms: Heat transfer coefficient between the internal surface temperature and the medium [W/K]
	h_tr_em: Heat conductance from the outside through opaque elements [W/K]
	h_ve_adj: Ventilation heat transmission coefficient [W/K]

	phi_m_tot: see formula for the calculation, eq C.5 in standard [W]
	phi_m: Combination of internal and solar gains directly to the medium [W]
	phi_st: combination of internal and solar gains directly to the internal surface [W]
	phi_ia: combination of internal and solar gains to the air [W]
	energy_demand: Heating and Cooling of the Supply air [W]

	h_tr_1: combined heat conductance, see function for definition [W/K]
	h_tr_2: combined heat conductance, see function for definition [W/K]
	h_tr_3: combined heat conductance, see function for definition [W/K]


	
###INPUT PARAMETER DEFINITION 

	window_area: Area of the Glazed Surface in contact with the outside [m2]
	external_envelope_area: Area of all envelope surfaces, including windows in contact with the outside
	room_depth=7.0 Depth of the modeled room [m]
	room_width=4.9 Width of the modeled room [m]
	room_height=3.1 Height of the modeled room [m]
	glass_solar_transmittance: Fraction of Radiation transmitting through the window []
	glass_light_transmittance: Fraction of visible light (luminance) transmitting through the window []
	lighting_load: Lighting Load [W/m2] 
	lighting_control: Lux threshold at which the lights turn on [Lx]
	U_walls: U value of opaque surfaces  [W/m2K]
	U_windows: U value of glazed surfaces [W/m2K]
	ACH_vent: Air changes per hour through ventilation [Air Changes Per Hour]
	ACH_infl: Air changes per hour through infiltration [Air Changes Per Hour]
	ventilation_efficiency: The efficiency of the heat recovery system for ventilation. Set to 0 if there is no heat recovery []
	thermal_capacitance_per_floor_area: Thermal capacitance of the room per floor area [J/m2K]
	T_set_heating : Thermal heating set point [C]
	T_set_cooling: Thermal cooling set point [C]
	max_cooling_energy_per_floor_area: Maximum cooling load. Set to -np.inf for unresctricted cooling [C]
	max_heating_energy_per_floor_area: Maximum heating load per floor area. Set to no.inf for unrestricted heating [C]
	heatingSupplySystem: The type of heating system. Choices are DirectHeater, ResistiveHeater, HeatPumpHeater. Direct heater 
		has no changes to the heating demand load, a resistive heater takes an efficiency into account, and a HeatPumpHeater
		calculates a COP based on the outdoor and indoor temperature 
	coolingSupplySystem: The type of cooling system. Choices are DirectCooler HeatPumpCooler. DirectCooler
		has no changes to the cooling demand load, a HeatPumpCooler calculates a COP based on the outdoor and indoor temperature 
	heatingEfficiency: Efficiency of the heating system (note for DirectHeater this is always 1)
	coolingEfficiency: Efficiency of the cooling system (note for DirectCooler this is always 1)

###CLASS ATTRIBUTES	

	self.T_m : Room medium temperature
	self.T_air : Room air temperature
	self.T_s : Room internal surface temperature
	self.energy_demand: Room heating/cooling load. Negative if cooling, positive if heating
	self.energy_demand_unrestricted: Unrestricuted heating/coolign load. Negative if cooling, positive if heating
	self.heatingEnergy: Primary Energy input to the building (gas, electricity)
	self.coolingEnergy: Electricty input to the building
	self.lighting_demand: Lighting demand of the building
	self.has_heating_demand : Boolean if heating is required
	self.has_cooling_demand : Boolean if cooling is required


	self.heatingSystem
	self.coolingSystem
	self.heatiningEfficiency
	self.coolingEfficiency

There are other attributes that are not very important, and can be found within buildingPhysics.py. Post an issue if you have any questions

##References

Madsen, Henrik, and Jan Holst. "Estimation of continuous-time models for the heat dynamics of a building." Energy and Buildings 22.1 (1995): 67-79.

Bacher, Peder, and Henrik Madsen. "Identifying suitable models for the heat dynamics of buildings." Energy and Buildings 43.7 (2011): 1511-1522.

Sonderegger, Robert. "Diagnostic tests determining the thermal response of a house." Lawrence Berkeley National Laboratory (2010).

