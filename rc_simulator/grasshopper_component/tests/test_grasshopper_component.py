"""
Aims:
1. Compare the results generated in the ghpython simulation to a python-run model, for the same inputs
2. embed the tests from testRCmodel into grasshopper. (should auto-update to match python unit tests)

Methodology:
1. load inputs and outputs from grasshopper

2. Run simulation using inputs generated in grasshopper, over the period specified in grasshopper

- default ghpython model should be the same as the python model.
- make sure that all the inputs are the same
    - internal gains, solar gains (probably need to be taken from grasshopper)
- assert that the simulation outputs are also the same.
"""
import os, sys


import unittest
import pandas as pd

# Load grasshopper results and combine them into a single data frame
gh_result = pd.read_csv('grasshopper_result.csv')

# Todo: Figure out a better way to do this
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))
from building_physics import Building  # Importing Building Class


class TestSimulation(unittest.TestCase):


    def test_gh_results(self):
        # This should be the default rc zone, or a replication of the zone in grasshopper.
        TestZone = Building()
        t_m_prev = 20

        # Empty Lists for Storing Data to Plot
        ElectricityOut = []
        HeatingDemand = []  # Energy required by the zone
        HeatingEnergy = []  # Energy required by the supply system to provide HeatingDemand
        CoolingDemand = []  # Energy surplus of the zone
        CoolingEnergy = []  # Energy required by the supply system to get rid of CoolingDemand
        IndoorAir = []

        for h in range(0,len(gh_result)):
            internal_gains = gh_result.loc[h,'internal_gains']
            solar_gains = gh_result.loc[h,'solar_gains']
            t_out = gh_result.loc[h, 'outdoor_air_temperature']
            ill = gh_result.loc[h, 'ill']
            occupancy = gh_result.loc[h,'occupancy']

            TestZone.solve_building_energy(internal_gains, solar_gains, t_out, t_m_prev)
            TestZone.solve_building_lighting(ill, occupancy)

            ElectricityOut.append(TestZone.electricity_out)
            HeatingDemand.append(TestZone.heating_demand)
            CoolingDemand.append(TestZone.cooling_demand)
            IndoorAir.append(TestZone.t_air)

        self.assertEqual(gh_result.indoor_air_temperature[0], round(IndoorAir[0],2))



if __name__ == '__main__':
    unittest.main()