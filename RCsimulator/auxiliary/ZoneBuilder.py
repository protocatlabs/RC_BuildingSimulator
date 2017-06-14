"""
=========================================
A more flexible zone definition for the Building object in buildingPhysics.py. Objectives are to make the Building
object suitable for:
    non-rectangular floor plans
    rooms bounded by roofs in terms of transmission area and the resulting room volumes
    different windows bounding the same zone
    different wall constructions along the same zone
    bounding surfaces (wall and ground slab) below grade

=========================================
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

class element(object):
    def __init__(self,
                 name = 'wall', #Wall, Window, Ground slab, Roof
                 area = 15, #element area, m2
                 U = 1.0, #element U-value, W/m2
                 subgrade = False #element above or below ground level
                 ):

        self.name = name
        self.area = area
        self.U = U
        self.subgrade = subgrade
        self.h_tr = self.U * self.area


class zone(object):
    def __init__(self,
                 elements = [],
                 floor_area = 35,
                 Room_Vol = 105,
                 total_internal_area = 142
                ):

        self.h_tr_em = 0
        self.h_tr_w = 0

        self.elements = elements
        if self.elements == []:
            self.addElements(element(area=11,U=0.2))
            self.addElements(element(name='window',area=4,U=1.1))
        else:
            for each_element in elements:
                self.addElements(each_element)

        self.floor_area = floor_area
        self.Room_Vol = Room_Vol
        self.total_internal_area =total_internal_area

    def addElements(self,e):
        # self.elements.append(e)
        if e.name == 'window':
            self.h_tr_w += e.h_tr
        if e.name in ['wall','roof','groundslab']:
            self.h_tr_em += e.h_tr



if __name__ == '__main__':
    test = zone(elements=[element(U=0.3,area=0.3)])
    print test.h_tr_w
    print test.h_tr_em
