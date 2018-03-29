import logging
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import UnitConverter as units

root_path = os.path.dirname(os.path.realpath(__file__))
runlog = logging.getLogger('runlog')
alglog = logging.getLogger('alglog')


def polar_array(w, x, y, z):
    """
    Calculates the Inclination and Azimuth from the Quaternion for an entire array.

    :param w: W Quarternion
    :type w: np.ndarray
    :param x: X Quarternion
    :type x: np.ndarray
    :param y: Y Quarternion
    :type y: np.ndarray
    :param z: Z Quarternion
    :type z: np.ndarray
    :return: Roll (phi), Pitch (Theta), Yaw (psi)
    """
    phi, theta, psi = np.array(np.zeros(len(w))), np.array(np.zeros(len(w))), np.array(np.zeros(len(w)))
    inc, azi = np.array(np.zeros(len(w))), np.array(np.zeros(len(w)))

    for i in range(0, len(w)):
        phi[i], theta[i], psi[i] = quarternion_to_euler(w[i], x[i], y[i], z[i])
        inc[i] = 90 + theta[i]
        if psi[i] > 0:
            azi[i] = psi[i]
        else:
            azi[i] = 360 + psi[i]
    return inc, azi


def euler_angles_array(w, x, y, z):
    """
    Calculates the Euler Angles from Quaternion for an entire array.

    :param w: W Quarternion
    :type w: np.ndarray
    :param x: X Quarternion
    :type x: np.ndarray
    :param y: Y Quarternion
    :type y: np.ndarray
    :param z: Z Quarternion
    :type z: np.ndarray
    :return: Roll (phi), Pitch (Theta), Yaw (psi)
    """

    phi, theta, psi = np.array(np.zeros(len(w))), np.array(np.zeros(len(w))), np.array(np.zeros(len(w)))

    for i in range(0, len(w)):
        phi[i], theta[i], psi[i] = quarternion_to_euler(w[i], x[i], y[i], z[i])

    return phi, theta, psi


def quarternion_to_euler(w, x, y, z, radians=False):
    """
    Calculates the polar coordinate angles from quarternion values.

    :param w: W Quarternion
    :type w: float
    :param x: X Quarternion
    :type x: float
    :param y: Y Quarternion
    :type y: float
    :param z: Z Quarternion
    :type z: float
    :param vertical_axis: The axis designated as the vertical axis. (x=1, y=2, z=3)
    :type vertical_axis: int
    :param radians: Return radians or degrees
    :type radians: bool
    :return: phi, theta, psi
    """

    phi = np.arctan2(2 * (w * x + y * z), 1 - 2 * (x ** 2 + y ** 2))
    theta = np.arcsin(2 * (w * y - x * z))
    psi = np.arctan2(2 * (w * z + x * y), 1 - 2 * (y ** 2 + z ** 2))

    if radians:
        return phi, theta, psi
    return units.from_si(phi, 'dega'), units.from_si(theta, 'dega'), units.from_si(psi, 'dega')


def plot_quarternion(t, w, x, y, z, a=False):
    fig = plt.figure()
    plt.plot(t, w, label='W')
    plt.plot(t, x, label='X')
    plt.plot(t, y, label='Y')
    plt.plot(t, z, label='Z')
    if isinstance(a, np.ndarray):
        plt.plot(t, a, label='Acc')
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Quarternion')
    axes = plt.gca()
    axes.set_ylim(-1, 1)
    plt.grid()
    plt.legend()


def plot_euler(t, phi, theta, psi):
    fig = plt.figure()
    plt.plot(t, phi, label='Roll')
    plt.plot(t, theta, label='Pitch')
    plt.plot(t, psi, label='Yaw')
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Angle, (deg)')
    axes = plt.gca()
    axes.set_ylim(-180, 180)
    axes.yaxis.set_major_locator(plt.MultipleLocator(30))
    plt.grid()
    plt.legend()


def plot_incazi(t, inclination, azimuth):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    line1 = ax1.plot(t, inclination, 'b', label='Inc')
    line2 = ax2.plot(t, azimuth, 'r', label='Azi')
    lines = line1 + line2
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc=0)

    ax1.axes.set_ylim(0, 180)
    ax1.yaxis.set_major_locator(plt.MultipleLocator(30))
    ax1.yaxis.set_minor_locator(plt.MultipleLocator(5))
    ax2.axes.set_ylim(0, 360)
    ax2.yaxis.set_major_locator(plt.MultipleLocator(60))
    ax2.yaxis.set_minor_locator(plt.MultipleLocator(10))
    ax1.grid()
    ax1.set_xlabel('Time (Seconds)')
    ax1.set_ylabel('Inclination, $\Theta$ (deg)')
    ax2.set_ylabel('Azimuth, $\phi$ (deg)')
