# Libraries
import pyaudio
import wave
import numpy as np
from scipy.fftpack import fft, ifft
from scipy.io import wavfile
from collections import deque
import sounddevice as sd
import time
import serial
import os.path


p  = input("Acknowledge you have copied filter_fir.cpp into the correct directory")

# TEST TONE (change file to whatever is being tested)
test_file = input("Enter name of test tone file: ")
file_path = input("Enter file path of directory (Ex. /home/pi/Desktop/EECS452/Project/filters): ")
fsT, test_tone = wavfile.read(test_file)
const_len = len(test_tone)
print("Test tone sampling rate: ", fsT)
print("Length of test tone array: ", const_len)

# INITIALIZE EMPTY HEADER FILE
size = str(0)
directory = file_path #folder path
#get file path
headerPath = os.path.join(directory, "filter" + '.h')

# CREATE HEADER FILE
# defineGuard = itemName.upper() + '_H_INCLUDED'
with open(headerPath, 'w') as headerFile:
    headerFile.write('#include <stdint.h>')
    headerFile.write('\n#define BPL ' + size + '\n\n')
    headerFile.write('real64_t BP[' + size + '] = {' + '\n')
    headerFile.write('    ')
    headerFile.write('};')

p = input("Acknowledge that you have flashed the Teensy: ")

# START LOOP: WHILE "EXIT" IS NOT TRUE
exit = False
x = 99 # Allow up to 50% error
error = 100 # begin with 100% error
register = deque([], 2)
register.append([10])
register.append([1])

while exit == False:
    if error > x:

        # PLAY START_TONE & TEST TONE AND BEGIN RECORDING WAV FILE
        ft, startTone = wavfile.read("start_tone.wav")
        np.asarray(startTone)   # Start Tone (const gain for 2 sec)
        np.asarray(test_tone)        # Test Tone (ex. center.wav)
        dur_sec = len(test_tone) / float(fsT)
        print(test_file, " is ", dur_sec, " seconds long ")
        
        sd.play(startTone)
        sd.wait()
        time.sleep(2)
        sd.play(test_tone)
        print("Playing ", test_file)

        # RECORD AND WRITE TO WAV FILE
        # ACTIVATE MICROPHONE 
        form_1 = pyaudio.paInt16 # 16-bit resolution
        chans = 1 # 1 channel
        samp_rate = fsT # 48kHz sampling rate
        chunk = 4096 # 2^12 samples for buffer
        dev_index = 2 # device index found by p.get_device_info_by_index(ii)
        audio = pyaudio.PyAudio() # create pyaudio instantiation

        # create pyaudio stream
        stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                            input_device_index = dev_index,input = True, \
                            frames_per_buffer=chunk)
        print("mic active")
        
        # RECORD TO ARRAY
        record_secs = dur_sec # seconds to record
        wav_output_filename = "received.wav" # name of .wav file
        print("recording received.wav")
        frames = []
        for ii in range(0,int((samp_rate/chunk)*record_secs)):
            data = stream.read(chunk)
            frames.append(data)
        print("finished recording")

        # WRITE ARRAY TO WAV FILE
        print("writing to received.wav file")
        wavefile = wave.open(wav_output_filename,'wb')
        wavefile.setnchannels(chans)
        wavefile.setsampwidth(audio.get_sample_size(form_1))
        wavefile.setframerate(samp_rate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()
        print("received.wav file complete")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # FILTER GENERATION
        print("Continue process to find stable coefficients")
        fsR, received = wavfile.read("received.wav")
        received_init = fft(received)
        print("Received sampling rate: ", fsR)
        testF = fft(test_tone)
        
        if fsT != fsR:
            print("received.wav and test.wav do not have the same sampling rate")
            exit()

        # ENSURE LENGTH OF TEST AND RECEIVED ARE SAME
        if len(received_init) == len(testF): #same size, no change
            print("Same size")
            receivedF = received_init
            

        elif len(received_init) < len(testF): #rec is smaller, concat first elems onto beginning of rec
            print("received smaller than test")
            diff = len(testF) - len(received_init)
            receivedF = np.concatenate((testF[0:(diff)], received_init))

        elif len(received_init) > len(testF): #rec is larger, remove last elem, concat first elems
            print("received larger than test")
            diff = len(received_init) - len(testF)
            copy = received_init[0:(len(received_init) - (2*diff))]
            receivedF = np.concatenate((testF[0:(diff)], copy))

        # FILTER CALCULATION
        filterF = testF/receivedF
        pre_filter = ifft(filterF) # h(t) = IFFT{Y(S)/X(S)}
        filters = abs(pre_filter)
        print("Generated filter: ", filters)

        # SENDING FILTER TO TEENSY
        size = str(len(filters))
        directory = file_path #folder path
        #get file path
        headerPath = os.path.join(directory, "filter" + '.h')

        # CREATE HEADER FILE
        # defineGuard = itemName.upper() + '_H_INCLUDED'
        with open(headerPath, 'w') as headerFile:
            headerFile.write('#include <stdint.h>')
            headerFile.write('\n#define BPL ' + size + '\n\n')
            headerFile.write('real64_t BP[' + size + '] = {' + '\n')
            headerFile.write('    ')
            for n in filters:
                n = str(n)
                headerFile.write(n + ',')
            headerFile.write('};')
        p = input("Acknowledge you have flashed the Teensy with new coefficients: ")
        
        # ITERATIVE METHOD
        register.append(filters)
        a = register[0]
        b = register[1]
        a_len = len(a)
        b_len = len(b)

        if a_len == b_len: # must be CONSTANT length
            error_array = [abs(i-j)/i*100 for i,j in zip(a,b)] # Find percent error elementwise
            error = np.mean(error_array)
            print("Element wise error is: ", error_array)
            print("Average error is: ", error)
            time.sleep(4)
    
    else:
        print("Iteration complete and filter is stable")
        exit = True





