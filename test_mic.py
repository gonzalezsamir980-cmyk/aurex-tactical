# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== DISPOSITIVOS DE ENTRADA ===")
devices = sd.query_devices()
default_in = sd.default.device[0]
entradas = [(i, d) for i, d in enumerate(devices) if d['max_input_channels'] > 0]
for i, d in entradas:
    marca = " <-- DEFAULT" if i == default_in else ""
    print(f"[{i}] {d['name']} | sr={int(d['default_samplerate'])} Hz{marca}")

print()
print("=== PROBANDO CON 48000 Hz (formato Windows) ===")
print("Hable cuando vea 'GRABANDO'...")

for i, d in entradas:
    sr = int(d['default_samplerate'])
    try:
        print(f"  [{i}] Probando... (HABLE AHORA)", end=' ', flush=True)
        data = sd.rec(sr * 2, samplerate=sr, channels=1, dtype='float32', device=i)
        sd.wait()
        rms = float(np.sqrt(np.mean(data**2)))
        pico = float(np.max(np.abs(data)))
        estado = "OK - tiene voz" if rms > 0.001 else ("ruido bajo" if rms > 0.00005 else "sin señal")
        print(f"RMS={rms:.6f}  PICO={pico:.6f}  [{estado}]")
    except Exception as e:
        print(f"ERROR: {e}")

print()
print("El dispositivo con mayor RMS es su microfono activo.")
