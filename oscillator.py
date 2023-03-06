import numpy as np
import pygame as pg
import itertools
from matplotlib import pyplot as plt

frequencies = {}
frequencies[97] = 1
sampleRate = 44100

class Oscillator():
    def __init__(self, freq=frequencies[97], phase=0, amp=1,sample_rate=sampleRate, wave_range=(-1, 1),buffer = 512):
        self._frequency = freq
        self._amp = amp
        self._phase = phase
        self._sample_rate = sample_rate
        self._wave_range = wave_range
        self._buffer = buffer
        # [Dynamic properties]
    
    ## [Getters]
    def getFrequency(self):
        return self._frequency
    def getPhase(self):
        return self._phase
    def getAmp(self):
        return self._amp
    def getBuffer(self):
        return self._buffer
    
    ## [Setters]
    def setFrequency(self, value):
        self._frequency = value
    
    def setPhase(self,value):
        self._phase = value
    
    def setAmp(self,value):
        self._amp = value

    def setBuffer(self,value):
        self._buffer = value

    def __iter__(self):
        return self


class sineOscillator(Oscillator):
    def __init__(self, freq=frequencies[97], phase=0, amp=1, sample_rate=sampleRate, wave_range=(-1, 1)):
        super().__init__(freq, phase, amp, sample_rate, wave_range)

        self.stepSize = (2 * np.pi * self.getFrequency()) / self._sample_rate
        self._iterator = 0
        

    def __next__(self):
        self.stepSize = (2 * np.pi * self.getFrequency()) / self._sample_rate
        value = np.cos(self._iterator)
        self._iterator = self._iterator + self.stepSize
        return value
    