"""
=========================================
Supply System Parameters for Heating and Cooling

=========================================
"""

import numpy as np
#from emissionSystem import *


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
"""

class SupplyDirector:
    
    """
    The director sets what Supply system is being used, and runs that set Supply system
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


class SupplyBuilder:

    """ The base class in which Supply systems are built from 
    """

    def __init__(self, Load, T_out, heatingSupplyTemperature, coolingSupplyTemperature, has_heating_demand, has_cooling_demand):
        self.Load=Load                              #Energy Demand of the building at that time step
        self.T_out=T_out                        #Outdoor Air Temperature
        self.heatingSupplyTemperature = heatingSupplyTemperature  #Temperature required by the emission system
        self.coolingSupplyTemperature = coolingSupplyTemperature
        self.has_heating_demand = has_heating_demand
        self.has_cooling_demand=has_cooling_demand
        
    name = None

    def calcLoads(self): pass



class OilBoilerOld(SupplyBuilder):
    #Old oil boiler with fuel efficiency of 63 percent (medium of range in report of semester project M. Fehr)
    #No condensation, pilot light

    def calcLoads(self):
        system = SupplyOut()
        system.fossilsIn = self.Load/0.63
        system.electricityIn = 0
        system.electricityOut = 0
        return system
    
    name = 'Old Oil Boiler'

class OilBoilerMed(SupplyBuilder):
    #Classic oil boiler with fuel efficiency of 82 percent (medium of range in report of semester project M. Fehr)
    #No condensation, but better nozzles etc.
    
    def calcLoads(self):
        system = SupplyOut()
        system.fossilsIn = self.Load/0.82
        system.electricityIn = 0
        system.electricityOut = 0
        return system

    name = 'Standard Oil Boiler'


class OilBoilerNew(SupplyBuilder):
    #New oil boiler with fuel efficiency of 98 percent (value from report of semester project M. Fehr)
    #Condensation boiler, latest generation

    def calcLoads(self):
        system = SupplyOut()
        system.fossilsIn = self.Load/0.98
        system.electricityIn = 0
        system.electricityOut = 0
        return system
    
    name = 'Top-Notch Oil Boiler'

class HeatPumpAir(SupplyBuilder):
    """
    BETA Version
    Air-Water heat pump. Outside Temperature as reservoir temperature.
    COP based off regression anlysis of manufacturers data
    Source: "A review of domestic heat pumps, Iain Staffell, Dan Brett, Nigel Brandonc and Adam Hawkes"
    http://pubs.rsc.org/en/content/articlepdf/2012/ee/c2ee22653g
    """
    #TODO: Validate this methodology 

    def calcLoads(self):
        system = SupplyOut()

        if self.has_heating_demand:
            #determine the temperature difference, if negative, set to 0
            deltaT=max(0,self.heatingSupplyTemperature-self.T_out)
            system.COP=6.81 - 0.121*deltaT + 0.000630*deltaT**2 #Eq (4) in Staggell et al.
            system.electricityIn=self.Load/system.COP

        elif self.has_cooling_demand:
            #determine the temperature difference, if negative, set to 0
            deltaT=max(0,self.T_out-self.coolingSupplyTemperature)
            system.COP=6.81 - 0.121*deltaT + 0.000630*deltaT**2 #Eq (4) in Staggell et al.
            system.electricityIn = self.Load/system.COP

        else:
            raise ValueError('HeatPumpAir called although there is no heating/cooling demand')

        system.fossilsIn = 0    
        system.electricityOut = 0
        return system

    name = 'Air Source Heat Pump'

class HeatPumpWater(SupplyBuilder):
    """"
    BETA Version
    Reservoir temperatures 7 degC (winter) and 12 degC (summer).
    Air-Water heat pump. Outside Temperature as reservoir temperature.
    COP based off regression anlysis of manufacturers data
    Source: "A review of domestic heat pumps, Iain Staffell, Dan Brett, Nigel Brandonc and Adam Hawkes"
    http://pubs.rsc.org/en/content/articlepdf/2012/ee/c2ee22653g
    """
    #TODO: Validate this methodology 

    def calcLoads(self):
        system = SupplyOut()
        if self.has_heating_demand:   
            deltaT=max(0,self.heatingSupplyTemperature-7.0)
            system.COP=8.77 - 0.150*deltaT + 0.000734*deltaT**2 #Eq (4) in Staggell et al.
            system.electricityIn = self.Load/system.COP

        elif self.has_cooling_demand:
            deltaT=max(0,12.0-self.coolingSupplyTemperature)
            system.COP=8.77 - 0.150*deltaT + 0.000734*deltaT**2 #Eq (4) in Staggell et al.
            system.electricityIn = self.Load/system.COP


        system.fossilsIn = 0
        system.electricityOut = 0
        return system

    name = 'Ground Water Source Heat Pump'

# class HeatPumpGround(SupplyBuilder):
#     #Ground-Water heat pump. epsilon_carnot = 0.45. Reservoir temperatures 7 degC (winter) and 12 degC (summer). (Same as HeatPumpWater except for lower e_Carnot)

#     def calcLoads(self):
#         heater = SupplyOut()
#         if self.has_heating_demand:                                   #Heating
#             heater.electricityIn = self.Load/(0.45*(self.heatingSupplyTemperature+273.0)/(self.heatingSupplyTemperature-7.0))
#         else:                                              #Cooling 
#             if self.coolingSupplyTemperature > 11.9:                 #Only by pumping 
#                 heater.electricityIn = self.Load*0.1
#             else:                                           #Heat Pump active
#                 heater.electricityIn = self.Load/(0.45*(self.coolingSupplyTemperature+273.0)/(12.0-self.coolingSupplyTemperature))
#         heater.electricityOut = 0
#         heater.fossilsIn = 0
#         return heater

#     name = 'Ground Source Heat Pump'

class ElectricHeating(SupplyBuilder):
    #Straight forward electric heating. 100 percent conversion to heat.
    
    def calcLoads(self):
        system=SupplyOut()
        system.electricityIn = self.Load
        system.fossilsIn = 0
        system.electricityOut = 0
        return system
    
    name = 'Electric Heating'

class CHP(SupplyBuilder):
    #Combined heat and power unit with 60 percent thermal and 33 percent electrical fuel conversion. 93 percent overall
    
    def calcLoads(self):
        system=SupplyOut()
        system.fossilsIn = self.Load/0.6
        system.electricityIn = 0
        system.electricityOut = system.fossilsIn*0.33
        return system

    name = 'Combined Heat and Power'

class DirectHeater(SupplyBuilder):
    #Created by PJ to check accuracy against previous simulation
    
    def calcLoads(self):
        system=SupplyOut()
        system.electricityIn = self.Load
        system.fossilsIn = 0
        system.electricityOut = 0
        return system

    name = 'Direct Heater'

class DirectCooler(SupplyBuilder):
    #Created by PJ to check accuracy against previous simulation
    
    def calcLoads(self):
        system=SupplyOut()
        system.electricityIn = self.Load
        system.fossilsIn = 0
        system.electricityOut = 0
        return system

    name = 'Direct Cooler'

class SupplyOut:
    #The System class which is used to output the final results
    fossilsIn = None
    electricityIn = None
    electricityOut = None
    COP = None

