import numpy as np
from scipy.fftpack import fft, ifft, fftshift
from scipy.io import wavfile


# Take in 2 wav files and output a matrix of coefficients
# Note: fsR and fsT should be equal to prevent sampling frequency discrepencies
import matplotlib.pyplot as plt
# Teceived tone
fsR, received = wavfile.read("received.wav")
wR16 = np.asarray( received/abs(received).max() * (1<<15), np.int16)
receivedF = fft(received)
print("received.wav array: ", received)
print("received.wav fft: ", receivedF) 

# Test tone
fsT, test = wavfile.read("test.wav")
wT16 = np.asarray(test/abs(test).max() * (1<<15), np.int16)
testF = fft(test)
print("test.wav array: ", test)
print("received.wav fft: ", testF)

# Dynamic Filter h(t) = IFFT{Y(S)/X(S)}
filterF = testF/receivedF
filter = ifft(filterF)
print("filter(w): ", filterF)
print("filter(t): ", filter)

# Check: x(t)*h(t) = y(t)
# testOut should be close to test.wav
testOut = np.convolve(received, filter)
print("testOut: ", testOut)


# Spectrogram
from pylab import show, semilogy
from scipy.signal import welch
show()
semilogy(*welch(test), "b") # test.wav is blue
semilogy(*welch(received), "g") # received.wav is green
semilogy(*welch(filter), "r") # dynamic filter is red
semilogy(*welch(testOut), "k") # testOut is black. This should be close to test.wav
show()


