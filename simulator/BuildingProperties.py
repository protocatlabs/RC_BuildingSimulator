

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
		Ri=42,
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
		self.Cm=Cm #[kWh/K] Room Capacitance based of Madsen2011
		self.Ri=Ri #[K/kWh] Resistance to outside air. Based off glass having a Uvalue of 1.978W/m2K, 12m2 facade glass

HPZ=Building()

print HPZ.Fenst_A