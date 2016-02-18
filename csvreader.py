import csv
import numpy as np
import PyOpenWorm as P
P.connect()

## Create a numpy array from the connectome csv file
## (Delimiter param may have to be changed to match csv if using outside csv source)

with open('connectome.csv', 'rb') as connectomefile:
	readfile = np.genfromtxt(connectomefile, dtype = None, delimiter = ';', usecols = (0, 1))


## Find all unique neuron names in that array, assign numerical values to them,
## then save them to a file called n_output.csv
## To do: Allow custom filenames, or at least append time and date to this filename

neuron_names = np.unique(readfile)

print 'Writing n_output.csv...'

with open('n_output.csv', 'w') as nameswritefile:
        for v,k in enumerate(neuron_names):
                nameswritefile.write(k)
                nameswritefile.write(',')
                nameswritefile.write("%i\n" % (v))

print 'Done'


## Generate a matrix from that same array and save that matrix as a csv
