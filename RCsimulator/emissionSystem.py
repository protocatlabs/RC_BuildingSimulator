"""
=========================================
Emission System Parameters for Heating and Cooling

=========================================
"""

import numpy as np


__author__ = "Prageeth Jayathissa, Michael Fehr"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["CEA Toolbox"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Development"



"""
Model of different Emission systems. New Emission Systems can be introduced by adding new classes

Note that this is currently in a very basic form, and has been created to allow for more complex expansion 

Supply temperatures are taken from the CEA Toolbox 
https://github.com/architecture-building-systems/CEAforArcGIS/blob/master/cea/databases/CH/Systems/emission_systems.xls

TODO: Validation is still required
TODO: Need to double check supply temperatures, waiting on reply from the CEA team

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

    def __init__(self, energy_demand):

      self.energy_demand = energy_demand

    def heatFlows(self): pass




class OldRadiators(EmissionBuilder):
    #Old building with radiators and high supply temperature
    #Heat is emitted to the air node

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia_plus = self.energy_demand
        flows.phi_st_plus = 0 
        flows.phi_m_plus = 0 

        flows.heatingSupplyTemperature = 65
        flows.heatingReturnTemperature = 45
        flows.coolingSupplyTemperature = 12
        flows.coolingReturnTemperature = 21


        return flows

class NewRadiators(EmissionBuilder):
    #Newer building with radiators and medium supply temperature
    #Heat is emitted to the air node

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia_plus = self.energy_demand
        flows.phi_st_plus = 0 
        flows.phi_m_plus = 0 
        
        flows.heatingSupplyTemperature = 50
        flows.heatingReturnTemperature = 35
        flows.coolingSupplyTemperature = 12
        flows.coolingReturnTemperature = 21


        return flows
    

class ChilledBeams(EmissionBuilder):
    #Chilled beams: identical to newRadiators but used for cooling
    #Heat is emitted to the air node 

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia_plus = self.energy_demand
        flows.phi_st_plus = 0 
        flows.phi_m_plus = 0 

        flows.heatingSupplyTemperature = 50
        flows.heatingReturnTemperature = 35
        flows.coolingSupplyTemperature = 18
        flows.coolingReturnTemperature = 21

        return flows


class AirConditioning(EmissionBuilder):
    #All heat is given to the air via an AC-unit. HC input via the air node as in the ISO standard.
    #supplyTemperature as with new radiators (assumption)
    #Heat is emitted to the air node

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia_plus = self.energy_demand
        flows.phi_st_plus = 0 
        flows.phi_m_plus = 0 

        flows.heatingSupplyTemperature = 40
        flows.heatingReturnTemperature = 20
        flows.coolingSupplyTemperature = 6
        flows.coolingReturnTemperature = 15
        

        return flows


class FloorHeating(EmissionBuilder):
    #All HC energy goes into the surface node, supplyTemperature low
    #Heat is emitted to the surface node

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia_plus = 0 
        flows.phi_st_plus = self.energy_demand
        flows.phi_m_plus = 0 

        flows.heatingSupplyTemperature = 40
        flows.heatingReturnTemperature = 5
        flows.coolingSupplyTemperature = 12
        flows.coolingReturnTemperature = 21


        return flows


class TABS(EmissionBuilder):
    #Thermally activated Building systems. HC energy input into bulk node. Supply Temperature low.
    #Heat is emitted to the thermal mass node

    def heatFlows(self):
        flows = EmissionOut()
        flows.phi_ia_plus = 0 
        flows.phi_st_plus = 0 
        flows.phi_m_plus = self.energy_demand

        flows.heatingSupplyTemperature = 50
        flows.heatingReturnTemperature = 35
        flows.coolingSupplyTemperature = 12
        flows.coolingReturnTemperature = 21

        return flows


class EmissionOut:
    #The System class which is used to output the final results

    phi_ia_plus= None
    phi_m_plus= None
    phi_st_plus= None

    heatingSupplyTemperature = None
    coolingSupplyTemperature = None



