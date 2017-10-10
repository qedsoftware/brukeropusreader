from brukeropusreader.opus_reader import opus_reader
from os import walk
import os
import sys


def filter_fun(nm):
    return (nm[0] != '.') and (nm[-2:] in ('.0', '.1', '.2', '.3'))


def main(path_to_opus_files):
    i = 0
    all_files = 0
    for path, subdirs, files in walk(path_to_opus_files):
        for name in filter(filter_fun, files):
            all_files += 1
            try:
                od = opus_reader(os.path.join(path, name))
                od.plot_raw()
            except Exception as e:
                i += 1
                print i, ":", name, str(e)


if __name__ == '__main__':
    main(sys.argv[1])
