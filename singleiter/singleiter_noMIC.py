# Libraries
from scipy.fftpack import fft, ifft
from scipy.io import wavfile
import pyaudio
import wave
import numpy as np
from collections import deque
import sounddevice as sd
import time
import os.path

# Goal: Input 2 wav files and output a matrix of coefficients

# Received tone
fsR, received = wavfile.read("center_received.wav")
received_init = fft(received)

# Test tone
fsT, test = wavfile.read("center.wav")
testF = fft(test)

# fsR and fsT should be equal to prevent sampling frequency discrepencies
if fsT != fsR:
    print("received.wav and test.wav do not have the same sampling rate")
    exit()
    
# ENSURE LENGTH OF TEST AND RECEIVED ARE SAME
if len(received_init) == len(testF):  # same size, no change
    print("Same size")
    receivedF = received_init
elif len(received_init) < len(testF):  # rec is smaller, concat first elems onto beginning of rec
    print("received smaller than test")
    diff = len(testF) - len(received_init)
    receivedF = np.concatenate((testF[0:(diff)], received_init))
elif len(received_init) > len(testF):  # rec is larger, remove last elem, concat first elems
    print("received larger than test")
    diff = len(received_init) - len(testF)
    copy = received_init[0:(len(received_init) - (2 * diff))]
    receivedF = np.concatenate((testF[0:(diff)], copy))

# FILTER CALCULATION
filterF = testF / receivedF
pre_filter = ifft(filterF)  # h(t) = IFFT{Y(S)/X(S)}
pre_filter = np.around(abs(pre_filter))
coefficients = pre_filter.astype(int)

print("Generated filter: ", coefficients)

# INITIALIZE EMPTY HEADER FILE
file_path = input("Enter file path of directory (Ex. /home/pi/Desktop/Project452/filters): ")
size = str(0)
directory = file_path #folder path
#get file path
headerPath = os.path.join(directory, "filters" + '.h')

# CREATE HEADER FILE
with open(headerPath, 'w') as headerFile:
    headerFile.write('#include <stdint.h>')
    headerFile.write('\n#define FILT_L = ' + size + '\n\n')
    headerFile.write('int16_t FILT[' + size + '] = {' + '\n')
    headerFile.write('    ')
    for n in coefficients:
        n = str(n)
        headerFile.write(n + ',')
    headerFile.write('};')
p = input("Acknowledge you have flashed the Teensy with new coefficients: ")
