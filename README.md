# Fiber Optical Gyroscope (FOG) - Beijing Group
In this guide, we will introduce our project: a fiber optical gyroscope (FOG). The goal of this project was to use the Sagnac effect to build the gyroscope, let the gyroscope produce interference patterns, and apply labJack to convert the shifted fringes to a function of angular velocity. The figures of angular velocity can in turn check if our gyroscope is successful. Now let's discuss our project in detail.


### Table of Contents

- [List of Components](#1-list-of-components)
- [Theory](#2-theory)
- [Design](#3-design)
- [Building Process](#4-building-process)
- [Code](#5-code)
- [Finished Product](#6-finished-project)
  * [Structure](#61-structure)
  * [Plots](#61-plots)
- [Contributors](#6-contributors)
  * [1.1 Purpose](#11-purpose)
  * [1.2 Scope](#12-scope)
  * [1.3 Acronyms](#13-acronyms)
  * [1.4 References](#14-references)
    + [1.4.1 Internal References](#141-internal-references)
    + [1.4.2 External References](#142-external-references)
  * [1.5 Overview](#15-overview)

# List of Components

- A turntable [two choices]:
  * Lazy susan (~¥100)
    + small disadvantage: most of the lazy susans can not rotate very fast.
  * We can also make one with a small turntable and cardboard (~¥20)
- Manual 3-Paddle Fiber Polarization Controller [1310nm] (~¥400)
- 1310nm FC/APC Single Mode Patch Cables (~¥115)
- 1310nm 2x2 Fiber Coupler (~¥50)
- 1310nm 5mW FP SM Laser Diode (~¥100)
- 75um 2.5GHZ Analog InGaAS PIN Photodiode (~¥40)
- FC/APC fiber adapters (~¥3 each, ~¥15 in total)
- 5A DC-DC Voltage Regulator Module (~¥15)
- GY-511 LSM303DLHC Magnetometer Module (~¥30)
- Wireless Network Print Server (~¥250)
  * This is to achieve a USB virtualization. We can use this print server to transfer data from labJack to our computer from a long distance without wires.
- Common components like breadboard, wires, batteries, switches, resistors (~¥10)
- Labjack HV (from PHYS CS 15A)

Note:
All of the components are bought in Beijing, China, so their prices are typically cheaper than those in the United States. Here is an example purchase link that include most of the components for people in the US: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=343.

The total investment (include shipping cost) is about ~¥1000 [~$150]. Comparing to buying a gyroscope directly [~  ], our project is about ___ times cheapter. 

# Theory: Sagnac Effect

# Design
This is the simplified version of our circuit diagram. Before making the whole system wireless, it is easier to use this diagram to perform all kinds of testing. Later, the voltimeter shown in the diagram will be changed into labJack, and the process of transmitting data wirelessly will also be involved in this section.
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Circuit%20Diagram%20-%20Testing.png)
The blue module serves as a magnetometer. The magnetometer measures the magnetic field (Bx, By, Bz), and we use a coding program (goodbyemagnetometer.py) to convert the field information into a function of angular velocity versus time.
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/LabJack%20%26%20Magnetometer.png)
The idea of using tubes to construct the structure is credited to Qikai Gao in UCD.


# Building Process
### Tips:
  - Material Selection  
    - The building process is actually relatively simple; the difficult approach is to select the approriate/matching materials.
      * Fibers should be all single mode or all multimode. Single mode fibers are typically cheaper, so it is better to use them in labs.
      * All of the components should be in the same light range (e.g. 1310nm).
      * All of the components should have the same type of connectors (e.g. FC/APC).
  - Stablization  
    - Since a small change in the geometry of the fibers will result in a big difference in interference patterns, we need to make sure that the whole system is stable.
    - After we have obtained a stable system, we can confidently claim that the changes in intensity data are due to rotation instead of distortion in geometry.
      + Battery - use a buck converter to stablize the power
      + Fibers - use iron wires and tapes to ensure that when we rotate the whole structure, the geometry of cables do not change

# Codes

# Finished Products
## Structure
This is the finished gyroscope.  
  
The magnetometer is fixed at the center of lazy susan, and we use it to measure the geomagnetic field. This is to avoid the effects of any other magnetic fields that are uneven through space.  
  
We used the labJack instead of AA batteries to provide power to the laser diode. The GND and DAC0 provide 1.2V to the laser diode, and the GND and AIN0 measure the voltage of the photodiode. There are a great number of advantages of using labJack instead of batteries. For example, the laser diode can only take a voltage of 1.2 ~ 1.5V, so most of the times we need to apply a voltage stabilizer to the AA batteries (6V in common). LabJack, however, can provide a stable voltage, and we can change its magnitude by using a small convenient program (mentioned in the code section). The black power bank in the corner will provide power for the labJack.  
  
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Structure.jpeg)
This is an video showing how our project works:


## Plots
Since we align the x-axis of the magnetometer with the z-axis of gyroscope (pointing upwards), the x-component of the magnetic field (Bx) is a constant (which makes sense).
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Magnetic%20Field%20(Bx%2C%20By%2C%20Bz).png)
When the gyroscope slows down naturally, the intensity decreases over time.
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Intensity%20v.s.%20Time%20(slows%20down).png)


# Contributors
This project is made by Yuan Li, Changyuan Wang, and Haopu Yang under the supervision of Dr. Jayich in the course PHYS CS 15C at UCSB.
