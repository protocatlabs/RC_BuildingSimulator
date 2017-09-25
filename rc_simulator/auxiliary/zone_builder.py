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

#testing

__authors__ = "Justin Zarb"
__copyright__ = "Copyright 2017, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Prageeth Jayathissa"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Justin Zarb"
__email__ = "zarbj@arch.ethz.ch"
__status__ = "under development"

class Element(object):
    """
    Element object representing an opaque or transparent element.

    ##OUTLOOK##
    Subgrade: currently a dummy attribute but this would indicate that the element is in contact with the ground
    rather than the outside air.

    absorptivity, reflectivity: Not yet implemented, but adding these parameters would make it possible to include
    solar gains calculations to opaque elements. The RC model would need to be adapted for this.

    Note to future developers: when adding attributes, make sure to upadate the copy method below with the same
    attributes!
    """
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

        if any(x in str.lower(self.name) for x in ['window','glazing','glazed','fenster','skylight','sky light']):
            self.solar_transmittance = solar_transmittance
            self.light_transmittance = light_transmittance
        else:
            self.solar_transmittance = 0
            self.light_transmittance = 0

    def copy(self):
        return Element(name = self.name,
                       area = self.area,
                       u_value = self.u_value,
                       subgrade = self.subgrade,
                       azimuth_tilt = self.azimuth_tilt,
                       altitude_tilt = self.altitude_tilt,
                       solar_transmittance = self.solar_transmittance,
                       light_transmittance= self.light_transmittance,
                       shading_factor= self.shading_factor)

class ThermalBridge(object):
    def __init__(self,
                 name,
                 length,
                 linear_conductance):
        self.name = name
        self.length = length
        self.linear_conductance = linear_conductance
        self.h_tr = length * linear_conductance

    def copy(self):
        return ThermalBridge(name = self.name,
                             length = self.length,
                             linear_conductance= self.linear_conductance)


class Zone(object):
    def __init__(self,
                 name = 'Default Zone', #for Calibrated Retrofit Analyisis, this should be of the form "Building#"
                 occupants = 1,
                 elements = None,
                 thermal_bridges = None,
                 floor_area = 34.3,
                 volume = 106.33,
                 thermal_capacitance_per_floor_area=165000,
                 ach_vent=1.5,
                 ach_infl=0.5,
                 ventilation_efficiency=1,
                 t_set_heating = 20,
                 t_set_cooling = 26,
                 max_heating_energy_per_floor_area = np.inf,
                 max_cooling_energy_per_floor_area = -np.inf,
                 heating_supply_system = supply_system.OilBoilerMed,
                 heating_emission_system = emission_system.OldRadiators,
                 cooling_supply_system = supply_system.HeatPumpAir,
                 cooling_emission_system = emission_system.AirConditioning
                ):

        self.name = name
        self.accepted_opaque_element_names = ['wall','groundslab','slab','floor','door','roof',
                                              'dach','wand','boden','ture','decke']
        self.accepted_glazing_names = ['window','glazed','glazing','fenster','skylight', 'sky light']
        # Element objects
        self.elements = elements
        self.elements_added = 0  # for reporting purposes
        self.element_names = []  # for reporting purposes
        # Thermal bridges
        self.thermal_bridges = thermal_bridges

        # direct inputs
        self.occupants = occupants
        self.floor_area = floor_area
        self.volume = volume
        self.total_internal_area = floor_area * 4.5 #ISO13790 7.2.2.2
        self.ach_vent = ach_vent
        self.ach_infl = ach_infl
        self.ventilation_efficiency = ventilation_efficiency
        self.thermal_capacitance_per_floor_area=thermal_capacitance_per_floor_area
        self.max_heating_energy_per_floor_area = max_heating_energy_per_floor_area
        self.max_cooling_energy_per_floor_area = max_cooling_energy_per_floor_area
        self.heating_supply_system = heating_supply_system
        self.heating_emission_system = heating_emission_system
        self.cooling_supply_system = cooling_supply_system
        self.cooling_emission_system = cooling_emission_system
        self.t_set_heating = t_set_heating
        self.t_set_cooling = t_set_cooling

        # initialize envelope properties
        self.h_tr_em = 0
        self.h_tr_w = 0
        self.wall_area = 0
        self.window_area = 0
        self.window_wall_ratio = 0

        #if left blank, zone elements will be set to ASF default values
        if self.elements == None:
            Window = Element(name='ASF_window', area=13.5, u_value=1.1)
            Wall = Element(name='ASF_wall', area=1.69, u_value=0.2)
            self.elements = [Window,Wall]

        for element in self.elements:
            self.add_elements(element)

        if self.thermal_bridges is not None:
            for tb in self.thermal_bridges:
                self.add_thermal_bridge(tb)


    def add_elements(self,e):
        self.element_names.append(e.name)
        #raise error for invalid names
        if not any(x in str.lower(e.name) for x in self.accepted_opaque_element_names + self.accepted_glazing_names):
            raise NameError('element ', e.name, ' is not an accepted element name')
        # add window conductance to window conductances
        if any(x in str.lower(e.name) for x in self.accepted_glazing_names):
            self.h_tr_w += e.h_tr
            self.elements_added += 1
            self.window_area += e.area
        # add surface conductances to conductance of mass
        if any(x in str.lower(e.name) for x in self.accepted_opaque_element_names):
            self.h_tr_em += e.h_tr
            self.elements_added += 1
            self.wall_area += e.area

    def add_thermal_bridge(self,tb):
        self.h_tr_em += tb.h_tr
        self.elements_added += 1

    def summary(self):
        #report the number of elements added to facilitate bug detection
        print 'Zone with %i elements'%len(self.elements)

        print 'Conductance of opaque surfaces to exterior [W/K], h_tr_em:', self.h_tr_em
        print 'Conductance to exterior through glazed surfaces [W/K], h_tr_w', self.h_tr_w
        print 'windows: %f m2, walls: %f m2, total: %f m2'%(self.window_area,self.wall_area,self.window_area+self.wall_area)
        print 'window to wall ratio: %f %%\n' %(int(round(self.window_area/self.wall_area*100,1)))


    def copy(self):
        return Zone(name = self.name,
                 occupants = self.occupants,
                 elements = [e.copy() for e in self.elements],
                 thermal_bridges = [tb.copy() for tb in self.thermal_bridges],
                 floor_area = self.floor_area,
                 volume = self.volume,
                 thermal_capacitance_per_floor_area=self.thermal_capacitance_per_floor_area,
                 ach_vent=self.ach_vent,
                 ach_infl=self.ach_infl,
                 ventilation_efficiency=self.ventilation_efficiency,
                 t_set_heating = self.t_set_heating,
                 t_set_cooling = self.t_set_cooling,
                 max_heating_energy_per_floor_area = self.max_heating_energy_per_floor_area,
                 heating_supply_system = self.heating_supply_system,
                 heating_emission_system = self.heating_emission_system)

    def change_elements(self,newelements):
        return Zone(name = self.name,
                 occupants = self.occupants,
                 elements = newelements,
                 floor_area = self.floor_area,
                 volume = self.volume,
                 thermal_capacitance_per_floor_area=self.thermal_capacitance_per_floor_area,
                 ach_vent=self.ach_vent,
                 ach_infl=self.ach_infl,
                 ventilation_efficiency=self.ventilation_efficiency,
                 t_set_heating = self.t_set_heating,
                 t_set_cooling = self.t_set_cooling,
                 max_heating_energy_per_floor_area = self.max_heating_energy_per_floor_area,
                 heating_supply_system = self.heating_supply_system,
                 heating_emission_system = self.heating_emission_system)



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
