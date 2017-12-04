"""
Aim
Compare the results generated in the ghpython simulation to a python-run model

methodology:
1. load inputs and outputs from grasshopper

2. Run simulation using inputs generated in grasshopper, over the period specified in grasshopper

- default ghpython model should be the same as the python model.
- make sure that all the inputs are the same
    - internal gains, solar gains (probably need to be taken from grasshopper)
- assert that the simulation outputs are also the same.
"""
import unittest
import pandas as pd

# Load grasshopper results

internal_gains
solar_gains
