"""

A more flexible Zone definition for the Building object in buildingPhysics.py. Objectives are to make the Building
object suitable for:
    non-rectangular floor plans
    rooms bounded by roofs in terms of transmission area and the resulting room volumes
    different windows bounding the same Zone
    different wall constructions along the same Zone
    bounding surfaces (wall and ground slab) below grade


"""

import numpy as np

import rc_simulator.rc_simulator.supply_system as supply_system
import rc_simulator.rc_simulator.emission_system as emission_system


__authors__ = "Justin Zarb"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Prageeth Jayathissa"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Justin Zarb"
__email__ = "zarbj@arch.ethz.ch"
__status__ = "under development"

class Element(object):
    def __init__(self,
                 name = 'wall', #should contain one of the following: [Wall, Window, Ground slab, Roof]
                 area = 15.0, #Element area, [m2]
                 u_value = 1.0, #Element u_value-value, [W/m2.K]
                 subgrade = False, #Element above or below ground level. todo: modify building_physics accordingly
                 azimuth_tilt = 0, #South facing by default
                 altitude_tilt = 90, #vertical surfaces by default
                 solar_transmittance = 0.7,
                 light_transmittance=0.8,
                 shading_factor=1.0
                 ):

        self.name = name
        self.area = area
        self.u_value = u_value
        self.subgrade = subgrade
        self.h_tr = self.u_value * self.area #element conductance [W/K]
        self.azimuth_tilt = azimuth_tilt
        self.altitude_tilt = altitude_tilt
        self.shading_factor = shading_factor

        if any(x in str.lower(self.name) for x in ['window','glazing','glazed','fenster']):
            self.solar_transmittance = solar_transmittance
            self.light_transmittance = light_transmittance
        else:
            self.solar_transmittance = 0
            self.light_transmittance = 0


class Zone(object):
    def __init__(self,
                 name = 'Default Zone',
                 elements = None,
                 floor_area = 34.3,
                 room_vol = 106.33,
                 total_internal_area = 142.380,
                 thermal_capacitance_per_floor_area=165000,
                 ach_vent=1.5,
                 ach_infl=0.5,
                 ventilation_efficiency=0.6,
                 max_heating_energy_per_floor_area = np.inf,
                 heating_supply_system = supply_system.OilBoilerMed,
                 heating_emission_system = emission_system.OldRadiators
                ):

        self.name = name
        # Element objects
        self.elements = elements
        self.elements_added = 0  # for reporting purposes
        self.element_names = []  # for reporting purposes
        # calculated from Elements
        self.h_tr_em = 0
        self.h_tr_w = 0
        self.wall_area = 0
        self.window_area = 0
        self.window_wall_ratio = 0
        # direct inputs
        self.floor_area = floor_area
        self.room_vol = room_vol
        self.total_internal_area = 0
        self.ach_vent = ach_vent
        self.ach_infl = ach_infl
        self.ventilation_efficiency = ventilation_efficiency
        self.thermal_capacitance_per_floor_area=thermal_capacitance_per_floor_area

        self.max_heating_energy_per_floor_area = max_heating_energy_per_floor_area
        self.heating_supply_system = heating_supply_system,
        self.heating_emission_system = heating_emission_system

        #if left blank, zone elements will be set to ASF default values
        if self.elements == None:
            Window = Element(name='ASF_window', area=13.5, u_value=1.1)
            Wall = Element(name='ASF_wall', area=1.69, u_value=0.2)
            self.add_elements(Window)
            self.add_elements(Wall)
            self.total_internal_area = total_internal_area
        else:
            for element in self.elements:
                self.add_elements(element)
                self.total_internal_area += element.area
                #todo: is this ok? or should this parameter include internal floors and partitions?

        #report the number of elements added to facilitate bug detection
        if self.elements != None:
            print 'Zone with %s of %i elements specified'%(str(self.element_names),len(self.elements))

        print 'Conductance of opaque surfaces to exterior [W/K], h_tr_em:', self.h_tr_em
        print 'Conductance to exterior through glazed surfaces [W/K], h_tr_w', self.h_tr_w
        print 'window to wall ratio: %f %%\n' %(round(self.window_area/self.wall_area*100,1))


    def add_elements(self,e):
        self.element_names.append(e.name)
        #raise error for invalid names
        if not any(x in str.lower(e.name) for x in ['window','wall','groundslab','ground','teile','fenster','door','roof']):
            raise NameError('element ', e.name, ' is not a valid input. Please choose one from "'"wall"'","'"window"'","'"door"'",""'"groundslab"'","'"roof"'"')
        # add window conductance to window conductances
        if any(x in str.lower(e.name) for x in ['window','glazed','glazing','fenster']):
            self.h_tr_w += e.h_tr
            self.elements_added += 1
            self.window_area += e.area
        # add surface conductances to conductance of mass
        if any(x in str.lower(e.name) for x in ['wall','roof','groundslab','ground slab']):
            self.h_tr_em += e.h_tr
            self.elements_added += 1
            self.wall_area += e.area


if __name__ == '__main__':
    test_window = Element(name='window_S')
    print test_window.name, 'light transmittance: ', test_window.light_transmittance

    test_wall = Element(name='wall_E',azimuth_tilt=-90)
    print test_wall.name, 'light transmittance: ', test_wall.light_transmittance

    print 'testing zone:'
    test_zone = Zone()
    print 'window area: %f wall area: %s'%(test_zone.window_area, test_zone.wall_area)
    print 'h_tr_w: ',test_zone.h_tr_w
    print 'h_tr_em: ',test_zone.h_tr_em
