import pygame as pg
import numpy as np
import itertools
import sys
import oscillator

pg.mixer.pre_init(44100, -16, 2, 2048)
pg.mixer.init()
mixer = pg.mixer
pg.init()
screen = pg.display.set_mode((480,480))


playableKeys = 'awsedftgyhujk'  # One octave of playable keys
playableFrequencies = [261.63, 277.18, 293.66, 311.13, 329.63,
                       349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25]

# initalise frequencies and add to dictionary

#Create list of pygame keys
pygameKeys = []
for key in playableKeys:
    pygameKeys.append("pg.K_"+key)

pygameKeys = [eval(i) for i in pygameKeys]

# Create a dicitionary of frequencies corresponding to the pressed key
frequencies = {}
for position in range(len(pygameKeys)):
    frequencies[pygameKeys[position]] = playableFrequencies[position]


# Initialise Oscillator
osc = oscillator.sineOscillator()


sampleRate = 44100      # Samples per second [Hz]
bufferSize = int(sampleRate*10)      # Samples per buffer
print("initialising ...")

# Create dictionary of playable sounds ## Fake synthesizer
notes = {}
for key in pygameKeys:
    osc.setFrequency(frequencies[key])
    buffer = np.asarray([32767*next(osc) for _ in range(bufferSize)]).astype(np.int16)
    soundObject = mixer.Sound(buffer)
    notes[key] = soundObject




running = True
while running:
    for event in pg.event.get():
        if event == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
            pg.quit()
            sys.exit()
            
        if event.type == pg.KEYDOWN:
            key = event.key
            if key in pygameKeys:
                print("Pressed Down")
                holding = True
                while holding:
                    ## Listen for new events
                    notes[key].set_volume(0.33)
                    notes[key].play()
                    for event in pg.event.get():
                        if event.type == pg.KEYUP:
                            notes[key].stop()
                            print("Released Key")
                            holding = False
                    
    
                
                
            
                

                




pg.mixer.quit()
pg.quit()
