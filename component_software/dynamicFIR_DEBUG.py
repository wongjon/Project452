# Libraries
import numpy as np
from scipy.fftpack import fft, ifft, fftshift
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Goal: Input 2 wav files and output a matrix of coefficients

# Received tone
fsR, received = wavfile.read("leftandright_received.wav")
receivedF = fft(received)
print("received.wav array: ", received)
print("received.wav fft: ", receivedF) 

# Test tone
fsT, test = wavfile.read("leftandright.wav")
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
# MAYBE ADD ABSOLUTE VALUES???

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

# Stop process when coefficients stop changing with X% margin of error after Y iterations
# Arbitrarily say <2% error after 2 iterations
from collections import deque
register = deque([], 2)
register.extend(10)
register.extend(1) # ensures register isn't empty

[1,10]
register.extend(3)

[[h1,h2,h3,h4],[f1,f2,f3,f4],[g1,g2,g3,g4]]

error = [abs(i-j)/i*100 if i != 0 else None for i,j in zip(register(1), register(2))] # stack overflow
if error <= 0.02:
    exit()

# make a consecutive counter of ex. 10 times
counter = 0
if counter < 10: 
    
    counter = counter + 1
    


