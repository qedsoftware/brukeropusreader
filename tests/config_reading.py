from unittest import TestCase, main
from brukeropusreader.configuration import Config
from configparser import NoSectionError


class ConfigurationTest(TestCase):

    def test_loading_file(self):
        try:
            self.data = Config.read_conf_from_file("../conf/opus.conf")
        except NoSectionError:
            self.fail("Cannot load configuration file")

    def test_correct_max_wave(self):
        self.assertEqual(self.data.wave_start, 12489.456160)

    def test_correct_min_wave(self):
        self.assertEqual(self.data.wave_end, 3594.86)

    def test_correct_wave_len(self):
        self.assertEqual(self.data.iwsize, 1154)


if __name__ == '__main__':
    main()
