
from sPyMem.hippocampus_with_forgetting import hippocampus_with_forgetting
import spynnaker8 as sim
import math
import numpy as np


# Reconstruct memory state from output spikes
def memory_state_from_spikes(formatSpikes, simTime, timeStep, xlength, ylength, cueSizeInBin):
    map_state = np.zeros((ylength, xlength), dtype=int)
    # Get spikes by timestamp
    for timeStamp in range(0, simTime, int(timeStep)):
        cueInSameStamp = []
        # For each neuron in cue, find which cue fired in each time stamp
        for neuronId, neuronCue in enumerate(formatSpikes[:cueSizeInBin]):
            if timeStamp in neuronCue:
                cueInSameStamp.append(neuronId)
        # Convert neuron id of cues in cue as int
        cue = 0
        for neuronId in cueInSameStamp:
            cue = cue + 2**neuronId
        # If there is a cue in that timestamp, check the next stamp to get the content of the memory
        if not(cue == 0):
            for neuronId, neuronCont in enumerate(formatSpikes[cueSizeInBin:]):
                if timeStamp+1 in neuronCont:
                    # Keep coherence with important information over free cell state
                    if (neuronId == 5) and (timeStamp+1 in formatSpikes[cueSizeInBin+3] or timeStamp+1 in formatSpikes[cueSizeInBin+4]):
                        continue
                    map_state[int((cue-1) / xlength)][int((cue-1) % xlength)] = neuronId
    return map_state


# Create the input spikes to make a memory sweep
def memory_sweep_input_spikes(numInputLayerNeurons, xlength, ylength, cueSizeInBin):
    inputSpikes = [[] for i in range(numInputLayerNeurons)]
    simTime = 1
    binLearningOps = []
    # Create the binary representation of the cue for learning operation
    for cellId in range(1, xlength*ylength+1):
        binLearningOps.append(int_to_binary_int(cellId))
    # For each operation, create the input spike representation
    for operation in binLearningOps:
        for neuron in operation:
            if neuron < cueSizeInBin:
                inputSpikes[neuron].append(simTime)
        simTime = simTime + 10
    return inputSpikes, simTime+3


# Convert an int number to a list of position that indicate which positions in binary are 1
def int_to_binary_int(number):
    binaryIndexList = []
    index = 0
    while number != 0:
        bit = int(number % 2)
        number = int(number / 2)
        if bit == 1:
            binaryIndexList.append(index)
        index = index + 1
    return binaryIndexList


# Make a memory sweep to reconstruct the final map state learned
def simulate_memory_sweep(final_path_w, numInputLayerNeurons, xlength, ylength, cueSizeInBin, timeStep, cueSize, contSize, debug):
    # Transform the map state 2d array to a input spikes sequence to learn it in the memory
    inputSpikes, simTime = memory_sweep_input_spikes(numInputLayerNeurons, xlength, ylength, cueSizeInBin)

    # Setup simulation
    sim.setup(timeStep)

    # Create network
    # Input layer
    ILayer = sim.Population(numInputLayerNeurons, sim.SpikeSourceArray(spike_times=inputSpikes), label="ILayer")
    # Output layer: fire a spike when receive a spike
    neuronParameters = {"cm": 0.27, "i_offset": 0.0, "tau_m": 3.0, "tau_refrac": 1.0, "tau_syn_E": 0.3,
                        "tau_syn_I": 0.3,
                        "v_reset": -60.0, "v_rest": -60.0, "v_thresh": -57.5}
    OLayer = sim.Population(numInputLayerNeurons, sim.IF_curr_exp(**neuronParameters), label="OLayer")
    OLayer.set(v=-60)

    # Create the synapse weight format
    finalCA3W = []
    for synapse in final_path_w:
        finalCA3W.append((synapse[0], synapse[1], synapse[2], 1.0))
    # Create memory
    memory = hippocampus_with_forgetting.Memory(cueSize, contSize, sim, ILayer, OLayer, initCA3W=finalCA3W)

    # Parameters to store
    OLayer.record(["spikes"])

    # Begin simulation
    sim.run(simTime)

    # Get data from Output
    OLData = OLayer.get_data(variables=["spikes"])
    spikesOut = OLData.segments[0].spiketrains
    formatSpikes = []
    for neuron in spikesOut:
        formatSpikes.append(neuron.as_array().tolist())

    # End simulation
    sim.end()

    # Reconstruct memory state from output spikes
    map_state = memory_state_from_spikes(formatSpikes, simTime, timeStep, xlength, ylength, cueSizeInBin)

    if debug:
        print("Final path learning")
        print("SimTime = " + str(simTime))
        print("MAP = \n" + str(map_state))

    return map_state


if __name__ == "__main__":
    # Debug mode
    debug = True

    # Grid map size
    # + Horizontal
    xlength = 6
    # + Vertical
    ylength = 6

    # Network and simulation parameters:
    # + Number of directions of the memory -> one for each cell in grid map
    cueSize = xlength * ylength
    # + Size of the patterns in bits/neuron -> one for each possible state of a cell
    contSize = 8
    # + CA3 weight with learning
    file = open("results/test6x6complex/final_w.txt", "r")
    initial_path_w = eval(file.read())
    file.close()
    # + Number of neurons in input layer: the number of bits neccesary to represent the number of directions in
    # binary + the size of patterns
    cueSizeInBin = math.ceil(math.log2(cueSize + 1))
    numInputLayerNeurons = cueSizeInBin + contSize
    # + Time step of the simulation
    timeStep = 1.0

    # Make a memory sweep to reconstruct the final map state learned
    simulate_memory_sweep(initial_path_w, numInputLayerNeurons, xlength, ylength, cueSizeInBin, timeStep, cueSize,
                          contSize, debug)
