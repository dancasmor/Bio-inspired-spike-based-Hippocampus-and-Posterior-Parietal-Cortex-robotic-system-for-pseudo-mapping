# Bio-inspired spike-based Hippocampus and Posterior Parietal Cortex robotic system for environment pseudo-mapping and navigation

<h2 name="Description">Description</h2>
<p align="justify">
Code on which the paper entitled "Bio-inspired spike-based Hippocampus and Posterior Parietal Cortex robotic system for environment pseudo-mapping and navigation" is based, sent to a journal and awaiting review.
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

<strong>Abstract</strong>: 

<strong>Keywords</strong>: 

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
		<li><strong>sPyNNaker8</strong>: last stable version <a href="http://spinnakermanchester.github.io/development/gitinstall.html">compiled from source</a></li>
		<li><strong>numpy</strong> 1.21.4</li>
		<li><strong>matplotlib</strong> 3.5.0</li>
		<li><strong>sPyBlocks</strong>: 0.0.4</li>
	</ul>
</ol>
</p>
<p align="justify">
To run any script, follow the python nomenclature: 
<code>
python script.py
</code>
</p>


<h2 name="RepositoryContent">Repository content</h3>
<p align="justify">
<ul>
	<li><p align="justify"><a href="posterior_parietal_cortex.py">posterior_parietal_cortex.py</a>: </p></li>
	<li><p align="justify"><a href="real_time_map_and_nav_app.py">real_time_map_and_nav_app.py</a>: </p></li>
	<li><p align="justify"><a href="memory_sweep.py">memory_sweep.py</a>: </p></li>
	<li><p align="justify"><a href="plot.py">plot.py</a>: </p></li>
	<li><p align="justify"><a href="results/">results</a> folder: </p></li>
	<li><p align="justify"><a href="robot/">robot</a> folder: </p></li>
		<ul>
			<li><p align="justify"><a href="robot/robot_control/robot_control.ino">robot_control.ino</a>: </p></li>
			<li><p align="justify"><a href="robot/robot_wifi_redirect_udp/robot_wifi_redirect_udp.ino">robot_wifi_redirect_udp.ino</a>: </p></li>
		</ul>
</ul>
</p>


<h2 name="Usage">Usage</h2>
<p align="justify">
Still under construction.
</p>


<h2 name="CiteThisWork">Cite this work</h2>
<p align="justify">
Still under construction.
</p>


<h2 name="Credits">Credits</h2>
<p align="justify">
The author of the original idea is Daniel Casanueva-Morato while working on a research project of the <a href="http://www.rtc.us.es/">RTC Group</a>.

This research was partially supported by the Spanish grant MINDROB (PID2019-105556GB-C33/AEI/10.13039/501100011033). 

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
