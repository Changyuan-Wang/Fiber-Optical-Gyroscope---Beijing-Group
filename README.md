# Fiber Optical Gyroscope (FOG) - Beijing Group
In this guide, we will introduce our project: a fiber optical gyroscope (FOG). The goal of this project was to use the Sagnac effect to build the gyroscope, let the gyroscope produce interference patterns, and apply labJack to convert the shifted fringes to a function of angular velocity. The figures of angular velocity can in turn check if our gyroscope is successful.  
  
We choose to build a fiber optical gyroscope instead of a mechanical gyroscope because FOG turns out to an elegant replacement for a mechanical gyroscope in the future. FOG exhibits some great features, like high accuracy, high reliability, high tolerance for shock, and absence of 'g' sensitivity. Even though FOG are typically larger and more expensive, it is a useful tool for inertial navigation and measuring rotations, and it may be more commonly applied later on as the technology of fibers grows [<cite>[1]</cite>]. FOG is an interesting topic with a promising future, so we decide to build one by ourselves and explore it in detail.

[1]: https://www.researchgate.net/publication/243781972_Fiber_Optic_Rate_Gyros_as_Replacements_for_Mechanical_Gyros

### Table of Contents

- [List of Components](#1-list-of-components)
- [Theory](#2-theory)
- [Design](#3-design)
- [Building Process](#4-building-process)
  * [Structure](#41-structure)
  * [Tips](#42-tips)
- [Code](#5-code)
- [Finished Product](#6-finished-project)
  * [Plots](#61-plots)
  * [Calibration Function](#62-calibration-function)
- [Anomaly](#7-anomaly)
- [Future Outlook](#8-future-outlook)
- [Contributors](#9-contributors)

# List of Components

- A turntable [two choices]:
  * Lazy susan (~¥100)
    + a minor disadvantage: most of the lazy susans can not rotate very fast.
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
- LabJack U3-HV (from PHYS CS 15A)

Note:
We bought all of the components in Beijing, China, so their prices are typically cheaper than those in the United States. Here is an example purchase link that includes most of the components for people in the US: https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=343.

The total investment (include shipping cost) is about \~¥1000 (\~$150), which is acceptable if we do not use some fancy part kits like polarization-maintaining optical fiber.

# Theory: Sagnac Effect
A beam of light is split into two and the two beams are made to follow the same path but in opposite directions. After looping around, they eventually arrive at the same point and we observe an interference pattern there. If the whole setup is at rest, the two beams will travel the same distance and there should be no interference pattern observed since there is no phase difference. If the whole setup is rotated at some angular velocity, the two beams will travel a different distance and generate a phase difference and hence produce an interference pattern.  
  
To summarize, if the setup makes lights travel in the opposite direction in a loop, rotation of the setup will cause an interference pattern. This effect is called the Sagnac effect.   
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Theory/Sagnac%20Effect.png)
  
This figure is credited to <cite>[Anthony Dandridge][2]</cite>.

[2]: https://www.researchgate.net/figure/Basic-optical-configuration-of-the-Sagnac-interferometer-and-Ring-resonator_fig2_243755491

# Design
This schematic diagram is the simplified version of our project. The coupler splits light evenly into two beams, which will go into opposite directions and come back to the coupler. The polarization controller can change the polarization of the two light. Before making the whole system wireless, it is easier to use this circuit to perform all kinds of testing. Later, the voltmeter shown in the diagram will be changed into labJack, and the process of transmitting data wirelessly is also related to labJack.  
  
To be noted, labJack can also provide power, so we can change the battery into labJack as well. The procedure of how to use labJack to provide power can be easily found online, and we will also mention it in the "Finished Produce - Structure" section.  
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Design/Circuit%20Diagram%20-%20Testing.png)

We used the magnetometer to measure the geomagnetic field, which will give us a function of angular velocity versus time. At the same time, the labJack will measure the voltage of the photodiode, which will be converted into a function of intensity over time because the voltage of a photodiode is proportional to the light intensity it receives. In the end, we will combine the angular velocity plot and the intensity plot into a function of angular velocity over intensity, which will help us measure the speed of rotation of this gyroscope.
  
The blue GY-511 module serves as a magnetometer. The magnetometer measures the magnetic field (Bx, By, Bz), and we use a coding program (goodbyemagnetometer.py) to convert the field information into a function of angular velocity versus time.
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Design/LabJack%20%26%20Magnetometer.png)
The idea of using tubes to construct the structure is credited to Qikai Gao at UC Davis.


# Building Process
## Structure
This is the finished gyroscope.  
  
The magnetometer is fixed at the center of the lazy susan because we want to avoid the effects of any other magnetic fields that are uneven through space.  
  
The gray box above the labJack implements USB virtualization. It transmits data from labJack to our computer wirelessly, and our coding program will automatically generate relevant plots, like the functions of magnetic field or light intensity over time.  
  
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Building%20Process/Structure.jpeg)
  
We used the labJack instead of AA batteries to provide power to the laser diode. The GND and DAC0 provide 1.2V to the laser diode, and the GND and AIN0 measure the voltage of the photodiode. There are a great number of advantages of using labJack instead of batteries. For example, the laser diode can only take a voltage of 1.2 ~ 1.5V, so most of the time we need to apply a voltage stabilizer to the AA batteries (6V in common). LabJack, however, can provide a stable voltage, and we can change its magnitude by using a small convenient program (included in the goodbyemagnetometer.py file). The black power bank in the corner will provide power to the labJack.  
  
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Building%20Process/Transforming%20to%20Wireless%20System.png)
  
  
This is a video showing how our project works: https://youtu.be/JSChJpj-myk.  
  
As we can see in the video, the reading in the multimeter is different if we rotate the gyroscope in different directions. Thus, we can use data to distinguish if the gyroscope is rotating in a clockwise or counterclockwise direction.

## Tips:
  - Material Selection  
    - The building process is actually relatively simple; the difficult approach is to select the appropriate/matching materials.
      * Fibers should be all single-mode or all multimode. Single-mode fibers are typically cheaper, so it is better to use them in labs.
      * All of the components should be in the same light range (e.g. 1310nm).
      * All of the components should have the same type of connectors (e.g. FC/APC).
  - Stabilization  
    - Since a small change in the geometry of the fibers will result in a big difference in interference patterns, we need to make sure that the whole system is stable.
    - After we have obtained a stable system, we can confidently claim that the changes in intensity data are due to rotation instead of distortion in geometry.
      + Battery - use a buck converter to stabilize the power
      + Fibers - use iron wires and tapes to ensure that when we rotate the whole structure, the geometry of cables do not change
   - Calibration
     - Since the geometry may be different every time we use the gyroscope, we need to calibrate our system each time before we use it. The calibration process will take less than 1 minute.

# Pipeline
We reused some of the codes in the file hellomagnetometer.py in PHYS CS 15A, which is credited to Dr. Patterson at UCSB. Yuan Li chooses to name our project's code file as <cite>[goodbyemagnetometer.py][3]</cite> because the coding was driving him crazy.

[3]: https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/blob/main/goobyeMagnetometer.py
  
The following is the structure of the pipeline.

![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Pipeline/Pipeline.png)

# Finished Products
## Plots
Since we align the x-axis of the magnetometer with the z-axis of the gyroscope (pointing upwards), the x-component of the magnetic field (Bx) is a constant (which makes sense).
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Magnetic%20Field%20(Bx%2C%20By%2C%20Bz).png)
When the gyroscope slows down naturally, the intensity decreases over time.
![Image](https://github.com/Changyuan-Wang/Fiber-Optical-Gyroscope---Beijing-Group/raw/main/IMG/Intensity%20v.s.%20Time%20(slows%20down).png)

## Calibration Function

# Anomaly

# Future Outlook


# Contributors
This project is made by Yuan Li, Changyuan Wang, and Haopu Yang under the supervision of Dr. Jayich in the course PHYS CS 15C at UCSB.
