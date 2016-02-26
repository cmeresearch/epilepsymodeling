import csv
import numpy as np
import PyOpenWorm as P
P.connect()

## This is the main neural network simulation script

## Read the output file from the csvreader script, and generate the neural network matrix from that csv file

print 'Reading neuron names, numbers, and types...'

with open('n_output.csv', 'rb') as neuronfile:
	neural_net = np.genfromtxt(neuronfile, dtype = None, delimiter = ',')

print neural_net

print 'Done'
