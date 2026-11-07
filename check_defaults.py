# -*- coding: utf-8 -*-
import sounddevice as sd

print("Default device:", sd.default.device)
devs = sd.query_devices()
print(f"Total devices: {len(devs)}")
validos = []
for i, d in enumerate(devs):
    if d['max_input_channels'] > 0:
        print(f"Index {i}: {d['name']} (canales={d['max_input_channels']}, sr={d['default_samplerate']})")
        validos.append(i)

print("Dispositivos de entrada validos:", validos)
