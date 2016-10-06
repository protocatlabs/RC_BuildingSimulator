"""
=========================================
Main file to calculate the building loads
EN-13970
=========================================
"""

import numpy as np
from buildingProperties import Building #Importing Building Class

__author__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"



"""
The equations presented here is this code are derived from ISO 13790 Annex C 



VARIABLE DEFINITION

theta_m_t: Medium temperature of the enxt time step 
theta_m_prev: Medium temperature from the previous time step
c_m: Thermal Capacitance of the medium 
h_tr_3: combined heat conductance, see function for definition
h_tr_em: Heat conductance from the outside through opaque elements TODO: Check this
phi_m_tot: see formula for the calculation, eq C.5 in standard

phi_m: Combination of internal and solar gains directly to the medium 
theta_e: External air temperature
phi_st: combination of internal and solar gains directly to the internal surface
h_tr_w: Heat transfer from the outside through windows, doors
h_tr_1: combined heat conductance, see function for definition
phi_ia: combination of internal and solar gains to the air 
phi_hc_nd: Heating and Cooling of the supply air
h_ve_adj: Ventilation heat transmission coefficient 
h_tr_2: combined heat conductance, see function for definition 

h_tr_is: Some heat transfer coefficient between the air and the inside surface TODO: Check this

H_tr_ms: Heat transfer coefficient between the internal surface temperature and the medium

theta_m: Some wierd average between the previous and current timestep of the medium TODO: Check this

"""

#Set Building Parameters
Office=Building()

