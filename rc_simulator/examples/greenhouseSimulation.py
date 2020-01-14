"""
Example of an Annual Simulation
"""
__author__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = []
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"


import sys
import os

# Set root folder one level up, just for this example
mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from building_physics import Building  # Importing Building Class
import supply_system
import emission_system
from radiation import Location
from radiation import Window

matplotlib.style.use('ggplot')

# Empty Lists for Storing Data to Plot
ElectricityOut = []
HeatingDemand = []  # Energy required by the zone
HeatingEnergy = []  # Energy required by the supply system to provide HeatingDemand
CoolingDemand = []  # Energy surplus of the zone
CoolingEnergy = []  # Energy required by the supply system to get rid of CoolingDemand
IndoorAir = []
OutsideTemp = []
SolarGains = []
COP = []


# Initialise the Location with a weather file
Wellington = Location(epwfile_path=os.path.join(
		mainPath, 'auxiliary', 'wellington_2006.epw'))

# Initialise an instance of the building. Empty spaces take on the default
# parameters. See buildingPhysics.py to see the default values
Greenhouse = Building(window_area=370.0,
									external_envelope_area=370.0 + 160.0,
									room_depth=20.0,
									room_width=8.0,
									room_height=3.0,
									lighting_load=0.0,
									lighting_control=0.0,
									u_walls=0.2,
									u_windows=1.5,
									ach_vent=0.0,
									ach_infl=0.5,
									ventilation_efficiency=0.0,
									thermal_capacitance_per_floor_area=20000 * 15,
									t_set_heating=-20.0,
									t_set_cooling=260.0,
									max_cooling_energy_per_floor_area=-np.inf,
									max_heating_energy_per_floor_area=np.inf,
									heating_supply_system=supply_system.DirectHeater,
									cooling_supply_system=supply_system.DirectCooler,
									heating_emission_system=emission_system.NewRadiators,
									cooling_emission_system=emission_system.AirConditioning,)

# Define Windows

EastWall = Window(azimuth_tilt=270, alititude_tilt=90, glass_solar_transmittance=0.8,
										 glass_light_transmittance=0.9, area=60.0)

WestWall = Window(azimuth_tilt=90, alititude_tilt=90, glass_solar_transmittance=0.8,
										 glass_light_transmittance=0.9, area=60.0)

EastRoof = Window(azimuth_tilt=270, alititude_tilt=30, glass_solar_transmittance=0.8,
										 glass_light_transmittance=0.9, area=92.0)

WestRoof = Window(azimuth_tilt=90, alititude_tilt=30, glass_solar_transmittance=0.8,
										 glass_light_transmittance=0.9, area=92.0)


SouthWall = Window(azimuth_tilt=0, alititude_tilt=90, glass_solar_transmittance=0.8,
										 glass_light_transmittance=0.8, area=33.0)

NorthWall = Window(azimuth_tilt=180, alititude_tilt=90, glass_solar_transmittance=0.8,
										 glass_light_transmittance=0.8, area=33.0)



# Find default ventilation conductance rate
h_ve_adj_default = Greenhouse.h_ve_adj
print("default h_ve_sdj is:", h_ve_adj_default)

# Starting temperature of the builidng
t_m_prev = 20

heating_hours = 0

# Loop through all 8760 hours of the year
for hour in range(8760):


		# Extract the outdoor temperature in Wellington for that hour
		t_out = Wellington.weather_data['drybulb_C'][hour]

		Altitude, Azimuth = Wellington.calc_sun_position(
				latitude_deg= -40.750, longitude_deg=175.13, year=2020, hoy=hour)

		# Loop through all windows
		total_solar_gains = 0
		for selected_window in [EastWall, WestWall, EastRoof, WestRoof, SouthWall, NorthWall]:
			selected_window.calc_solar_gains(sun_altitude=Altitude, sun_azimuth=Azimuth,
												normal_direct_radiation=Wellington.weather_data[
												'dirnorrad_Whm2'][hour],
												horizontal_diffuse_radiation=Wellington.weather_data['difhorrad_Whm2'][hour])

			#print(selected_window.solar_gains)
			total_solar_gains += selected_window.solar_gains
		#print("hour is",hour)
		# print("south", SouthWindow.solar_gains)
		# print("north", NorthWindow.solar_gains)
		# print("roof",Roof.solar_gains)
		# print("total", total_solar_gains)

		
		Greenhouse.solve_building_energy(internal_gains=0,solar_gains=total_solar_gains, t_out=t_out, t_m_prev=t_m_prev)


		# Add ventilation control to reduce upper bound temperatures 
		if Greenhouse.t_air > 35:
			Greenhouse.h_ve_adj = h_ve_adj_default * 10 # Open windows, rough assumption
			# Rerun calculation with windows open
			Greenhouse.solve_building_energy(internal_gains=0,solar_gains=total_solar_gains, t_out=t_out, t_m_prev=t_m_prev)
		else:
			Greenhouse.h_ve_adj = h_ve_adj_default # closed windows

		if Greenhouse.t_air < 15:
			heating_hours += 1

		# Set the previous temperature for the next time step
		t_m_prev = Greenhouse.t_m_next

		HeatingDemand.append(Greenhouse.heating_demand)
		HeatingEnergy.append(Greenhouse.heating_energy)
		CoolingDemand.append(Greenhouse.cooling_demand)
		CoolingEnergy.append(Greenhouse.cooling_energy)
		ElectricityOut.append(Greenhouse.electricity_out)
		IndoorAir.append(Greenhouse.t_air)
		OutsideTemp.append(t_out)
		SolarGains.append(total_solar_gains)
		COP.append(Greenhouse.cop)


annualResults = pd.DataFrame({
		'HeatingDemand': HeatingDemand,
		'HeatingEnergy': HeatingEnergy,
		'CoolingDemand': CoolingDemand,
		'CoolingEnergy': CoolingEnergy,
		'IndoorAir': IndoorAir,
		'OutsideTemp':  OutsideTemp,
		'SolarGains': SolarGains,
		'COP': COP
})

# print(annualResults.IndoorAir)
# print(annualResults.IndoorAir[0:10])

print("hours of heating are", heating_hours)

start = 4200
end = 4200 + 24*7

fig = plt.figure()
plt.plot(range(start,end), annualResults.IndoorAir[start:end], range(start,end), annualResults.OutsideTemp[start:end], alpha = 0.5 )
plt.xlabel('Hour of the year (0 - 8760)')
plt.ylabel('Temperature (C)')
plt.legend(['Indoor Air','Outdoor Air'])
plt.savefig("temp.png", format="png")
#annualResults[['OutsideTemp','IndoorAir']].plot(alpha=0.5)
plt.show()

