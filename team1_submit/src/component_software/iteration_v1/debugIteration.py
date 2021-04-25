import numpy as np
from scipy.fftpack import fft, ifft, fftshift
from scipy.io import wavfile
import matplotlib.pyplot as plt
import debugDynamicFIR.py

# Stop process when coefficients stop changing with X% margin of error after Y iterations
# Arbitrarily say <2% error after 2 iterations
from collections import deque
register = deque([], 2)
register.extend(10)
register.extend(1) # ensures register isn't empty
                   # Currently: register = [1, 10]

register.extend(filter) # Currently: register = [10, [filter(1), filter(2), ...]]
                        # Will become: [[h1,h2,h3,h4], [f1,f2,f3,f4]]
i = register[1]
j = register[2]

error = [abs(i-j)/i*100 if i != 0 else None for i,j in zip(register(1), register(2))] # stack overflow
if error <= 0.02: # Error of 2%
    exit()

# make a consecutive counter of ex. 10 times
counter = 0
if counter < 10: 
    
    counter = counter + 1

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
    


