# Bio-inspired spike-based Hippocampus and Posterior Parietal Cortex robotic system for environment pseudo-mapping and navigation

<h2 name="Description">Description</h2>
<p align="justify">
Code on which the paper entitled "Bio-inspired spike-based Hippocampus and Posterior Parietal Cortex robotic system for environment pseudo-mapping and navigation" is based, published in Advanced Intelligent Systems journal.
</p>
<p align="justify">
A functional robotic system bio-inspired on Hippocampus and Posterior Parietal Cortex cerebral areas for environment pseudo-mapping and navigation implemented on the <a href="https://apt.cs.manchester.ac.uk/projects/SpiNNaker/">SpiNNaker</a> hardware platform using the technology of the Spiking Neuronal Network (SNN) is presented. The code is written in Python and makes use of the PyNN library and their adaptation for SpiNNaker called <a href="https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjaxOCWhrn3AhVL1BoKHVtQDvsQFnoECAkQAQ&url=https%3A%2F%2Fgithub.com%2FSpiNNakerManchester%2FsPyNNaker&usg=AOvVaw3e3TBMJ-08yBqtsKza_RiE">sPyNNaker</a>. Not only software tests of the system were carried out, but also a demo on a robotic platform based on a 2-wheeled car. In addition, the necessary scripts to replicate the tests, robotic demo and plots carried out in the paper are included, together with data and plots of these tests and demo.
</p>
<p align="justify">
Please go to section <a href="#CiteThisWork">cite this work</a> to learn how to properly reference the works cited here.
</p>

<h2>Table of contents</h2>
<p align="justify">
<ul>
<li><a href="#Description">Description</a></li>
<li><a href="#Article">Article</a></li>
<li><a href="#Instalation">Instalation</a></li>
<li><a href="#Usage">Usage</a></li>
<li><a href="#RepositoryContent">Repository content</a></li>
<li><a href="#CiteThisWork">Cite this work</a></li>
<li><a href="#Credits">Credits</a></li>
<li><a href="#License">License</a></li>
</ul>
</p>


<h2 name="Article">Article</h2>
<p align="justify">
<strong>Title</strong>: Bio-inspired spike-based Hippocampus and Posterior Parietal Cortex robotic system for environment pseudo-mapping and navigation

<strong>Abstract</strong>: The brain has a great capacity for computation, adaptability and efficient resolution of complex problems, far surpassing modern computers. In this regard, neuromorphic engineering seeks to mimic the basic principles of the brain to develop systems capable of achieving such capabilities. In the neuromorphic field, navigation systems are of great interest due to their potential applicability to robotics, although this systems are still a challenge to be solved. Navigation is possible due to the activity of differrent regions, such as the hippocampus and the Posterior Parietal Cortex. In this work, we propose a spike-based robotic navigation and environment pseudomapping system. This system is formed by a bio-inspired hippocampal memory model connected to a bio-inspired PPC model. The hippocampal memory is in charge of maintaining a representation of a state map of the environment, and the PPC is in charge of local decision-making. This system was implemented on the SpiNNaker hardware platform using Spiking Neural Networks. A set of real-time experiments was applied to demonstrate the correct functioning of the system components and the complete system in virtual and physical environments on a robotic platform. The system is able to navigate through the environment to reach a goal position starting from an initial position, avoiding obstacles and mapping the environment. To the best of the authors knowledge we propose the first implementation of an environment pseudo-mapping system with dynamic learning based on a bio-inspired spiking hippocampal memory.

<strong>Keywords</strong>: spatial navigation, environment state map, Spiking Neural Networks, Hippocampus, Posterior Parietal Cortex, Neuromorphic engineering, SpiNNaker

<strong>Author</strong>: Daniel Casanueva-Morato

<strong>Contact</strong>: dcasanueva@us.es
</p>


<h2 name="Instalation">Instalation</h2>
<p align="justify">
<ol>
	<li>Have or have access to the SpiNNaker hardware platform. In case of local use, follow the installation instructions available on the <a href="http://spinnakermanchester.github.io/spynnaker/6.0.0/index.html">official website</a></li>
	<li>Python version 3.8.10</li>
	<li>Python libraries:</li>
	<ul>
		<li><strong>sPyNNaker</strong></li>
		<li><strong>numpy</strong> 1.21.4</li>
		<li><strong>matplotlib</strong> 3.5.0</li>
		<li><strong>sPyMem</strong>: 0.0.4</li>
	</ul>
</ol>
</p>
<p align="justify">
To run any script, follow the python nomenclature: <code>python script.py</code>
</p>


<h2 name="RepositoryContent">Repository content</h3>
<p align="justify">
<ul>
	<li><p align="justify"><a href="posterior_parietal_cortex.py">posterior_parietal_cortex.py</a>: class that is responsible for the construction of the PPC module. This module has comparison inputs to which it reacts to generate output and the start-of-operation input that indicates when the hippocampal read cycle begins. It contains the necessary code so that when executed on its own, it generates the example plot of operation of the module itself.</p></li>
	<li><p align="justify"><a href="real_time_map_and_nav_app.py">real_time_map_and_nav_app.py</a>: script in charge of generating the navigation and pseudomapping system. Instantiates the previously existing hippocampus and PPC modules, generating the necessary connections to develop the complete system. The inputs and outputs of the system are defined for direct real-time operation, so both the software simulations and the demo use the same code.</p></li>
	<li><p align="justify"><a href="memory_sweep.py">memory_sweep.py</a>: a set of functions that calculate the input to be given to the system in order to perform a memory sweep to reconstruct the initial and/or final state of the grid map.</p></li>
	<li><p align="justify"><a href="plot.py">plot.py</a>: functions needed to generate the plots used to understand the correct functioning of the system and in the article.</p></li>
	<li><p align="justify"><a href="results/">results</a> folder: where the data and plots of the different simulations of the whole system are stored, as well as a demonstration of the operation of the PPC (posterior parietal cortex module) separately. These files contain the initial and final map in both a compact format for use in the code and in a more "user-friendly" and visual format for easy viewing by the user. They also contain the weights of the memory synapses after the simulation, i.e. the contents of the memory with the pseudomapping of the environment. Finally, it includes other files with the activity at the spike level of the memory and the PPC for the subsequent reconstruction of the desired plots.</p></li>
	<li><p align="justify"><a href="robot/">robot</a> folder: code of the robotic system in order to carry out the demo. The robotic system is divided into two boards and therefore two codes:</p></li>
		<ul>
			<li><p align="justify"><a href="robot/robot_control/robot_control.ino">robot_control.ino</a>: is responsible for motor control and collection of ultrasound measurements of the environment under explicit commands.</p></li>
			<li><p align="justify"><a href="robot/robot_wifi_redirect_udp/robot_wifi_redirect_udp.ino">robot_wifi_redirect_udp.ino</a>: in charge of the wifi communication between the robot and SpiNNaker. To do this, it generates a wifi network to which the system controlling SpiNNaker must connect and redirects the communication in both directions. Communication to the robot is via input and output pins, while communication to the system with SpiNNaker is direct via the serial port.</p></li>
		</ul>
</ul>
</p>


<h2 name="Usage">Usage</h2>
<p align="justify">
In order to use the system, you only need to define a set of global variables that define the scenario on which the system will operate and run the script <a href="real_time_map_and_nav_app.py">real_time_map_and_nav_app.py</a>. This script is in charge of instantiating the complete system with the configuration indicated through the variables defined above. Each simulation or demo must be identified by a unique id. The id of the experiment to be reproduced must be indicated at the beginning of the script. It is this number that will be used to distinguish within an if which set of global variables is used in the next execution of the system. These global variables are: 
</p>
<p align="justify">
<ul>
	<li><p align="justify"><strong>xlength and ylength</strong>: size of the grid map as a function of the number of rows (y-axis) and columns (x-axis).</p></li>
	<li><p align="justify"><strong>xinit, yinit, xend and yend</strong>: x and y coordinates of the initial and final positions of the robot within the grid map.</p></li>
	<li><p align="justify"><strong>experimentName</strong>: name of the experiment, used as the base for the name of the generated folders and files.</p></li>
	<li><p align="justify"><strong>simTime</strong>: duration of the simulation to be performed in miliseconds, in case of real time demo, use a very long duration.</p></li>
	<li><p align="justify"><strong>obstacles</strong>: the position within the grid map where the obstacles are located in the case of the software simulations or an empty list in the case of the demo.</p></li>
	<li><p align="justify"><strong>robotDirection</strong>: initial direction in which the robot is facing from a top-down perspective (0 = top, 1 = left, 2 = bottom, 4 = right).</p></li>
	<li><p align="justify"><strong>maxMoveTime</strong>: variable indicating the maximum time needed for the robot to move from one cell to another, taking into account turning times. It is only used for the real time demo.</p></li>
</ul>
</p>
<p align="justify">
There are other global variables that can be set, following the declaration of the experiment, however, it is recommended to leave them as default.
</p>
<p align="justify">
In the case of a software simulation, nothing more would need to be done, however, in the case of a demo on the robot, it would be necessary to have the robotic platform ready to send and receive the indicated commands. To reproduce the demo presented in the paper, a Romeo BLE board was used to control the hardware system and an Adafruit ESP32 Feather board for wifi communication. In case you want your own robotic platforms, you will have to adapt the code from the repository available in the <a href="robot/">robot</a> folder.
</p>
<p align="justify">
In both cases, after the end of the experiment, the relevant data from the simulation will be returned as a set of files under the folder with the name of the experiment. These files can then be used in the script called <a href="plot.py">plot.py</a> to generate the desired plots.
</p>


<h2 name="CiteThisWork">Cite this work</h2>
<p align="justify">
<b>APA</b>: Casanueva-Morato, D., Ayuso-Martinez, A., Dominguez-Morales, J.P., Jimenez-Fernandez, A., Jimenez-Moreno, G. and Perez-Peña, F. (2023), Bioinspired Spike-Based Hippocampus and Posterior Parietal Cortex Models for Robot Navigation and Environment Pseudomapping. Adv. Intell. Syst. 2300132. https://doi.org/10.1002/aisy.202300132
</p>
<p align="justify">
<b>BibTeX</b>: @article{https://doi.org/10.1002/aisy.202300132,
	author = {Casanueva-Morato, Daniel and Ayuso-Martinez, Alvaro and Dominguez-Morales, Juan P. and Jimenez-Fernandez, Angel and Jimenez-Moreno, Gabriel and Perez-Peña, Fernando},
	title = {Bioinspired Spike-Based Hippocampus and Posterior Parietal Cortex Models for Robot Navigation and Environment Pseudomapping},
	journal = {Advanced Intelligent Systems},
	pages = {2300132},
	doi = {https://doi.org/10.1002/aisy.202300132}
}
</p>


<h2 name="Credits">Credits</h2>
<p align="justify">
The author of the original idea is Daniel Casanueva-Morato while working on a research project of the <a href="http://www.rtc.us.es/">RTC Group</a>.

This research was partially supported by the CHIST-ERA H2020 grant SMALL (CHIST-ERA-18-ACAI-004, PCI2019-111841-2/AEI/10.13039/501100011033 and by project PID2019-105556GB-C33 funded by MCIN/ AEI /10.13039/501100011033.

D. C.-M. was supported by a "Formación de Profesor Universitario" Scholarship from the Spanish Ministry of Education, Culture and Sport.
</p>


<h2 name="License">License</h2>
<p align="justify">
This project is licensed under the GPL License - see the <a href="https://github.com/dancasmor/Bio-inspired-spike-based-Hippocampus-and-Posterior-Parietal-Cortex-robotic-system-for-pseudo-mapping/blob/main/LICENSE">LICENSE.md</a> file for details.
</p>
<p align="justify">
Copyright © 2022 Daniel Casanueva-Morato<br>  
<a href="mailto:dcasanueva@us.es">dcasanueva@us.es</a>
</p>

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
