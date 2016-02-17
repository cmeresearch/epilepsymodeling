import csv
import numpy as np
import PyOpenWorm as P
P.connect()

## Create a numpy array from the connectome csv file
with open('connectome.csv', 'rb') as connectomefile:
	readfile = np.genfromtxt(connectomefile, dtype = None, delimiter = ';', usecols = (0, 1))
	print readfile.shape
	for row in readfile:
		print row
