

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
T_out,glbRad, glbIll= f.read_EWP(epw_name='data/Zurich-Kloten_2013.epw') #C, W, lx
Q_fenstRad=f.read_transmittedR(myfilename='data/radiation_Building_Zh.csv') #kWh/h
occupancy, Q_human=f.read_occupancy(myfilename='data/Occupancy_COM.csv') #people/m2/h, kWh/h
Ill_Eq= f.Equate_Ill(epw_name='data/Zurich-Kloten_2013.epw') #Equation coefficients for linear polynomial


#Set Office Building Parameters. See BuildingProperties.py
Office=Building(Cm=2.07, R_wi=42, Infl=0.5)


#Calculate Illuminance in the room. 
fenstIll=Q_fenstRad*1000*Ill_Eq[0] #Lumens.  Note that the constant has been ignored because it should be 0
TransIll=fenstIll*Office.glass_light_transmitance
Lux=TransIll/Office.Floor_A

#Other Set Points
occupancy['tintH_set']=20
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
T_in=20 #Starting internal temperature
Data_T_in=[] 
Data_Heating=np.empty([8760])
Data_Cooling=np.empty([8760])
Data_Lighting=np.empty([8760])

#PID setup
heatingControl=PID_controller.PID(P=0.5, I=1.0, D=0.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500)
coolingControl=PID_controller.PID(P=0.5, I=1.0, D=0.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500)

#Differential Equation Parameters
dt=0.25 #hours

for ii in range(0, int(8760)):
	#Initialise hourly energy requirements
	Heat_hr=0
	Cool_hr=0
	Lighting_hr=0
	Office.setVentilation(occupancy['People'][ii])


	for jj in range(0,int(1/dt)):

			

		dT_in=((Q.iat[ii,0]+Q_heat+Q_cool)/(Office.Cm) + (1/(Office.Cm*Office.R_i))*(float(T_out[ii])-T_in))*dt
		T_in=T_in+dT_in
		if occupancy['tintH_set'].iat[ii]>=0 and occupancy['tintH_set'].iat[ii]>T_in:
			heatingControl.setPoint(occupancy['tintH_set'].iat[ii])

			Q_heat= heatingControl.update(T_in)/10
		else:
			Q_heat=0
		Heat_hr+=Q_heat


		if T_in>tintC_set:
			coolingControl.setPoint(tintC_set)
			Q_cool = coolingControl.update(T_in)/2
		else:
			Q_cool=0
		Cool_hr+=Q_cool

	Heat_hr=Heat_hr*dt
	Cool_hr=Cool_hr*dt

	Total_Heating+=Heat_hr
	Total_Cooling+=Cool_hr
	#Lighting calc. Double check this as I wrote it rushed. Try find allternative for .iat

	if Lux.get_value(ii,0)< Office.LightingControl and occupancy['People'].iat[ii]>0:
		Lighting_hr=Office.LightLoad*Office.Floor_A
		Total_Lighting+=Lighting_hr



	Data_T_in.append(T_in)
	Data_Heating[ii]=Heat_hr
	Data_Cooling[ii]=abs(Cool_hr)
	Data_Lighting[ii]=Lighting_hr

print 'Total Heating Load is:', Total_Heating, 'kWh'
print 'Total Cooling Load is:', Total_Cooling*-1, 'kWh'
print 'Total Lighting Load is:', Total_Lighting, 'kWh'
#Heating is good
#Cooling is about 1000kWh lower than Diva, but the same as design builder
#Lighting is 150kWh lower than design builder and DIVA
#		heating 	Cooling 	Lighting
#Diva 	1224		4337		427
#Db 	1386		2990		497


# plt.plot(range(0, int(8760)),Data_Cooling, range(0, int(8760)),Data_Heating)
# plt.show()