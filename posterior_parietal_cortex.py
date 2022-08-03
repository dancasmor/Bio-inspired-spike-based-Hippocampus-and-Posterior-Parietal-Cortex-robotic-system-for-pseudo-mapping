
import spynnaker8 as sim
import matplotlib.pyplot as plt
import sys

class PPC:
    def __init__(self, ReadINLayer, ComparisonINLayer, OLayer, numCommands, operationDelay, initialDelay, sim):
        """Constructor method
        """
        # Storing parameters
        self.ReadINLayer = ReadINLayer
        self.ComparisonINLayer = ComparisonINLayer
        self.OLayer = OLayer
        self.sim = sim
        self.numCommands = numCommands
        self.operationDelay = operationDelay
        self.initialDelay = initialDelay

        # Create the network
        self.create_population()
        self.create_synapses()


    def create_population(self):
        """Create all populations of the memory model

                    :returns:
                """
        # Define neurons parameters
        self.neuronParameters = {"cm": 0.27, "i_offset": 0.0, "tau_m": 3.0, "tau_refrac": 1.0, "tau_syn_E": 0.3, "tau_syn_I": 0.3,
                                     "v_reset": -60.0, "v_rest": -60.0, "v_thresh": -57.0}
        # ReadLayer
        self.ReadLayer = self.sim.Population(1, self.sim.IF_curr_exp(**self.neuronParameters), label="ReadLayer")

        # DelayLayer
        self.DelayLayer = self.sim.Population(self.numCommands, self.sim.IF_curr_exp(**self.neuronParameters), label="DelayLayer")

        # ComparisonLayer
        self.ComparisonLayer = self.sim.Population(self.numCommands, self.sim.IF_curr_exp(**self.neuronParameters), label="ComparisonLayer")

        # InhLayer
        self.InhLayer = self.sim.Population(1, self.sim.IF_curr_exp(**self.neuronParameters), label="InhLayer")


    def create_synapses(self):
        """Create all synapses of the memory model

                    :returns:
                """
        # ReadINLayer-ReadLayer -> 1 to 1, excitatory and static
        self.ReadINL_ReadL = self.sim.Projection(self.ReadINLayer, self.ReadLayer, self.sim.OneToOneConnector(),
            synapse_type=self.sim.StaticSynapse(weight=6, delay=1.0), receptor_type="excitatory")

        # ReadLayer-DelayLayer -> 1 to 1 (first neuron), excitatory and static
        self.ReadL_DelayL = self.sim.Projection(self.ReadLayer, self.sim.PopulationView(self.DelayLayer, [0]), self.sim.OneToOneConnector(),
                                                 synapse_type=self.sim.StaticSynapse(weight=6.0, delay=self.initialDelay),
                                                 receptor_type="excitatory")

        # DelayLayer-DelayLayer -> 1 to 1 (i -> i+1), excitatory and static
        for neuronId in range(self.numCommands-1):
            self.sim.Projection(self.sim.PopulationView(self.DelayLayer, [neuronId]), self.sim.PopulationView(self.DelayLayer, [neuronId+1]),
                                self.sim.OneToOneConnector(),synapse_type=self.sim.StaticSynapse(weight=6.0, delay=self.operationDelay),
                                receptor_type="excitatory")

        # DelayLayer-ComparisonLayer -> 1 to 1, excitatory and static
        self.DelayL_ComparisonL = self.sim.Projection(self.DelayLayer, self.ComparisonLayer, self.sim.OneToOneConnector(),
                                                 synapse_type=self.sim.StaticSynapse(weight=2.5, delay=1.0),
                                                 receptor_type="excitatory")

        # ComparisonINLayer-ComparisonLayer -> all to 1 (for each), excitatory and static
        for neuronId in range(self.numCommands):
            self.sim.Projection(self.ComparisonINLayer, self.sim.PopulationView(self.ComparisonLayer, [neuronId]),
                                self.sim.AllToAllConnector(allow_self_connections=True),
                                synapse_type=self.sim.StaticSynapse(weight=2.5, delay=1.0),
                                receptor_type="excitatory")

        # ComparisonLayer-OLayer -> 1 to 1, excitatory and static
        self.ComparisonL_OL = self.sim.Projection(self.ComparisonLayer, self.OLayer,
                                                      self.sim.OneToOneConnector(),
                                                      synapse_type=self.sim.StaticSynapse(weight=6.0, delay=1.0),
                                                      receptor_type="excitatory")

        # DelayLayer-InhLayer
        self.DelayL_InhL = self.sim.Projection(self.sim.PopulationView(self.DelayLayer, [self.numCommands-1]), self.InhLayer,
                                                        self.sim.OneToOneConnector(),
                                                        synapse_type=self.sim.StaticSynapse(weight=6.0,
                                                                                            delay=1.0),
                                                        receptor_type="excitatory")

        # InhLayer-ComparisonLayer
        self.InhL_ComparisonL = self.sim.Projection(self.InhLayer, self.ComparisonLayer,
                                                  self.sim.AllToAllConnector(),
                                                  synapse_type=self.sim.StaticSynapse(weight=6.0, delay=1.0),
                                                  receptor_type="inhibitory")


"""
Test: 
    - Module: Creation of a ppc for the mapping of 4 commands in time after the activation of the read signal with two possible command activation signals.
    - Input: 4 readings operations are taken, activating a different command for each reading. For this, an inter-operation time of 7 ms and initial operation
            delay of 9 is used.
        If reading operation begin in ms = 1, the input comp spikes will have to arrive in ms:
        1) 11
        2) 18
        3) 25
        4) 32
"""


def test():
    inputReadSpikes = [1, 51, 101, 151]
    inputCompSpikes = [[11, 68, 125, 182], []]
    simTime = 200
    operationDelay = 7
    initialDelay = 9

    ######################################
    # Simulation parameters
    ######################################
    # Setup simulation
    sim.setup(1.0)

    ######################################
    # Create network
    ######################################
    # Neuron model parameters
    neuronParameters = {"cm": 0.27, "i_offset": 0.0, "tau_m": 3.0, "tau_refrac": 1.0, "tau_syn_E": 0.3,
                        "tau_syn_I": 0.3,
                        "v_reset": -60.0, "v_rest": -60.0, "v_thresh": -57.5}

    # Input layers
    #  + Read IN
    ReadINLayer = sim.Population(1, sim.SpikeSourceArray(spike_times=inputReadSpikes), label="ReadINLayer")
    #  + Comparison IN
    ComparisonINLayer = sim.Population(2, sim.SpikeSourceArray(spike_times=inputCompSpikes), label="ReadINLayer")

    # Output layer: fire a spike when receive a spike
    OLayer = sim.Population(4, sim.IF_curr_exp(**neuronParameters), label="OLayer")

    # PPC
    ppc = PPC(ReadINLayer, ComparisonINLayer, OLayer, 4, operationDelay, initialDelay, sim)

    ######################################
    # Parameters to store
    ######################################
    OLayer.record(["spikes"])
    ppc.DelayLayer.record(["spikes"])
    ppc.ComparisonLayer.record(["spikes"])
    ppc.InhLayer.record(["spikes"])

    ######################################
    # Execute the simulation
    ######################################
    sim.run(simTime)

    # Get data from:
    #  + Output
    OLData = OLayer.get_data(variables=["spikes"])
    spikesOut = OLData.segments[0].spiketrains
    formatSpikesOut = []
    for neuron in spikesOut:
        formatSpikesOut.append(neuron.as_array().tolist())
    # Delay
    DelayLData = ppc.DelayLayer.get_data(variables=["spikes"])
    spikesDelay = DelayLData.segments[0].spiketrains
    formatSpikesDelay = []
    for neuron in spikesDelay:
        formatSpikesDelay.append(neuron.as_array().tolist())
    # Comparison
    ComparisonLData = ppc.ComparisonLayer.get_data(variables=["spikes"])
    spikesComp = ComparisonLData.segments[0].spiketrains
    formatSpikesComp = []
    for neuron in spikesComp:
        formatSpikesComp.append(neuron.as_array().tolist())
    # Inh
    InhLData = ppc.InhLayer.get_data(variables=["spikes"])
    spikesInh = InhLData.segments[0].spiketrains
    formatSpikesInh = []
    for neuron in spikesInh:
        formatSpikesInh.append(neuron.as_array().tolist())

    ######################################
    # End simulation
    ######################################
    sim.end()

    # Represent information
    print("IN read = " + str(inputReadSpikes))
    print("IN comp = " + str(inputCompSpikes))
    print("Delay = " + str(formatSpikesDelay))
    print("Comparison = " + str(formatSpikesComp))
    print("Inh = " + str(formatSpikesInh))
    print("OUT = " + str(formatSpikesOut))
    spikes_plot([[inputReadSpikes], inputCompSpikes, formatSpikesDelay, formatSpikesComp, formatSpikesInh, formatSpikesOut],
                ["INreadPPC", "INcompPPC", "Delay", "Comparison", "Inh", "OUT"],
                ["o", "o", "o", "o", "o", "o"], ["goldenrod", "Green", "Red", "darkviolet", "Blue", "Green"],
                ["INreadPPC", "INcompPPC", "Delay", "Comparison", "Inh", "OUT"], "PPC population spikes",
                "results/", "ppc", False, True)


# Plot the spike information
def spikes_plot(spikes, popNames, pointTypes, colors, labels, title, outFilePath, baseFilename, plot, write):
    plt.figure(figsize=(20, 12))

    # Add point for each neuron of each population that fire, take y labels and x labels
    populationsXValues = []
    populationsYValues = []
    globalIndex = 0
    maxXvalue = 0
    minXvalue = 99999999
    listYticks = []
    listXticks = []
    for indexPop, populationSpikes in enumerate(spikes):
        xvalues = []
        yvalues = []
        # Assign y value (population index) and y label
        for indexNeuron, spikesSingleNeuron in enumerate(populationSpikes):
            listYticks.append(popNames[indexPop] + str(indexNeuron))
            xvalues = xvalues + spikesSingleNeuron
            yvalues = yvalues + [indexNeuron+globalIndex for i in spikesSingleNeuron]
        globalIndex = globalIndex + len(populationSpikes)
        # Add to the populations values list
        populationsXValues.append(xvalues)
        populationsYValues.append(yvalues)
        # Find max and mix
        if xvalues[len(xvalues)-1] > maxXvalue:
            maxXvalue = xvalues[len(xvalues)-1]
        if xvalues[0] < minXvalue:
            minXvalue = xvalues[0]
        # Add xvalues to labels
        listXticks = list(set(listXticks+xvalues))

    # Lines for each points
    for indexPop in range(len(spikes)):
        plt.vlines(populationsXValues[indexPop], ymin=-1, ymax=populationsYValues[indexPop], color=colors[indexPop], alpha=0.1)
        plt.hlines(populationsYValues[indexPop], xmin=-1, xmax=populationsXValues[indexPop], color=colors[indexPop], alpha=0.1)

    # Add spikes to scatterplot
    for indexPop in range(len(spikes)):
        plt.plot(populationsXValues[indexPop], populationsYValues[indexPop], pointTypes[indexPop], color=colors[indexPop], label=labels[indexPop], markersize=10)

    # Metadata
    plt.xlabel("Simulation time (ms)", fontsize=20)
    plt.ylabel("Neuron spikes", fontsize=20)
    plt.title(title, fontsize=20)
    plt.ylim([-1, globalIndex])
    plt.xlim(-1 + minXvalue, maxXvalue + 2)
    plt.yticks(range(len(listYticks)), listYticks, fontsize=20)
    plt.legend(fontsize=20)

    # Divide xticks list in pair or odd position
    listXticks.sort()
    listXticksOdd = [int(tick) for index, tick in enumerate(listXticks) if not(index % 2 == 0)]
    listXticksPair = [int(tick) for index, tick in enumerate(listXticks) if index % 2 == 0]
    # Write them with alternate distance
    ax = plt.gca()
    ax.set_xticklabels(listXticksOdd, minor=True)
    ax.set_xticks(listXticksOdd, minor=True)
    ax.set_xticklabels(listXticksPair, minor=False)
    ax.set_xticks(listXticksPair, minor=False)
    ax.tick_params(axis='x', which='minor', pad=35)
    ax.tick_params(axis='x', which='both', labelsize=13, rotation=90)

    # Save and/or plot
    if write:
        plt.savefig(outFilePath + baseFilename + ".png")
    if plot:
        plt.show()


if __name__ == "__main__":
    test()
