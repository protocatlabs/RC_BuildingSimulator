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
Zurich = Location(epwfile_path=os.path.join(
		mainPath, 'auxiliary', 'wellington_2006.epw'))

# Initialise an instance of the building. Empty spaces take on the default
# parameters. See buildingPhysics.py to see the default values
Greenhouse = Building(window_area=110.0,
									external_envelope_area=110.0,
									room_depth=10.0,
									room_width=5.0,
									room_height=3.0,
									lighting_load=0.0,
									lighting_control=0.0,
									lighting_utilisation_factor=0.45,
									lighting_maintenance_factor=0.9,
									u_walls=0.2,
									u_windows=5.0,
									ach_vent=2.0,
									ach_infl=1.2,
									ventilation_efficiency=0.0,
									thermal_capacitance_per_floor_area=20000,
									t_set_heating=-20.0,
									t_set_cooling=260.0,
									max_cooling_energy_per_floor_area=-np.inf,
									max_heating_energy_per_floor_area=np.inf,
									heating_supply_system=supply_system.DirectHeater,
									cooling_supply_system=supply_system.DirectCooler,
									heating_emission_system=emission_system.NewRadiators,
									cooling_emission_system=emission_system.AirConditioning,)

# Define Windows
SouthWindow = Window(azimuth_tilt=0, alititude_tilt=90, glass_solar_transmittance=0.5,
										 glass_light_transmittance=0.8, area=30)

NorthWindow = Window(azimuth_tilt=180, alititude_tilt=90, glass_solar_transmittance=0.5,
										 glass_light_transmittance=0.8, area=30)

Roof = Window(azimuth_tilt=180, alititude_tilt=0, glass_solar_transmittance=0.5,
										 glass_light_transmittance=0.8, area=50)



# Starting temperature of the builidng
t_m_prev = 20

# Loop through all 8760 hours of the year
for hour in range(8760):


		# Extract the outdoor temperature in Zurich for that hour
		t_out = Zurich.weather_data['drybulb_C'][hour]

		Altitude, Azimuth = Zurich.calc_sun_position(
				latitude_deg=47.480, longitude_deg=8.536, year=2015, hoy=hour)

		# Loop through all windows
		for selected_window in [SouthWindow, NorthWindow, Roof]:
			selected_window.calc_solar_gains(sun_altitude=Altitude, sun_azimuth=Azimuth,
																			 normal_direct_radiation=Zurich.weather_data[
																					 'dirnorrad_Whm2'][hour],
																			 horizontal_diffuse_radiation=Zurich.weather_data['difhorrad_Whm2'][hour])



		Greenhouse.solve_building_energy(internal_gains=0,
																 solar_gains=SouthWindow.solar_gains, t_out=t_out, t_m_prev=t_m_prev)


		# Set the previous temperature for the next time step
		t_m_prev = Greenhouse.t_m_next

		HeatingDemand.append(Greenhouse.heating_demand)
		HeatingEnergy.append(Greenhouse.heating_energy)
		CoolingDemand.append(Greenhouse.cooling_demand)
		CoolingEnergy.append(Greenhouse.cooling_energy)
		ElectricityOut.append(Greenhouse.electricity_out)
		IndoorAir.append(Greenhouse.t_air)
		OutsideTemp.append(t_out)
		SolarGains.append(SouthWindow.solar_gains)
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

# Plotting has been commented out as it can not be conducted in a virtual environment over ssh
annualResults[['OutsideTemp','IndoorAir']].plot(alpha=0.5)
plt.show()
