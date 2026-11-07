"""
Test del auto-detector de micrófono de AUREX — corra esto HABLANDO en voz alta
"""
import sounddevice as sd
import numpy as np

print(f"Default device: {sd.default.device}")
devs = sd.query_devices()
print(f"Total dispositivos: {len(devs)}\n")

# Solo WDM-KS (hostapi=3) con entrada
candidatos_wdm = [(i, d) for i, d in enumerate(devs)
                  if d["hostapi"] == 3 and d["max_input_channels"] > 0]

print(f"--- Dispositivos WDM-KS con entrada ({len(candidatos_wdm)}) ---")
mejores = []
for idx, d in candidatos_wdm:
    sr = int(d["default_samplerate"])
    ch = min(2, d["max_input_channels"])
    try:
        datos = sd.rec(int(sr * 0.5), samplerate=sr, channels=ch, dtype="float32", device=idx)
        sd.wait()
        mono = np.mean(datos, axis=1) if datos.ndim > 1 else datos.flatten()
        rms = float(np.sqrt(np.mean(mono**2)))
        estado = "🟢 VOZ OK" if rms > 0.001 else ("🟡 BAJO" if rms > 0.00005 else "🔴 SILENCIO")
        print(f"  [{idx}] {d['name'][:45]} => RMS={rms:.6f} {estado}")
        mejores.append((rms, idx, sr, ch, d["name"]))
    except Exception as e:
        print(f"  [{idx}] {d['name'][:45]} => FALLO: {str(e)[:50]}")

if mejores:
    mejores.sort(key=lambda x: -x[0])
    rms, idx, sr, ch, nombre = mejores[0]
    print(f"\n✅ AUREX usará: [{idx}] {nombre}")
    print(f"   sr={sr} | ch={ch} | RMS={rms:.6f}")
    if rms < 0.00005:
        print("\n⚠️  RMS=0 en todos — el micrófono no capta voz.")
        print("   Solución: Panel de control > Sonido > Grabar")
        print("   → 'Varios micrófonos' → Propiedades → Niveles → 100%")
        print("   → Vuelva a correr este script HABLANDO en voz alta")
else:
    print("\n❌ Ningún dispositivo WDM-KS disponible")
