#!/usr/bin/env python3
"""Pass input directly to output.
See https://www.assembla.com/spaces/portaudio/subversion/source/HEAD/portaudio/trunk/test/patest_wire.c
"""

from threading import Thread
from time import sleep
import sys

import pyaudio
import tkinter

from scipy.io.wavfile import read

import numpy as np
import wave

from operator import add

import array

from itertools import zip_longest

# Add wavs to the soundboard
# Because of the limitations of audio channels (and my bad coding), these wavs should be:
# stereo
# a specific bit resolution
# a sampling rate of 44100 Hz
sounds = [None] * 20
def setup():
    for i in range(len(sounds)):
        try:
            with wave.open('sfx/' + str(i) + '.wav') as fd:
                sounds[i] = fd.readframes(1000000000)
                print("Read file", str(i), ".wav with", len(sounds[i]), "samples")
        except FileNotFoundError:
            pass

# Load the ui on the main frame
q = []
def create_ui():
    root = tkinter.Tk()
    root.title("Soundboard")

    def callback(idx):
        print("You pressed button", idx)
        q.append(idx)

    for i in range(len(sounds)):
        button = tkinter.Button(root, text=i, width=25,
            command=lambda j=i: callback(j))
        button.pack()

    button = tkinter.Button(root, text='Stop', width=25, command=root.destroy)
    button.pack()

    root.mainloop()

# Run the audio management on a separate thread
def listen_in():
    CHUNK = 1024
    WIDTH = 2
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    MICROPHONE_INPUT_CHANNEL = 2
    LINE_OUTPUT_CHANNEL = 8
     = 6

    microphone_stream = p.open(
                    format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=MICROPHONE_INPUT_CHANNEL,
                    output_device_index=LINE_OUTPUT_CHANNEL
                    )

    headphone_stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=RATE,
        # input=True,
        output=True,
        frames_per_buffer=CHUNK,
        output_device_index=PASS_THROUGH_CHANNEL
    )

    print("* recording")
    copy = bytearray()

    while True:
        data = microphone_stream.read(CHUNK)
        print(data)

        if q:
            try:
                key = q.pop(0)
                copy = bytearray(sounds[key])
            except TypeError:
                pass

        if len(copy) > 0:
            data_length = len(data)
            copy_length = len(copy)

            # fix this ugly code
            if copy_length >= data_length:
                data = bytes([y for x,y in zip(data,copy)])
                del copy[0:data_length]
            elif copy_length < data_length:
                data = bytes([y if y is not None else x for x,y in zip_longest(data,copy)])
                del copy[0:data_length]

        microphone_stream.write(data, CHUNK)
        headphone_stream.write(data, CHUNK)

    print("* done")

    microphone_stream.stop_stream()
    microphone_stream.close()

    p.terminate()

setup()

t1 = Thread(target=listen_in)
t1.start()

create_ui()
