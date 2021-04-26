# Source Code Usage
Contributors: Arjun Chandresekhar, Ravynne Jenkins, Stephen Lee, Jonathan Wong


Uniqnames: arjuncha, ravyjenk, steptlee, wongjon



## Requirements

### You will need:
* Raspberry Pi 4 or other Linux computer
* Teensy 4.1
* Teensy 4.1 audio shield
* Speaker sound system
* USB Microphone
* USB to micro USB cable
* Audio jack cables

### **Hardware**
Connect your Teensy 4.1 to your Raspberry Pi 4 via a USB to micro USB cable. Install Arduino IDE and Teensyduino here:
* Arduino IDE: https://www.arduino.cc/en/Main/Software
* Teensyduino: https://www.pjrc.com/teensy/td_download.html

Once installed, ensure the Teensy allows for a 6000 taps filter. Go to `arduino-1.8.13 → hardware → teensy → avr → libraries → Audio → filter_fir.h` and redefine `FIR_MAX_COEFFS` as `6000`. Check to see if the serial python library contains the function `Serial`. Flash the `passthrough_filt.ino` under the `passthrough_filt` directory onto the Teensy using the Arduino IDE.

### **Software**
Ensure your have the required software and libraries on your Raspberry Pi 4. You will need **Python 3** and the following libraries. You can install them using `pip`.

Python Libraries:
* pyaudio
* wave
* numpy
* scipy
* collections (for iterative method)
* time
* os.path
* matplotlib (for testing/debugging)

## Running Single Iter

The directory `singleiter` contains the software deliverable. Connect the microphone and Teensy to your Raspberry Pi 4 via USB. Use the Teensy audio shield to connect the Raspberry Pi 4 audio out to the Teensy audio in and the Teensy audio out to your speaker sound system. Flash `passthrough_filt.ino` as described above if you have not already done so.

Navigate to the `singleiter` directory and in the command line, run:
```
$ single_iter.py
```
The software will prompt you to acknowledge if you have flashed the passthrough filter. Press any key to continue.

You will be prompted to enter the test tone file. Enter:
```
filter_gen1.wav
```
`filter_gen.wav` is a 100 ms chirp that will be outputted by the speaker and used as the test tone in the calculations. 

You will then be prompted to enter the directory of the `filters` folder. If this project is placed on the Raspberry Pi 4 Desktop, an example path would be: 
```
/home/pi/Desktop/team1_submit/singleiter/filters
```

The software will play a two second start tone followed by `filter_gen.wav`. As soon as `filter_gen.wav` plays, the microphone will begin recording the audio. A `received.wav` will be generated that contains the recorded audio. The software will calculate the coefficients, convert them to **int16** and output them to the terminal.

The softwawre will also output the coefficients to a C Header File named `filters.h` in the `filters` directory. Once the header file has been generated, navigate to the `filters` directory and flash `filters.ino` onto the Teensy. This will flash the generated filter onto the Teensy. Acknowledge the process is complete by pressing any key.

## Using the Filter

Once `filters.ino` has been flashed onto the Teensy, the Teensy will apply the generated filter onto any incoming audio. The Teensy no longer needs the Raspberry Pi 4 and can be supplied with any USB power source. Connnect the Teensy audio in to any audio device, such as your laptop or phone, and the audio will automatically be filtered.

### Planned Features
Currently, only a single iteration of the filter coefficients is functional. A serial connection to the Teensy is under development so we can apply our iterative filter generation method. This ensures that the filter generated is stable. 

