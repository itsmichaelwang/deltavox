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

sounds = [None] * 20
def setup():
    for i in range(20):
        try:
            with wave.open('sfx/' + str(i) + '.wav') as fd:
                sounds[i] = fd.readframes(100000000)
                print("Read file", str(i), ".wav with", len(sounds[i]), "samples")
        except FileNotFoundError:
            pass

q = []
def create_ui():
    root = tkinter.Tk()
    root.title("Soundboard")

    def callback(idx):
        print("You pressed button", idx)
        q.append(idx)

    for i in range(20):
        button = tkinter.Button(root, text=i, width=25,
            command=lambda j=i: callback(j))
        button.pack()

    button = tkinter.Button(root, text='Stop', width=25, command=root.destroy)
    button.pack()

    root.mainloop()

def listen_in():
    CHUNK = 1024
    WIDTH = 1
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

    # print(p.get_format_from_width(WIDTH))

    print("* recording")

    copy = bytearray()

    while True:
        data = stream.read(CHUNK)

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
                data = bytes([(x+y)//2 for x,y in zip(data,copy)])
                del copy[0:data_length]
            elif copy_length < data_length:
                data = bytes([(x+y)//2 if y is not None else x for x,y in zip_longest(data,copy)])
                del copy[0:data_length]

        stream.write(data, CHUNK)

    print("* done")

    stream.stop_stream()
    stream.close()

    p.terminate()

setup()

t1 = Thread(target=listen_in)
t1.start()

create_ui()
