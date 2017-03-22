#!/usr/bin/env python
import laspy, laspy.file
import numpy as np
import os, glob

def clip(coordinats, extend):
    """Clip point to extend
    :param coordinats: Array Vstack [x, y] [m]
    :type coords2d: float
    :param value: Array of values for feature calculation (z, intensity, linearitiy etc...)
    :type value: float
    :param extend: Array [minX minY, maxX maxY]
    :type extend: float
    :param label: By default create features for learning samples, if you pas Labels it creates training data
    :type label: int
    """
    xmin = extend[0, 0]
    ymin = extend[0, 1]
    xmax = extend[1, 0]
    ymax = extend[1, 1]

    coordinats = coordinats[coordinats[:, 0] < xmax]
    coordinats = coordinats[coordinats[:, 0] > xmin]
    coordinats = coordinats[coordinats[:, 1] < ymax]
    coordinats = coordinats[coordinats[:, 1] > ymin]

    return coordinats


def save_npy(featureset):
    np.save(path + filename + '.npy', featureset)

def downsample(points_length, sampling_rate):
    n = np.prod(points_length)
    x = np.fromstring(np.random.bytes(n), np.uint8, n)
    return (x < 255 * sampling_rate).reshape(points_length)

def keep_all_label(points, keep_label):
    return np.array([points == keep_label]).reshape(len(points))

def get_extend(las):
    e = np.array([[las.header.min[0], las.header.min[1]],
                 [las.header.max[0], las.header.max[1]]])
    return e

def get_list_of_las(directory):
    os.chdir(directory)
    return glob.glob("*.las")

########################################################
#            TROLOLO                                   #
########################################################
if __name__ == '__main__':

    filename = 'Hangar'
    sampling_rate = 0.1
    noise = 1 #Noise up to one unit (one meter)

    lasin = laspy.file.File(filename + '.las', mode='r')
    lasout = laspy.file.File(filename + "_randomize.las", mode = "w", header = lasin.header)
    pointsin = np.vstack((lasin.x, lasin.y, lasin.z)).transpose()

    extend = np.array([[lasin.header.min[0], lasin.header.min[1]],
                    [lasin.header.max[0], lasin.header.max[1]]])

    n_points = len(lasin.x)

    randomX = np.random.uniform(0, noise, size=n_points)
    randomY = np.random.uniform(0, noise, size=n_points)
    randomZ = np.random.uniform(0, noise, size=n_points)

    lasout.x = lasin.x + randomX
    lasout.y = lasin.y + randomY
    lasout.z = lasin.z + randomZ

    lasout.close()




