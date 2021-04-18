# Libraries
from scipy.fftpack import fft, ifft
from scipy.io import wavfile
import numpy as np

# Goal: Input 2 wav files and output a matrix of coefficients

# Teceived tone
fsR, received = wavfile.read("received.wav")
receivedF = fft(received)

# Test tone
fsT, test = wavfile.read("test.wav")
testF = fft(test)

# fsR and fsT should be equal to prevent sampling frequency discrepencies
if fsT != fsR:
    print("received.wav and test.wav do not have the same sampling rate")
    exit()

# Dynamic Filter h(t) = IFFT{Y(S)/X(S)}
filterF = testF/receivedF
filter = ifft(filterF)
print(filter)

np.savetxt("foo.csv", filter, delimiter=",")

