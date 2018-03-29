import logging
import matplotlib.pyplot as plt
import os
import sys
import datetime

import numpy as np
import ReadFromFile as read
import UnitConverter as units
import Orientation


# LOGGING
def setup_logger(name, log_file, level=logging.INFO):
    # Logging Levels:
    # CRITICAL
    # ERROR
    # WARNING
    # INFO
    # DEBUG

    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


# Setup Log Files
root_path = os.path.dirname(os.path.realpath(__file__))
runlog = setup_logger('runlog', root_path + '/Logs/run.log', level=logging.DEBUG)
alglog = setup_logger('alglog', root_path + '/Logs/alg.log')

runlog.info('START: Thermodynamic Analysis of Multi-Phase Petroleum Fluids.')

orientation_file = root_path + '/Data/orientation3.csv'
# orientation = read.orientation(orientation_file, True)
t, a, w, x, y, z = read.orientation(orientation_file)
# print(datetime.datetime.fromtimestamp(t[0]).strftime('%Y-%m-%d %H:%M:%S.%f'))
# print(datetime.datetime.fromtimestamp(t[1]).strftime('%Y-%m-%d %H:%M:%S.%f'))
print(w[0])

phi, theta, psi = Orientation.euler_angles_array(w, x, y, z)
inc, azi = Orientation.polar_array(w, x, y, z)
Orientation.plot_quarternion(t, w, x, y, z, a)
Orientation.plot_euler(t, phi, theta, psi)
Orientation.plot_incazi(t, inc, azi)
plt.show()


runlog.info('END: Target Destroyed.')
