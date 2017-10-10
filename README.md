# Bruker OPUS Reader

## Introduction
The Python scripts in this project enable the reading of Bruker OPUS files.

## Usage
Run the function brukeropusreader.opus_reader.opus_reader to read OPUS files.

## Structure of OPUS files
OPUS files consist of several spectrum series. 
Each series is described by a few parameters: 

- NPT (number of points)
- FXV (value of first wavelength)
- LXV (value of last wavelength)
- END (address of spectra series)

This parameters are found by searching for ASCII strings in the binary files.
After finding a match, we must move the pointer a few bytes further to read values.
There is not a standard describing how much further the pointer should be moved. 
We empirically checked that it is 12 bytes for END and 8 for NPT, FXV, and LXV.
In addition, each file contains some metadata about the hardware used for measurement.

## Controversies
Bruker OPUS is a proprietary file format, so we do not know its structure exactly.
One problem is, given only a few series, how to decide which are absorption spectra?
Our solution (empirically developed) is:

1. Remove broken series (ones with FXV > LXV, missing NPT information, etc.)
2. Remove interferograms. (See https://github.com/philipp-baumann/simplerspec) Interferrograms have a starting value of 0.
3. If after these two steps we still have more than one series left, we can choose the one with the highest average value. We empirically checked that other series are usually random noise with values near 0.


## Contact
For developer issues, please start a ticket in Github. 
You can also write to the dev team directly at bruker-opus-reader-dev@qed.ai. 
For other issues, please write to: bruker-opus-reader@qed.ai

--
QED | https://qed.ai
