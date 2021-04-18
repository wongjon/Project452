import os.path

# read in csv from Jon's code
#df = pd.read_csv('foo.csv', sep=',', header=None)
#print(df.values[1])

filters = [1, 2, 3, 4, 5]
size = str(len(filters))

#get the directory
directory = "/Users/Stephen/Documents/School/EECS452/speakerproject/" #folder path


#get file path
headerPath = os.path.join(directory, "filter" + '.h')

#create header
#defineGuard = itemName.upper() + '_H_INCLUDED'
with open(headerPath, 'w') as headerFile:
    headerFile.write('#include <stdint.h>')
    headerFile.write('\n#define BPL ' + size + '\n\n')
    headerFile.write('real64_t BP[' + size + '] = {' + '\n')
    headerFile.write('    ')
    for n in filters:
        n = str(n)
        headerFile.write(n + ',')
    headerFile.write('};')

