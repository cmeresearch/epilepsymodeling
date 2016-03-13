import csv
import numpy as np
#import PyOpenWorm as P
#P.connect()

## This is the main neural network simulation script

## Read the output file from the csvreader script, and create dictionaries for looking up index values and neuron types

matrix_size = 1 	## This will be used to determine the size of the initial matrix of zeros
indexdict = {}
tpyesdict = {}

print 'Reading neuron names, numbers, and types...'

with open('n_output.csv', 'rb') as neuronfile:
	neuron_indices = np.genfromtxt(neuronfile, dtype = None, delimiter = ',', usecols = (0, 1))
	indexdict = {k1:v1 for k1,v1 in neuron_indices}
	matrix_size = len(neuron_indices)	## Determine size of neural net matrix

with open('n_output.csv', 'rb') as neuronfile:
	neuron_types = np.genfromtxt(neuronfile, dtype = None, delimiter = ',', usecols = (1, 2))
	typesdict = {k2:v2 for k2,v2 in neuron_types}

print 'Done'

## Generate an array of zeroes, with its dimensions being determined by the number of neurons

print 'Generating neural network...'

neuralnet = np.zeros((matrix_size, matrix_size), dtype = int)

## Plug in connection data, using the index and type dictionaries and connectome.csv

with open('connectome.csv', 'rb') as connectomefile:
	connectionarray = np.genfromtxt(connectomefile, dtype = None, delimiter = ';', usecols = (0, 1))
	for i in range(len(connectionarray)):
		presynaptic = connectionarray[i, 0]
		presynapticindex = indexdict.get(presynaptic)
		postsynaptic = connectionarray[i, 1]
		postsynapticindex = indexdict.get(postsynaptic)
		neuralnet[presynapticindex, postsynapticindex] = typesdict.get(presynapticindex)

print 'Done'
