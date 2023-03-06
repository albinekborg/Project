import numpy as np
from scipy import interpolate as ip
from scipy import signal
import matplotlib.pyplot as plt

np.random.seed(10)
sampleRate = 44100
    
def smoothen(linearFunction,resolution):
    kernel = signal.windows.hann(int(sampleRate/resolution))
    convolved = signal.convolve(linearFunction,kernel,mode='same') / sum(kernel)
    return convolved


def generateWaveForm(resolution):
    waveForm = np.zeros((1,sampleRate))[0]
    amplitude = 1

    points = []
    for point in range(resolution):
        point = np.random.rand(amplitude)*2 - 1
        points.append(point[0])
    
    ## Create periodicity
    left = points
    points += points
    points = left + points

    ## Interpolate linearly, then smoothen the function
    f = ip.interp1d(np.arange(len(points)),points)

    waveForm = f(np.arange(0,resolution*3, resolution/sampleRate))
    ipWaveForm = smoothen(waveForm,resolution)
    waveForm = waveForm[sampleRate:2*sampleRate]
    ipWaveForm = ipWaveForm[sampleRate:2*sampleRate]

    return ipWaveForm


additiveSynthesis = np.zeros((sampleRate,))

for resolution in range(2,8):
    waveform = generateWaveForm(resolution)
    #plt.plot(waveform, label=f"Synthesis with resolution {str(resolution)}")
    additiveSynthesis += waveform
 

## Normalize to 1:
additiveSynthesis = additiveSynthesis/max(additiveSynthesis)


## Increase Frequency:
def setPitch(waveform,frequency):
    ## interpolate and post to new array with more datapoints
    newWaveform = np.zeros(len(waveform))
    newLength = int(sampleRate/frequency)
    resampled = signal.resample(waveform,newLength)

    for split in range(frequency):
        newWaveform[int(split*sampleRate/frequency):int(split*sampleRate/frequency) + int(sampleRate/frequency)] = resampled

    return newWaveform


plt.plot(additiveSynthesis,label="final")
plt.plot(setPitch(additiveSynthesis,2),label = "freq 2")
plt.legend()
plt.show()