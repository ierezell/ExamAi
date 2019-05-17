import sounddevice as sd
import soundfile as sf
import numpy as np

# print(sd.query_devices())
# data, fs = sf.read('guitartune.wav', dtype='float32')
# print(data)
# print(fs)
# print("play")
# sd.play(data, fs)
# print("1")
# print(sd.check_input_settings())
# # print("2")
# # print(sd.check_output_settings())
# print("3")
# print(sd.get_portaudio_version())
# print("4")
# print(sd.get_status())
# print("5")
# print(sd.get_stream())
# print("6")
# print(sd.query_hostapis())
# sd.wait()
# sd.stop()
# print("\n\n\n\n\n\n\n\n")
print(sd.query_devices())
sd.default.samplerate = 44100
sd.default.channels = 2
sd.default.device = 5
sd.default.dtype = 'float32'
duration = 3
print("parle")
reccorded = np.zeros((44100*3, 1))
reccorded = sd.rec(int(duration*44100))
sd.wait()
print(reccorded)
print(np.max(reccorded))
print(len(reccorded))
print("play")
sd.play(reccorded, samplerate=44100, blocking=True, device=5)
print("writing")
sf.write('coucoutoi.wav', reccorded, 44100)
