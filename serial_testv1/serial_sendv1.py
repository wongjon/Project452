import numpy as np
from serial import Serial

filter_coeff = np.linspace(0,10,11)
ser = serial.Serial()
"""("/dev/ttyACMO", 9600, timeout=None)
for i in filter_coeff:
    ser.write(array[i])
    """