
import sys
import os

# Set root folder one level up, just for this example
mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from buildingPhysics import Building  # Importing Building Class
from auxiliary import epwReader
from auxiliary import sunPositionReader

from radiation import Location

matplotlib.style.use('ggplot')


def calculate_sun_angles():
    Zurich = Location(epwfile_path=os.path.join(
        mainPath, 'auxiliary', 'Zurich-Kloten_2013.epw'))

    Zurich.calc_sun_position(latitude_deg=47.480, longitude_deg=8.536, year=2015, HOY=3708)

    Azimuth = []
    Altitude = []
    SunnyHOY = []

    for HOY in range(8760):
        sun = Zurich.calc_sun_position(
            latitude_deg=47.480, longitude_deg=8.536, year=2015, HOY=HOY)
        Altitude.append(sun[0])
        Azimuth.append(sun[1])
        SunnyHOY.append(HOY + 1)

    sunPosition = pd.read_csv(os.path.join(
        mainPath, 'auxiliary', 'SunPosition.csv'), skiprows=1)

    transSunPos = sunPosition.transpose()
    HOY_check = transSunPos.index.tolist()
    HOY_check = [float(ii) for ii in HOY_check]
    Azimuth_check = (180 - transSunPos[1]).tolist()

    Altitude_check = transSunPos[0].tolist()

    plt.style.use('ggplot')

    plt.plot(SunnyHOY, Azimuth, HOY_check, Azimuth_check,
             SunnyHOY, Altitude, HOY_check, Altitude_check)
    plt.legend(['Azimuth', 'Azimuth Check', 'Altitude', 'Altitude_check'])

    plt.show()

if __name__ == '__main__':
    calculate_sun_angles()
