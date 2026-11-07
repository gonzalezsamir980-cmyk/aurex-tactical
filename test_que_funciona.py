# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np

print("sd.default.device inicial:", sd.default.device)
devs = sd.query_devices()

print("\n--- PROBANDO TODOS LOS DISPOSITIVOS DE ENTRADA ---")
funciona = []
for i, d in enumerate(devs):
    if d['max_input_channels'] > 0:
        sr = int(d['default_samplerate'])
        ch = min(2, d['max_input_channels'])
        try:
            data = sd.rec(int(0.3 * sr), samplerate=sr, channels=ch, dtype='float32', device=i)
            sd.wait()
            rms = float(np.sqrt(np.mean(data**2)))
            print(f"[{i}] {d['name']} (HostAPI {d['hostapi']}) -> EXITO! RMS={rms:.6f}")
            funciona.append(i)
        except Exception as e:
            print(f"[{i}] {d['name']} (HostAPI {d['hostapi']}) -> FALLO: {e}")

print("\nDispositivos que FUNCIONAN sin error:", funciona)
