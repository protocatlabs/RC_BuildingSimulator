# Glazed element
#
# Nest: A energy simulation plugin developed by the A/S chair at ETH Zurich
# This component is based on building_physics.py in the RC_BuildingSimulator Github repository
# https://github.com/architecture-building-systems/RC_BuildingSimulator
# Extensive documentation is available on the project wiki.
#
# Author: Justin Zarb <zarbj@student.ethz.ch>
#
# This file is part of Nest
#
# Licensing/Copyright and liability comments go here.
# <Copyright 2018, Architecture and Building Systems - ETH Zurich>
# <Licence: MIT>

"""
Define an opaque by adding a surface.
-
Provided by Nest 0.0.1
    
    Args:
        _window_geometry: a surface or polysurface representing the 
            heat-transfer area of the element
        window_name: optional element name
        _u_value: element u-value [W/(m^2.K)]
        solar_transmittance: (aka. g-factor) the percentage of radiation that can pass through glazing
        light_transmittance: the percentage of light that passes through glazing
    Returns:
        centers: list of center points to check input
        normals: list of normals to check input
        glazed_elements: list of element objects representing each surface that was inputted.
"""

ghenv.Component.Name = "Glazed Element"
ghenv.Component.NickName = 'GlazedElement'
ghenv.Component.Message = 'VER 0.0.1\nMar_06_2018'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Nest"
ghenv.Component.SubCategory = " 1 | Zone"
#compatibleNestVersion = VER 0.0.1\nFEB_21_2018
try: ghenv.Component.AdditionalHelpFromDocStrings = "2"
except: pass

import scriptcontext as sc

Builder = sc.sticky['ElementBuilder'](window_name,u_value,
    solar_transmittance,light_transmittance,frame_factor,opaque=False)

centers,normals,glazed_elements = Builder.Elements(_window_geometry)