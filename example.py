from brukeropusreader import read_file

import sys
import argparse
import matplotlib.pyplot as plt


def main(path_to_file):
    print(f'Reading opus file from path'
          f'{path_to_file}')
    opus_data = read_file(path_to_file)

    print(f'Dimension of data: '
          f'{len(opus_data.wave_nums)}')

    print(f'Spectrum range: ['
          f'{min(opus_data.spectrum)}; '
          f'{max(opus_data.spectrum)}]')

    print(f'Metadata: '
          f'{opus_data.meta}')

    plt.plot(opus_data.wave_nums, opus_data.spectrum)
    plt.title(f'Spectrum {path_to_file}')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("opus_path",
                        help="Path to opus file",
                        action="store")
    args = parser.parse_args()
    main(sys.argv[1])
