import sounddevice as sd
import numpy as np

devs = sd.query_devices()
print(f"Default device: {sd.default.device}")
print(f"Total dispositivos: {len(devs)}")
print("\n--- TODOS los dispositivos ---")
for i, d in enumerate(devs):
    print(f"[{i}] {d['name'][:45]} hostapi={d['hostapi']} in={d['max_input_channels']} out={d['max_output_channels']}")

print("\n--- Probando TODOS (incluyendo WDM-KS) ---")
ok = []
for i, d in enumerate(devs):
    if d["max_input_channels"] > 0 or d["hostapi"] == 3:
        try:
            sr = int(d["default_samplerate"])
            ch = max(1, d["max_input_channels"])
            if ch == 0:
                ch = 1
            data = sd.rec(sr // 4, samplerate=sr, channels=ch, dtype="float32", device=i)
            sd.wait()
            mono = np.mean(data, axis=1) if data.ndim > 1 else data.flatten()
            rms = float(np.sqrt(np.mean(mono**2)))
            print(f"  [{i}] {d['name'][:40]} (hostapi={d['hostapi']}) -> EXITO RMS={rms:.6f}")
            ok.append((i, rms))
        except Exception as e:
            print(f"  [{i}] {d['name'][:40]} -> FALLO: {str(e)[:60]}")

print(f"\nFuncionan: {ok}")
if ok:
    mejor = max(ok, key=lambda x: x[1])
    print(f"Mejor dispositivo (mayor RMS): [{mejor[0]}] con RMS={mejor[1]:.6f}")
