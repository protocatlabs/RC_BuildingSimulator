

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

import numpy as np
import math
import input_data as f
import matplotlib.pyplot as plt
import PID_controller
from BuildingProperties import Building #Importing Building Class

#Import Data
To,glbRad, glbIll= f.read_EWP(epw_name='Zurich-Kloten_2013.epw') #C, W, lx
Q_fenstRad=f.read_transmittedR(my_filename='radiation_combination2.csv') #kWh/h I think. Check this
occupancy, Q_human=f.read_occupancy(myfilename='Occupancy_COM.csv') #people/m2/h, kWh/h
Ill_Eq= f.Equate_Ill(epw_name='Zurich-Kloten_2013.epw') #Equation coefficients for linear polynomial


#Set Office Building Parameters. See BuildingProperties.py
Office=Building(Cm=2.07, Ri=42)


#Calculate Illuminance in the room. 
fenstIll=Q_fenstRad*1000*Ill_Eq[0] #Lumens.  Note that the constant has been ignored because it should be 0
TransIll=fenstIll*Office.glass_light_transmitance
Lux=TransIll/Office.Floor_A

#Other Set Points
tintC_set=26 #Because data in occupancy is a bit wierd and will causes control issues FIX THIS


#Calculate external heat gains
Q_fenstRad=Q_fenstRad*Office.glass_solar_transmitance #Solar Gains
Q=Q_fenstRad.add(Q_human, axis=0) #only solar gains and human gains for now

#Initialise Conditions
Q_heat=0
Q_cool=0
Total_Heating=0
Total_Cooling=0
Total_Lighting=0
Ti=20 #Starting internal temperature
Data_Ti=[] 
Data_Heating=np.empty([0,8760])
print Data_Heating
Data_Cooling=[]
Data_Lighting=[]

#PID setup
heatingControl=PID_controller.PID(P=2.0, I=4.0, D=0.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500)
coolingControl=PID_controller.PID(P=2.0, I=4.0, D=0.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500)

#Differential Equation Parameters
dt=.25 #hours

for ii in range(0, int(8760)):
	#Initialise hourly energy requirements
	Heat_hr=0
	Cool_hr=0


	for jj in range(0,int(1/dt)):

			

		dTi=((Q.iat[ii,0]+Q_heat+Q_cool)/(Office.Cm) + (1/(Office.Cm*Office.Ri))*(float(To[ii])-Ti))*dt
		Ti=Ti+dTi
		if occupancy['tintH_set'].iat[ii]>=0 and occupancy['tintH_set'].iat[ii]>Ti:
			heatingControl.setPoint(occupancy['tintH_set'].iat[ii])

			Q_heat= heatingControl.update(Ti)/10
		else:
			Q_heat=0
		Heat_hr+=Q_heat


		if Ti>tintC_set:
			coolingControl.setPoint(tintC_set)
			Q_cool = coolingControl.update(Ti)/2
		else:
			Q_cool=0
		Cool_hr+=Q_cool


	Total_Heating+=Heat_hr
	Total_Cooling+=Cool_hr
	#Lighting calc. Double check this as I wrote it rushed. Try find allternative for .iat

	if Lux.get_value(ii,0)< Office.LightingControl and occupancy['People'].iat[ii]>0:
		Total_Lighting+=Office.LightLoad*Office.Floor_A



	Data_Ti.append(Ti)

print 'Total Heating Load is:', Total_Heating, 'kWh'
print 'Total Cooling Load is:', Total_Cooling*-1, 'kWh'
print 'Total Lighting Load is:', Total_Lighting, 'kWh'
#Heating and Lighting values look good. Cooling is about 2x high. Most likely because theres no natural ventilation


# plt.plot(range(0, int(8760)),To, range(0, int(8760)),Data_Ti)
# plt.show()