import csv
import numpy as np
import random

## Create a numpy array from the connectome csv file
## Delimiter and usecols params may have to be changed to match csv if using outside csv source

print 'Reading connectome file...'

with open('connectome.csv', 'rb') as connectomefile:
	namesreadfile = np.genfromtxt(connectomefile, dtype = None, delimiter = ';', usecols = (0, 1))

	print 'Done'

## Find all unique neuron names in that array, assign numerical values to them, assign random types (excitatory or inhibitory) to them, then save them to a file called n_output.csv. Currently randomizes equally between excitatory and inhibitory

neuron_names = np.unique(namesreadfile)

print 'Writing n_output.csv...'

with open('n_output.csv', 'w') as nameswritefile:
	for v,k in enumerate(neuron_names):
		nameswritefile.write(k)
		nameswritefile.write(',')
		nameswritefile.write('%i,' % (v))
		neurontype = random.sample([-1, 1], 1)
		nameswritefile.write('%i' % (neurontype[0]))
		nameswritefile.write('\n')

print 'Done'

## To do: Prompt user for i/e ratio or seed, which can then be appended to the filename, potentially along with time and date

## Below are code snippets that may be useful for future implementation of reading neuron types from the original connectome.csv

#typesreadfile = np.genfromtxt(connectomefile, dtype = None, delimiter = ';', usecols = (0, 4))
