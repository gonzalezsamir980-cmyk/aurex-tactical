# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np

print("Buscando el dispositivo de entrada que SI tiene audio...")
devs = sd.query_devices()
for i, d in enumerate(devs):
    if d['max_input_channels'] > 0:
        try:
            sr = int(d['default_samplerate'])
            ch = min(2, d['max_input_channels'])
            data = sd.rec(int(0.2 * sr), samplerate=sr, channels=ch, dtype='float32', device=i)
            sd.wait()
            rms = float(np.sqrt(np.mean(data**2)))
            print(f"[{i}] {d['name']} -> SR={sr} CH={ch} RMS={rms:.6f}")
        except Exception as e:
            print(f"[{i}] {d['name']} -> ERROR: {e}")
