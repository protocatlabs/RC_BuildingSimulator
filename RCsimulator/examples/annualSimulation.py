"""
=========================================
Example of an Annual Simulation
=========================================
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
from buildingPhysics import Building  # Importing Building Class
import supplySystem
import emissionSystem
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
    mainPath, 'auxiliary', 'Zurich-Kloten_2013.epw'))

# Initialise an instance of the building. Empty spaces take on the default
# parameters. See buildingPhysics.py to see the default values
Office = Building(window_area=4.0,
                  external_envelope_area=15.0,
                  room_depth=7.0,
                  room_width=5.0,
                  room_height=3.0,
                  lighting_load=11.7,
                  lighting_control=300.0,
                  lighting_utilisation_factor=0.45,
                  lighting_maintenance_factor=0.9,
                  U_walls=0.2,
                  U_windows=1.1,
                  ACH_vent=1.5,
                  ACH_infl=0.5,
                  ventilation_efficiency=0.6,
                  thermal_capacitance_per_floor_area=165000,
                  T_set_heating=20.0,
                  T_set_cooling=26.0,
                  max_cooling_energy_per_floor_area=-np.inf,
                  max_heating_energy_per_floor_area=np.inf,
                  heatingSupplySystem=supplySystem.OilBoilerMed,
                  coolingSupplySystem=supplySystem.HeatPumpAir,
                  heatingEmissionSystem=emissionSystem.NewRadiators,
                  coolingEmissionSystem=emissionSystem.AirConditioning,)

# Define Windows
SouthWindow = Window(azimuth_tilt=0, alititude_tilt=90, glass_solar_transmittance=0.7,
                     glass_light_transmittance=0.8, area=4)


# Define constants for the building
gain_per_person = 100  # W per person
appliance_gains = 14  # W per sqm
max_occupancy = 3.0


# Read Occupancy Profile
occupancyProfile = pd.read_csv(os.path.join(
    mainPath, 'auxiliary', 'schedules_el_OFFICE.csv'))

# Starting temperature of the builidng
T_m_prev = 20

# Loop through all 8760 hours of the year
for hour in range(8760):

    # Occupancy for the time step
    occupancy = occupancyProfile.loc[hour, 'People'] * max_occupancy
    # Gains from occupancy and appliances
    internal_gains = occupancy * gain_per_person + \
        appliance_gains * Office.floor_area

    # Extract the outdoor temperature in Zurich for that hour
    T_out = Zurich.weather_data['drybulb_C'][hour]

    Altitude, Azimuth = Zurich.calc_sun_position(
        latitude_deg=47.480, longitude_deg=8.536, year=2015, HOY=hour)

    SouthWindow.calc_solar_gains(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                 normal_direct_radiation=Zurich.weather_data[
                                     'dirnorrad_Whm2'][hour],
                                 horizontal_diffuse_radiation=Zurich.weather_data['difhorrad_Whm2'][hour])

    SouthWindow.calc_illuminance(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                 normal_direct_illuminance=Zurich.weather_data[
                                     'dirnorillum_lux'][hour],
                                 horizontal_diffuse_illuminance=Zurich.weather_data['difhorillum_lux'][hour])

    Office.solve_building_energy(internal_gains=internal_gains,
                                 solar_gains=SouthWindow.solar_gains, T_out=T_out, T_m_prev=T_m_prev)

    Office.solve_building_lighting(
        illuminance=SouthWindow.transmitted_illuminance, occupancy=occupancy)

    # Set the previous temperature for the next time step
    T_m_prev = Office.T_m_next

    HeatingDemand.append(Office.heatingDemand)
    HeatingEnergy.append(Office.heatingEnergy)
    CoolingDemand.append(Office.coolingDemand)
    CoolingEnergy.append(Office.coolingEnergy)
    ElectricityOut.append(Office.electricityOut)
    IndoorAir.append(Office.T_air)
    OutsideTemp.append(T_out)
    SolarGains.append(SouthWindow.solar_gains)
    COP.append(Office.COP)

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


annualResults[['HeatingEnergy', 'CoolingEnergy']].plot()
plt.show()
