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
                 subgrade = False #Element above or below ground level. todo: modify building_physics accordingly
                 ):

        self.name = name
        self.area = area
        self.u_value = u_value
        self.subgrade = subgrade
        self.h_tr = self.u_value * self.area #element conductance [W/K]


class Zone(object):
    def __init__(self,
                 elements = [],
                 floor_area = 34.3,
                 room_vol = 106.33,
                 total_internal_area = 142.380
                ):

        self.h_tr_em = 0
        self.h_tr_w = 0
        self.floor_area = floor_area
        self.room_vol = room_vol
        self.total_internal_area = total_internal_area
        self.elements = elements
        self.elements_added = 0 #counter to check that the zone contains exactly the specified elements.
        self.element_names = []

        #if left blank, zone elements will be set to ASF default values
        if self.elements == []:
            Window = Element(name='ASF_window', area=13.5, u_value=1.1)
            Wall = Element(name='ASF_wall', area=1.69, u_value=0.2)
            self.add_elements(Window)
            self.add_elements(Wall)

        for each_element in elements:
            self.add_elements(each_element)

        #report the number of elements added to facilitate bug detection
        if self.elements != []:
            print 'Zone with %i/%i elements specified'%(self.elements_added,len(self.elements))
        else:
            print 'Zone with default (ASF) elements: %s'%str(self.element_names)


    def add_elements(self,e):
        self.element_names.append(e.name)
        #raise error for invalid names
        if not any(x in str.lower(e.name) for x in ['window','wall','groundslab','ground slab','roof']):
            raise NameError('element ', e.name, ' is not a valid input. Please choose one from "'"wall"'","'"window"'","'"groundslab"'","'"roof"'"')
        # add window conductance to window conductances
        if any(x in str.lower(e.name) for x in ['window']):
            self.h_tr_w += e.h_tr
            self.elements_added += 1
        # add surface conductances to conductance of mass
        if any(x in str.lower(e.name) for x in ['wall','roof','groundslab','ground slab']):
            self.h_tr_em += e.h_tr
            self.elements_added += 1


if __name__ == '__main__':
    test = Zone()
    print test.h_tr_w
    print test.h_tr_em
