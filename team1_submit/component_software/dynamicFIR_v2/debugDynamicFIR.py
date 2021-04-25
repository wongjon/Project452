# Libraries
import numpy as np
from scipy.fftpack import fft, ifft, fftshift
from scipy.io import wavfile
import matplotlib.pyplot as plt


# Goal: Input 2 wav files and output a matrix of coefficients

# Teceived tone
fsR, received = wavfile.read("received.wav")
receivedF = fft(received)
print("received.wav array: ", received)
print("received.wav fft: ", receivedF) 

# Test tone
fsT, test = wavfile.read("test.wav")
testF = fft(test)
print("test.wav array: ", test)
print("received.wav fft: ", testF)

# Note: fsR and fsT should be equal to prevent sampling frequency discrepencies
if fsT != fsR:
    print("received.wav and test.wav do not have the same sampling rate")
    exit()

# Dynamic Filter h(t) = IFFT{Y(S)/X(S)}
filterF = testF/receivedF
filter = ifft(filterF)
print("filter(w): ", filterF)
print("filter(t): ", filter)

# Check: x(t)*h(t) = y(t)
# testOut should be close to test.wav
testOut = np.convolve(received, filter) # takes a while
print("testOut: ", testOut)

# Frequency Response
from pylab import show, semilogy
from scipy.signal import welch
show()
semilogy(*welch(test), "b") # test.wav is blue
semilogy(*welch(received), "g") # received.wav is green
semilogy(*welch(filter), "r") # dynamic filter is red
semilogy(*welch(testOut), "k") # testOut is black. This should be close to test.wav
show()