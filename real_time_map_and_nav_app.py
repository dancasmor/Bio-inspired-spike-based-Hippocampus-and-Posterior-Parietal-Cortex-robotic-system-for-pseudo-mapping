
from sPyMem import hippocampus_with_forgetting
import spynnaker8 as sim
import math
from threading import Condition
import time
import numpy as np
import os
import socket
import memory_sweep
import posterior_parietal_cortex

"""

Map state codes:
    + 0 -> unexplored
    + 1 -> start
    + 2 -> end
    + 3 -> step in path
    + 4 -> crossroad
    + 5 -> free (no obstacle)
    + 6 -> obstacle
    + 7 -> dead end
"""

#############################################
# MAIN users global variables
#############################################
# Choose the desired experiment:
#   + 0  -> Robot demo: test 1 with a real robot
#   + 1  -> Test 1: 4x4 map with 1 obstacle in the path
#   + 2  -> Test 2: 6x6 map with various obstacle in the map
#   + 3  -> Test 3: 6x6 map with various obstacle in the map blocking the manhattan possible paths
experiment = 0


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
    # Time parameters:
    # + Duration of the simulation
    simTime = 60000
    # Initial direction of virtual robot [0 = top, 1 = left, 2 = bottom, 4 = right]
    robotDirection = 2
    # Maximum time robot need to move
    maxMoveTime = 3.2
    # ositions (cellY * xlength + cellX + 1) with obstacle
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
    # Time parameters:
    # + Duration of the simulation
    simTime = 5000
    # (ONLY SIMULATION TEST)
    #  + Positions (cellY * xlength + cellX + 1) with obstacle
    obstacles = [11]
    #  + Initial direction of virtual robot [0 = top, 1 = left, 2 = bottom, 4 = right]
    robotDirection = 2


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
    # Time parameters:
    # + Duration of the simulation
    simTime = 10000
    # (ONLY SIMULATION TEST)
    #  + Positions (cellY * xlength + cellX + 1) with obstacle
    obstacles = [5, 12, 15, 23, 30, 34]
    #  + Initial direction of virtual robot [0 = top, 1 = left, 2 = bottom, 4 = right]
    robotDirection = 2


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
    # Time parameters:
    # + Duration of the simulation
    simTime = 20000
    # (ONLY SIMULATION TEST)
    #  + Positions (cellY * xlength + cellX + 1) with obstacle
    obstacles = [5, 9, 12, 15, 21, 23, 28, 30]
    #  + Initial direction of virtual robot [0 = top, 1 = left, 2 = bottom, 4 = right]
    robotDirection = 2


#############################################
# Declarate OTHER user global variables
#############################################


# Number of states of the map state
numStates = 8
# Debug level: 0 = no debug, 1 = soft debug, 2 = mid debug, 3 = hard debug
debugLevel = 2
# True if write the results in files
write = True
# Time to wait between operations in memory
operationTime = 0.03
# operationTime = 0.015
# How many repeated iterations of searching cells is considered a dead end
maxRepeatedIteration = 3


#############################################
# Callbacks for live injection
#############################################
# + Create a condition to avoid overlapping prints
print_condition = Condition()


# + Callback send live spikes
def send_spikes_to(label, sender):
    global obstacleCells, freeCells, backtracking, unachievable, finish, searchCommandFinish

    # Learn initial and end cell of the path
    if debugLevel >= 1:
        print_condition.acquire()
        print("Start and end cells learning...")
        print_condition.release()
    reinforced_learning(label, sender, memory_sweep.int_to_binary_int(yinit * xlength + xinit + 1) + [1 + cueSizeInBin], operationTime)
    reinforced_learning(label, sender, memory_sweep.int_to_binary_int(yend * xlength + xend + 1) + [2 + cueSizeInBin], operationTime)

    while(not finish and not unachievable):
        # Debug info
        if debugLevel >= 1:
            print_condition.acquire()
            print("- Iteration:")
            print_condition.release()

        # Check real and virtual neighbours of current cell
        searchCommandFinish = False
        check_neighbours(label, sender)

        # Check if following normal path searching the target o backtracking due to a dead end
        if not backtracking:
            # Following normal path: go to the next step or search it if it does not exist
            searching_target(label, sender)
        else:
            # Backtracking: search crossroad to continue the following of the target
            searching_crossroad(label, sender)

        # Empty the other cells for the next iteration of the path
        obstacleCells = []
        freeCells = []


# + Callback receive live spikes
def received_spikes(label, _time, neuron_ids):
    global nextCellX, nextCellY, nextCellFound, obstacleCells, searchingNeighbour, lastNeuronsId, lastCell, freeCells,\
        command, searchCommandFinish, searchCommandBegin, crossroadCell
    # Debug info -> ignore ILayer and OPPCLayer for not command spikes in debug mode 2
    if debugLevel >= 3 or not((debugLevel == 2) and (label == "ILayer" or (label == "OPPCLayer" and not searchCommandBegin))):
        print_condition.acquire()
        print("t=" + str(_time) + " p=" + label + " " + str(neuron_ids))
        print_condition.release()

    # Only proccess spikes when we are sending searching input operation
    if searchingNeighbour and label == "OLayer":
        if (7 + cueSizeInBin) in neuron_ids:
            pass
        elif (6 + cueSizeInBin) in neuron_ids:
            # Extract the position of the obstacle (lastNeuronsId have the last output neurons which fired, i.e., cue)
            obstacleCells.append([neuron_ids_to_cell_coordinate(lastNeuronsId)])
        elif (3 + cueSizeInBin) in neuron_ids or (2 + cueSizeInBin) in neuron_ids or (4 + cueSizeInBin) in neuron_ids:
            # Extract the position of the next step (lastNeuronsId have the last output neurons which fired,i.e., cue)
            nextCellX, nextCellY = neuron_ids_to_cell_coordinate(lastNeuronsId)
            nextCellFound = True
            # Special flag activation for last cell of path and crossroad cells
            if (2 + cueSizeInBin) in neuron_ids:
                lastCell = True
            elif (3 + cueSizeInBin) in neuron_ids:
                pass
            elif (4 + cueSizeInBin) in neuron_ids:
                crossroadCell = True
        elif (5 + cueSizeInBin) in neuron_ids:
            # Extract the position of the empty cells
            freeCells.append(neuron_ids_to_cell_coordinate(lastNeuronsId))
        else:
            # Get the last neurons which fire
            lastNeuronsId = neuron_ids

    # Get PPC output command
    if label == "OPPCLayer" and searchCommandBegin:
        # 0 = top, 1 = left, 2 = right, 3 = bot
        command = neuron_ids[0]
        searchCommandFinish = True


#############################################
# Functions fragments of receive callback
#############################################

# Check real and virtual neighbours of current cell
def check_neighbours(label, sender):
    global debugLevel, searchCommandBegin
    # Check the actual status of neighbouring boxes (update the memory with real information)
    if debugLevel >= 2:
        print_condition.acquire()
        print("Checking real map...")
        print_condition.release()
    check_real_neighbours(label, sender)
    # Given a cell in the map, check the 4 neighbours and calculate the next command
    if debugLevel >= 2:
        print_condition.acquire()
        print("Checking virtual map...")
        print_condition.release()
    searchCommandBegin = True
    check_virtual_neighbours(label, sender)
    searchCommandBegin = False


# Check the 4 neighbours and calculate the next command, avoid the previus cell and out
def check_virtual_neighbours(label, sender):
    global cellX, cellY, lastCellX, lastCellY, searchingNeighbour, operationTime, numInputLayerNeurons, \
        robotPath, backtracking, xlength
    # Indicate sender callback to read
    searchingNeighbour = True
    # Send lecture signal to PPC
    sender.send_spikes(label, [numInputLayerNeurons], send_full_keys=True)
    # 1) Top
    if cellY > 0 and not (cellY-1 == lastCellY and cellX == lastCellX):
        # Avoid backtracking loop
        if backtracking or not((cellY-1) * xlength + cellX + 1 in robotPath):
            sender.send_spikes(label, memory_sweep.int_to_binary_int((cellY-1) * xlength + cellX + 1), send_full_keys=True)
    time.sleep(operationTime)
    # 2) Left
    if cellX > 0 and not (cellY == lastCellY and cellX-1 == lastCellX):
        # Avoid backtracking loop
        if backtracking or not (cellY * xlength + cellX-1 + 1 in robotPath):
            sender.send_spikes(label, memory_sweep.int_to_binary_int(cellY * xlength + cellX-1 + 1), send_full_keys=True)
    time.sleep(operationTime)
    # 3) Bot
    if cellY < ylength-1 and not (cellY+1 == lastCellY and cellX == lastCellX):
        # Avoid backtracking loop
        if backtracking or not((cellY+1) * xlength + cellX + 1 in robotPath):
            sender.send_spikes(label, memory_sweep.int_to_binary_int((cellY+1) * xlength + cellX + 1), send_full_keys=True)
    time.sleep(operationTime)
    # 4) Right
    if cellX < xlength-1 and not (cellY == lastCellY and cellX+1 == lastCellX):
        # Avoid backtracking loop
        if backtracking or not(cellY * xlength + cellX+1 + 1 in robotPath):
            sender.send_spikes(label, memory_sweep.int_to_binary_int(cellY * xlength + cellX+1 + 1), send_full_keys=True)
    time.sleep(operationTime)
    searchingNeighbour = False


# Following normal path: go to the next step or search it if it does not exist
def searching_target(label, sender):
    global nextCellFound, iterationsRepeated, unachievable, maxRepeatedIteration

    # If there is a step in the path, follow it
    if nextCellFound:
        following_next_step()
        iterationsRepeated = 0
    else:
        # If there is no step to follow, it have to search a new one
        search_new_step(label, sender)

        # Avoid robot to keep in infinite loop
        iterationsRepeated = iterationsRepeated + 1
        if iterationsRepeated >= maxRepeatedIteration:
            if debugLevel >= 1:
                print_condition.acquire()
                print("UNACHIEVABLE TARGET!")
                print_condition.release()
            unachievable = True


# Follow the next step found in the path to the target and indicate if the target is reached
def following_next_step():
    global nextCellFound, lastCellX, lastCellY, cellX, cellY, nextCellX, nextCellY, searchCommandFinish, debugLevel, \
        lastCell, crossroadCell, finish

    # Calculate next move action
    nextCellFound = False
    lastCellX = cellX
    lastCellY = cellY
    cellX = nextCellX
    cellY = nextCellY

    # Add new step into the passed steps of the following path
    robotPath.append(cellY * xlength + cellX + 1)

    # Wait for searching of next robot movement command
    while (not searchCommandFinish):
        # 0.001
        time.sleep(0.005)
    searchCommandFinish = False
    # Send command to the robot
    send_command_to_robot()

    if debugLevel >= 1:
        print_condition.acquire()
        print("Next step = " + str(cellX) + "," + str(cellY))
        print_condition.release()

    # If last cell found, finish the algorithm
    if lastCell:
        if debugLevel >= 1:
            print_condition.acquire()
            print("Target reached!")
            print_condition.release()
        finish = True

    # Close special flag for crossroad cells
    crossroadCell = False


# Search a new step for the path from the free ones or begin backtracking because of the dead end found
def search_new_step(label, sender):
    global crossroadCell, debugLevel, freeCells, xend, yend, xlength, cueSizeInBin, operationTime, cellY, cellX, \
        experiment, robotPath, backtracking, robotDirection, iterationsRepeated, lastCellX, lastCellY, nearestCell

    # If there is free cells around, choose the nearest as the next step
    if not (len(freeCells) == 0):
        # If there is no new step on the path, look for a free cell and use it as a new step on the path
        if debugLevel >= 2:
            print_condition.acquire()
            print("Not next step. Searching new...")
            print("Free cells: " + str(freeCells) + " , target: (" + str(xend) + "," + str(yend) + ")")
            print_condition.release()

        # Search another step in the path to reach the target (take the cell closest to the final target)
        #  1) Get cells with the nearest distance to target
        nearestCells = manhattan_nearest_cell_to_target([xend, yend], freeCells)

        # Add the new step in the path to memory
        if debugLevel >= 2:
            print_condition.acquire()
            print("Learning new path step = (" + str(nearestCells[len(nearestCells) - 1][0]) + "," + str(
                nearestCells[len(nearestCells) - 1][1]) + ")")
            print_condition.release()

        #  2) If there are more than 1 cell, use the last for the next step and mark the current cell as crossroad
        nearestCell = nearestCells[len(nearestCells) - 1]
        reinforced_learning(label, sender, memory_sweep.int_to_binary_int(nearestCell[1] * xlength + nearestCell[0] + 1) + [3 + cueSizeInBin], operationTime)
        if len(freeCells) > 1:
            reinforced_learning(label, sender, memory_sweep.int_to_binary_int(cellY * xlength + cellX + 1) + [4 + cueSizeInBin], operationTime)

        #  3) If there is only 1 free cell and is crossroad, convert to normal path step
        if crossroadCell:
            crossroadCell = False
            if len(freeCells) == 1:
                reinforced_learning(label, sender, memory_sweep.int_to_binary_int(cellY * xlength + cellX + 1) + [3 + cueSizeInBin], operationTime)

    else:
        # If there isn't free cells around, begin backtracking

        # If the current step was a crossroad, convert it in a new dead end (no free cells to the target)
        if crossroadCell:
            # Convert current cell to dead end
            reinforced_learning(label, sender, memory_sweep.int_to_binary_int(cellY * xlength + cellX + 1) + [7 + cueSizeInBin], operationTime)
            crossroadCell = False
        # Activate special flag for backtracking
        backtracking = True
        # Change robot direction
        robotDirection = (robotDirection + 2) % 4

        # Reboot global variables for unavailable target
        iterationsRepeated = 0
        # Delete last cell of the path to get it in backtracking
        lastCellX = -1
        lastCellY = -1

        if debugLevel >= 1:
            print_condition.acquire()
            print("No free cells around. Dead end reached. Begining backtracking...")
            print_condition.release()


# Backtracking: search crossroad to continue the following of the target
def searching_crossroad(label, sender):
    global crossroadCell, nextCellFound, cellY, cellX, xlength, cueSizeInBin, operationTime, lastCellX, lastCellY,\
        nextCellX, nextCellY, backtracking, iterationsRepeated, unachievable, searchCommandFinish, robotPath

    if debugLevel >= 2:
        print_condition.acquire()
        print("Backtracking...")
        print_condition.release()

    if crossroadCell:
        # If robot found crossroad, follow it and finish backtracking
        backtracking = False
        nextCellFound = False
    elif nextCellFound:
        # If there is a step in the backtracking path, follow it
        nextCellFound = False
        iterationsRepeated = 0

    # Convert current cell to dead end
    reinforced_learning(label, sender, memory_sweep.int_to_binary_int(cellY * xlength + cellX + 1) + [7 + cueSizeInBin], operationTime)

    # Follow next step
    lastCellX = cellX
    lastCellY = cellY
    cellX = nextCellX
    cellY = nextCellY

    # Wait for searching of next robot movement command
    while (not searchCommandFinish):
        # 0.001
        time.sleep(0.005)
    searchCommandFinish = False
    # Send command to the robot
    send_command_to_robot()

    if debugLevel >= 1:
        print_condition.acquire()
        print("Next backtracking step = " + str(cellX) + "," + str(cellY))
        if not backtracking:
            print("Crossroad found!")
        print_condition.release()

    # Avoid robot to keep in infinite loop
    iterationsRepeated = iterationsRepeated + 1
    if iterationsRepeated >= maxRepeatedIteration:
        if debugLevel >= 1:
            print_condition.acquire()
            print("UNACHIEVABLE TARGET!")
            print_condition.release()
        unachievable = True
    if not backtracking:
        iterationsRepeated = 0


# Make a reinforced learning in memory; reinforced learning is a learning operation with an inmediate recall operation
def reinforced_learning(label, sender, neuronIds, operationTime):
    # Learning
    for i in range(3):
        sender.send_spikes(label, neuronIds, send_full_keys=True)
        time.sleep(0.001)
    time.sleep(operationTime)
    # Recall
    recallNeuronIds = [neuronId for neuronId in neuronIds if neuronId < cueSizeInBin]
    sender.send_spikes(label, recallNeuronIds, send_full_keys=True)
    time.sleep(operationTime)


#############################################
# Robot comunication
#############################################


# Send movement command to the robot
def send_command_to_robot():
    global command, robotDirection
    if debugLevel >= 2:
        commandName = ["Top", "Left", "Bottom", "Right"]
        print_condition.acquire()
        print("Command: " + commandName[command])
        print_condition.release()

    # Update the robot direction
    robotDirection = command

    # FOR EMULATION WITH REAL ROBOT ONLY
    if experiment == 0:
        global send_udp
        # Send command
        localCommand = command+1
        send_udp.sendto(localCommand.to_bytes(1, byteorder="little"), ("192.168.4.1", 8888))
        # Wait until it is finished
        time.sleep(maxMoveTime)


# Robot communication to check the actual status of neighbouring boxes
def check_real_neighbours(label, sender):
    global contador, cellY, cellX, xlength, obstacles, robotDirection, robotPath, nearestCell
    # FOR SIMULATION ONLY
    if experiment >= 1:
        # For each direction
        for i in range(4):
            # Position and state of the neighbour step
            position = -1
            state = -1

            # Ignore the back of the robot
            if (i+2)%4 == robotDirection:
                continue

            # i = 0 -> TOP -> avoid wall
            if (i == 0) and not (cellY-1 < 0):
                position = (cellY-1) * xlength + cellX + 1
            # i = 1 -> LEFT -> avoid wall
            if (i == 1) and not (cellX - 1 < 0):
                position = cellY * xlength + cellX - 1 + 1
            # i = 2 -> BOTTOM -> avoid wall
            if (i == 2) and not (cellY + 1 >= ylength):
                position = (cellY+1) * xlength + cellX + 1
            # i = 3 -> RIGHT -> avoid wall
            if (i == 3) and not (cellX + 1 >= xlength):
                position = cellY * xlength + cellX + 1 + 1

            # State depends on obstacle, path and next step
            if position == nearestCell[1] * xlength + nearestCell[0] + 1 or position == yend * xlength + xend + 1:
                # Next step and last cell are not in the path yet, so it have to avoid erase information
                pass
            elif position in obstacles:
                # If there are obstales, mark it
                state = 6 + cueSizeInBin
            elif not(position == -1) and not(position in robotPath) and not backtracking:
                # To give a cell a free state, positions in robot path and cells in backtracking have to be avoided
                state = 5 + cueSizeInBin

            # Make the learning of the real (simulated) neighbours state
            if not(position == -1) and not(state == -1):
                reinforced_learning(label, sender, memory_sweep.int_to_binary_int(position) + [state], operationTime)

    # FOR EMULATION WITH REAL ROBOT ONLY
    if experiment == 0:
        global send_udp, rcv_udp
        # Send robot signal to begin the scanning of neighbours: command = 5
        readCommand = 5
        send_udp.sendto(readCommand.to_bytes(1, byteorder="little"), ("192.168.4.1", 8888))
        # Receive the real state of neighbours: 5 = free and 6 = obstacle
        #  + Right state
        packet = rcv_udp.recvfrom(64)
        byte = packet[0]
        rightState = int.from_bytes(byte, byteorder="little", signed=False)
        time.sleep(0.2)
        #  + Front state
        packet = rcv_udp.recvfrom(64)
        byte = packet[0]
        frontState = int.from_bytes(byte, byteorder="little", signed=False)
        time.sleep(0.2)
        #  + Left state
        packet = rcv_udp.recvfrom(64)
        byte = packet[0]
        leftState = int.from_bytes(byte, byteorder="little", signed=False)
        time.sleep(0.2)
        # Add to array to facilitate the processing
        states = [rightState, frontState, leftState]

        if debugLevel >= 2:
            print_condition.acquire()
            print("State right: " + str(rightState))
            print("State front: " + str(frontState))
            print("State left: " + str(leftState))
            print_condition.release()

        # Convert local state to global state
        localStatesPositions = [robotDirection-1%4, robotDirection, robotDirection+1%4]

        # Change memory map state with real state (reinforce learning)
        for index, state in enumerate(states):
            # Transform local position of the state to x and y coordinates
            localCellX = cellX
            localCellY = cellY
            # TOP
            if localStatesPositions[index] == 0:
                localCellY = localCellY - 1
                # Avoid walls
                if (localCellY < 0):
                    continue
            # LEFT
            if localStatesPositions[index] == 1:
                localCellX = localCellX - 1
                # Avoid walls
                if (localCellX < 0):
                    continue
            # BOTTOM
            if localStatesPositions[index] == 2:
                localCellY = localCellY + 1
                # Avoid walls
                if (localCellY >= ylength):
                    continue
            # RIGHT
            if localStatesPositions[index] == 3:
                localCellX = localCellX + 1
                # Avoid walls
                if (localCellX >= xlength):
                    continue
            # Check and avoid restrictions
            position = localCellY * xlength + localCellX + 1
            if position == nearestCell[1] * xlength + nearestCell[0] + 1 or position == yend * xlength + xend + 1:
                # Next step and last cell are not in the path yet, so it have to avoid erase information
                continue
            elif position in robotPath or backtracking:
                # Positions in robot path and cells in backtracking have to be avoided
                continue
            elif position in obstacles:
                # Avoid overwrite obstacles
                continue

            # Make the learning of the real neighbours state
            reinforced_learning(label, sender, memory_sweep.int_to_binary_int(position) + [state + cueSizeInBin], operationTime)

            # If obstacle, add to the list of obstacles
            if state == 6:
                obstacles.append(position)

    # Time to let learning operation finish
    time.sleep(operationTime / 2)

#############################################
# Tools
#############################################


# Converts from ids of neurons which fired to the cell x and y axis coded
def neuron_ids_to_cell_coordinate(neuron_ids):
    global xlength
    cellID = -1
    for neuronID in neuron_ids:
        if neuronID < cueSizeInBin:
            cellID = cellID + 2 ** neuronID
    return cellID % xlength, int(cellID / xlength)


# Get list of cells with the nearest distance to the target with manhattan distance
def manhattan_nearest_cell_to_target(target, cells):
    nearestCells = None
    nearestDistance = -1
    # For each cell
    for cell in cells:
        distance = abs(cell[0] - target[0]) + abs(cell[1] - target[1])
        # Compare and choose the nearest and set of nearest
        if nearestDistance == -1 or distance <= nearestDistance:
            if distance == nearestDistance:
                nearestCells.append(cell)
            else:
                nearestCells = [cell]
            nearestDistance = distance
    return nearestCells


# Write data in file and create path if it not exist
def check_folder_and_create_file(data, path, fileName):
    # Check if folder exist, if not, create it
    if not os.path.isdir(path):
        os.mkdir(path)
    # Create file and write data
    file = open(path + fileName, "w")
    file.write(str(data))
    file.close()


#############################################
# Main simulation
#############################################


def real_time_map_and_nav():
    global finish

    ######################################
    # Simulation parameters
    ######################################
    # Setup simulation
    sim.setup(timeStep)

    ######################################
    # Live tools
    ######################################
    # LIVE SENDER CONNECTION
    # Set up the live connection for sending spikes
    live_spikes_connection_send = sim.external_devices.SpynnakerLiveSpikesConnection(receive_labels=None,
                                                                                     local_port=None,
                                                                                     send_labels=["LiveInjectionLayer"])
    # Set up callbacks to occur at the start of simulation
    live_spikes_connection_send.add_start_resume_callback("LiveInjectionLayer", send_spikes_to)

    # LIVE RECEIVER CONNECTION
    # A new spynnaker live spikes connection is created to define that there is a python function which receives
    # the spikes.
    live_spikes_connection_receive = sim.external_devices.SpynnakerLiveSpikesConnection(
        receive_labels=["OLayer", "ILayer", "OPPCLayer"], local_port=None, send_labels=None)
    # Set up callbacks to occur when spikes are received
    live_spikes_connection_receive.add_receive_callback("OLayer", received_spikes)
    live_spikes_connection_receive.add_receive_callback("ILayer", received_spikes)
    live_spikes_connection_receive.add_receive_callback("OPPCLayer", received_spikes)

    ######################################
    # Create network
    ######################################
    # Input layer (live injection)
    LiveInjectionLayer = sim.Population(numInputLayerNeurons+1, sim.external_devices.SpikeInjector(
        database_notify_port_num=live_spikes_connection_send.local_port),
                                        label='LiveInjectionLayer',
                                        additional_parameters={'virtual_key': 0x70000, })

    # Input layer (real input population to debug): fire a spike when receive a spike
    neuronParameters = {"cm": 0.27, "i_offset": 0.0, "tau_m": 3.0, "tau_refrac": 1.0, "tau_syn_E": 0.3,
                        "tau_syn_I": 0.3,
                        "v_reset": -60.0, "v_rest": -60.0, "v_thresh": -57.5}
    ILayer = sim.Population(numInputLayerNeurons+1, sim.IF_curr_exp(**neuronParameters), label="ILayer")

    # Output memory layer: fire a spike when receive a spike
    OLayer = sim.Population(numInputLayerNeurons, sim.IF_curr_exp(**neuronParameters), label="OLayer")
    # Output ppc layer: fire a spike when receive a spike -> 4 possible directions commands
    OPPCLayer = sim.Population(4, sim.IF_curr_exp(**neuronParameters), label="OPPCLayer")

    # Memory:
    memory = hippocampus_with_forgetting.Memory(cueSize, contSize, sim, sim.PopulationView(LiveInjectionLayer, range(numInputLayerNeurons)), OLayer)

    # PPC
    ppc = posterior_parietal_cortex.PPC(sim.PopulationView(LiveInjectionLayer, [numInputLayerNeurons]),
                                        sim.PopulationView(memory.CA3contLayer, [2, 3, 4]),
                                        OPPCLayer, 4, operationTime*1000, 0.007*1000, sim)

    # Create extra synapses
    sim.Projection(LiveInjectionLayer, ILayer, sim.OneToOneConnector(), sim.StaticSynapse(weight=6.0))

    ######################################
    # Parameters to store
    ######################################
    # Activate the sending of live spikes
    sim.external_devices.activate_live_output_for(OLayer,
                                                  database_notify_port_num=live_spikes_connection_receive.local_port)
    sim.external_devices.activate_live_output_for(ILayer,
                                                  database_notify_port_num=live_spikes_connection_receive.local_port)
    sim.external_devices.activate_live_output_for(OPPCLayer,
                                                  database_notify_port_num=live_spikes_connection_receive.local_port)

    OLayer.record(["spikes"])
    OPPCLayer.record(["spikes"])

    ######################################
    # Execute the simulation
    ######################################
    sim.run(simTime)

    # End threads if the keep
    finish = True

    # Get STDP weight data
    w_ca3_learning = memory.CA3cueL_CA3contL_conn.get('weight', format='list', with_address=True)
    # Get data from Output Memory
    OUTMemSpikes = OLayer.get_data(variables=["spikes"]).segments[0].spiketrains
    formatOUTMemSpikes = []
    for neuron in OUTMemSpikes:
        formatOUTMemSpikes.append(neuron.as_array().tolist())
    # Get data from Output PPC
    OUTPPCSpikes = OPPCLayer.get_data(variables=["spikes"]).segments[0].spiketrains
    formatOUTPPCSpikes = []
    for neuron in OUTPPCSpikes:
        formatOUTPPCSpikes.append(neuron.as_array().tolist())

    ######################################
    # End simulation
    ######################################
    sim.end()

    return w_ca3_learning, formatOUTMemSpikes, formatOUTPPCSpikes


# Define and calculate the initial value of global params that not depends on the user
def init_global_params():
    global cueSize, contSize, cueSizeInBin, numInputLayerNeurons, searchingNeighbour, cellX, cellY, lastCellX, lastCellY,\
        nextCellX, nextCellY, nextCellFound, obstacleCells, freeCells, lastCell, lastNeuronsId, command,\
        searchCommandFinish, searchCommandBegin, timeStep, debug, debugLevel, experimentName, filePath, numStates, \
        robotPath, backtracking, crossroadCell, unachievable, iterationsRepeated, finish, \
        nearestCell, send_udp, rcv_udp
    # Network parameters:
    # + Number of directions of the memory -> one for each cell in grid map
    cueSize = xlength * ylength
    # + Size of the patterns in bits/neuron -> one for each possible state of a cell
    contSize = numStates
    # + Number of neurons in input layer: the number of bits neccesary to represent the number of directions in
    # binary + the size of patterns
    cueSizeInBin = math.ceil(math.log2(cueSize + 1))
    numInputLayerNeurons = cueSizeInBin + contSize

    # Simulation time parameters
    # + Time step of the simulation
    timeStep = 1.0

    # Control state of the nav and map
    # + Indicate the receiver to proccess the input
    searchingNeighbour = False
    # + Coordinates of the last, current and next grid-cell
    cellX = xinit
    cellY = yinit
    lastCellX = xinit
    lastCellY = yinit
    nextCellX = xinit
    nextCellY = yinit
    # + Next cell found
    nextCellFound = False
    # + Cells with obstacle founds in the current step
    obstacleCells = []
    # + Cells free founds in the current step
    freeCells = []
    # + Last cell found
    lastCell = False
    # + Last neurons id which spikes has been received
    lastNeuronsId = []
    # + Crossroad cell found
    crossroadCell = False
    # + Nearest free cell to the current step
    nearestCell = [0,0]

    # + Next robot movement command
    command = 0
    # + Indicate if command search is finished
    searchCommandFinish = False
    #  + Indicate if command search is beginning
    searchCommandBegin = False
    #  + Indicate if robot is making backtracking searching another path or following the normal path
    backtracking = False

    #  + Indicate if target is unachievable
    unachievable = False
    #  + Count repeated iterations
    iterationsRepeated = 0
    #  + If target achieved or simulation end
    finish = False

    # Sockets
    if experiment == 0:
        send_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        rcv_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        rcv_udp.bind(("192.168.4.2", 8889))

    # Path of the robot
    robotPath = [yinit * xlength + xinit + 1]

    # File creation
    filePath = "results/" + experimentName + "/"

    # Debug
    if debugLevel == 0:
        debug = False
    else:
        debug = True


def main():
    # Initialize global params that not depends on the user
    init_global_params()

    # Get initial map state (start and end cells only)
    initial_map_state = np.zeros((ylength, xlength), dtype=int)
    initial_map_state[yinit][xinit] = 1
    initial_map_state[yend][xend] = 2
    if debugLevel >= 1:
        print("Initial map = \n" + str(initial_map_state))

    # Run the map and nav app
    final_path_w, formatOUTMemSpikes, formatOUTPPCSpikes = real_time_map_and_nav()

    # Memory sweep to recreate the final map state
    final_map_state = memory_sweep.simulate_memory_sweep(final_path_w, numInputLayerNeurons, xlength, ylength, cueSizeInBin,
                                                   timeStep, cueSize, contSize, debug)

    # Store the weight and map state
    if write:
        check_folder_and_create_file(initial_map_state, filePath, "initial_map_formatted.txt")
        check_folder_and_create_file(initial_map_state.tolist(), filePath, "initial_map.txt")
        check_folder_and_create_file(final_path_w, filePath, "final_w.txt")
        check_folder_and_create_file(final_map_state, filePath, "final_map_formatted.txt")
        check_folder_and_create_file(final_map_state.tolist(), filePath, "final_map.txt")
        check_folder_and_create_file(formatOUTMemSpikes, filePath, "out_mem_spikes.txt")
        check_folder_and_create_file(formatOUTPPCSpikes, filePath, "out_ppc_spikes.txt")


if __name__ == "__main__":
    # Init app
    main()


