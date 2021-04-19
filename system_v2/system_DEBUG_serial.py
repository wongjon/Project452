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
import pandas as pd

# TEST TONE (change file to whatever is being tested)
test_file = input("Enter name of test tone file: ")
fsT, test_tone = wavfile.read(test_file)
const_len = len(test_tone)
print("Test tone sampling rate: ", fsT)
print("Length of test tone array: ", const_len)

# START LOOP: WHILE "EXIT" IS NOT TRUE
exit = False
x = 10 # Allow up to 10% error
error = [100] # begin with 100% error
register = deque([], 2)
register.append([10])
register.append([1])

while exit == False:
    if any(y > x for y in error):

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
        
        record_secs = dur_sec # seconds to record
        wav_output_filename = "received.wav" # name of .wav file
        print("recording received.wav")
        frames = []
        for ii in range(0,int((samp_rate/chunk)*record_secs)):
            data = stream.read(chunk)
            frames.append(data)
        print("finished recording")

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
        receivedF = fft(received)
        print("Received sampling rate: ", fsR)
        testF = fft(test_tone)

        if fsT != fsR:
            print("received.wav and test.wav do not have the same sampling rate")
            exit()

        filterF = testF/receivedF
        filter = ifft(abs(filterF)) # h(t) = IFFT{Y(S)/X(S)}
        print(filter)
        np.savetxt("coefficients.csv", filter, delimiter=",") # Just for Debugging purposes

        # Connect to serial
        ser = serial.Serial("/dev/ttyACM0", timeout=None)
        # Read in array by index
        for i in filter:
            ser.write(i)
        
        # ITERATIVE METHOD
        register.append(filter)
        a = register[0]
        b = register[1]
        a_len = len(a)
        b_len = len(b)

        if a_len == b_len: # must be CONSTANT length
            error = [abs(i-j)/i*100 for i,j in zip(a,b)] # Find percent error elementwise
    
    else:
        print("Iteration complete; Filter optimized")
        exit = True
exit()




