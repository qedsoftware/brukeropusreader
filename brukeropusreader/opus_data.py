import csv
import numpy as np
from numpy import linalg
from scipy.interpolate import interp1d


class OpusData(object):
    def __init__(self, raw_data, interp=None, meta=None):
        self.raw_data = raw_data
        self.interpolated_data = interp
        self.meta = meta

    def compare_with(self, file_path):
        with open(file_path, 'rb') as csv_file:
            csv_reader = csv.reader(csv_file)
            y_r = np.array(map(lambda x: float(x), next(csv_reader)[2:]))
            dist = linalg.norm(y_r - self.raw_data[1], ord=1)
            print("L1 distance between series:", dist)

    def interpolate(self, start, stop, num):
        xav, yav = self.raw_data[0], self.raw_data[1]
        iwavenumber = np.linspace(start,
                                  stop,
                                  num)
        f2 = interp1d(xav, yav,
                      kind='cubic',
                      assume_sorted=True,
                      fill_value='extrapolate')
        return iwavenumber, f2(iwavenumber)
