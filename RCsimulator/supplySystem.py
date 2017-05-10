"""
=========================================
Supply System Parameters for Heating and Cooling

=========================================
"""

import numpy as np

__author__ = "Prageeth Jayathissa, Michael Fehr"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = [""]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "BETA"


"""
Model of different Supply systems. New Supply Systems can be introduced by adding new classes

TODO: Have a look at CEA calculation methodology 
https://github.com/architecture-building-systems/CEAforArcGIS/blob/master/cea/technologies/heatpumps.py
"""


class SupplyDirector:

    """
    The director sets what Supply system is being used, and runs that set Supply system
    """

    __builder = None

    # Sets what building system is used
    def setBuilder(self, builder):
        self.__builder = builder

    # Calcs the energy load of that system. This is the main() fu
    def calcSystem(self):

        # Director asks the builder to produce the system body. self.__builder
        # is an instance of the class

        body = self.__builder.calcLoads()

        return body


class SupplyBuilder:

    """ The base class in which Supply systems are built from 
    """

    def __init__(self, Load, T_out, heatingSupplyTemperature, coolingSupplyTemperature, has_heating_demand, has_cooling_demand):
        self.Load = Load  # Energy Demand of the building at that time step
        self.T_out = T_out  # Outdoor Air Temperature
        # Temperature required by the emission system
        self.heatingSupplyTemperature = heatingSupplyTemperature
        self.coolingSupplyTemperature = coolingSupplyTemperature
        self.has_heating_demand = has_heating_demand
        self.has_cooling_demand = has_cooling_demand

    def calcLoads(self): pass


class OilBoilerOld(SupplyBuilder):
    # Old oil boiler with fuel efficiency of 63 percent (medium of range in report of semester project M. Fehr)
    # No condensation, pilot light

    def calcLoads(self):
        system = SupplyOut()
        system.fossilsIn = self.Load / 0.63
        system.electricityIn = 0
        system.electricityOut = 0
        return system


class OilBoilerMed(SupplyBuilder):
    # Classic oil boiler with fuel efficiency of 82 percent (medium of range in report of semester project M. Fehr)
    # No condensation, but better nozzles etc.

    def calcLoads(self):
        system = SupplyOut()
        system.fossilsIn = self.Load / 0.82
        system.electricityIn = 0
        system.electricityOut = 0
        return system


class OilBoilerNew(SupplyBuilder):
    # New oil boiler with fuel efficiency of 98 percent (value from report of semester project M. Fehr)
    # Condensation boiler, latest generation

    def calcLoads(self):
        system = SupplyOut()
        system.fossilsIn = self.Load / 0.98
        system.electricityIn = 0
        system.electricityOut = 0
        return system


class HeatPumpAir(SupplyBuilder):
    """
    BETA Version
    Air-Water heat pump. Outside Temperature as reservoir temperature.
    COP based off regression analysis of manufacturers data
    Source: "A review of domestic heat pumps, Iain Staffell, Dan Brett, Nigel Brandonc and Adam Hawkes"
    http://pubs.rsc.org/en/content/articlepdf/2012/ee/c2ee22653g
    """
    # TODO: Validate this methodology

    def calcLoads(self):
        system = SupplyOut()

        if self.has_heating_demand:
            # determine the temperature difference, if negative, set to 0
            deltaT = max(0, self.heatingSupplyTemperature - self.T_out)
            # Eq (4) in Staggell et al.
            system.COP = 6.81 - 0.121 * deltaT + 0.000630 * deltaT**2
            system.electricityIn = self.Load / system.COP

        elif self.has_cooling_demand:
            # determine the temperature difference, if negative, set to 0
            deltaT = max(0, self.T_out - self.coolingSupplyTemperature)
            # Eq (4) in Staggell et al.
            system.COP = 6.81 - 0.121 * deltaT + 0.000630 * deltaT**2
            system.electricityIn = self.Load / system.COP

        else:
            raise ValueError(
                'HeatPumpAir called although there is no heating/cooling demand')

        system.fossilsIn = 0
        system.electricityOut = 0
        return system


class HeatPumpWater(SupplyBuilder):
    """"
    BETA Version
    Reservoir temperatures 7 degC (winter) and 12 degC (summer).
    Ground-Water heat pump. Outside Temperature as reservoir temperature.
    COP based off regression analysis of manufacturers data
    Source: "A review of domestic heat pumps, Iain Staffell, Dan Brett, Nigel Brandonc and Adam Hawkes"
    http://pubs.rsc.org/en/content/articlepdf/2012/ee/c2ee22653g
    """
    # TODO: Validate this methodology

    def calcLoads(self):
        system = SupplyOut()
        if self.has_heating_demand:
            deltaT = max(0, self.heatingSupplyTemperature - 7.0)
            # Eq (4) in Staggell et al.
            system.COP = 8.77 - 0.150 * deltaT + 0.000734 * deltaT**2
            system.electricityIn = self.Load / system.COP

        elif self.has_cooling_demand:
            deltaT = max(0, 12.0 - self.coolingSupplyTemperature)
            # Eq (4) in Staggell et al.
            system.COP = 8.77 - 0.150 * deltaT + 0.000734 * deltaT**2
            system.electricityIn = self.Load / system.COP

        system.fossilsIn = 0
        system.electricityOut = 0
        return system


class ElectricHeating(SupplyBuilder):
    # Straight forward electric heating. 100 percent conversion to heat.

    def calcLoads(self):
        system = SupplyOut()
        system.electricityIn = self.Load
        system.fossilsIn = 0
        system.electricityOut = 0
        return system


class CHP(SupplyBuilder):
    # Combined heat and power unit with 60 percent thermal and 33 percent
    # electrical fuel conversion. 93 percent overall

    def calcLoads(self):
        system = SupplyOut()
        system.fossilsIn = self.Load / 0.6
        system.electricityIn = 0
        system.electricityOut = system.fossilsIn * 0.33
        return system


class DirectHeater(SupplyBuilder):
    # Created by PJ to check accuracy against previous simulation

    def calcLoads(self):
        system = SupplyOut()
        system.electricityIn = self.Load
        system.fossilsIn = 0
        system.electricityOut = 0
        return system


class DirectCooler(SupplyBuilder):
    # Created by PJ to check accuracy against previous simulation

    def calcLoads(self):
        system = SupplyOut()
        system.electricityIn = self.Load
        system.fossilsIn = 0
        system.electricityOut = 0
        return system


class SupplyOut:
    # The System class which is used to output the final results
    fossilsIn = None
    electricityIn = None
    electricityOut = None
    COP = None
