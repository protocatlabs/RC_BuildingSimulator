"""
=========================================
Physics Required to calculate sensible space heating and space cooling loads, and space lighting loads
EN-13970
=========================================
"""

import numpy as np
#from SupplySystem import SupplyDirector
from supplySystem import *
from emissionSystem import * 


__authors__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle, Justin Zarb, Michael Fehr"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "BETA"



"""
The equations presented here is this code are derived from ISO 13790 Annex C, Methods are listed in order of apperance in the Annex 

Daylighting is based on methods in The Environmental Science Handbook, S V Szokolay

HOW TO USE
from buildingPhysics import Building #Importing Building Class
Office=Building() #Set an instance of the class
Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev) #Solve for Heating
Office.solve_building_lighting(ill, occupancy) #Solve for Lighting


VARIABLE DEFINITION

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


	
INPUT PARAMETER DEFINITION 

	window_area: Area of the Glazed Surface  [m2]
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
"""



class Building(object):
	'''Sets the parameters of the building. '''

	def __init__(self,
				 window_area=13.5,
				 room_depth=7.0,
				 room_width=4.9,
				 room_height=3.1,
				 glass_solar_transmittance=0.687,
				 glass_light_transmittance=0.744,
				 lighting_load=11.7,
				 lighting_control = 300,
				 lighting_utilisation_factor=0.45,
				 lighting_maintenance_factor=0.9,
				 U_walls = 0.2,
				 U_windows = 1.1,
				 ACH_vent=1.5,
				 ACH_infl=0.5,
				 ventilation_efficiency=.6,
				 thermal_capacitance_per_floor_area = 165000,
				 T_set_heating = 20.0,
				 T_set_cooling = 26.0,
				 max_cooling_energy_per_floor_area=-np.inf,
				 max_heating_energy_per_floor_area=np.inf,
				 heatingSupplySystem=OilBoilerMed,
				 coolingSupplySystem=HeatPumpAir,
				 heatingEmissionSystem=NewRadiators,
				 coolingEmissionSystem=AirConditioning,
				 ):
		

		#Building Dimensions
		self.window_area=window_area #[m2] Window Area
		self.room_depth=room_depth #[m] Room Depth
		self.room_width=room_width #[m] Room Width
		self.room_height=room_height #[m] Room Height

		#Fenstration and Lighting Properties
		self.glass_solar_transmittance=glass_solar_transmittance #Dbl LoE (e=0.2) Clr 3mm/13mm Air
		self.glass_light_transmittance=glass_light_transmittance #Dbl LoE (e=0.2) Clr 3mm/13mm Air
		self.lighting_load=lighting_load #[kW/m2] lighting load
		self.lighting_control = lighting_control #[lux] Lighting setpoint
		self.lighting_utilisation_factor=lighting_utilisation_factor #How the light entering the window is transmitted to the working plane
		self.lighting_maintenance_factor= lighting_maintenance_factor #How dirty the window is. Section 2.2.3.1 Environmental Science Handbook

		#Calculated Properties
		self.floor_area=room_depth*room_width #[m2] Floor Area
		self.mass_area=self.floor_area* 2.5 #[m2] Effective Mass Area assuming a medium weight building #12.3.1.2
		self.Room_Vol=room_width*room_depth*room_height #[m3] Room Volume
		self.total_internal_area=self.floor_area*2 + room_width*room_height*2 + room_depth*room_height*2
		self.A_t=self.total_internal_area #TODO: Standard doesn't explain what A_t is. Needs to be checked

		#Single Capacitance  5 conductance Model Parameters
		self.c_m= thermal_capacitance_per_floor_area * self.floor_area #[kWh/K] Room Capacitance. Default based on ISO standard 12.3.1.2 for medium heavy buildings
		self.h_tr_em = U_walls*(room_height*room_width-window_area) #Conductance of opaque surfaces to exterior [W/K]
		self.h_tr_w = U_windows*window_area  #Conductance to exterior through glazed surfaces [W/K], based on U-wert of 1W/m2K
		
		#Determine the ventilation conductance
		ACH_tot=ACH_infl+ACH_vent #Total Air Changes Per Hour
		b_ek=(1-(ACH_vent/(ACH_tot))*ventilation_efficiency) #temperature adjustement factor taking ventilation and inflimtration [ISO: E -27]
		self.h_ve_adj =    1200*b_ek*self.Room_Vol*(ACH_tot/3600)  #Conductance through ventilation [W/M]
		self.h_tr_ms =     9.1 * self.mass_area #transmittance from the internal air to the thermal mass of the building
		self.h_tr_is =     self.total_internal_area * 3.45 # Conductance from the conditioned air to interior building surface

		#Thermal set points
		self.T_set_heating = T_set_heating
		self.T_set_cooling = T_set_cooling

		#Thermal Properties
		self.has_heating_demand=False #Boolean for if heating is required
		self.has_cooling_demand=False #Boolean for if cooling is required
		self.max_cooling_energy = max_cooling_energy_per_floor_area*self.floor_area #max cooling load (W/m2)
		self.max_heating_energy = max_heating_energy_per_floor_area*self.floor_area #max heating load (W/m2)

		#Building System Properties
		self.heatingSupplySystem=heatingSupplySystem
		self.coolingSupplySystem=coolingSupplySystem
		self.heatingEmissionSystem=heatingEmissionSystem
		self.coolingEmissionSystem=coolingEmissionSystem

		
	def calc_heat_flow(self,T_out, internal_gains, solar_gains, energy_demand):
		#C.1 - C.3 in [C.3 ISO 13790]

		#Calculates the heat flows to various points of the building based on the breakdown in section C.2, formulas C.1-C.3
		#Emission System Director is called to action (setBuilder and calcFlows available)
		emDirector = EmissionDirector()
		
		
		emDirector.setBuilder(self.heatingEmissionSystem(T_out=T_out, internal_gains=internal_gains, solar_gains=solar_gains, energy_demand=energy_demand, mass_area=self.mass_area, A_t=self.A_t, h_tr_w=self.h_tr_w, T_set_heating=self.T_set_heating, T_set_cooling=self.T_set_cooling))  #heatingEmissionSystem chosen
		
		flows = emDirector.calcFlows()
		
		self.phi_ia = flows.phi_ia 
		self.phi_st = flows.phi_st 
		self.phi_m = flows.phi_m 
		self.heatingSupplyTemperature = flows.heatingSupplyTemperature
		self.coolingSupplyTemperature = flows.coolingSupplyTemperature


	def calc_T_m_next(self, T_m_prev):
		# (C.4) in [C.3 ISO 13790]
		#Primary Equation, calculates the temperature of the next time step
		self.T_m_next = ((T_m_prev*((self.c_m/3600.0)-0.5*(self.h_tr_3+self.h_tr_em))) + self.phi_m_tot) / ((self.c_m/3600.0)+0.5*(self.h_tr_3+self.h_tr_em))


	def calc_phi_m_tot(self, T_out):
		# (C.5) in [C.3 ISO 13790]
		# h_ve = h_ve_adj and T_supply = T_out [9.3.2 ISO 13790]

		#Calculates a global heat transfer. This is a definition used to simplify equation calc_T_m_next so it's not so long to write out

		T_supply=T_out #ASSUMPTION: Supply air comes straight from the outside air

		self.phi_m_tot = self.phi_m + self.h_tr_em*T_out + \
		self.h_tr_3*(self.phi_st + self.h_tr_w*T_out+self.h_tr_1*((self.phi_ia/self.h_ve_adj)+T_supply))/self.h_tr_2


	def calc_h_tr_1(self):
		# (C.6) in [C.3 ISO 13790]
		#Definition to simplify calc_phi_m_tot
		self.h_tr_1 = 1.0/(1.0/self.h_ve_adj + 1.0/self.h_tr_is)


	def calc_h_tr_2(self):
		# (C.7) in [C.3 ISO 13790]
		#Definition to simplify calc_phi_m_tot
		self.h_tr_2 = self.h_tr_1 + self.h_tr_w


	def calc_h_tr_3(self):
		# (C.8) in [C.3 ISO 13790]
		#Definition to simplify calc_phi_m_tot
		self.h_tr_3 = 1.0/(1.0/self.h_tr_2 + 1.0/self.h_tr_ms)
		
		#print 'h_tr_3=', self.h_tr_3

	'''Functions to Calculate the temperatures at the nodes'''

	def calc_T_m(self,T_m_prev):
		#Temperature used for the calculations, average between newly calculated and previous bulk temperature
		# (C.9) in [C.3 ISO 13790]
		self.T_m = (self.T_m_next+T_m_prev)/2.0

	def calc_T_s(self, T_out):
		# (C.10) in [C.3 ISO 13790]
		# h_ve = h_ve_adj and T_supply = T_out [9.3.2 ISO 13790]

		#Calculate the temperature of the inside room surfaces
		T_supply=T_out #ASSUMPTION: Supply air comes straight from the outside air

		self.T_s = (self.h_tr_ms*self.T_m+self.phi_st+self.h_tr_w*T_out+self.h_tr_1*(T_supply+self.phi_ia/self.h_ve_adj)) / \
				  (self.h_tr_ms+self.h_tr_w+self.h_tr_1)



	def calc_T_air(self, T_out):
		# (C.11) in [C.3 ISO 13790]
		# h_ve = h_ve_adj and T_supply = T_out [9.3.2 ISO 13790]

		T_supply=T_out

		#Calculate the temperature of the inside air
		self.T_air = (self.h_tr_is * self.T_s + self.h_ve_adj * T_supply + self.phi_ia) / (self.h_tr_is + self.h_ve_adj)


	def calc_T_opperative(self):

		# (C.12) in [C.3 ISO 13790]

		#The opperative temperature is a weighted average of the air and mean radiant temperatures. It is not used in any further calculation at this stage
		self.T_opperative = 0.3 * self.T_air + 0.7 * self.T_s

	'''Derivate using the Crank-Nicolson method'''

	def calc_temperatures_crank_nicolson(self, energy_demand, internal_gains, solar_gains, T_out, T_m_prev):
		# section C.3 in [C.3 ISO 13790]
		# calculates air temperature and operative temperature for a given heating/cooling load
		#It effectively runs all the functions above


		self.calc_heat_flow(T_out, internal_gains, solar_gains, energy_demand)

		self.calc_phi_m_tot(T_out)

		self.calc_T_m_next(T_m_prev)  #calculates the new bulk temperature POINT from the old one

		self.calc_T_m(T_m_prev)  #calculates the AVERAGE bulk temperature used for the remaining calculation

		self.calc_T_s(T_out)

		self.calc_T_air(T_out)

		self.calc_T_opperative()

		return self.T_m, self.T_air, self.T_opperative
	
	

	def has_demand(self,internal_gains, solar_gains,T_out, T_m_prev):
		# step 1 in section C.4.2 in [C.3 ISO 13790]
		#Determines if the building has a heating or cooling demand

		#set energy demand to 0 and see if temperatures are within the confort range
		energy_demand=0
		#Solve for the internal temperature T_Air
		self.calc_temperatures_crank_nicolson(energy_demand, internal_gains, solar_gains, T_out, T_m_prev)

		#If the air temperature is less or greater than the set temperature, there is a heating/cooling load
		if self.T_air < self.T_set_heating:
			self.has_heating_demand=True
			self.has_cooling_demand=False
		elif self.T_air > self.T_set_cooling:
			self.has_cooling_demand=True
			self.has_heating_demand=False
		else:
			self.has_heating_demand=False
			self.has_cooling_demand=False


	def calc_energy_demand_unrestricted(self, energy_floorAx10, T_air_set, T_air_0, T_air_10):
		# calculates unrestricted heating power
		# (C.13) in [C.3 ISO 13790]

		'''Based on the Thales Intercept Theorem. 
		Where we set a heating case that is 10x the floor area and determine the temperature as a result 
		Assuming that the relation is linear, one can draw a right angle triangle. 
		From this we can determine the heating level required to achieve the set point temperature
		This assumes a perfect HVAC control system
		'''
		self.energy_demand_unrestricted = energy_floorAx10*(T_air_set - T_air_0)/(T_air_10 - T_air_0)


	def calc_energy_demand(self, internal_gains, solar_gains, T_out, T_m_prev):
		# Crank-nicolson calculation procedure if heating/cooling system is active
		# Step 1 - Step 4 in Section C.4.2 in [C.3 ISO 13790]

		# Step 1: Check if heating or cooling is needed (Michael: check isn't needed, is in calling function)
		#Set heating/cooling to 0
		energy_demand_0 = 0
		#Calculate the air temperature with no heating/cooling
		T_air_0=self.calc_temperatures_crank_nicolson(energy_demand_0, internal_gains, solar_gains, T_out, T_m_prev)[1] #This is more stable
		#T_air_0 = self.T_air #This should return the same value


		# Step 2: Calculate the unrestricted heating/cooling required

		#determine if we need heating or cooling based based on the condition that no heating or cooling is required
		if self.has_heating_demand:
			T_air_set = self.T_set_heating
		elif self.has_cooling_demand:
			T_air_set=self.T_set_cooling
		else:
			raise ValueError('heating function has been called even though no heating is required')

		#Set a heating case where the heating load is 10x the floor area (10 W/m2)
		energy_floorAx10 = 10 * self.floor_area

		#Calculate the air temperature obtained by having this 10 W/m2 setpoint
		T_air_10=self.calc_temperatures_crank_nicolson(energy_floorAx10, internal_gains, solar_gains, T_out, T_m_prev)[1]

		#Determine the unrestricted heating/cooling off the building
		self.calc_energy_demand_unrestricted(energy_floorAx10,T_air_set, T_air_0, T_air_10)


		# Step 3: Check if available heating or cooling power is sufficient
		if self.max_cooling_energy <= self.energy_demand_unrestricted <= self.max_heating_energy:

			self.energy_demand = self.energy_demand_unrestricted
			self.T_air_ac = T_air_set #not sure what this is used for at this stage TODO

		# Step 4: if not sufficient then set the heating/cooling setting to the maximum
		elif self.energy_demand_unrestricted > self.max_heating_energy: # necessary heating power exceeds maximum available power

			self.energy_demand = self.max_heating_energy

		elif self.energy_demand_unrestricted < self.max_cooling_energy: # necessary cooling power exceeds maximum available power

			self.energy_demand = self.max_cooling_energy

		else: 
			self.energy_demand = 0
			raise ValueError('unknown radiative heating/cooling system status')



		# calculate system temperatures for Step 3/Step 4
		self.calc_temperatures_crank_nicolson(self.energy_demand, internal_gains, solar_gains, T_out, T_m_prev)



	def solve_building_energy(self,internal_gains, solar_gains,T_out, T_m_prev):


		#Calculate the heat transfer definitions for formula simplification
		self.calc_h_tr_1()
		self.calc_h_tr_2()
		self.calc_h_tr_3()

		# check demand
		self.has_demand(internal_gains, solar_gains,T_out, T_m_prev)

		if not self.has_heating_demand and not self.has_cooling_demand:

			# no heating or cooling demand
			# calculate temperatures of building R-C-model and exit
			# --> rc_model_function_1(...)
			self.energy_demand=0
			self.calc_temperatures_crank_nicolson(self.energy_demand, internal_gains, solar_gains, T_out, T_m_prev)
			self.heatingDemand=0             #Energy required by the zone
			self.coolingDemand=0             #Energy surplus of the zone   
			self.heatingSysElectricity=0     #Energy (in electricity) required by the supply system to provide HeatingDemand
			self.heatingSysFossils=0         #Energy (in fossil fuel) required by the supply system to provide HeatingDemand
			self.coolingSysElectricity=0     #Energy (in electricity) required by the supply system to get rid of CoolingDemand
			self.coolingSysFossils=0          #Energy (in fossil fuel) required by the supply system to get rid of CoolingDemand
			self.electricityOut=0            #Electricity produced by the supply system (e.g. CHP)


		else:

			# has heating/cooling demand
			
			self.calc_energy_demand(internal_gains, solar_gains, T_out, T_m_prev)  # Calculates energy_demand used below
  
			self.calc_temperatures_crank_nicolson(self.energy_demand, internal_gains, solar_gains, T_out, T_m_prev)[1]  
			#calculates the actual T_m resulting from the actual heating demand (energy_demand)
			

			##Calculate the Heating/Cooling Input Energy Required

			supDirector = SupplyDirector() #Initialise Heating System Manager

			if self.has_heating_demand:
				supDirector.setBuilder(self.heatingSupplySystem(Load=self.energy_demand, T_out=T_out, heatingSupplyTemperature=self.heatingSupplyTemperature, coolingSupplyTemperature=self.coolingSupplyTemperature, has_heating_demand=self.has_heating_demand, has_cooling_demand=self.has_cooling_demand))  
				supplyOut = supDirector.calcSystem()
				self.heatingDemand=self.energy_demand                       #All Variables explained underneath line 467
				self.heatingSysElectricity=supplyOut.electricityIn
				self.heatingSysFossils=supplyOut.fossilsIn
				self.coolingDemand=0
				self.coolingSysElectricity=0
				self.coolingSysFossils=0
				self.electricityOut=supplyOut.electricityOut


			elif self.has_cooling_demand:
				supDirector.setBuilder(self.coolingSupplySystem(Load=self.energy_demand*(-1), T_out=T_out, heatingSupplyTemperature=self.heatingSupplyTemperature, coolingSupplyTemperature=self.coolingSupplyTemperature, has_heating_demand=self.has_heating_demand, has_cooling_demand=self.has_cooling_demand))
				supplyOut = supDirector.calcSystem()
				self.heatingDemand=0
				self.heatingSysElectricity=0
				self.heatingSysFossils=0
				self.coolingDemand=self.energy_demand
				self.coolingSysElectricity=supplyOut.electricityIn
				self.coolingSysFossils=supplyOut.fossilsIn
				self.electricityOut=supplyOut.electricityOut
			
			self.COP=supplyOut.COP

		self.sysTotalEnergy = self.heatingSysElectricity + self.heatingSysFossils + self.coolingSysElectricity + self.coolingSysFossils
		self.heatingEnergy = self.heatingSysElectricity + self.heatingSysFossils
		self.coolingEnergy = self.coolingSysElectricity + self.coolingSysFossils
		
		return

	####################################################Lighting Calculations###################################################
	def solve_building_lighting(self, ill, occupancy, probLighting=1):

		#Cite: Environmental Science Handbook, SV Szokolay, Section 2.2.1.3
		Lux=(ill*self.lighting_utilisation_factor*self.lighting_maintenance_factor*self.glass_light_transmittance)/self.floor_area #[Lux]

		if Lux < self.lighting_control and occupancy>0 and probLighting>0.1:
			self.lighting_demand=self.lighting_load*self.floor_area #Lighting demand for the hour
		else:
			self.lighting_demand=0










