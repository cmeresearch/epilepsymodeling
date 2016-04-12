## Deprecated, since the class ends up being four lines long. Not worth importing separately. Left for my own reference and testing.

class Neuron:
    def __init__(self):
        self.inrefractory = False
        self.inputsum = 0
    def incrementinputsum(self):
        self.inputsum = self.inputsum + 1
        return self.inputsum

x = Neuron()
y = Neuron()

x.inrefractory = True

print x.incrementinputsum()
