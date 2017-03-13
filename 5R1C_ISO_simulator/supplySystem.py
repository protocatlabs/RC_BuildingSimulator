"""
=========================================
Supply System Parameters for Heating and Cooling

=========================================
"""

import numpy as np
from emissionSystem import *


__author__ = "Prageeth Jayathissa, Michael Fehr"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = [""]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"



"""
Model of different SUPPLY systems. New SUPPLY Systems can be introduced by adding new classes
"""

class supplyDirector:
    
    """
    The director sets what SUPPLY system is being used, and runs that set SUPPLY system
    """

    __builder = None
    

    #Sets what building system is used
    def setBuilder(self, builder):
        self.__builder = builder

    # Calcs the energy load of that system. This is the main() fu
    def calcSystem(self):

        # Director asks the builder to produce the system body. self.__builder is an instance of the class
        
        body = self.__builder.calcLoads()

        return body 


class supplyBuilder:

    """ The base class in which supply systems are built from 
    """

    def __init__(self, Load, theta_e, theta_m, supplyTemperature):
        self.Load=Load #Energy Demand of the building at that time step
        self.theta_e=theta_e #Outdoor Air Temperature
        self.theta_m=theta_m #Room Temperature at that timestep
        self.supplyTemperature = supplyTemperature # Temperature required by the emission system
        


    def calcLoads(self): pass
#    def calcCoolingLoads(self): pass


class OilBoilerOld(supplyBuilder):
    #Old oil boiler with fuel efficiency of 63% (medium of range in report of semester project M. Fehr)
    #No condensation, pilot light

    def calcLoads(self):
        heater = SupplyOut()
        heater.energyIn = self.Load/0.63
        heater.electricityOut = 0
        return heater


class OilBoilerMed(supplyBuilder):
    #Classic oil boiler with fuel efficiency of 82% (medium of range in report of semester project M. Fehr)
    #No condensation, but better nozzles etc.
    
    def calcLoads(self):
        heater = SupplyOut()
        heater.energyIn = self.Load/0.82
        heater.electricityOut = 0
        return heater


class OilBoilerNew(supplyBuilder):
    #New oil boiler with fuel efficiency of 98% (value from report of semester project M. Fehr)
    #Condensation boiler, latest generation

    def calcLoads(self):
        heater = SupplyOut()
        heater.energyIn = self.Load/0.98
        heater.electricityOut = 0
        return heater


class HeatPumpAir(supplyBuilder):
    #Air-Water heat pump. epsilon_carnot = 0.4. Outside Temperature as reservoir temperature.

    def calcLoads(self):
        if self.Load > 0:                                   #Heating
            heater = SupplyOut()
            heater.energyIn = self.Load/(0.4*(self.supplyTemperature+273)/(self.supplyTemperature-self.theta_e))
            heater.electricityOut = 0
        else:                                               #Cooling
            heater = SupplyOut()
            heater.energyIn = self.Load/(0.4*(self.supplyTemperature+273)/(self.theta_e-self.supplyTemperature))
            heater.electricityOut = 0
        return heater

class HeatPumpWater(supplyBuilder):
    #Water-Water heat pump. epsilon_carnot = 0.5. Outside Temperature as reservoir temperature.

    def calcLoads(self):
        if self.Load > 0:                                   #Heating
            heater = SupplyOut()
            heater.energyIn = self.Load/(0.5*(self.supplyTemperature+273)/(self.supplyTemperature-self.theta_e))
            heater.electricityOut = 0
        else:                                               #Cooling
            heater = SupplyOut()
            heater.energyIn = self.Load/(0.5*(self.supplyTemperature+273)/(self.theta_e-self.supplyTemperature))
            heater.electricityOut = 0
        return heater


class HeatPumpGround(supplyBuilder):
    #Ground-Water heat pump. epsilon_carnot = 0.45. Outside Temperature as reservoir temperature.

    def calcLoads(self):
        if self.Load > 0:                                   #Heating
            heater = SupplyOut()
            heater.energyIn = self.Load/(0.45*(self.supplyTemperature+273)/(self.supplyTemperature-self.theta_e))
            heater.electricityOut = 0
        else:                                               #Cooling
            heater = SupplyOut()
            heater.energyIn = self.Load/(0.45*(self.supplyTemperature+273)/(self.theta_e-self.supplyTemperature))
            heater.electricityOut = 0
        return heater


class ElectricHeating(supplyBuilder):
    #The heat pump calculates a COP with an efficiency and outputs the electricty input requirement
    
    def calcLoads(self):
        cooler=SupplyOut()
        cooler.COP=self.efficiency*((self.theta_m_prev+273.0)/(self.theta_e-self.theta_m_prev))
        if cooler.COP<=0: #TODO: This is a quick hackaround of the actual system!!! FIX!!!!
            cooler.COP=self.efficiency*100
        cooler.electricity=self.Load/cooler.COP
        return cooler
    


class CHP(supplyBuilder):
    #The heat pump calculates a COP with an efficiency and outputs the electricty input requirement
    
    def calcLoads(self):
        cooler=SupplyOut()
        cooler.COP=self.efficiency*((self.theta_m_prev+273.0)/(self.theta_e-self.theta_m_prev))
        if cooler.COP<=0: #TODO: This is a quick hackaround of the actual system!!! FIX!!!!
            cooler.COP=self.efficiency*100
        cooler.electricity=self.Load/cooler.COP
        return cooler


class SupplyOut:
    #The System class which is used to output the final results
    energyIn = None
    electricityOut = None




#if __name__ == "__main__":
#    print "Resistive Office Heater"
#    director = Director()
#    director.setBuilder(HeatPumpHeater(Load=100, theta_e=10,theta_m_prev=20,efficiency=0.8))
#    system = director.calcSystem()
#
#
#    print system.electricity
#    print system.COP


