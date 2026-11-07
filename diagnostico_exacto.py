# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np

devices = sd.query_devices()
print(f"Total devices: {len(devices)}")
for i, d in enumerate(devices):
    if d['max_input_channels'] > 0:
        print(f"Index [{i}]: {d['name']} (channels={d['max_input_channels']}, sr={d['default_samplerate']})")

print("\nProbando cada uno con sd.rec...")
for i, d in enumerate(devices):
    if d['max_input_channels'] > 0:
        try:
            sr = int(d['default_samplerate'])
            ch = min(2, d['max_input_channels'])
            a = sd.rec(int(0.1 * sr), samplerate=sr, channels=ch, dtype='float32', device=i)
            sd.wait()
            print(f"  [{i}] EXITO! RMS={float(np.sqrt(np.mean(a**2))):.6f}")
        except Exception as e:
            print(f"  [{i}] FALLO con error: {e}")
