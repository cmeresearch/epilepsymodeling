import csv
import numpy as np
import bisect as b
import random
from datetime import datetime

## This file is the main neural network simulation script
## Refractory period will be 5, delta time added on firing will be 3, duration of signal will be 10
## Queue entries are (simulation time, eventID, target neuron, signal)

## Neuron base class

class Neuron:
    def __init__(self):
        self.refractory = False
        self.inputsum = 0

## Main simulation class

class Simulator:
    def __init__(self, numneurons):
        self.numberofneurons = numneurons
        self.timestamp = datetime.now().strftime('%m-%d-%Y - %H-%M-%S')
        self.neuralnet = np.zeros((numneurons, numneurons), dtype = int)
        self.clock = 0
        self.neuronarray = [Neuron() for i in range(numneurons)]
        self.queue = []
        self.simlog = open('simulationevents ' + self.timestamp + '.txt', 'w')
    def fireneuron(self, numneurons, neuronindex):
        for i in range(numneurons):
            if self.neuralnet[neuronindex][i] != 0:
                b.insort_right(self.queue, (self.clock + 3, 1, i, self.neuralnet[neuronindex][i]))
                b.insort_right(self.queue, (self.clock + 3 + 10, 2, i, self.neuralnet[neuronindex][i]))
        self.simlog.write('%i' % (neuronindex))
        self.simlog.write(', at simulation time ')
        self.simlog.write('%i' % (self.clock))
        self.simlog.write('\n')
        self.neuronarray[neuronindex].refractory = True
        self.neuronarray[neuronindex].inputsum = 0
        b.insort_right(self.queue, (self.clock + 5, 3, neuronindex, 0))
    def startsignal(self, neuronindex, signal):
        n = self.neuronarray[neuronindex]
        n.inputsum = n.inputsum + signal
        if (n.refractory == False and n.inputsum > 0):
            self.fireneuron(self.numberofneurons, neuronindex)
    def endsignal(self, neuronindex, signal):
        n = self.neuronarray[neuronindex]
        n.inputsum = n.inputsum - signal
        if (n.refractory == False and n.inputsum > 0):
            self.fireneuron(self.numberofneurons, neuronindex)
    def exitrefractory(self, neuronindex):
        n = self.neuronarray[neuronindex]
        n.refractory = False
        if n.inputsum > 0:
            self.fireneuron(self.numberofneurons, neuronindex)

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

print 'Generating neural network...'

## Create an instance of the Simulator class

sim = Simulator(matrix_size)

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

## To do: Prompt the user for max simulation duration and how many neurons to fire initially
## Current code should do this in theory, but Atom doesn't accept user input. Running in N++ or IDLE should allow uncommenting these input lines

#maxcount = int(input('Enter maximum simulation cycles: '))

maxcount = 100

print 'Maximum sim cycles set to ' + str(maxcount)

#initialneurons = int(input('How many neurons do you want to fire at simulation start? '))

initialneurons = 5

sim.simlog.write('Max sim cycles set to ')
sim.simlog.write('%i' % (maxcount))
sim.simlog.write('\n')
sim.simlog.write('Initializing by firing ')
sim.simlog.write('%i' % (initialneurons))
sim.simlog.write(' neurons')
sim.simlog.write('\n')

## Populate the queue with an initial set of randomized firing events, set the cycle counter to 0, and begin running the simulation

for i in range(initialneurons):
    sim.fireneuron(matrix_size, random.randrange(matrix_size))

count = 0

print 'Beginning simulation by firing ' + str(initialneurons) + ' neurons'

## Simulation will stop running when we have either reached the user-specified maximum number of cycles or there are no more events in the queue

while (count < maxcount and len(sim.queue) > 0):
    count += 1
    currentevent = sim.queue.pop(0)
    sim.clock = currentevent[0]
    if currentevent[1] == 1:
        sim.startsignal(currentevent[2], currentevent[3])
    elif currentevent[1] == 2:
        sim.endsignal(currentevent[2], currentevent[3])
    elif currentevent[1] == 3:
        sim.exitrefractory(currentevent[2])
    else:
        print 'Something has gone wrong during simulation'
        sim.simlog.close()

sim.simlog.close()

print 'Simulation has finished running. Please see output file simulationevents.txt for a log of which neurons fired'
