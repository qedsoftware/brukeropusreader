#!/usr/bin/python3

#This requires python 3, and brukeropusreader, which can be installed with pip3 install brukeropusreader (or sometimes just pip install...)
# but to be sure it's up to date, get it from https://github.com/qedsoftware/brukeropusreader


from brukeropusreader import read_file
from brukeropusreader import parse_sm

import matplotlib.pyplot as plt
import numpy as np
import glob
import sys
import os 

plot=False



def ProcessFile(filename):
	opus_data = read_file(filename)
	SC_X=opus_data.get_range("ScSm")
	IG_X=opus_data.get_range("IgSm")
	ScSm=parse_sm(opus_data)
	IgSm=parse_sm(opus_data,"IgSm")
	format_Ig=["%d"]
	format_Ig.extend(["%.8e"]*np.shape(IgSm)[1])
	format_Sc="%.8e"
	print (format_Ig)
	print(format_Sc)
	print (ScSm)

	np.savetxt(filename+"IG.txt",np.c_[IG_X,IgSm], fmt=format_Ig)
	np.savetxt(filename+"SC.txt",np.c_[SC_X,ScSm], fmt=format_Sc)
	
	if plot:
		plt.plot(SC_X,ScSm[:,0])
		plt.show()
		plt.plot(IG_X,IgSm[:,0])
		plt.show()

for arg in sys.argv:
	if arg.lower().find('plot')>=0:
		plot=True
	elif len(arg.lower())>=1 :
		InputFileName=arg
print (InputFileName)		
if InputFileName.find("*")>=0 or InputFileName.find("?")>=0:#called with wildcards
	InputFileName=os.path.join(os.getcwd(),InputFileName)
	for InputFile in glob.glob(InputFileName):
		print ("Globbed input: loading file "+InputFile)
		
		ProcessFile(InputFile)
else:
	InputFile=InputFileName
	print ("Loading file "+InputFile)	
	ProcessFile(InputFile)		