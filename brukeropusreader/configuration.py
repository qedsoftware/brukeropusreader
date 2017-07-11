from configparser import ConfigParser


class Config(object):
    def __init__(self, wave_start=None, wave_end=None, wave_size=None):
        self.wave_start = wave_start
        self.wave_end = wave_end
        self.iwsize = wave_size

    @staticmethod
    def read_conf_from_file(path):
        config = ConfigParser()
        config.read(path)
        wave_start = float(config.get('mpa', 'start_wn'))
        wave_end = float(config.get('mpa', 'end_wn'))
        wave_size = int(config.get('mpa', 'num_wn'))
        return Config(wave_start, wave_end, wave_size)
