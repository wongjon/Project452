# EECS 452 Project W21
## 3-D Optimization Tool
Contributors: Arjun Chandresekhar, Ravynne Jenkins, Stephen Lee, Jonathan Wong


Uniqnames: arjuncha, ravyjenk, steptlee, wongjon

## Overview
This folder contains the code in development for the 3-D Optimization Tool project. Software in the `component_software` contain component code at various time stamps. Files with the extension `_DEBUG` are not stable, while files without this extension can be run. `passthrough_filt` contains a filter that allows audio to be passed through the Teensy with no alteration. `serial` contains code that opens a UART bridge to the Teensy and allows coefficients to be sent to the Teensy from the Raspberry Pi 4. This is not yet complete. `singleiter` contains the main code that will be run on the Raspberry Pi 4.

## Requirements
Ensure the Teensy allows for a 6000 taps filter. Go to `arduino-1.8.13 → hardware → teensy → avr → libraries → Audio → filter_fir.h` and redefine `FIR_MAX_COEFFS` as `6000`. Check to see if the serial python library contains the function `Serial`. Flash the `passthrough_filt.ino` onto the Teensy using the Arduino IDE.
  
## Single Iteration Method
Instructions on how to operate the `single_iter.py` code are built into the file. When choosing the filter generation file, use `filter_gen1.wav`. 

## Iterative Method
Bulk of the code has been completed. The only things under development is incorporating in the serial sending method developed and implementation of the code fragments that allow parsing and interpreations of the information send through serial.

## Deliverables
The final presentation, poster and report are uploaded in this folder. Video demos are uploaded in the `videos` folder.