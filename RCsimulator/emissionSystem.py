"""
=========================================
Emission System Parameters for Heating and Cooling

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
__status__ = "Production"



"""
Model of different Emission systems. New Emission Systems can be introduced by adding new classes

TODO: 
- find a way to accurately calculate the supply temperatures. For now we set constants for each system
"""

class EmissionDirector:

    """
    The director sets what Emission system is being used, and runs that set Emission system
    """

#    __builder = None
    builder = None

    #Sets what Emission system is used
    def setBuilder(self, builder):
#        self.__builder = builder
        self.builder = builder
    # Calcs the energy load of that system. This is the main() fu
    def calcFlows(self):

        # Director asks the builder to produce the system body. self.__builder is an instance of the class

#        body = self.__builder.heatFlows()
        body = self.builder.heatFlows()


        return body





class EmissionBuilder:

    """ The base class in which systems are built from
    """

    def __init__(self, building, energy_demand):

      self.energy_demand = energy_demand

      self.phi_ia=building.phi_ia
      self.phi_st=building.phi_st
      self.phi_m = building.phi_m

    def heatFlows(self): pass




class OldRadiators(EmissionBuilder):
    #Old building with radiators and high supply temperature

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = self.phi_ia+self.energy_demand
        flows.phi_st = self.phi_st
        flows.phi_m = self.phi_m

        flows.heatingSupplyTemperature=50
        flows.coolingSupplyTemperature=12

        # flows.heatingSupplyTemperature = self.T_set_heating - 37.0/30 * (self.T_out-self.T_set_heating)
        # flows.coolingSupplyTemperature = self.T_set_cooling - 37.0/30 * (self.T_out-self.T_set_cooling)

        return flows

class NewRadiators(EmissionBuilder):
    #Newer building with radiators and medium supply temperature

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = self.phi_ia+self.energy_demand
        flows.phi_st = self.phi_st
        flows.phi_m = self.phi_m
        
        flows.heatingSupplyTemperature=50
        flows.coolingSupplyTemperature=12


        # flows.heatingSupplyTemperature = self.T_set_heating - 24.0/30 * (self.T_out-self.T_set_heating)
        # flows.coolingSupplyTemperature = self.T_set_cooling - 24.0/30 * (self.T_out-self.T_set_cooling)

        return flows
    

class ChilledBeams(EmissionBuilder):
    #Chilled beams: identical to newRadiators but used for cooling 

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = self.phi_ia+self.energy_demand
        flows.phi_st = self.phi_st
        flows.phi_m = self.phi_m

        flows.heatingSupplyTemperature=50
        flows.coolingSupplyTemperature=12

        # flows.heatingSupplyTemperature = self.T_set_heating - 24.0/30 * (self.T_out-self.T_set_heating)
        # flows.coolingSupplyTemperature = self.T_set_cooling - 24.0/30 * (self.T_out-self.T_set_cooling)
        return flows


class AirConditioning(EmissionBuilder):
    #All heat is given to the air via an AC-unit. HC input via the air node as in the ISO standard.
    #supplyTemperature as with new radiators (assumption)

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = self.phi_ia+self.energy_demand
        flows.phi_st = self.phi_st
        flows.phi_m = self.phi_m

        flows.heatingSupplyTemperature=50
        flows.coolingSupplyTemperature=12
        # flows.heatingSupplyTemperature = self.T_set_heating-24.0/30* (self.T_out-self.T_set_heating)
        # flows.coolingSupplyTemperature = self.T_set_cooling-24.0/30* (self.T_out-self.T_set_cooling)
        

        return flows


class FloorHeating(EmissionBuilder):
    #All HC energy goes into the surface node, supplyTemperature low

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = self.phi_ia
        flows.phi_st = self.phi_st+self.energy_demand
        flows.phi_m = self.phi_m

        flows.heatingSupplyTemperature=50
        flows.coolingSupplyTemperature=12

        # flows.heatingSupplyTemperature = self.T_set_heating - 18.0/30 * (self.T_out-self.T_set_heating)
        # flows.coolingSupplyTemperature = self.T_set_cooling - 18.0/30 * (self.T_out-self.T_set_cooling)

        return flows


class TABS(EmissionBuilder):
    #Thermally activated Building systems. HC energy input into bulk node. Supply Temperature low.

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia = self.phi_ia
        flows.phi_st = self.phi_st
        flows.phi_m = self.phi_m+self.energy_demand

        flows.heatingSupplyTemperature=50
        flows.coolingSupplyTemperature=12

        # flows.heatingSupplyTemperature = self.T_set_heating - 18.0/30 * (self.T_out-self.T_set_heating)
        # flows.coolingSupplyTemperature = self.T_set_cooling - 18.0/30 * (self.T_out-self.T_set_cooling)
        return flows


class EmissionOut:
    #The System class which is used to output the final results

    phi_ia= None
    phi_m= None
    phi_st= None

    heatingSupplyTemperature = None
    coolingSupplyTemperature = None



