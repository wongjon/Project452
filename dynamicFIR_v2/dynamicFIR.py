# Libraries
from scipy.fftpack import fft, ifft
from scipy.io import wavfile
import numpy as np

# Goal: Input 2 wav files and output a matrix of coefficients

# Received tone
fsR, received = wavfile.read("center_received.wav")
receivedF = fft(received)
received_init = receivedF


# Test tone
fsT, test = wavfile.read("center.wav")
testF = fft(test)

# fsR and fsT should be equal to prevent sampling frequency discrepencies
if fsT != fsR:
    print("received.wav and test.wav do not have the same sampling rate")
    exit()

# ENSURE LENGTH OF TEST AND RECEIVED ARE SAME
if len(received_init) == len(testF): #same size, no change
    print("Same size")
    receivedF = received_init
elif len(received_init) < len(testF): #rec is smaller, concat first elems onto beginning of rec
    print("received smaller than test")
    diff = len(testF) - len(received_init)
    receivedF = np.concatenate((testF[0:(diff)], received_init))
elif len(received_init) > len(testF): #rec is larger, remove last elem, concat first elems
    print("received larger than test")
    diff = len(received_init) - len(testF)
    copy = received_init[0:(len(received_init) - (2*diff))]
    receivedF = np.concatenate((testF[0:(diff)], copy))

# Dynamic Filter h(t) = IFFT{Y(S)/X(S)}
filterF = testF/receivedF
filter_i = ifft(filterF)
filter = abs(filter_i)
print(filter)

np.savetxt("coefficients.csv", filter, delimiter=",") # For debugging purposes

