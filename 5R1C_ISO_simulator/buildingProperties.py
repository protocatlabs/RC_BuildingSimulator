
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
	'''Sets the parameters of the building. '''

	def __init__(self, 
		Fenst_A=13.5 ,
		Room_Depth=7 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		LightLoad=0.0117 ,
		LightingControl = 300,
		h_tr_em = 47 , 
		h_tr_w = 13,
		h_ve_adj = 45,
		c_m = 2.07,
		h_tr_ms = 45,
		h_tr_is = 15,
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
		self.c_m=c_m #[kWh/K] Room Capacitance. Default based of Madsen2011, consider changing to ISO standard
		self.h_tr_em = h_tr_em #Conductance of opaque surfaces to exterior
		self.h_tr_w = 	h_tr_w  #Conductance to exterior through glazed surfaces
		self.h_ve_adj =	h_ve_adj  #Conductance through ventilation
		self.c_m = c_m 			#Thermal Capacitance
		self.h_tr_ms = 	h_tr_ms #Opaque transimitance #TODO: Check what this really means
		self.h_tr_is = 	h_tr_is # Conductance from the conditioned air to interior building surface

		






