# Libraries
import pyaudio
import wave
import numpy as np
from scipy.fftpack import fft, ifft
from scipy.io import wavfile
from scipy.signal import find_peaks
from collections import deque
import sounddevice as sd
import time
import os.path
from scipy.io.wavfile import write
audio = pyaudio.PyAudio()
p  = input("Acknowledge you have flashed the pass-through filter")

# TEST TONE (change file to whatever is being tested)
test_file = input("Enter name of test tone file: ")
file_path = input("Enter file path of directory (Ex. /home/pi/Desktop/Project452/singleiter/filters): ")
fsT, test_tone = wavfile.read(test_file)
const_len = len(test_tone)
print("Test tone sampling rate: ", fsT)
print("Length of test tone array: ", const_len)

# INITIALIZE EMPTY HEADER FILE
size = str(0)
directory = file_path #folder path
#get file path
headerPath = os.path.join(directory, "filters" + '.h')

# PLAY START_TONE & TEST TONE AND BEGIN RECORDING WAV FILE
ft, startTone = wavfile.read("start_tone.wav")
np.asarray(startTone)  # Start Tone (const gain for 2 sec)
np.asarray(test_tone)  # Test Tone (ex. center.wav)
dur_sec = len(test_tone) / float(fsT)
print(test_file, " is ", dur_sec, " seconds long ")

sd.play(startTone)
sd.wait()
time.sleep(2)

sd.play(test_tone)
"""
myrecording = sd.rec(int(dur_sec * ft), samplerate=ft, channels = 1)
sd.wait()
print("Playing ", test_file)


#sd.wait()
write('received.wav', ft, myrecording)
"""


# RECORD AND WRITE TO WAV FILE
# ACTIVATE MICROPHONE
form_1 = pyaudio.paInt16  # 16-bit resolution
chans = 1  # 1 channel
samp_rate = fsT  # kHz sampling rate defined by test tone
chunk = 4096  # 2^12 samples for buffer
dev_index = 2  # device index found by p.get_device_info_by_index(ii)
audio = pyaudio.PyAudio()  # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format=form_1, rate=samp_rate, channels=chans, \
                    input_device_index=dev_index, input=True, \
                    frames_per_buffer=chunk)
print("mic active")

# RECORD TO FRAMES ARRAY
record_secs = dur_sec  # seconds to record
wav_output_filename = "received.wav"  # name of .wav file
print("recording received.wav")
frames = []
for ii in range(0, int((samp_rate / chunk) * record_secs)):
    data = stream.read(chunk)
    frames.append(data)
print("finished recording")

# WRITE FRAMES ARRAY TO WAV FILE
print("writing to received.wav file")
wavefile = wave.open(wav_output_filename, 'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form_1))
wavefile.setframerate(samp_rate)
wavefile.writeframes(b''.join(frames))
wavefile.close()
print("received.wav file complete")

# STOP MICROPHONE STREAM
stream.stop_stream()
stream.close()
audio.terminate()

# FILTER GENERATION
print("Continue process to find stable coefficients")
fsR, received = wavfile.read("received.wav")
received_init = fft(received)
print("Received sampling rate: ", fsR)
testF = fft(test_tone)
peaks_full_neg = find_peaks(-testF, height = 2e7)
peaks_neg = peaks_full_neg[0]


if fsT != fsR:  # Ensure same sampling rate
    print("received.wav and test.wav do not have the same sampling rate")
    exit()

# ENSURE LENGTH OF TEST AND RECEIVED ARE SAME
if len(received_init) == len(testF):  # same size, no change
    print("Same size")
    receivedF = received_init
elif len(received_init) < len(testF):  # rec is smaller, concat first elems onto beginning of rec
    print("received smaller than test")
    diff = len(testF) - len(received_init)
    print(diff)
    receivedF = np.concatenate((testF[0:(diff)], received_init))
elif len(received_init) > len(testF):  # rec is larger, remove last elem, concat first elems
    print("received larger than test")
    diff = len(received_init) - len(testF)
    copy = received_init[0:(len(received_init) - (2 * diff))]
    receivedF = np.concatenate((testF[0:(diff)], copy))

# FILTER CALCULATION
filterF = testF / receivedF
print(peaks_neg)
filterF = filterF[(peaks_neg[0]):(peaks_neg[1])]
print("Filterf: ", filterF)
pre_filter = ifft(filterF)  # h(t) = IFFT{Y(S)/X(S)}
print("Prefilter: ", pre_filter)
pre_filter = abs(pre_filter)
print("Prefilter abs: ", pre_filter)
coefficients_max = max(pre_filter)
#coefficients_max = 1 #comment out
coefficients_scale = int(32767 / coefficients_max)
coefficients_double = coefficients_scale * pre_filter
coefficients = coefficients_double.astype(int)


size = str(len(coefficients))
print("Generated filter: ", coefficients)
"""
coefficients = np.zeros(6000)
coefficients[0] = int(32767)
size = str(len(coefficients))
print(len(coefficients))
"""

# CREATE HEADER FILE
# defineGuard = itemName.upper() + '_H_INCLUDED'

with open(headerPath, 'w') as headerFile:
    headerFile.write('#include <stdint.h>')
    headerFile.write('\n#define FILT_L = ' + size + ';\n\n')
    headerFile.write('int16_t FILT[' + size + '] = {' + '\n')
    headerFile.write('    ')
    for n in range(len(coefficients)-1):
        n = str(coefficients[n])
        headerFile.write(n + ',')
    headerFile.write(str(coefficients[len(coefficients)-1]))
    headerFile.write('};')
p = input("Acknowledge you have flashed the Teensy with new coefficients: ")


