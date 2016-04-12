# RC_BuildingSimulator

Simulates the energy balance of a single zone room based on an RC model. This project is still under development

## RC Model used
![RC Model](./Images/1c_rc_circuit.png)

`T_out`: External temperature in C extracted from an EPW weather file

`T_in`: Calculated internal temperature

`R_env`: Resistance of the envelope. Must be caluclated by hand and inputted into the `Building` class in `BuildingProperties.py`

`R_infl`: Equivalent resistance due to infiltration. This is calculated within `BuildingProperties.py`

`R_vent`: Equivalent resistance due to ventelation. A variable resistance calculated by the `setVentelation` method in within the `Building` class of `BuildingProperties.py`

`Cm`: Capacitance of the room. Must be caluclated by hand and inputted into the `Building` class in `BuildingProperties.py`

`Q_Heat`: Heat energy supplied or removed by the heater or cooler. This is determined through a controller based on the temperature set points

`Q_rad`: Heat energy to the sun. Hourly radiation data through the windows must be determined in advance and read through the `read_transmittedR` funtion of `input_data.py`

`Q_gains`: Internal heat gains of people. Determined through the occupancy profile which is read in through the `read_occupancy` function of `input_data.py`






##References

Madsen, Henrik, and Jan Holst. "Estimation of continuous-time models for the heat dynamics of a building." Energy and Buildings 22.1 (1995): 67-79.

Bacher, Peder, and Henrik Madsen. "Identifying suitable models for the heat dynamics of buildings." Energy and Buildings 43.7 (2011): 1511-1522.

Sonderegger, Robert. "Diagnostic tests determining the thermal response of a house." Lawrence Berkeley National Laboratory (2010).
