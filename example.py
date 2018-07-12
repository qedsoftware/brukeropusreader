from brukeropusreader import opus_reader

import sys
import argparse


def main(path_to_file):
    od = opus_reader(path_to_file)
    print(od.raw_data[1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("opus_path",
                        help="Path to opus file",
                        action="store")
    args = parser.parse_args()
    main(sys.argv[1])
