

"""
===========================
RC Model of a single zone building
===========================
File history and credits:
Prageeth Jayathissa
Mario Frei
Jeremias Schmidli
Amr Elesawy 
"""

class Building(object):
	'''Sets the parameters of the building. Default arguments are:
	Building(Fenst_A=13.5 , Room_Depth=7 , Room_Width=4.9 ,Room_Height=3.1 ,glass_solar_transmitance=0.687 ,
	glass_light_transmitance=0.744 ,LightLoad=0.0117 , LightingControl = 300,Cm=2.07, Ri=42) '''

	def __init__(self, 
		Fenst_A=13.5 ,
		Room_Depth=7 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		LightLoad=0.0117 ,
		LightingControl = 300,
		Cm=2.07,
		R_wi=42,
		Infl=0.5,
		minAirFlowPp=0.00944,
		averageOccupancy=0.1
		):

		#Building Dimensions
		self.Fenst_A=Fenst_A #[m2] Window Area
		self.Room_Depth=Room_Depth #[m] Room Depth
		self.Room_Width=Room_Width #[m] Room Width
		self.Room_Height=Room_Height #[m] Room Height

		#Fenstration and Lighting Properties
		self.glass_solar_transmitance=glass_solar_transmitance #Dbl LoE (e=0.2) Clr 3mm/13mm Air
		self.glass_light_transmitance=glass_light_transmitance #Dbl LoE (e=0.2) Clr 3mm/13mm Air
		self.LightLoad=LightLoad #[kW/m2] lighting load
		self.LightingControl = LightingControl #[lux] Lighting setpoint

		#Calculated Propoerties
		self.Floor_A=Room_Depth*Room_Width #[m2] Floor Area
		self.Room_Vol=Room_Width*Room_Depth*Room_Height #[m3] Room Volume

		#Single Capacitance Model Parameters
		self.Cm=Cm #[kWh/K] Room Capacitance. Default based of Madsen2011
		self.R_wi=R_wi #[K/kWh] Wall resistance to outside air. Default based off glass having a Uvalue of 1.978W/m2K, 12m2 facade glass

		#Infiltration and Ventilation
		#ToDO, take this away from __init__ and make a method that computes this based on the occupancy profile
		#Refer to line 398 - 476 in CEA functions.py for more informaiton
		self.Infl=Infl #Air Changes per hour
		self.R_infl=1.0/(Infl*self.Room_Vol*1.2*1/3600) #Resistance due to infiltration
		self.R_minVent=1.0/(minAirFlowPp*averageOccupancy*self.Floor_A*1.2*1)
		self.R_i=1.0/((1.0/self.R_wi) + (1.0/self.R_infl)+ (1.0/self.R_minVent))
		print 'Wall resistance including infiltration of', Infl, 'exchange per hour and ventelation of ', minAirFlowPp, 'm3/s/person: is :', self.R_i

		# print self.R_infl
		# print self.R_minVent
		# if self.R_infl<self.R_minVent:
		# 	self.R_i=1.0/((1.0/self.R_wi) + (1.0/self.R_infl))
		# 	print 'Infiltration of is greater than the min air flow requirements'
		# 	print 'Wall resistance including infiltration of', Infl, 'exchange per hour is:', self.R_i
		# else:
		# 	self.R_i=1.0/((1.0/self.R_wi) + (1.0/self.R_minVent))
		# 	print 'Min air flow is greater than infiltration, using min air flow to set envelope resistance'
		# 	print 'Wall resistance including minimum air flow of', minAirFlowPp, 'm3/s/person:', self.R_i




# HPZ=Building()

# print HPZ.Floor_A






