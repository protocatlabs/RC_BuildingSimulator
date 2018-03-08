# This comoponent contains an object-oriented adaptation of the RC model referred to as the 'Simple Hourly Method' in ISO 13790, (superceded by EN ISO 52016-1).
# The code is a slightly modified version of building_physics.py in the main 
# branch, and is based on the nested_rc branch. The modifications make it easier
# to accomodate a more modular zone definiton, made of a zone and elements. 

# Nest: An educational plugin developed by the A/S chair at ETH Zurich
# This component is based on building_physics.py in the RC_BuildingSimulator 
# github repository
# https://github.com/architecture-building-systems/RC_BuildingSimulator
# Extensive documentation is available on the project wiki.
#
# Authors: Prageeth Jayathissa <jayathissa@arch.ethz.ch>, Justin Zarb 
# <zarbj@student.ethz.ch>
# Adapted for Grasshopper by Justin Zarb
#
# This file is part of Nest
#
# Licensing/Copywrite and liability comments go here.
# Copyright 2018, Architecture and Building Systems - ETH Zurich
# Licence: MIT

"""
Place this component in the grasshopper workspace so that zones can be defined and simulations run.
-
Provided by Nest 0.0.1
"""

ghenv.Component.Name = "Modular Building Physics"
ghenv.Component.NickName = 'ModularBuildingPhysics'
ghenv.Component.Message = 'VER 0.0.1\nMAR_08_2018'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Nest"
ghenv.Component.SubCategory = "0 | Core"

try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import scriptcontext as sc
import rhinoscriptsyntax as rs
import Rhino as rc

class Element(object):
    """
    Element object representing an opaque or transparent element.
    ##OUTLOOK##
    absorptivity, reflectivity: Not yet implemented, but adding these parameters 
    would improve the accuracy of solar gains calculations in opaque and 
    transparent elements.The RC model would need to be adapted for this. Note to 
    future developers: when adding attributes, make sure to upadate the copy 
    method below with the same attributes!
    """
    def __init__(self,
                 name = 'Element', #should contain one of the following: [Wall, Window, Ground slab, Roof]
                 area = 15.0, #Element area, [m2]
                 u_value = 1.0, #Element u_value-value, [W/m2.K]
                 azimuth_tilt = 0, #South facing by default
                 altitude_tilt = 90, #vertical surfaces by default
                 opaque = True,
                 solar_transmittance = 0.7,
                 light_transmittance=0.8,
                 frame_factor=1.0
                 ):

        self.name = name
        self.area = area
        self.u_value = u_value
        self.h_tr = self.u_value * self.area #element conductance [W/K]
        self.azimuth_tilt = azimuth_tilt
        self.altitude_tilt = altitude_tilt
        self.frame_factor = frame_factor
        self.opaque = opaque

        if opaque:
            self.solar_transmittance = 0
            self.light_transmittance = 0
        else:
            self.solar_transmittance = solar_transmittance
            self.light_transmittance = light_transmittance


class ElementBuilder(object):
    def __init__(self,element_name,u_value,solar_transmittance,
                light_transmittance,frame_factor,opaque):
        
        self.opaque= opaque
        if self.opaque:
            self.element_name = element_name if element_name is not None else 'Wall'
            self.u_value = 0.2 if u_value is None else u_value
            self.solar_transmittance = 0
            self.light_transmittance = 0
            self.frame_factor = 1
        else:
            self.element_name = element_name if element_name is not None else 'Window'
            self.u_value = 1 if u_value is None else u_value
            self.solar_transmittance = 0.7 if solar_transmittance is None else solar_transmittance
            self.light_transmittance = 0.8 if light_transmittance is None else light_transmittance
            self.frame_factor = 1 if frame_factor is None else frame_factor

    def get_data(self,surface):
        north = rc.Geometry.Vector3d(0,1,0)
        vertical = rc.Geometry.Vector3d(0,0,1)
        faces_west = False
        # Get area, normal (show this in rhino),
        centroid = rs.SurfaceAreaCentroid(surface)[0]
        normal = rs.SurfaceNormal(surface,[0.5,0.5])
        if normal[0] < 0:
            faces_west = True
        else:
            faces_west = False
        normal_xy = rc.Geometry.Vector3d(normal[0],normal[1],0)
        normal_xz = rc.Geometry.Vector3d(normal[0],0,normal[2])
        try:
            azimuth = rs.VectorAngle(north,normal_xy)
            if faces_west:
                azimuth = 360-azimuth
        except ValueError:
            azimuth = 0
        try: 
            altitude = rs.VectorAngle(vertical,normal_xz)
        except ValueError:
            altitude = 0
        area = rs.SurfaceArea(surface)[0]
        return centroid,normal,area,azimuth,altitude

    def Elements(self,geometry):
        centroids = []
        normals = []
        glazed_elements = []
        if geometry is not None:
            # Invalid input
            if not (rs.IsSurface(geometry) or rs.IsPolysurface(geometry)):
                error = """geometry is not a surface or polysurface"""
                w = gh.GH_RuntimeMessageLevel.Error
                ghenv.Component.AddRuntimeMessage(w, warning)
        
            # Single surface
            elif rs.IsSurface(geometry):
                centroid,normal,area,azimuth,altitude = self.get_data(geometry)
                centroids = centroid
                normals = normal
                glazed_elements = sc.sticky['Element'](
                    name=self.element_name,
                    area=area,
                    u_value=self.u_value, 
                    azimuth_tilt=azimuth,
                    altitude_tilt=altitude,
                    opaque=self.opaque,
                    solar_transmittance=self.solar_transmittance,
                    light_transmittance=self.light_transmittance,
                    frame_factor=self.frame_factor)

            # Polysurface
            elif rs.IsPolysurface(geometry):
                all_parts = rs.ExplodePolysurfaces(geometry)
                for part in all_parts:
                    centroid,normal,area,azimuth,angle = self.get_data(part)
                    centroids.append(centroid)
                    normals.append(n)
                    glazed_element = sc.sticky['Element'](
                        name=self.element_name,
                        area=area,
                        u_value=self.u_value, 
                        azimuth_tilt=azimuth,
                        altitude_tilt=altitude,
                        opaque=self.opaque,
                        solar_transmittance=self.solar_transmittance,
                        light_transmittance=self.light_transmittance,
                        frame_factor=self.frame_factor)
                    glazed_elements.append(glazed_element)
        return centroids,normals,glazed_elements


class ThermalBridge(object):
    def __init__(self,
                 name,
                 length,
                 linear_conductance):
        self.name = name
        self.length = length
        self.linear_conductance = linear_conductance
        self.h_tr = length * linear_conductance


class Zone(object):
    def __init__(self,
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
                 max_heating_energy_per_floor_area = 12,
                 max_cooling_energy_per_floor_area = -12,
                 heating_supply_system=sc.sticky["DirectHeater"],
                 cooling_supply_system=sc.sticky["DirectCooler"],
                 heating_emission_system=sc.sticky["AirConditioning"],
                 cooling_emission_system=sc.sticky["AirConditioning"],
                ):

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
        # add surface conductances to conductance of mass
        if e.opaque:
            self.h_tr_em += e.h_tr
            self.elements_added += 1
            self.wall_area += e.area
        # add window conductance to window conductances
        else:
            self.h_tr_w += e.h_tr
            self.elements_added += 1
            self.window_area += e.area
        

    def add_thermal_bridge(self,tb):
        self.h_tr_em += tb.h_tr
        self.elements_added += 1

    def summary(self):
        #report the number of elements added to facilitate bug detection
        print 'Zone with %i elements'%len(self.elements)
        print 'Conductance of opaque surfaces to exterior [W/K], h_tr_em:', self.h_tr_em
        print 'Conductance to exterior through glazed surfaces [W/K], h_tr_w', self.h_tr_w
        print 'windows: %f m2, walls: %f m2, total: %f m2'%(self.window_area,self.wall_area,self.window_area+self.wall_area)
        try:
            print 'window to wall ratio: %f %%\n'%(int(round(self.window_area/self.wall_area*100,1)))
        except ZeroDivisionError:
            print '100% glazed'


class Building(object):
    '''Sets the parameters of the building. '''

    def __init__(self,
                 zone=None,
                 lighting_load=11.7,
                 lighting_control=300.0,
                 lighting_utilisation_factor=0.45,
                 lighting_maintenance_factor=0.9,
                 ):

        # Initialise Zone
        self.zone = zone
        if self.zone == None:
            self.zone = Zone()

        # Fenestration and Lighting Properties
        self.lighting_load = lighting_load  # [kW/m2] lighting load
        self.lighting_control = lighting_control  # [lux] Lighting set point
        # How the light entering the window is transmitted to the working plane
        self.lighting_utilisation_factor = lighting_utilisation_factor
        # How dirty the window is. Section 2.2.3.1 Environmental Science
        # Handbook
        self.lighting_maintenance_factor = lighting_maintenance_factor

        # Calculated Properties
        self.floor_area = self.zone.floor_area # [m2] Floor Area
        # [m2] Effective Mass Area assuming a medium weight building #12.3.1.2
        # very light: 2.5 x Af
        # heavy: 3.0 x Af
        # very heavy: 3.5 x Af
        self.mass_area = self.floor_area * 2.5
        self.room_vol = self.zone.volume# [m3] Room Volume
        self.total_internal_area = self.zone.total_internal_area
        # TODO: Standard doesn't explain what A_t is. Needs to be checked
        self.A_t = self.total_internal_area

        # Single Capacitance  5 conductance Model Parameters
        # [kWh/K] Room Capacitance. Default based on ISO standard 12.3.1.2 for medium heavy buildings
        self.c_m = self.zone.thermal_capacitance_per_floor_area * self.floor_area
        # Conductance of opaque surfaces to exterior [W/K]
        self.h_tr_em = self.zone.h_tr_em
        # Conductance to exterior through glazed surfaces [W/K], based on
        # U-wert of 1W/m2K
        self.h_tr_w = self.zone.h_tr_w
        # Determine the ventilation conductance
        ach_tot = self.zone.ach_infl + self.zone.ach_vent  # Total Air Changes Per Hour
        # temperature adjustment factor taking ventilation and infiltration
        # [ISO: E -27]
        if ach_tot > 0:
            b_ek = 1 - (self.zone.ach_vent / ach_tot) * self.zone.ventilation_efficiency
        else:
            b_ek = 1
        # b_ek = (self.zone.ach_vent/ ach_tot) * self.zone.ventilation_efficiency
        self.h_ve_adj = 1200 * b_ek * self.room_vol * \
            (ach_tot / 3600)  # Conductance through ventilation [W/M]
        # transmittance from the internal air to the thermal mass of the
        # building
        self.h_tr_ms = 9.1 * self.mass_area
        # Conductance from the conditioned air to interior building surface
        self.h_tr_is = self.total_internal_area * 3.45

        # Thermal set points
        self.t_set_heating = self.zone.t_set_heating
        self.t_set_cooling = self.zone.t_set_cooling

        # Thermal Properties
        self.has_heating_demand = False  # Boolean for if heating is required
        self.has_cooling_demand = False  # Boolean for if cooling is required
        self.max_cooling_energy = zone.max_cooling_energy_per_floor_area * \
            self.floor_area  # max cooling load (W/m2)
        self.max_heating_energy = zone.max_heating_energy_per_floor_area * \
            self.floor_area  # max heating load (W/m2)
        # Building System Properties
        self.heating_supply_system = zone.heating_supply_system
        self.cooling_supply_system = zone.cooling_supply_system
        self.heating_emission_system = zone.heating_emission_system
        self.cooling_emission_system = zone.cooling_emission_system

    def solve_building_lighting(self, illuminance, occupancy):
        """
        Calculates the lighting demand for a set timestep
        :param illuminance: Illuminance transmitted through the window [Lumens]
        :type illuminance: float
        :param : Probability of full occupancy
        :type occupancy: float
        :return: self.lighting_demand, Lighting Energy Required for the timestep
        :rtype: float
        """
        # Cite: Environmental Science Handbook, SV Szokolay, Section 2.2.1.3
        # also, this might be sped up by pre-calculating the constants, but idk. first check with profiler...
        lux = (illuminance * self.lighting_utilisation_factor *
               self.lighting_maintenance_factor) / self.floor_area  # [Lux]

        if lux < self.lighting_control and occupancy > 0:
            # Lighting demand for the hour
            self.lighting_demand = self.lighting_load * self.floor_area
        else:
            self.lighting_demand = 0

    def solve_building_energy(self, internal_gains, solar_gains, t_out, t_m_prev):
        """
        Calculates the heating and cooling consumption of a building for a set timestep
        :param internal_gains: internal heat gains from people and appliances [W]
        :type internal_gains: float
        :param solar_gains: solar heat gains [W]
        :type solar_gains: float
        :param t_out: Outdoor air temperature [C]
        :type t_out: float
        :param t_m_prev: Previous air temperature [C]
        :type t_m_prev: float
        :return: self.heating_demand, space heating demand of the building
        :return: self.heating_sys_electricity, heating electricity consumption
        :return: self.heating_sys_fossils, heating fossil fuel consumption
        :return: self.cooling_demand, space cooling demand of the building
        :return: self.cooling_sys_electricity, electricity consumption from cooling
        :return: self.cooling_sys_fossils, fossil fuel consumption from cooling
        :return: self.electricity_out, electricity produced from combined heat pump systems
        :return: self.sys_total_energy, total exergy consumed (electricity + fossils) for heating and cooling
        :return: self.heating_energy, total exergy consumed (electricity + fossils) for heating
        :return: self.cooling_energy, total exergy consumed (electricity + fossils) for cooling
        :return: self.cop, Coefficient of Performance of the heating or cooling system
        :rtype: float
        """
        # Main File
        # Calculate the heat transfer definitions for formula simplification
        self.calc_h_tr_1()
        self.calc_h_tr_2()
        self.calc_h_tr_3()

        # check demand, and change state of self.has_heating_demand, and self._has_cooling_demand
        self.has_demand(internal_gains, solar_gains, t_out, t_m_prev)

        if not self.has_heating_demand and not self.has_cooling_demand:
            # no heating or cooling demand
            # calculate temperatures of building R-C-model and exit
            # --> rc_model_function_1(...)
            self.energy_demand = 0

            # y u no pep8 bra?
            self.heating_demand = 0  # Energy required by the Zone
            self.cooling_demand = 0  # Energy surplus of the Zone
            # Energy (in electricity) required by the supply system to provide
            # HeatingDemand
            self.heating_sys_electricity = 0
            # Energy (in fossil fuel) required by the supply system to provide
            # HeatingDemand
            self.heating_sys_fossils = 0
            # Energy (in electricity) required by the supply system to get rid
            # of CoolingDemand
            self.cooling_sys_electricity = 0
            # Energy (in fossil fuel) required by the supply system to get rid
            # of CoolingDemand
            self.cooling_sys_fossils = 0
            # Electricity produced by the supply system (e.g. CHP)
            self.electricity_out = 0

        else:
            # has heating/cooling demand

            # Calculates energy_demand used below
            self.calc_energy_demand(
                internal_gains, solar_gains, t_out, t_m_prev)

            self.calc_temperatures_crank_nicolson(
                self.energy_demand, internal_gains, solar_gains, t_out, t_m_prev)
            # calculates the actual t_m resulting from the actual heating
            # demand (energy_demand)

            # Calculate the Heating/Cooling Input Energy Required

            supply_director = sc.sticky["SupplyDirector"]()  # Initialise Heating System Manager

            if self.has_heating_demand:
                supply_director.set_builder(self.heating_supply_system(load=self.energy_demand,
                                                                t_out=t_out,
                                                                heating_supply_temperature=self.heating_supply_temperature,
                                                                cooling_supply_temperature=self.cooling_supply_temperature,
                                                                has_heating_demand=self.has_heating_demand,
                                                                has_cooling_demand=self.has_cooling_demand))
                supplyOut = supply_director.calc_system()
                # All Variables explained underneath line 467
                self.heating_demand = self.energy_demand
                self.heating_sys_electricity = supplyOut.electricity_in
                self.heating_sys_fossils = supplyOut.fossils_in
                self.cooling_demand = 0
                self.cooling_sys_electricity = 0
                self.cooling_sys_fossils = 0
                self.electricity_out = supplyOut.electricity_out

            elif self.has_cooling_demand:
                supply_director.set_builder(self.cooling_supply_system(load=self.energy_demand * (-1),
                                                                t_out=t_out,
                                                                heating_supply_temperature=self.heating_supply_temperature,
                                                                cooling_supply_temperature=self.cooling_supply_temperature,
                                                                has_heating_demand=self.has_heating_demand,
                                                                has_cooling_demand=self.has_cooling_demand))
                supplyOut = supply_director.calc_system()
                self.heating_demand = 0
                self.heating_sys_electricity = 0
                self.heating_sys_fossils = 0
                self.cooling_demand = self.energy_demand
                self.cooling_sys_electricity = supplyOut.electricity_in
                self.cooling_sys_fossils = supplyOut.fossils_in
                self.electricity_out = supplyOut.electricity_out

            self.cop = supplyOut.cop

        self.sys_total_energy = self.heating_sys_electricity + self.heating_sys_fossils + \
            self.cooling_sys_electricity + self.cooling_sys_fossils
        self.heating_energy = self.heating_sys_electricity + self.heating_sys_fossils
        self.cooling_energy = self.cooling_sys_electricity + self.cooling_sys_fossils

    # TODO: rename. this is expected to return a boolean. instead, it changes state??? you don't want to change state...
    # why not just return has_heating_demand and has_cooling_demand?? then call the function "check_demand"
    # has_heating_demand, has_cooling_demand = self.check_demand(...)
    def has_demand(self, internal_gains, solar_gains, t_out, t_m_prev):
        """
        Determines whether the building requires heating or cooling
        Used in: solve_building_energy()
        # step 1 in section C.4.2 in [C.3 ISO 13790]
        """
        # set energy demand to 0 and see if temperatures are within the comfort
        # range
        energy_demand = 0
        # Solve for the internal temperature t_Air
        self.calc_temperatures_crank_nicolson(
            energy_demand, internal_gains, solar_gains, t_out, t_m_prev)
        # If the air temperature is less or greater than the set temperature,
        # there is a heating/cooling load
        if self.t_air < self.t_set_heating:
            self.has_heating_demand = True
            self.has_cooling_demand = False
        elif self.t_air > self.t_set_cooling:
            self.has_cooling_demand = True
            self.has_heating_demand = False
        else:
            self.has_heating_demand = False
            self.has_cooling_demand = False

    def calc_temperatures_crank_nicolson(self, energy_demand, internal_gains, solar_gains, t_out, t_m_prev):
        """
        Determines node temperatures and computes derivation to determine the new node temperatures
        Used in: has_demand(), solve_building_energy(), calc_energy_demand()
        # section C.3 in [C.3 ISO 13790]
        """
        self.calc_heat_flow(t_out, internal_gains, solar_gains, energy_demand)

        self.calc_phi_m_tot(t_out)

        # calculates the new bulk temperature POINT from the old one
        self.calc_t_m_next(t_m_prev)

        # calculates the AVERAGE bulk temperature used for the remaining
        # calculation
        self.calc_t_m(t_m_prev)

        self.calc_t_s(t_out)

        self.calc_t_air(t_out)

        self.calc_t_opperative()
        return self.t_m, self.t_air, self.t_opperative

    def calc_energy_demand(self, internal_gains, solar_gains, t_out, t_m_prev):
        """
        Calculates the energy demand of the space if heating/cooling is active
        Used in: solve_building_energy()
        # Step 1 - Step 4 in Section C.4.2 in [C.3 ISO 13790]
        """

        # Step 1: Check if heating or cooling is needed
        #(Not needed, but doing so for readability when comparing with the standard)
        # Set heating/cooling to 0
        energy_demand_0 = 0
        # Calculate the air temperature with no heating/cooling
        t_air_0 = self.calc_temperatures_crank_nicolson(
            energy_demand_0, internal_gains, solar_gains, t_out, t_m_prev)[1]

        # Step 2: Calculate the unrestricted heating/cooling required

        # determine if we need heating or cooling based based on the condition
        # that no heating or cooling is required
        if self.has_heating_demand:
            t_air_set = self.t_set_heating
        elif self.has_cooling_demand:
            t_air_set = self.t_set_cooling
        else:
            raise NameError(
                'heating function has been called even though no heating is required')

        # Set a heating case where the heating load is 10x the floor area (10
        # W/m2)
        energy_floorAx10 = 10 * self.floor_area

        # Calculate the air temperature obtained by having this 10 W/m2
        # setpoint
        t_air_10 = self.calc_temperatures_crank_nicolson(
            energy_floorAx10, internal_gains, solar_gains, t_out, t_m_prev)[1]

        # Determine the unrestricted heating/cooling off the building
        self.calc_energy_demand_unrestricted(
            energy_floorAx10, t_air_set, t_air_0, t_air_10)

        # Step 3: Check if available heating or cooling power is sufficient
        if self.max_cooling_energy <= self.energy_demand_unrestricted <= self.max_heating_energy:

            self.energy_demand = self.energy_demand_unrestricted
            self.t_air_ac = t_air_set  # not sure what this is used for at this stage TODO

        # Step 4: if not sufficient then set the heating/cooling setting to the
        # maximum
        # necessary heating power exceeds maximum available power
        elif self.energy_demand_unrestricted > self.max_heating_energy:
            self.energy_demand = self.max_heating_energy

        # necessary cooling power exceeds maximum available power
        elif self.energy_demand_unrestricted < self.max_cooling_energy:

            self.energy_demand = self.max_cooling_energy

        else:
            self.energy_demand = 0
            raise ValueError('unknown radiative heating/cooling system status')

        # calculate system temperatures for Step 3/Step 4
        self.calc_temperatures_crank_nicolson(
            self.energy_demand, internal_gains, solar_gains, t_out, t_m_prev)

    def calc_energy_demand_unrestricted(self, energy_floorAx10, t_air_set, t_air_0, t_air_10):
        """
        Calculates the energy demand of the system if it has no maximum output restrictions
        # (C.13) in [C.3 ISO 13790]
        Based on the Thales Intercept Theorem.
        Where we set a heating case that is 10x the floor area and determine the temperature as a result
        Assuming that the relation is linear, one can draw a right angle triangle.
        From this we can determine the heating level required to achieve the set point temperature
        This assumes a perfect HVAC control system
        """
        self.energy_demand_unrestricted = energy_floorAx10 * \
            (t_air_set - t_air_0) / (t_air_10 - t_air_0)

    def calc_heat_flow(self, t_out, internal_gains, solar_gains, energy_demand):
        """
        Calculates the heat flow from the solar gains, heating/cooling system, and internal gains into the building
        The input of the building is split into the air node, surface node, and thermal mass node based on
        on the following equations
        #C.1 - C.3 in [C.3 ISO 13790]
        Note that this equation has diverged slightly from the standard
        as the heating/cooling node can enter any node depending on the
        emission system selected
        """

        # Calculates the heat flows to various points of the building based on the breakdown in section C.2, formulas C.1-C.3
        # Heat flow to the air node
        self.phi_ia = 0.5 * internal_gains
        # Heat flow to the surface node
        self.phi_st = (1 - (self.mass_area / self.A_t) - (self.h_tr_w /
                            (9.1 * self.A_t))) * (0.5 * internal_gains + solar_gains)
        # Heatflow to the thermal mass node
        self.phi_m = (self.mass_area / self.A_t) * \
            (0.5 * internal_gains + solar_gains)

        # We call the EmissionDirector to modify these flows depending on the
        # system and the energy demand
        emDirector = sc.sticky["EmissionDirector"]()
        # Set the emission system to the type specified by the user

        emDirector.set_builder(self.heating_emission_system(
            energy_demand=energy_demand))
        # Calculate the new flows to each node based on the heating system
        flows = emDirector.calc_flows()

        # Set modified flows to building object
        self.phi_ia += flows.phi_ia_plus
        self.phi_st += flows.phi_st_plus
        self.phi_m += flows.phi_m_plus

        # Set supply temperature to building object
        # TODO: This currently is constant for all emission systems, to be
        # modified in the future
        self.heating_supply_temperature = flows.heating_supply_temperature
        self.cooling_supply_temperature = flows.cooling_supply_temperature

    def calc_t_m_next(self, t_m_prev):
        """
        Primary Equation, calculates the temperature of the next time step
        # (C.4) in [C.3 ISO 13790]
        """

        self.t_m_next = ((t_m_prev * ((self.c_m / 3600.0) - 0.5 * (self.h_tr_3 + self.h_tr_em))) +
                         self.phi_m_tot) / ((self.c_m / 3600.0) + 0.5 * (self.h_tr_3 + self.h_tr_em))

    def calc_phi_m_tot(self, t_out):
        """
        Calculates a global heat transfer. This is a definition used to simplify equation
        calc_t_m_next so it's not so long to write out
        # (C.5) in [C.3 ISO 13790]
        # h_ve = h_ve_adj and t_supply = t_out [9.3.2 ISO 13790]
        """

        t_supply = t_out  # ASSUMPTION: Supply air comes straight from the outside air
        h_tr_3 = False
        for key in self.__dict__:
            if 'h_tr_3' in key:
                h_tr_3 = True
        if not h_tr_3: # This is the case when heating is supplied and crank-nicholson is called directly
            self.calc_h_tr_3()


        self.phi_m_tot = self.phi_m + self.h_tr_em * t_out + \
            self.h_tr_3 * (self.phi_st + self.h_tr_w * t_out + self.h_tr_1 *
                           ((self.phi_ia / self.h_ve_adj) + t_supply)) / self.h_tr_2

    def calc_h_tr_1(self):
        """
        Definition to simplify calc_phi_m_tot
        # (C.6) in [C.3 ISO 13790]
        """
        self.h_tr_1 = 1.0 / (1.0 / self.h_ve_adj + 1.0 / self.h_tr_is)

    def calc_h_tr_2(self):
        """
        Definition to simplify calc_phi_m_tot
        # (C.7) in [C.3 ISO 13790]
        """
        h_tr_1 = False
        for key in self.__dict__:
            if 'h_tr_1' in key:
                h_tr_1 = True
        if not h_tr_1:
            self.calc_h_tr_1 ()

        self.h_tr_2 = self.h_tr_1 + self.h_tr_w

    def calc_h_tr_3(self):
        """
        Definition to simplify calc_phi_m_tot
        # (C.8) in [C.3 ISO 13790]
        """
        h_tr_2 = False
        for key in self.__dict__:
            if 'h_tr_2' in key:
                h_tr_2 = True
        if not h_tr_2:
            self.calc_h_tr_2()

        self.h_tr_3 = 1.0 / (1.0 / self.h_tr_2 + 1.0 / self.h_tr_ms)

    def calc_t_m(self, t_m_prev):
        """
        Temperature used for the calculations, average between newly calculated and previous bulk temperature
        # (C.9) in [C.3 ISO 13790]
        """
        self.t_m = (self.t_m_next + t_m_prev) / 2.0
    def calc_t_s(self, t_out):
        """
        Calculate the temperature of the inside room surfaces
        # (C.10) in [C.3 ISO 13790]
        # h_ve = h_ve_adj and t_supply = t_out [9.3.2 ISO 13790]
        """

        t_supply = t_out  # ASSUMPTION: Supply air comes straight from the outside air

        self.t_s = (self.h_tr_ms * self.t_m + self.phi_st + self.h_tr_w * t_out + self.h_tr_1 * \
            (t_supply + self.phi_ia / self.h_ve_adj)) / \
            (self.h_tr_ms + self.h_tr_w + self.h_tr_1)

    def calc_t_air(self, t_out):
        """
        Calculate the temperature of the air node
        # (C.11) in [C.3 ISO 13790]
        # h_ve = h_ve_adj and t_supply = t_out [9.3.2 ISO 13790]
        """

        t_supply = t_out

        # Calculate the temperature of the inside air
        self.t_air = (self.h_tr_is * self.t_s + self.h_ve_adj *
                      t_supply + self.phi_ia) / (self.h_tr_is + self.h_ve_adj)

    def calc_t_opperative(self):
        """
        The opperative temperature is a weighted average of the air and mean radiant temperatures.
        It is not used in any further calculation at this stage
        # (C.12) in [C.3 ISO 13790]
        """
        
        self.t_opperative = 0.3 * self.t_air + 0.7 * self.t_s


sc.sticky["Element"] = Element
sc.sticky["ElementBuilder"] = ElementBuilder
sc.sticky["ThermalBridge"] = ThermalBridge
sc.sticky["Zone"] = Zone
sc.sticky["ModularRCZone"] = Building

print 'Modular Building Physics is go!'