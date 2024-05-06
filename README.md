# Machine Vision System for Conveyor System

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)

## General info

<p align="center">
  <img src="../main/VisionSystemScreenCap.gif">
</p>

A project as part of the mechatronics systems integration course, was to implement an improvement in the conveyor system used during our labs. This system consisted of several conveyor belts in a circle, each with a diverter arm. A camera at the start would detect the shape on the box and then sort it at the corresponding diverter arm. A problem that we noticed was that if the boxes were too close together on the conveyor belt, the diverter system would divert the whole group of boxes. This would cause the sorting of all following boxes to be incorrect. Our goal was to implement an addition to the current system to fix this problem.

The code provided here is just the portion which would detect whether or not the boxes were clumped together. This code was integrated with the existing conveyor system and sorting algorithm to preserve existing functionality.

Visit my portfolio [here](https://hariselva.github.io/Portfolio/) for more information about this and other projects.

## Technologies
* Python 3.9
* OpenCV (CV2 library)

