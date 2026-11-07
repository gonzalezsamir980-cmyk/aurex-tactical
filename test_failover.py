# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np

print("Probando dispositivos funcionales...")
devs = sd.query_devices()
encontrado = None

# Probar default
try:
    data = sd.rec(1600, samplerate=16000, channels=1, dtype='float32')
    sd.wait()
    print("DEFAULT funciona! RMS:", float(np.sqrt(np.mean(data**2))))
    encontrado = "default"
except Exception as e:
    print("DEFAULT fallo:", e)

if not encontrado:
    for i, d in enumerate(devs):
        if d['max_input_channels'] > 0:
            try:
                sr = int(d['default_samplerate'])
                ch = min(2, d['max_input_channels'])
                data = sd.rec(int(0.1 * sr), samplerate=sr, channels=ch, dtype='float32', device=i)
                sd.wait()
                print(f"Device [{i}] {d['name'][:30]} FUNCIONA!")
                encontrado = i
                break
            except Exception as e:
                print(f"Device [{i}] fallo: {e}")

print("Resultado final dispositivo funcional:", encontrado)
