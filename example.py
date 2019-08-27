import argparse
import sys

from brukeropusreader import read_file


def main(path_to_file):
    print(f"Reading opus file from path" f"{path_to_file}")
    opus_data = read_file(path_to_file)

    print(f"Data fields: " f"{list(opus_data.keys())}")

    ab_x = opus_data.get_range("AB")
    print(f"Absorption spectrum range: " f"{ab_x[0]} {ab_x[-1]}")
    print(f"Absorption elements num: " f'{len(opus_data["AB"])}')

    try:
        import matplotlib.pyplot as plt

        print("Plotting AB")
        plt.plot(opus_data.get_range("AB"), opus_data["AB"])
        plt.show()

        print("Plotting interpolated AB")
        plt.plot(*opus_data.interpolate(ab_x[0], ab_x[-1], 100))
        plt.show()

    except ImportError:
        print(f"Install matplotlib to plot spectra")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("opus_path", help="Path to opus file", action="store")
    args = parser.parse_args()
    main(sys.argv[1])
