import logging
import os

import numpy as np
import pandas as pd

root_path = os.path.dirname(os.path.realpath(__file__))
runlog = logging.getLogger('runlog')
alglog = logging.getLogger('alglog')


def is_file_large(file, limit=1e8):
    """
    Checks if file is larger than the limit.

    :param file: File path
    :type file: str
    :param limit: Size limit
    :type limit: int
    :return: bool
    """

    size = os.path.getsize(file)
    if size > limit:
        return True
    return False


def orientation(file, dataframe=False):
    """
    Get quaternion orientation data from SSXquaternion.csv

    :param file: File path
    :type file: str
    :param dataframe: Return pandas.dataframe bool
    :type dataframe: bool
    :return: time, W, X, Y, Z quaternions
    :return: pandas.dataframe or list of np.arrays
    """

    runlog.info('READ FILE: Orientation from file {0}'.format(file))

    df = pd.read_csv(file, delimiter=',', header=0, dtype=np.float64, names=["Time", "Acc", "W", "X", "Y", "Z"])
    if dataframe is True:
        return df
    else:
        t, acc, w, x, y, z = np.array(df["Time"]), np.array(df["Acc"]), np.array(df["W"]), np.array(df["X"]), \
                             np.array(df["Y"]), np.array(df["Z"])
        return t, acc, w, x, y, z


def accel_hf(file, time_initial, time_final, channel="Time", size=2**16):
    """
    Get high frequency data from SSXaccel.csv x-, y-, z-axis accelerometers:

    :param file: File path
    :type file: str
    :param time_initial: Beginning of time of interest (seconds)
    :type time_initial: float
    :param time_final: End of time of interest (seconds)
    :type time_final: float
    :param channel: Name of channel of interest
    :type channel: str
    :param size: Chunk size
    :type size: int
    :return:
    """

    runlog.info('READ FILE: High frequency data from {0} to {1} in file {2}.'.format(time_initial, time_final, file))
    time, accel = [], []

    for chunk in pd.read_csv(file, delimiter=',', header=0, dtype=np.float64, names=["Time", "X", "Y", "Z"],
                             chunksize=size):
        if chunk["Time"].iloc[-1] < time_initial:
            pass
        else:
            if chunk["Time"].iloc[0] > time_final:
                break
            else:
                time.append(chunk["Time"])
                accel.append(chunk[channel])

    if not time:
        pass
    else:
        t = np.array(pd.concat(time))
        time = np.extract(np.logical_and(t >= time_initial, t <= time_final), t)
        accel = np.array(pd.concat(accel))
        accel = np.extract(np.logical_and(time >= time_initial, time <= time_final), accel)

    return time, accel


def accel_dc(file, dataframe=False):
    """
    Get DC MEMS accelerometer data from SSXdcmems.csv

    :param file: File path
    :type file: str
    :param dataframe: Return pandas.dataframe bool
    :type dataframe: bool
    :return: time, X, Y, Z acceleration
    :return: pandas.dataframe or list of np.arrays
    """

    runlog.info('READ: DC MEMS accelerometer file from {0}'.format(file))

    df = pd.read_csv(file, delimiter=',', header=0, dtype=np.float64, names=["Time", "X (DC)", "Y (DC)", "Z (DC)"])
    if dataframe is True:
        return df
    else:
        t, x, y, z = np.array(df["Time"]), np.array(df["X (DC)"]), np.array(df["Y (DC)"]), np.array(df["Z (DC)"])
        return t, x, y, z


def accel_1Hz(file, dataframe=False):
    """
    Get quaternion orientation data from SSXdcmems.csv

    :param file: File path
    :type file: str
    :param dataframe: Return pandas.dataframe bool
    :type dataframe: bool
    :return: time, X, Y, Z acceleration
    :return: pandas.dataframe or list of np.arrays
    """

    df = pd.read_csv(file, delimiter=',', header=0, dtype=np.float64,
                     names=['Time', 'x_avg', 'x_min', 'x_max', 'x_std', 'y_avg', 'y_min', 'y_max', 'y_std', 'z_avg',
                            'z_min', 'z_max', 'z_std'])

    if dataframe is True:
        return df
    else:
        t, x, x_min, x_max, x_std = np.array(df["Time"]), np.array(df["x_avg"]), np.array(df["x_min"]), np.array(df["x_max"]), np.array(df["x_std"])
        y, y_min, y_max, y_std = np.array(df["y_avg"]), np.array(df["y_min"]), np.array(df["y_max"]), np.array(df["y_std"])
        z, z_min, z_max, z_std = np.array(df["z_avg"]), np.array(df["z_min"]), np.array(df["z_max"]), np.array(df["z_std"])
        return t, x, x_min, x_max, x_std, y, y_min, y_max, y_std, z, z_min, z_max, z_std
