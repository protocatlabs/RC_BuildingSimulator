from buildingSystem import *

if __name__ == "__main__":

	Heating=HeatPumpHeater

	print "Resistive Office Heater"
	director = Director()
	director.setBuilder(Heating(heatingLoad=100, theta_e=10,theta_m_prev=20,efficiency=0.8))
	system = director.calcSystem()


	print system.electricity
	print system.COP
