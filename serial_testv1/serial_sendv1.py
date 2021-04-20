import numpy as np
from serial import Serial

filter_coeff = np.linspace(0,10,11)
ser = Serial("/dev/ttyACM1", 9600, timeout=None)
for i in filter_coeff:
    ser.write((str(np.int(i)) + ',').encode('ascii'))
print('End')
    