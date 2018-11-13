import numpy as np
from scipy.interpolate import interp1d


class OpusData:
    def __init__(self, wave_nums, spectrum, meta=None):
        self.wave_nums = wave_nums
        self.spectrum = spectrum
        self.meta = meta

    def interpolate(self, start, stop, num):
        xav, yav = self.wave_nums, self.spectrum
        iwave_nums = np.linspace(start,
                                 stop,
                                 num)
        f2 = interp1d(xav, yav,
                      kind='cubic',
                      assume_sorted=True,
                      fill_value='extrapolate')
        return iwave_nums, f2(iwave_nums)
