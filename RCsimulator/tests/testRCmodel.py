import sys
import os

#Set root folder one level up, just for this example
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))

import unittest
import numpy as np
from buildingPhysics import Building #Importing Building Class
import supplySystem
import emissionSystem

class TestBuildingSim(unittest.TestCase):



    def test_NoHVACNoLight(self):
        T_out = 10
        T_m_prev = 22
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)


        self.assertEqual(round(Office.T_m,2), 22.33)
        self.assertEqual(Office.energy_demand,0)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)


    def test_CoolingRequired(self):
        T_out = 25
        T_m_prev = 24
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 4000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.energy_demand,2), -264.75)
        self.assertEqual(round(Office.coolingSysElectricity,2),264.75)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.T_m,2), 25.15)
        self.assertTrue(Office.has_cooling_demand)
        
        self.assertEqual(Office.lighting_demand,0)

    def test_HeatingRequired(self):


        T_out = 10
        T_m_prev = 20
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.T_m,2), 20.46)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand,2), 328.09)
        self.assertEqual(round(Office.heatingSysElectricity,2),328.09)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)

    def test_MaxCoolingRequired(self):
        T_out = 30
        T_m_prev = 25
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 5000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.T_m,2), 26.49)
        self.assertTrue(Office.has_cooling_demand)
        self.assertEqual(round(Office.energy_demand,2), -411.6)
        self.assertEqual(round(Office.coolingSysElectricity,2),411.6)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)

    def test_MaxHeatingRequired(self):


        T_out = 5
        T_m_prev = 19
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.T_m,2), 19.39)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand,2), 411.6)
        self.assertEqual(round(Office.heatingSysElectricity,2),411.6)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)

    def test_lightingrequired(self):

        T_out = 10
        T_m_prev = 22
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        #Illuminance after transmitting through the window 
        ill = 4000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20.0,
        T_set_cooling = 26.0,
        max_cooling_energy_per_floor_area = -12.0,
        max_heating_energy_per_floor_area = 12.0,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.T_m,2), 22.33)
        self.assertEqual(Office.energy_demand,0)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(round(Office.lighting_demand,2),401.31)

    
#     ###############################Tests with infiltration variation###############################

    def test_NoHVACNoLight_infl(self):
        T_out = 10
        T_m_prev = 22
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0.66,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.T_m,2), 22.44)
        self.assertEqual(Office.energy_demand,0)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)

    def test_CoolingRequired_infl(self):
        T_out = 25
        T_m_prev = 24
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 4000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0.6,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.energy_demand,2), -296.65)
        self.assertEqual(round(Office.coolingSysElectricity,2),296.65)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.T_m,2), 25.15)
        self.assertTrue(Office.has_cooling_demand)
        
        self.assertEqual(Office.lighting_demand,0)

    def test_HeatingRequired_infl(self):


        T_out = 10
        T_m_prev = 20
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0.6,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.T_m,2), 20.46)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand,2), 9.1)
        self.assertEqual(round(Office.heatingSysElectricity,2),9.1)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)

    def test_MaxCoolingRequired_infl(self):
        T_out = 30
        T_m_prev = 25
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 5000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0.6,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.T_m,2), 26.48)
        self.assertTrue(Office.has_cooling_demand)
        self.assertEqual(round(Office.energy_demand,2), -411.6)
        self.assertEqual(round(Office.coolingSysElectricity,2),411.6)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(Office.lighting_demand,0)

    def test_MaxHeatingRequired_infl(self):


        T_out = 5
        T_m_prev = 19
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0.6,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.T_m,2), 19.51)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand,2), 411.6)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(round(Office.heatingSysElectricity,2),411.6)
        self.assertEqual(Office.lighting_demand,0)

    def test_lightingrequired_infl(self):

        T_out = 10
        T_m_prev = 22
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        #Illuminance after transmitting through the window 
        ill = 14000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0.6,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20.0,
        T_set_cooling = 26.0,
        max_cooling_energy_per_floor_area = -12.0,
        max_heating_energy_per_floor_area = 12.0,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.T_m,2), 22.43)
        self.assertEqual(Office.energy_demand,0)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.lighting_demand,2),401.31)

    def test_lightingrequired_probabiltyOff(self):

        T_out = 10
        T_m_prev = 22
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        #Illuminance after transmitting through the window 
        ill = 14000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        probLighting = 0.01

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0.6,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20.0,
        T_set_cooling = 26.0,
        max_cooling_energy_per_floor_area = -12.0,
        max_heating_energy_per_floor_area = 12.0,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy, probLighting)

        self.assertEqual(round(Office.T_m,2), 22.43)
        self.assertEqual(Office.energy_demand,0)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.lighting_demand,2),0)

    
# ############################ System Variations ########################

    def test_HeatPumpCoolingRequiredHighCOP(self):
        """Warning! Not validated yet and may have errors"""
        T_out = 25
        T_m_prev = 24
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 4000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.HeatPumpAir,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.energy_demand,2), -264.75)
        self.assertEqual(round(Office.coolingSysElectricity,2),55.87)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.T_m,2), 25.15)
        self.assertEqual(round(Office.COP,2), 4.74)
        self.assertTrue(Office.has_cooling_demand)
        
        self.assertEqual(Office.lighting_demand,0)

    def test_HeatPumpCoolingRequired(self):
        """Warning! Not validated yet and may have errors"""
        T_out = 35
        T_m_prev = 24
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 4000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.HeatPumpAir,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.energy_demand,2), -411.6)
        self.assertEqual(round(Office.coolingSysElectricity,2),107.44)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.T_m,2), 25.33)
        self.assertEqual(round(Office.COP,2), 3.83)
        self.assertTrue(Office.has_cooling_demand)
        
        self.assertEqual(Office.lighting_demand,0)

    def test_WaterHeatPumpCoolingRequired(self):
        """Warning! Not validated yet and may have errors"""
        T_out = 35
        T_m_prev = 24
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 4000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.DirectHeater,
        coolingSupplySystem = supplySystem.HeatPumpWater,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.energy_demand,2), -411.6)
        self.assertEqual(round(Office.coolingSysElectricity,2),52.12)
        self.assertEqual(round(Office.heatingSysElectricity,2),0)
        self.assertEqual(round(Office.T_m,2), 25.33)
        self.assertEqual(round(Office.COP,2), 7.9)
        self.assertTrue(Office.has_cooling_demand)
        
        self.assertEqual(Office.lighting_demand,0)

    def test_AirHeatPump_HeatingRequired_infl(self):


        T_out = 10
        T_m_prev = 20
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0.6,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.HeatPumpAir,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.T_m,2), 20.46)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand,2), 9.1)
        self.assertEqual(round(Office.heatingSysElectricity,2),2.43)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(round(Office.COP,2), 3.75)
        self.assertEqual(Office.lighting_demand,0)

    def test_WaterHeatPump_HeatingRequired_infl(self):


        T_out = 10
        T_m_prev = 20
        #Internal heat gains, in Watts
        internal_gains = 10

        #Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        #Illuminance after transmitting through the window 
        ill = 44000 #Lumens

        #Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        #Set Building Parameters
        Office = Building(window_area = 13.5 ,
        external_envelope_area = 15.19,
        room_depth = 7 ,
        room_width = 4.9 ,
        room_height = 3.1 ,
        glass_solar_transmittance = 0.687 ,
        glass_light_transmittance = 0.744 ,
        lighting_load = 11.7 ,
        lighting_control = 300,
        lighting_utilisation_factor = 0.45,
        lighting_maintenance_factor = 0.9,
        U_walls = 0.2 , 
        U_windows = 1.1,
        ACH_vent = 1.5,
        ACH_infl = 0.5,
        ventilation_efficiency = 0.6,
        thermal_capacitance_per_floor_area = 165000,
        T_set_heating = 20,
        T_set_cooling = 26,
        max_cooling_energy_per_floor_area = -12,
        max_heating_energy_per_floor_area = 12,
        heatingSupplySystem = supplySystem.HeatPumpWater,
        coolingSupplySystem = supplySystem.DirectCooler,
        heatingEmissionSystem = emissionSystem.AirConditioning,
        coolingEmissionSystem = emissionSystem.AirConditioning,
        )

        Office.solve_building_energy(internal_gains, solar_gains, T_out, T_m_prev)
        Office.solve_building_lighting(ill, occupancy)

        self.assertEqual(round(Office.T_m,2), 20.46)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand,2), 9.1)
        self.assertEqual(round(Office.heatingSysElectricity,2),1.97)
        self.assertEqual(round(Office.coolingSysElectricity,2),0)
        self.assertEqual(round(Office.COP,2), 4.62)
        self.assertEqual(Office.lighting_demand,0)

if __name__  ==  '__main__':
    unittest.main()


