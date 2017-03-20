# import pyaudio
#
# CHUNK = 150
# WIDTH = 1
# CHANNELS = 1
# RATE = 44100
#
# p = pyaudio.PyAudio()
# microphone_stream = p.open(
#                 format=p.get_format_from_width(WIDTH),
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 # output=True,
#                 frames_per_buffer=CHUNK,
#                 input_device_index=1,
#                 # output_device_index=5
#                 )
#
# while True:
#     data = microphone_stream.read(CHUNK)
#     print(data)
#
#     # if q:
#     #     try:
#     #         key = q.pop(0)
#     #         copy = bytearray(sounds[key])
#     #     except TypeError:
#     #         pass
#     #
#     # if len(copy) > 0:
#     #     data_length = len(data)
#     #     copy_length = len(copy)
#     #
#     #     # fix this ugly code
#     #     if copy_length >= data_length:
#     #         data = bytes([(x+y)//2 for x,y in zip(data,copy)])
#     #         del copy[0:data_length]
#     #     elif copy_length < data_length:
#     #         data = bytes([(x+y)//2 if y is not None else x for x,y in zip_longest(data,copy)])
#     #         del copy[0:data_length]
#
#     # microphone_stream.write(data, CHUNK)
#
# microphone_stream.stop_stream()
# microphone_stream.close()
#
# p.terminate()
import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print("recording...")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")


# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
