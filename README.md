## Bruker OPUS binary files reader
Python scripts in this project allow to read Bruker OPUS propriertary files. You can provide scripts with config file(example in conf/) to perform interpolation of spectra.

## Usage
You can run function brukeropusreader.opus_reader.opus reader to read opus file.

## Structure of OPUS files
OPUS file always consist of spectrum series. Each series is described by few parameters: NPT (number of points), FXV (value of first wavelength), LXV (value of last wavelength), END (address of spectra series).

This parameters can be found by searching for particular string in binary file(in ASCII). After founding occurence one have to move pointer few bytes further to read value.
It is not established how far forward pointer should be moved. We empirically checked that is is 12 for end and 8 for npt, fxv, lxv.
Beyond that, each file contains some metadata about hardware used for measurement.

## Controversies
Bruker OPUS is proprieratry file, therefore we don't know exactly what is its structure. We can just guess it. The main problem is - having few series how to decide which one is absorption spectra?
Our solution (empirically developd) is:
* Removed broken series (ones with fxv greater than lxv, without npt information, etc...)
* Filter out interferrograms - taken from https://github.com/philipp-baumann/simplerspec. Interferrograms have starting value 0. We don't need them.
* If after these two steps we still have more than one spectrum left we can choose one with highest average. We empirically checked that others are usually random noise with values near 0.


