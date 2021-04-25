# Source Code Overview
Contributors: Arjun Chandresekhar, Ravynne Jenkins, Stephen Lee, Jonathan Wong


Uniqnames: arjuncha, ravyjenk, steptlee, wongjon

`src` contains all the files developed during the project. 

---

## `component_software`
This folder contains all component software at various stages of development. They have been broken down into different software functions. For example, `microphone.py` is an example code that activates the microphone for 3 seconds and records a `.wav` file. 

Files that contain the extension `_DEBUG` are not stable and may have bugs. Files without this extension are stable and can be used as unit tests for various software components. 

The folders contain a working demo of the software function. For example, `dynamicFIR_v2` contains a working demo of reading in a test tone and received tone (both `.wav` files) and printing the filter coefficients to the terminal. 

## `passthrough_filt`
This folder contains the code that flashes a passthrough filter onto the Teensy. After the **Requirements** have been met, the user can flash `passthrough_filt.ino` software onto the Teensy. This generates a passthrough filter that does not alter any audio. This creates a starting point that the user can compare the new generated filter to. The passthrough filter is simply the array: `[32767, 0, 0, 0]`.

## `serial`
This folder contains starting software to send data via UART from the Raspberry Pi 4 to the Teensy. This would be used for the iterative method so that the Teensy does not have to be reflashed every time a new filter is generated. The software is under development and is **not** functional.

## `singleiter`
This folder contains the main software deliverable that the user will run. `single_iter.py` will play a test tone to the speaker and record the audio via a microphone. It then generates a filter via a **C Header File** located in the folder `filters`. The user then uses `filters.ino` to flash the new filter onto the Teensy. 

**Note:** The filter does not automatically generate on the Teensy and must be flashed every time a new filter is generated. 