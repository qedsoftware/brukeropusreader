import matplotlib.pyplot as plt
import csv
import numpy as np
from numpy import linalg
from scipy.interpolate import interp1d


class NoInterpolatedDataException(Exception):
    pass


class WrongWavelengthsInConf(Exception):
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
            dist = linalg.norm(y_r - self.interpolated_data[1], ord=1)
            print("L1 distance between rbart and python versions:", dist)
            plt.plot(x_r, y_r, 'bo')
            plt.plot(self.interpolated_data[0],
                     self.interpolated_data[1],
                     'ro')
            plt.show()

    def gen_interp_waves(self, conf):
        wunit = (conf.wave_start - conf.wave_end) / (float(conf.iwsize - 1))
        a = conf.wave_start + wunit
        iwavenumber = [0] * conf.iwsize
        for i in range(len(iwavenumber)):
            a -= wunit
            iwavenumber[i] = a
        return iwavenumber

    def interpolate_spectra(self, conf):
        xav, yav = self.raw_data[0], self.raw_data[1]
        ab_wavenumbers = self.raw_data[0]
        iwavenumber = self.gen_interp_waves(conf)

        xa_min = min(ab_wavenumbers)
        xa_max = max(ab_wavenumbers)
        n_interp = conf.iwsize
        yi = []

        f2 = interp1d(xav, yav, kind='cubic', assume_sorted=True)

        for k in range(n_interp):
            if iwavenumber[k] < xa_min:
                if k == n_interp - 1:
                    yi.append(yav[0])
                else:
                    print("Wrong wavelengths for interpolating data")
            elif iwavenumber[k] > xa_max:
                if k == 0:
                    yi.append(yav[-1])
                else:
                    raise WrongWavelengthsInConf()
            else:
                yi.append(f2(iwavenumber[k]))
        return iwavenumber, yi
