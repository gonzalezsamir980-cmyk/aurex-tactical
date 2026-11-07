# -*- coding: utf-8 -*-
import sounddevice as sd

devs = sd.query_devices()
print(f"Total devices: {len(devs)}")
for i, d in enumerate(devs):
    if d['max_input_channels'] > 0:
        print(f"[{i}] {d['name']} | hostapi={d['hostapi']} | sr={d['default_samplerate']}")
