# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np

print("=== HOST APIS DISPONIBLES ===")
apis = sd.query_hostapis()
for i, a in enumerate(apis):
    print(f"API [{i}]: {a['name']} (dispositivos={len(a['devices'])}, default_in={a['default_input_device']})")

print("\n=== TODOS LOS DISPOSITIVOS CON INPUT ===")
devs = sd.query_devices()
for i, d in enumerate(devs):
    if d['max_input_channels'] > 0:
        api_name = apis[d['hostapi']]['name']
        print(f"[{i}] {d['name']} | API: {api_name} ({d['hostapi']}) | sr={d['default_samplerate']}")
