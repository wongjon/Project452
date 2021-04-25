# Test FIR Generator
# Goal: Have an input signal (received tone) and output signal (test tone)
# Generate a dynamic filter that converts input to output as close as possible
# Stop process while coefficients stop changing with 10% margin

# Libraries
import numpy as np
import scipy.io as sio
from scipy.fftpack import fft, ifft, fftshift
import matplotlib.pyplot as plt
from scipy import signal
from pylab import *
from scipy.io import wavfile
from scipy.signal import spectrogram
from scipy.signal import welch
from scipy.signal import lfilter

#Plot frequency and phase response
def mfreqz(b,a=1):
    w,h = signal.freqz(b,a)
    h_dB = 20 * log10 (abs(h))
    subplot(211)
    plot(w/max(w),h_dB)
    ylim(-150, 5)
    ylabel("Magnitude (db)")
    xlabel(r"Normalized Frequency (x$\pi$rad/sample)")
    title(r"Frequency response")
    subplot(212)
    h_Phase = unwrap(arctan2(imag(h),real(h)))
    plot(w/max(w),h_Phase)
    ylabel("Phase (radians)")
    xlabel(r"Normalized Frequency (x$\pi$rad/sample)")
    title(r"Phase response")
    subplots_adjust(hspace=0.5)

#Plot step and impulse response
def impz(b,a=1):
    l = len(b)
    impulse = repeat(0.,l); impulse[0] =1.
    x = arange(0,l)
    response = signal.lfilter(b,a,impulse)
    subplot(211)
    stem(x, response)
    ylabel("Amplitude")
    xlabel(r"n (samples)")
    title(r"Impulse response")
    subplot(212)
    step = cumsum(response)
    stem(x, step)
    ylabel("Amplitude")
    xlabel(r"n (samples)")
    title(r"Step response")
    subplots_adjust(hspace=0.5)

n = 1001
a = signal.firwin(n, cutoff = [0.2, 0.5], window = 'blackmanharris', pass_zero = False)
mfreqz(a)
show()
impz(a)
show()


# Take in 2 wav files and output a matrix of coefficients
# Note: fsR and fsT should be equal to prevent sampling frequency discrepencies

# Teceived tone
fsR, wR = wavfile.read("received tone.wav")
wR16 = np.asarray( wR/abs(wR).max() * (1<<15), np.int16)
receivedF = fft(wR)

# Test tone
fsT, wT = wavfile.read("testtone.wav")
wT16 = np.asarray(wT/abs(wR).max() * (1<<15), np.int16)
testF = fft(wT)

# Dynamic Filter h(t) = IFFT{Y(S)/X(S)}
filterF = testF/receivedF
filter = ifft(filterF)
print("dynamic filter: ", filter)




