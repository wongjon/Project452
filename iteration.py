import numpy as np
from collections import deque

register = deque([],2)
register.append([3,4,5])
register.append([4,5,6])
a = register[0]
b = register[1]
error = np.mean(a!=b)
print(error) # Output should be 1

register.append([0.642, 0.167, 1.856])
register.append([0.894, -0.057, 1.255])
a = register[0]
b = register[1]
error = np.mean(a!=b)
print(error) # Output should be

error = [abs(i-j)/i*100 for i,j in zip(a,b)]
print(error)

x = 10 # Allow up to 10% error
if any(y > x for y in error):
    print("Continue process to find stable coefficients")

else:
    print("Iteration complete")
    exit()