import numpy as np
from scipy.interpolate import interp1d


class OpusData(dict):
    def get_range(self, spec_name="AB", wavenums=True):
        param_key = f"{spec_name} Data Parameter"
        fxv = self[param_key]["FXV"]
        lxv = self[param_key]["LXV"]
        npt = self[param_key]["NPT"]
        x_no_unit = np.linspace(fxv, lxv, npt)
        if wavenums:
            return x_no_unit
        else:
            return 10_000_000 / x_no_unit

    def interpolate(self, start, stop, num, spec_name="AB"):
        xav = self.get_range(spec_name=spec_name)
        yav = self[spec_name]
        iwave_nums = np.linspace(start, stop, num)
        f2 = interp1d(xav, yav, kind="cubic", fill_value="extrapolate")
        return iwave_nums, f2(iwave_nums)
