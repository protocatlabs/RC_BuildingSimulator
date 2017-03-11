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
Model of different EMISSION systems. New EMISSION Systems can be introduced by adding new classes
"""

class emissionDirector:

    """
    The director sets what EMISSION system is being used, and runs that set EMISSION system
    """

    __builder = None

    #Sets what EMISSION system is used
    def setBuilder(self, builder):
        self.__builder = builder

    # Calcs the energy load of that system. This is the main() fu
    def calcSystem(self):

        # Director asks the builder to produce the system body. self.__builder is an instance of the class

        body = self.__builder.calcLoads()

        return body





class emissionBuilder:

    """ The base class in which systems are built from
    """

    def __init__(self, theta_e, phi_int, phi_sol):
      self.theta_e = theta_e   #Outdoor Air Temperature
      self.phi_int = phi_int
      self.phi_sol = phi_sol

    def heatFlows(self): pass





class OldRadiators(emissionBuilder):
    #The direct heater outputs the raw energy demand. No modifications are made

    def heatFlows(self):
        flows = System()
        flows.phi_ia = 0.5*(self.phi_int+self.phi_hc_nd_ac)
        flows.phi_st = (1-(self.A_m/self.A_t)-(self.h_tr_w/(9.1*self.A_t)))*(0.5*(self.phi_int+self.phi_hc_nd_ac)+self.phi_sol)
        flows.phi_m = (self.A_m/self.A_t)*(0.5*(self.phi_int+self.phi_hc_nd_ac)+self.phi_sol)
        flows.supplyTemperature = 44.67 - 1.23*self.theta_e
        return flows


class NewRadiators(emissionBuilder):
    #The direct cooler outputs the raw energy demand. No modificactons are made

    def calcLoads(self):
        heater = System()
        heater.electricity = self.Load
        return heater

class ChilledBeams(emissionBuilder):
    #The resistive heater converts electricty to heat with a set efficiency

    def calcLoads(self):
        heater = System()
        heater.electricity = self.Load * self.efficiency
        return heater


class AirConditioning(emissionBuilder):
    #The heat pump calculates a COP with an efficiency and outputs the electricty input requirement

    def calcLoads(self):
        heater= System()
        heater.COP=self.efficiency*((self.theta_m_prev+273.0)/(self.theta_m_prev-self.theta_e))
        if heater.COP<=0:
            heater.COP=self.efficiency*100 #TODO: This is a quick hackaround of the actual system!!! FIX!!!!
        heater.electricity=self.Load/heater.COP
        return heater

class FloorHeating(emissionBuilder):
    #The heat pump calculates a COP with an efficiency and outputs the electricty input requirement

    def calcLoads(self):
        cooler=System()
        cooler.COP=self.efficiency*((self.theta_m_prev+273.0)/(self.theta_e-self.theta_m_prev))
        if cooler.COP<=0: #TODO: This is a quick hackaround of the actual system!!! FIX!!!!
            cooler.COP=self.efficiency*100
        cooler.electricity=self.Load/cooler.COP
        return cooler

class TABS(emissionBuilder):
    #The heat pump calculates a COP with an efficiency and outputs the electricty input requirement

    def calcLoads(self):
        cooler=System()
        cooler.COP=self.efficiency*((self.theta_m_prev+273.0)/(self.theta_e-self.theta_m_prev))
        if cooler.COP<=0: #TODO: This is a quick hackaround of the actual system!!! FIX!!!!
            cooler.COP=self.efficiency*100
        cooler.electricity=self.Load/cooler.COP
        return cooler


class System:
    #The System class which is used to output the final results

    phi_ia= None

    phi_m= None

    phi_st= None

    supplyTemperature = None



#if __name__ == "__main__":
#    print "Resistive Office Heater"
#    director = Director()
#    director.setBuilder(HeatPumpHeater(Load=100, theta_e=10,theta_m_prev=20,efficiency=0.8))
#    system = director.calcSystem()
#
#
#    print system.electricity
#    print system.COP


