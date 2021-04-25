import serial
import numpy as np
import pandas as pd

import sys, datetime, os, os.path

# read in csv from Jon's code
#df = pd.read_csv('foo.csv', sep=',', header=None)
#print(df.values[1])

size = filter.len

def GetOption(option):
    if (option in sys.argv):
        index = sys.argv.index(option)
        if (len(sys.argv) < index + 1):
            print ('ERROR: Missing value for ' + option)
            ShowHelp()
            sys.exit()
        return sys.argv[index + 1]
    else:
        return False

#get the directory
directory = GetOption('--directory')
if (directory == False):
    directory = '.'

#get file path
headerPath = os.path.join(directory, "filter" + '.h')

#create header
defineGuard = itemName.upper() + '_H_INCLUDED'
with open(headerPath, 'w') as headerFile:

	headerFile.write('#include ' + defineGuard + '<stdint.h>' + '\n#define' + defineGuard + 'BPL ' + size + '\n\n')
	headerFile.write('real64_t BP[' + size + '] = {' + '\n') 
	
	headerFile.write('    ')
	
	for n in filter:
		headerFile.write(n + ',')

	headerFile.write('};')


# Connect to serial
ser = serial.Serial("/dev/ttyACM0", timeout=None)
# Read in array by index
ser.write(1)