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


##How it Works

### Reading External Data Files `input_data.py`
`input_data.py` contains the methods required to read epw weather files, radiation files and occupancy profiles

`read_EWP`: Reads the EPW file and outputs the average external temperature `T_out`, Global Irradiance, and Global Illuminance 

`read_transmittedMonthlyR`: Reads a radiation file outputted from Jeremias' ladybug script. The radiation file contains hourly radiation data for a day for each month. The data therefore needs to be converted into hourly data for the whole year

`read_transmittedR`: Reads radiation value outputted from a standard ladybug script. The radiation file should contain hourly radiation data for the whole year

`read_occupancy`: Reads the occupancy file used by the [CEA](https://github.com/architecture-building-systems/CEAforArcGIS/tree/master/cea/db/Schedules) tool.

`Equate_Ill`: measures the global irradiation and global illuminance of the weather file to obtain a formula of the type
$$Ill=Rad*x + y$$

This formula will then be used to determine the illuminance of room based off the radiaion supplied. NOTE: This is a bit of a hack. Try find a more elegant way of calculating the solar illumination of the room. **TO_DO**


### Setting your Building Parameters `BuildingProperties.py`
This script contains a `Building` class which sets your building parameters. Default values are already provided. Do not modify any of the parameters here. You will create an instance of this class in the `Main.py` file

`setVentilation`: A method which outputs the resistance between the inside and outside air temperatures. This is the combination of `R_env`, `R_vent` and `R_infl` as described in the RC Model Above

###Running your Simulation `Main.py`

This is the main file which you will modify and run. 

####Step 1: Import the data. 
The first lines should run the various methods form `import_data.py` and read in the necessary data

####Step 2: Set the Room Building Parameters
Simply typing `Office=Building()` will initialise your building with default parameters. If you want to specialise your building then run 



##References

Madsen, Henrik, and Jan Holst. "Estimation of continuous-time models for the heat dynamics of a building." Energy and Buildings 22.1 (1995): 67-79.

Bacher, Peder, and Henrik Madsen. "Identifying suitable models for the heat dynamics of buildings." Energy and Buildings 43.7 (2011): 1511-1522.

Sonderegger, Robert. "Diagnostic tests determining the thermal response of a house." Lawrence Berkeley National Laboratory (2010).
