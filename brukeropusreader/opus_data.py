import matplotlib.pyplot as plt
import csv
import numpy as np
from numpy import linalg


class NoInterpolatedDataException(Exception):
    pass


class OpusData(object):
    def __init__(self, raw_data, interp=None, meta=None):
        self.raw_data = raw_data
        self.interpolated_data = interp
        self.meta = meta

    def plot_raw(self):
        plt.plot(self.raw_data[0], self.raw_data[1], 'o', markeredgewidth=1,
                 markeredgecolor='r', markerfacecolor='None')
        plt.show()

    def plot_interpolated(self):
        if self.interpolated_data:
            plt.plot(self.interpolated_data[0], self.interpolated_data[1], 'o')
            plt.show()
        else:
            raise NoInterpolatedDataException()

    def plot_data(self):
        plt.plot(self.raw_data[0], self.raw_data[1], 'bo')
        if self.interpolated_data:
            plt.plot(self.interpolated_data[0],
                     self.interpolated_data[1],
                     'ro')
        plt.show()

    def compare_with(self, file_path):
        with open(file_path, 'rb') as csv_file:
            csv_reader = csv.reader(csv_file)
            x_r = np.array(map(lambda x: float(x[1:]), next(csv_reader)[2:]))
            y_r = np.array(map(lambda x: float(x), next(csv_reader)[2:]))
            dist = linalg.norm(y_r-self.interpolated_data[1], ord=1)
            print "L1 distance between rbart and python versions:", dist
            plt.plot(x_r, y_r, 'bo')
            plt.plot(self.interpolated_data[0],
                     self.interpolated_data[1],
                     'ro')
            plt.show()
