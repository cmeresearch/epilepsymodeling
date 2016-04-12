import csv
import numpy as np
import bisect as b

## This file is the main neural network simulation script

## Neuron base class

class Neuron:
    def __init__(self):
        self.refractory = False
        self.inputsum = 0

## Refractory period will be 5, delta time added on firing will be 3, duration of signal will be 10

## Main simulation class

class Simulator:
    def __init__(self, numneurons):
        self.neuralnet = np.zeros((numneurons, numneurons), dtype = int)
        self.clock = 0
        self.neuronarray = []
        self.queue = sorted()       ## (simulation time, eventID, target neuron, signal)
    def fireneuron(self, numneurons, neuronindex):
#        for i in range(numneurons):
        for i in range(numneurons):
            if self.neuralnet[neuronindex][i] != 0:
                b.insort_left(queue, (clock + 3, 1, i, self.neuralnet[neuronindex][i]))
                b.insort_left(queue, (clock + 3 + 10, 2, i, self.neuralnet[neuronindex][i]))
        simlog = simulationevents.txt
        simlog.write(neuronindex)
        simlog.write('\n')
        self.neuronarray[neuronindex].refractory = True
        self.neuronarray[neuronindex].inputsum = 0
        b.insort_left(queue, (clock + 5, 3, neuronindex, 0))
    def startsignal(self, neuronindex, signal):
        n = Neuron(self.neuronarray[neuronindex])
        n.inputsum = n.inputsum + signal
        if (n.refractory = False and n,inputsum > 0):
            fireneuron(neuronindex)
    def endsignal(self, neuronindex, signal):
        n = Neuron(self.neuronarray[neuronindex])
        n.inputsum = n.inputsum - signal
        if (n.inrefractory = False and inputsum > 0):
            fireneuron(neuronindex)
    def exitrefractory(self, neuronindex):
        n = Neuron(self.neuronarray[neuronindex])
        n.refractory = False
        if n.inputsum > 0:
            fireneuron(neuronindex)

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

sim = Simulator(matrix_size)

#neuralnet = np.zeros((matrix_size, matrix_size), dtype = int)

## Plug in connection data, using the index and type dictionaries and connectome.csv

with open('connectome.csv', 'rb') as connectomefile:
    connectionarray = np.genfromtxt(connectomefile, dtype = None, delimiter = ';', usecols = (0, 1))
    for i in range(len(connectionarray)):
        presynaptic = connectionarray[i, 0]
        presynapticindex = indexdict.get(presynaptic)
        postsynaptic = connectionarray[i, 1]
        postsynapticindex = indexdict.get(postsynaptic)
        sim.neuralnet[presynapticindex, postsynapticindex] = typesdict.get(presynapticindex)

print 'Done'
