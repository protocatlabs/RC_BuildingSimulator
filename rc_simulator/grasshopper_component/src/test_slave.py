# This component confirms that the model outputs match predefined values
#
# Oasys: A energy simulation plugin developed by the A/S chair at ETH Zurich
#
# This component is based on tests\testRCmodel.py (accessed 2/22/2018) 
# in the RC_BuildingSimulator Github repository:
# https://github.com/architecture-building-systems/RC_BuildingSimulator
# Documentation is available on the project wiki.
#
# Author: Justin Zarb <zarbj@student.ethz.ch>
#
# This file is part of Oasys
#
# Licensing/Copyright and liability comments go here.
# <Copyright 2018, Architecture and Building Systems - ETH Zurich>
# <Licence: MIT>

"""
Use this component to run standard tests on the RC model within the GH environment.
This test ensures that the grasshopper component returns the same results as the python model.
-
Provided by Oasys 0.0.1
    
    Args:
        pass
    Returns:
        pass
"""

ghenv.Component.Name = "Unit Test Slave"
ghenv.Component.NickName = 'unit_test_slave'
ghenv.Component.Message = 'VER 0.0.1\nFEB_26_2018'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Oasys"
ghenv.Component.SubCategory = "Simulation"
#compatibleOasysVersion = VER 0.0.1\nFEB_21_2018
try: ghenv.Component.AdditionalHelpFromDocStrings = "3"
except: pass


import scriptcontext as sc

# Initialise results
results = {'mass_temperature':mass_temperature,
           'lighting_demand':lighting_demand,
           'heating_sys_electricity':heating_sys_electricity,
           'cooling_sys_electricity':cooling_sys_electricity,
           'energy_demand':energy_demand,
           'cop':cop}

def is_equal(a,b):
    try:
        assert a==round(b,2)
        return True
    except:
        return False

# Create a truth dictionary based on whether each value matches
test = {}
for k in sc.sticky['expected_results'].keys():
    try:
        assert sc.sticky['expected_results'][k][sc.sticky['run_test']] is not None
        test[k] = (is_equal(sc.sticky['expected_results'][k][sc.sticky['run_test']],results[k]))
    except (KeyError,AssertionError): # there is no 'name' key in the results dictionary
        pass
print sc.sticky['expected_results']['name'][sc.sticky['run_test']]


for key in test.keys():
    value = str(round(results[key],2))+'/'+str(sc.sticky['expected_results'][key][sc.sticky['run_test']])
    token = 'passed' if test[key] else value
    print key,':',token

# Return True if all tests passed:
test_passed = reduce(lambda x, y: x * y, test.values(), 1)

sc.sticky['run_test']+=1