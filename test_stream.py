# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np

print("Probando InputStream por defecto...")
try:
    with sd.InputStream(channels=1, dtype='float32') as s:
        print("InputStream abierto con exito!")
        data, _ = s.read(1600)
        print("Leidos 1600 samples correctamente. RMS:", float(np.sqrt(np.mean(data**2))))
except Exception as e:
    print("Error al abrir InputStream:", e)
