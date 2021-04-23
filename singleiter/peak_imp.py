import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.io import wavfile
from scipy.fftpack import fft

fs, array = wavfile.read("peak_finderv1.wav")
array_fft = fft(array)
plt.plot(array_fft)
peaks_full_neg = find_peaks(-array_fft, height=2e7)
peaks_neg = peaks_full_neg[0]
print(peaks_neg)
#use_array_fft = array_fft[peaks_neg[0]:peaks_neg[1]]
#plt.plot(use_array_fft)
plt.show()
                          