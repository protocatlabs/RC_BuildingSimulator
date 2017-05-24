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


# this should be at the top, replace the first docstring with this one.
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

    # Sets what Emission system is used
    def setBuilder(self, builder):
        #        self.__builder = builder
        self.builder = builder
    # Calcs the energy load of that system. This is the main() fu

    def calcFlows(self):

        # Director asks the builder to produce the system body. self.__builder
        # is an instance of the class

        #        body = self.__builder.heatFlows()
        body = self.builder.heatFlows()

        return body

# why not call it EmissionSystemBuilder?
# also, why builder? it isn't a builder at all! instead, how about EmissionSystemBase? Or just EmissionSystem
class EmissionBuilder:

    """ The base class in which systems are built from
    """

    def __init__(self, energy_demand):

        self.energy_demand = energy_demand

    # at the very least add a docstring here (don't need to repeat at every implementation)
    # also, it looks like it returns a (constant?) `EmissionOut` object. Why is EmissionOut not called flows?
    # name is not pep8, should be heat_flows. or heat_emission_out.
    # also, could this be set in the constructor? idk yet - haven't read more of the code...
    def heatFlows(self): pass

# use docstrings instead of comments for stuff that could become API documentation!
class OldRadiators(EmissionBuilder):
    # Old building with radiators and high supply temperature
    # Heat is emitted to the air node

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

# use docstrings instead of comments for stuff that could become API documentation!
class NewRadiators(EmissionBuilder):
    # Newer building with radiators and medium supply temperature
    # Heat is emitted to the air node

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

# use docstrings instead of comments for stuff that could become API documentation!
class ChilledBeams(EmissionBuilder):
    # Chilled beams: identical to newRadiators but used for cooling
    # Heat is emitted to the air node

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

# use docstrings instead of comments for stuff that could become API documentation!
# which ISO standard? there are (literally) thousands!
class AirConditioning(EmissionBuilder):
    # All heat is given to the air via an AC-unit. HC input via the air node as in the ISO standard.
    # supplyTemperature as with new radiators (assumption)
    # Heat is emitted to the air node

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

# use docstrings instead of comments for stuff that could become API documentation!
class FloorHeating(EmissionBuilder):
    # All HC energy goes into the surface node, supplyTemperature low
    # Heat is emitted to the surface node

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

# use docstrings instead of comments for stuff that could become API documentation!
class TABS(EmissionBuilder):
    # Thermally activated Building systems. HC energy input into bulk node. Supply Temperature low.
    # Heat is emitted to the thermal mass node

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

# use docstrings instead of comments for stuff that could become API documentation!
# what is a "System" class?? oh. i get it. hm. naming is hard!
class EmissionOut:
    # The System class which is used to output the final results

    # since you're using numpy, why not make these NaN? and then when you assign them in the subclasses of EmissionBuilder,
    # assign doubles - that way you won't be mixing types.
    phi_ia_plus = None
    phi_m_plus = None
    phi_st_plus = None

    heatingSupplyTemperature = None
    coolingSupplyTemperature = None
    # return temperatures?
