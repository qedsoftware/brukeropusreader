import numpy as np
from struct import unpack_from
from .utils import find_all
from .opus_data import OpusData
from itertools import product


class NoAbsorbanceSpectra(Exception):
    pass


def read_file(filepath):
    with open(filepath, 'rb') as f:
        buff = f.read()

    # Reading all waves and spectra
    fxv_spc, spc, wavenumbers = read_all_spectra(buff)
    # Choose best ab spectra
    ab_spectra, ab_wavenumbers = choose_ab(fxv_spc, spc, wavenumbers)

    wave_num_abs_pair = reversed(list(zip(ab_wavenumbers, ab_spectra)))

    meta = get_metadata(buff)

    wave_nums, spectrum = list(zip(*wave_num_abs_pair))

    return OpusData(wave_nums, spectrum, meta=meta)


def choose_ab(fxv_spc, spc, wavenumbers):
    # Removing interferograms
    which_ig = np.where(fxv_spc == 0)[0]
    not_ig = np.setdiff1d(range(len(fxv_spc)), which_ig)

    # Removing single channel spectra
    # (heuristics are empirically derived)
    ab = []
    for x in not_ig:
        if np.average(spc[x]) > 0.25:
            ab.append(x)
    if len(ab) > 1:
        spc_avg = [np.average(spc[x]) for x in ab]
        max_avg_index = spc_avg.index(max(spc_avg))
        ab_p = ab[max_avg_index]
    elif len(ab) == 1:
        ab_p = ab[0]
    else:
        raise NoAbsorbanceSpectra()

    ab_spectra = spc[ab_p]
    ab_wavenumbers = wavenumbers[ab[0]]
    return ab_spectra, ab_wavenumbers


def keyword_positions(buff):
    end = np.array(list(find_all(b'END', buff))) + 12
    npt_all = np.array(list(find_all(b'NPT', buff))) + 8
    fxv_all = np.array(list(find_all(b'FXV', buff))) + 8
    lxv_all = np.array(list(find_all(b'LXV', buff))) + 8
    return end, npt_all, fxv_all, lxv_all


def filter_unpaired(fxv_all, lxv_all):
    if len(fxv_all) != len(lxv_all):
        prod = product(fxv_all, lxv_all)
        corr_adr = list(zip(*filter(lambda d: (d[1] - d[0]) == 16, prod)))
        fxv_all = np.array(corr_adr[0])
        lxv_all = np.array(corr_adr[1])
    return fxv_all, lxv_all


def read_all_spectra(buff):
    end, npt_all, fxv_all, lxv_all = keyword_positions(buff)
    fxv_all, lxv_all = filter_unpaired(fxv_all, lxv_all)

    # Number of wavepoints
    npt = [unpack_from('<i', buff, adr)[0] for adr in npt_all]
    # 'end_spc is vector of offsets where spectra start'
    end_spc = end[np.where(np.diff(end) > 4 * min(npt))]
    spc_param_list = {'npt': npt_all, 'fxv': fxv_all, 'lxv': lxv_all}

    # Filtering some corrupted series
    param_spc = filter_spc_params(end_spc, spc_param_list, npt_all)
    # Number of points in correct spectra
    npt_spc = [unpack_from('<i', buff, adr)[0] for adr in param_spc['npt']]
    npt_spc = np.array(npt_spc)

    mask = npt_spc > 0
    for key in param_spc.keys():
        param_spc[key] = param_spc[key][mask]
    npt_spc = npt_spc[mask]

    def read_spec(x):
        return np.array(unpack_from('<' + str(x[1]) + 'f', buff, x[0] - 4))

    def read_waves(x):
        return unpack_from('<2d', buff, x)[0]

    spc = list(map(read_spec, zip(param_spc['end'], npt_spc)))
    fxv_spc = np.array([read_waves(x) for x in param_spc['fxv']])
    lxv_spc = [unpack_from('<2d', buff, x)[0] for x in param_spc['lxv']]
    wavenumbers = generate_wavelengths(lxv_spc, fxv_spc, npt_spc)

    return fxv_spc, spc, wavenumbers


def generate_wavelengths(lxv_spc, fxv_spc, npt_spc):
    wavenumbers = []
    for lx, fx, npt1 in zip(lxv_spc, fxv_spc, npt_spc):
        ratio = (fx - lx) / (npt1 - 1)
        arr = np.flipud(np.arange(lx, fx + ratio, ratio))
        wavenumbers.append(arr)
    return wavenumbers


def find_key(buff, key):
    hit = buff.find(key) + 8
    value = unpack_from('2000s', buff, hit)[0]
    value = value[:value.find(b'\x00')]
    return value


def get_metadata(buff):
    meta = {}
    all_keys = ['INS', 'SRC', 'DAT', 'SNM', 'TIM', 'SFM']
    for k in all_keys:
        keystr = k
        value = find_key(buff, keystr.encode('utf-8'))
        meta[k] = value
    return meta


def filter_spc_params(end_spc, spc_param_list, npt_all):
    def indexes_of_valid_series(arr):
        return list(arr).index(min(filter(lambda x: x > 0, arr)))
    new_end = []
    new_fxv = []
    new_lxv = []
    fxv_spc = spc_param_list['fxv']
    lxv_spc = spc_param_list['lxv']
    for npy in npt_all:
        end_diff = npy - end_spc
        lxv_diff = lxv_spc - npy
        fxv_diff = fxv_spc - npy
        lxv_tmp = indexes_of_valid_series(lxv_diff)
        fxv_tmp = indexes_of_valid_series(fxv_diff)
        end_tmp = indexes_of_valid_series(end_diff)
        new_end.append(end_spc[end_tmp])
        new_fxv.append(fxv_spc[fxv_tmp])
        new_lxv.append(lxv_spc[lxv_tmp])
    spc_param_list['end'] = np.array(new_end)
    spc_param_list['lxv'] = np.array(new_lxv)
    spc_param_list['fxv'] = np.array(new_fxv)

    return spc_param_list
