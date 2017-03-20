import pyaudio

def getaudiodevices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print(str(i) + ": " + p.get_device_info_by_index(i).get('name'))

getaudiodevices()

p = pyaudio.PyAudio()
p.get_default_input_device_info()
