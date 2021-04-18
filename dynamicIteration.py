# Libraries
import numpy as np
from scipy.fftpack import fft, ifft
from scipy.io import wavfile
from collections import deque


# Stop process when coefficients stop changing with X% margin of error after Y iterations
# Arbitrarily say <2% error after 2 iterations
register = deque([], 2)
register.append([10])
register.append([1]) # ensures register isn't empty
                     # Currently: register = [1, 10]

x = 10 # Allow up to 10% error
error = [100] # begin with 100% error
while x == 10:
    if any(y > x for y in error):
        print("Continue process to find stable coefficients")
        
        # GOAL: Input 2 wav files and output a matrix of coefficients
        # Teceived tone
        fsR, received = wavfile.read("received.wav")
        receivedF = fft(received)

        # Test tone
        fsT, test = wavfile.read("center.wav")
        testF = fft(test)
        print(fsT)

        # fsR and fsT should be equal to prevent sampling frequency discrepencies
        if fsT != fsR:
            print("received.wav and test.wav do not have the same sampling rate")
            exit()

        # Dynamic Filter h(t) = IFFT{Y(S)/X(S)}
        filterF = testF/receivedF
        filter = ifft(abs(filterF))
        
        # GOAL: Compare previous filter and repeat if error is too great
        # Iterative Method
        register.append(filter) # Currently: register = [10, [filter(1), filter(2), ...]]
                                # Will become: [[h1,h2,h3,h4], [f1,f2,f3,f4]]
        a = register[0]
        b = register[1]
        a_len = len(a)
        b_len = len(b)

        if a_len == b_len: # must be CONSTANT length
            error = [abs(i-j)/i*100 for i,j in zip(a,b)]
        
    else:
        print("Iteration complete")
        print(filter)
        exit()