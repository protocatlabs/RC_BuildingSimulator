"""
=========================================
Physics Required to calculate the electricty required to achieve a set heating/cooling load
EN-13970
=========================================
"""

import numpy as np


__author__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = [""]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"



"""
This is an attempt at modeling the building system using the builder patters
"""

class Director:
	

	__builder = None

	def setBuilder(self, builder):
		self.__builder = builder

	# The algorithm for assembling a heating system
	def calcSystem(self):

		# Director asks the builder to produce the system body. self.__builder is an instance of the class
		
		body = self.__builder.calcLoads()

		return body 


class Builder:

	""" Creates various parts of a vehicle.
	This class is responsible for constructing all
	the parts for a vehicle.
	"""

	def __init__(self, Load, theta_e, theta_m_prev, efficiency):
		self.Load=Load
		self.theta_e=theta_e
		self.theta_m_prev=theta_m_prev
		self.efficiency=efficiency

	def calcLoads(self): pass
	def calcCoolingLoads(self): pass


class ResistiveHeater(Builder):

	""" Concrete Builder implementation.
	This class builds parts for Jeep's SUVs.
	"""

	def calcLoads(self):
		heater = Heater()
		heater.electricity = self.Load
		return heater

class HeatPumpHeater(Builder):

	def calcLoads(self):
		heater= System()
		heater.COP=self.efficiency*((self.theta_m_prev+273.0)/(self.theta_m_prev-self.theta_e))
		heater.electricity=self.Load/heater.COP
		return heater

class HeatPumpCooler(Builder):
	
	def calcLoads(self):
		cooler=System()
		cooler.COP=self.efficiency*((self.theta_m_prev+273.0)/(self.theta_e-self.theta_m_prev))
		cooler.electricity


class System:
	electricity = None
	COP=None




if __name__ == "__main__":
	print "Resistive Office Heater"
	director = Director()
	director.setBuilder(HeatPumpHeater(Load=100, theta_e=10,theta_m_prev=20,efficiency=0.8))
	system = director.calcSystem()


	print system.electricity
	print system.COP


