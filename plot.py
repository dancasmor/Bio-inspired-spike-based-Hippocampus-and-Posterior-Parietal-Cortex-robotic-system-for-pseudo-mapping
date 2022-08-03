
import math
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import os


#############################################
# MAIN users global variables
#############################################
# Choose the desired experiment:
#   + 0  -> Robot demo: test 1 with a real robot
#   + 1  -> Test 1: 4x4 map with 1 obstacle in the path
#   + 2  -> Test 2: 6x6 map with various obstacle in the map
#   + 3  -> Test 3: 6x6 map with various obstacle in the map blocking the manhattan possible paths
experiment = 2
# If create map plots
plotMap = False
# If create spikes plots
plotSpikes = True

# Robot demo: test 1 with a real robot
if experiment == 0:
    # Map parameters:
    #  + Grid map size
    #   - Horizontal
    xlength = 4
    #   - Vertical
    ylength = 4
    #  + Init position
    xinit = 2
    yinit = 0
    #  + End position
    xend = 0
    yend = 3
    # Name of the experiment to develop
    experimentName = "robotDemo"
    # Positions (cellY * xlength + cellX + 1) with obstacle
    obstacles = []


# Test 1) 4x4 map with 1 obstacle in the path
elif experiment == 1:
    # Map parameters:
    #  + Grid map size
    #   - Horizontal
    xlength = 4
    #   - Vertical
    ylength = 4
    #  + Init position
    xinit = 2
    yinit = 0
    #  + End position
    xend = 0
    yend = 3
    # Name of the experiment to develop
    experimentName = "test4x4simple"
    # Positions (cellY * xlength + cellX + 1) with obstacle
    obstacles = [11]
    # Dict of intervals time stamp of interest
    intervalInfoList = {0: {"interval": [11, 112], "title": "Iter. 0 - Start and end", "filename": "iter0"},
                        1: {"interval": [142, 307], "title": "Iter. 1 - Check neighbours", "filename": "iter1_neighbours"},
                        2: {"interval": [382, 443], "title": "Iter. 1 - Check map", "filename": "iter1_map"},
                        3: {"interval": [474, 573], "title": "Iter. 1 - Select next step", "filename": "iter1_select"},
                        4: {"interval": [603, 703], "title": "Iter. 2 - Check neighbours", "filename": "iter2_neighbours"},
                        5: {"interval": [778, 839], "title": "Iter. 2 - Check map", "filename": "iter2_map"}}
    # List of maps to plot
    mapsTitle = []
    mapsToPlot = {}
    # Plot metainfo
    baseTitle = "Iter."
    stepsTitle = ["Check neighbours", "Select next step"]
    stepsName = ["check_neighbours", "select_next_step"]
    # Add maps states
    mapsToPlot["1_" + str(stepsName[0])] = [[0, 5, 1, 5],
                                             [0, 0, 5, 0],
                                             [0, 0, 0, 0],
                                             [2, 0, 0, 0]]
    mapsTitle.append(baseTitle + " 1 - " + str(stepsTitle[0]))
    mapsToPlot["1_" + str(stepsName[1])] = [[0, 5, 4, 5],
                                       [0, 0, 3, 0],
                                       [0, 0, 0, 0],
                                       [2, 0, 0, 0]]
    mapsTitle.append(baseTitle + " 1 - " + str(stepsTitle[1]))
    mapsToPlot["3_" + str(stepsName[0])] = [[0, 5, 4, 5],
                                             [0, 5, 3, 5],
                                             [0, 0, 6, 0],
                                             [2, 0, 0, 0]]
    mapsTitle.append(baseTitle + " 3 - " + str(stepsTitle[0]))
    mapsToPlot["3_" + str(stepsName[1])] = [[0, 5, 4, 5],
                                       [0, 3, 4, 5],
                                       [0, 0, 6, 0],
                                       [2, 0, 0, 0]]
    mapsTitle.append(baseTitle + " 3 - " + str(stepsTitle[1]))
    mapsToPlot["5_" + str(stepsName[0])] = [[0, 5, 4, 5],
                                             [5, 3, 4, 5],
                                             [0, 5, 6, 0],
                                             [2, 0, 0, 0]]
    mapsTitle.append(baseTitle + " 5 - " + str(stepsTitle[0]))
    mapsToPlot["5_" + str(stepsName[1])] = [[0, 5, 4, 5],
                                       [5, 4, 4, 5],
                                       [0, 3, 6, 0],
                                       [2, 0, 0, 0]]
    mapsTitle.append(baseTitle + " 5 - " + str(stepsTitle[1]))
    mapsToPlot["7_" + str(stepsName[0])] = [[0, 5, 4, 5],
                                             [5, 4, 4, 5],
                                             [5, 3, 6, 0],
                                             [2, 5, 0, 0]]
    mapsTitle.append(baseTitle + " 7 - " + str(stepsTitle[0]))
    mapsToPlot["7_" + str(stepsName[1])] = [[0, 5, 4, 5],
                                       [5, 4, 4, 5],
                                       [5, 4, 6, 0],
                                       [2, 3, 0, 0]]
    mapsTitle.append(baseTitle + " 7 - " + str(stepsTitle[1]))
    mapsToPlot["8_" + str(stepsName[0])] = [[0, 5, 4, 5],
                                             [5, 4, 4, 5],
                                             [5, 4, 6, 0],
                                             [2, 3, 5, 0]]
    mapsTitle.append(baseTitle + " 8 - " + str(stepsTitle[0]))
    finalIteration = 9


# Test 2) 6x6 map with various obstacle in the map
elif experiment == 2:
    # Map parameters:
    #  + Grid map size
    #   - Horizontal
    xlength = 6
    #   - Vertical
    ylength = 6
    #  + Init position
    xinit = 2
    yinit = 0
    #  + End position
    xend = 5
    yend = 5
    # Name of the experiment to develop
    experimentName = "test6x6simple"
    # Positions (cellY * xlength + cellX + 1) with obstacle
    obstacles = [5, 12, 15, 23, 30, 34]
    # Dict of intervals time stamp of interest
    intervalInfoList = {0: {"interval": [4330, 4365], "title": "Iter. 16 - Check neighbours",
                            "filename": "iter16_neighbours"},
                        2: {"interval": [4410, 4471], "title": "Iter. 16 - Check map", "filename": "iter16_map"},
                        3: {"interval": [4531, 4565], "title": "Iter. 16 - Search crossroad", "filename": "iter16_crossroad"}}
    # List of maps to plot
    mapsTitle = []
    mapsToPlot = {}
    # Plot metainfo
    baseTitle = "Iter."
    stepsTitle = ["Check neighbours", "Select next step", "Backtracking"]
    stepsName = ["check_neighbours", "select_next_step", "backtracking"]
    # Add maps states
    iter = 1
    mapsToPlot[str(iter) + "_" + str(stepsName[0])] = \
        [[0, 5, 1, 5, 0, 0],
         [0, 0, 5, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[0]))
    mapsToPlot[str(iter) + "_" + str(stepsName[1])] = \
        [[0, 5, 4, 3, 0, 0],
         [0, 0, 5, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[1]))
    iter = 3
    mapsToPlot[str(iter) + "_" + str(stepsName[0])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 5, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[0]))
    mapsToPlot[str(iter) + "_" + str(stepsName[1])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 3, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[1]))
    iter = 5
    mapsToPlot[str(iter) + "_" + str(stepsName[0])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 3, 5, 0],
         [0, 0, 0, 5, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[0]))
    mapsToPlot[str(iter) + "_" + str(stepsName[1])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 0],
         [0, 0, 0, 5, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[1]))
    iter = 7
    mapsToPlot[str(iter) + "_" + str(stepsName[0])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 5, 5, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[0]))
    mapsToPlot[str(iter) + "_" + str(stepsName[1])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 5, 3, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[1]))
    iter = 9
    mapsToPlot[str(iter) + "_" + str(stepsName[0])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 5, 3, 5],
         [0, 0, 0, 0, 6, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[0]))
    mapsToPlot[str(iter) + "_" + str(stepsName[1])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 5, 4, 3],
         [0, 0, 0, 0, 6, 0],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[1]))
    iter = 11
    mapsToPlot[str(iter) + "_" + str(stepsName[0])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 5, 4, 3],
         [0, 0, 0, 0, 6, 5],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[0]))
    mapsToPlot[str(iter) + "_" + str(stepsName[1])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 5, 4, 3],
         [0, 0, 0, 0, 6, 3],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[1]))
    iter = 13
    mapsToPlot[str(iter) + "_" + str(stepsName[0])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 5, 4, 3],
         [0, 0, 0, 0, 6, 3],
         [0, 0, 0, 0, 0, 6],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[0]))
    iter = 16
    mapsToPlot[str(iter) + "_" + str(stepsName[2])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 5, 4, 3],
         [0, 0, 0, 0, 6, 7],
         [0, 0, 0, 0, 0, 6],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[2]))
    iter = 17
    mapsToPlot[str(iter) + "_" + str(stepsName[2])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 5, 4, 7],
         [0, 0, 0, 0, 6, 7],
         [0, 0, 0, 0, 0, 6],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[2]))
    iter = 18
    mapsToPlot[str(iter) + "_" + str(stepsName[1])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 3, 3, 7],
         [0, 0, 0, 0, 6, 7],
         [0, 0, 0, 0, 0, 6],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[1]))
    iter = 20
    mapsToPlot[str(iter) + "_" + str(stepsName[0])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 6, 3, 3, 7],
         [0, 0, 0, 5, 6, 7],
         [0, 0, 0, 0, 0, 6],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[0]))
    mapsToPlot[str(iter) + "_" + str(stepsName[1])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 6, 3, 3, 7],
         [0, 0, 0, 3, 6, 7],
         [0, 0, 0, 0, 0, 6],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[1]))
    iter = 22
    mapsToPlot[str(iter) + "_" + str(stepsName[0])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 6, 3, 3, 7],
         [0, 0, 5, 3, 6, 7],
         [0, 0, 0, 5, 0, 6],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[0]))
    mapsToPlot[str(iter) + "_" + str(stepsName[1])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 6, 3, 3, 7],
         [0, 0, 5, 4, 6, 7],
         [0, 0, 0, 3, 0, 6],
         [0, 0, 0, 0, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[1]))
    iter = 24
    mapsToPlot[str(iter) + "_" + str(stepsName[0])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 6, 3, 3, 7],
         [0, 0, 5, 4, 6, 7],
         [0, 0, 5, 3, 5, 6],
         [0, 0, 0, 6, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[0]))
    mapsToPlot[str(iter) + "_" + str(stepsName[1])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 6, 3, 3, 7],
         [0, 0, 5, 4, 6, 7],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 6, 0, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[1]))
    iter = 26
    mapsToPlot[str(iter) + "_" + str(stepsName[0])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 6, 3, 3, 7],
         [0, 0, 5, 4, 6, 7],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 6, 5, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[0]))
    mapsToPlot[str(iter) + "_" + str(stepsName[1])] = \
        [[0, 5, 4, 3, 6, 0],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 6, 3, 3, 7],
         [0, 0, 5, 4, 6, 7],
         [0, 0, 5, 4, 3, 6],
         [0, 0, 0, 6, 3, 2]]
    mapsTitle.append(baseTitle + " " + str(iter) + " - " + str(stepsTitle[1]))
    finalIteration = 28


# Test 3) 6x6 map with various obstacle in the map blocking the manhattan possible paths
elif experiment == 3:
    # Map parameters:
    #  + Grid map size
    #   - Horizontal
    xlength = 6
    #   - Vertical
    ylength = 6
    #  + Init position
    xinit = 2
    yinit = 0
    #  + End position
    xend = 5
    yend = 5
    # Name of the experiment to develop
    experimentName = "test6x6complex"
    # Positions (cellY * xlength + cellX + 1) with obstacle
    obstacles = [5, 9, 12, 15, 21, 23, 28, 30]


#############################################
# Declarate OTHER user global variables
#############################################

# State names and colors used to represent them
nameStateList = ["(0) unexplored", "(1) start", "(2) end", "(3) path step", "(4) crossroad", "(5) free", "(6) obstacle", "(7) dead-end"]
colorPalette = colors.ListedColormap(["white", "#F8F8B0", "#CAEEBE", "#98E2F7", "#C5D9FC", "#D0B1FC", "#FDB196", "#8A8985"])
# Number of states of the map state
numStates = 8
# True if write the results in files
write = True
# True if show the result in plot
plot = False


#############################################
# Plot functions
#############################################


# Convert a 2d list state map to a grid map plot with state and colors in functions os the state number
def map_state_to_color_map(stateMap, title, mapName=None):
    # Create grid color map
    plt.figure(figsize=(8, 7))
    plt.pcolor(stateMap[::-1], cmap=colorPalette, edgecolors='k', linewidths=1, vmin=0, vmax=numStates)
    # Axis labels
    plt.xticks(np.arange(0.5, xlength+0.5), np.arange(0, xlength), size=20)
    plt.yticks(np.arange(0.5, ylength+0.5), np.arange(0, ylength), size=20)
    # Add color bar legend
    colorbar = plt.colorbar()
    colorbar.set_ticks(np.arange(0.5, numStates+0.5))
    colorbar.set_ticklabels(nameStateList)
    # Add state number to cells in grid map
    positions = [[y*xlength+x+1 for x in range(xlength)] for y in range(ylength)]
    for y in range(ylength):
        for x in range(xlength):
            plt.text(x + 0.5, y + 0.5, stateMap[::-1][y][x], horizontalalignment='center', verticalalignment='center', size=20)
            plt.text(x + 0.1, y + 0.8, positions[::-1][y][x], size=12)
    # Add title
    plt.title(title, size=20)

    # Save and/or plot
    if write:
        plt.savefig(outFilePath + mapName + ".png")
    if plot:
        plt.show()


# Convert the list of state maps to color maps
def map_state_to_color_map_list():
    for index, maps in enumerate(mapsToPlot.items()):
        map_state_to_color_map(maps[1], mapsTitle[index], mapName=maps[0])


# Plot the spike information in an interval time stamp
def spikes_plot(memory, ppc, interval, title, baseFilename):
    plt.figure(figsize=(18, 12))

    # Add spikes for each population of neuron (memory out and ppc out) if they are in the interval of time
    xvaluesMemCue = []
    xvaluesMemCont = []
    xvaluesPPC = []
    yvaluesMemCue = []
    yvaluesMemCont = []
    yvaluesPPC = []
    # OUT memory
    for indexNeuron, spikesSingleNeuron in enumerate(memory):
        # Keep only those who belong to the interval
        spikesSingleNeuronInterval = [i for i in spikesSingleNeuron if i >= interval[0] and i <= interval[1]]
        if indexNeuron < cueSizeInBin:
            xvaluesMemCue = xvaluesMemCue + spikesSingleNeuronInterval
            yvaluesMemCue = yvaluesMemCue + [indexNeuron for i in spikesSingleNeuronInterval]
        else:
            xvaluesMemCont = xvaluesMemCont + spikesSingleNeuronInterval
            yvaluesMemCont = yvaluesMemCont + [indexNeuron for i in spikesSingleNeuronInterval]
    # OUT PPC
    for indexNeuron, spikesSingleNeuron in enumerate(ppc):
        # Keep only those who belong to the interval
        spikesSingleNeuronInterval = [i for i in spikesSingleNeuron if i >= interval[0] and i <= interval[1]]
        xvaluesPPC = xvaluesPPC + spikesSingleNeuronInterval
        yvaluesPPC = yvaluesPPC + [indexNeuron + len(memory) for i in spikesSingleNeuronInterval]

    # Lines for each points
    plt.vlines(xvaluesPPC, ymin=-1, ymax=yvaluesPPC, color="green", alpha=0.1)
    plt.hlines(yvaluesPPC, xmin=0, xmax=xvaluesPPC, color="green", alpha=0.1)
    plt.vlines(xvaluesMemCont, ymin=-1, ymax=yvaluesMemCont, color="red", alpha=0.1)
    plt.hlines(yvaluesMemCont, xmin=0, xmax=xvaluesMemCont, color="red", alpha=0.1)
    plt.vlines(xvaluesMemCue, ymin=-1, ymax=yvaluesMemCue, color="green", alpha=0.1)
    plt.hlines(yvaluesMemCue, xmin=0, xmax=xvaluesMemCue, color="green", alpha=0.1)

    # Add spikes to scatterplot
    plt.plot(xvaluesPPC, yvaluesPPC, "s", color="green", label="PPC")
    plt.plot(xvaluesMemCont, yvaluesMemCont, "^", color="red", label="MemCont")
    plt.plot(xvaluesMemCue, yvaluesMemCue, "o", color="blue", label="MemCue")

    # Metadata
    plt.xlabel("Simulation time (ms)", fontsize=20)
    plt.ylabel("Neuron spikes", fontsize=20)
    plt.title(title, fontsize=20)
    plt.ylim([-1, len(memory) + len(ppc)])
    plt.xlim(-0.5 + interval[0], interval[1] + 0.5)
    listYticks = []
    for indexNeuron in range(len(memory)):
        if indexNeuron < cueSizeInBin:
            listYticks.append("MemCue" + str(indexNeuron))
        else:
            listYticks.append("MemCont" + str(indexNeuron - cueSizeInBin))
    for indexNeuron in range(len(ppc)):
        listYticks.append("PPC" + str(indexNeuron))
    plt.yticks(range(len(memory) + len(ppc)), listYticks, fontsize=20)
    plt.legend(fontsize=20)

    # Divide xticks list in pair or odd position
    listXticks = list(set(xvaluesMemCue + xvaluesMemCont + xvaluesPPC))
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


# Plot the spike information of the given (global) intervals time stamps
def spikes_plots_interval_list(memory, ppc):
    for intervalInfo in intervalInfoList.values():
        spikes_plot(memory, ppc, intervalInfo["interval"], intervalInfo["title"], intervalInfo["filename"])


#############################################
# Tools functions
#############################################


# Open the file and return the data
def read_file(filename):
    file = open(filePath + filename, "r")
    data = eval(file.read())
    file.close()
    return data


# Check if folder exist, if not, create it
def check_folder(path):
    # Check if folder exist, if not, create it
    if not os.path.isdir(path):
        os.mkdir(path)


# Define and calculate the initial value of global params that not depends on the user
def init_global_params():
    global cueSize, contSize, cueSizeInBin, numInputLayerNeurons, filePath, outFilePath
    # Network parameters:
    # + Number of directions of the memory -> one for each cell in grid map
    cueSize = xlength * ylength
    # + Size of the patterns in bits/neuron -> one for each possible state of a cell
    contSize = numStates
    # + Number of neurons in input layer: the number of bits neccesary to represent the number of directions in
    # binary + the size of patterns
    cueSizeInBin = math.ceil(math.log2(cueSize + 1))
    numInputLayerNeurons = cueSizeInBin + contSize

    # Data file path
    filePath = "results/" + experimentName + "/"
    # Plots stored path
    outFilePath = filePath + "plots/"

    # Create plots folder
    check_folder(outFilePath)


#############################################
# Main
#############################################


def main():
    # Initialize global params that not depends on the user
    init_global_params()

    # List of maps -> only experiments 1 and 2
    if plotMap:
        if experiment >= 1 and experiment <= 2:
            # + Initial map
            initial_map = read_file("initial_map.txt")
            map_state_to_color_map(initial_map, baseTitle + " 0 - Initial map", "0_initial_map")
            # + Obstacle map
            obstacle_map = np.zeros((ylength, xlength), dtype=int)
            for y in range(ylength):
                for x in range(xlength):
                    if y*xlength+x+1 in obstacles:
                        obstacle_map[y][x] = 6

            map_state_to_color_map(obstacle_map, "Obstacle map", "0_obstacle_map")
            # + Wanted maps
            map_state_to_color_map_list()
            # + Final map
            final_map = read_file("final_map.txt")
            map_state_to_color_map(final_map, baseTitle + str(finalIteration) + " - Final map", str(finalIteration) + "_final_map")

    # Spike plots
    if plotSpikes:
        out_mem_spikes = read_file("out_mem_spikes.txt")
        out_ppc_spikes = read_file("out_ppc_spikes.txt")
        spikes_plots_interval_list(out_mem_spikes, out_ppc_spikes)

    print("Stored in: " + outFilePath)


if __name__ == "__main__":
    main()
