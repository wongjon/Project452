# EECS 452 Project W21
## 3-D Optimization Tool
Contributors: Arjun Chandresekhar, Ravynne Jenkins, Stephen Lee, Jonathan Wong
**UPDATE 4/18/21: Final Project submission is under team1_submit.**

## Overview
This folder contains the code in development for the 3-D Optimization Tool project. Software in the folders contain stable code at various time stamps. Software in the main folder is under development. Components and tests created during development are contained in the component_software folder. Files with the extension "_DEBUG" are not stable, while files without this extension can be run. Components and tests created during development are_

## Before Running
Before running:
  Go into arduino-1.8.13→hardware→teensy→avr→libraries→Audio→filter_fir.h and redefine FIR_MAX_COEFFS with 6000.
  Check to see if the serial python library contains the function Serial
  Flash the passthrough_filt.ino onto the Teensy
  
## Single Iteration Method
Instructions on how to operate the single_iter.py code are built into the file.
When choosing the filter generation file, use filter_gen1.wav

## Iterative Method
Bulk of the code has been completed. The only things under development is incorporating in the serial sending method developed and implementation of the code fragments that allow parsing and interpreations of the information send through serial.
