import sys
sys.path.append(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local')
from sensores_data import buscar_sensores_en_texto

# Simulate history
historial = [
    {
        "rol": "usuario",
        "texto": "que sensores hay para el agua?"
    },
    {
        "rol": "asistente",
        "texto": "Un sensor es un componente... 1. **Sensor de nivel de flotador**: se utiliza para medir el nivel de agua... 2. **Sensor de calidad del agua**: se utiliza para detectar la presencia de contaminantes..."
    }
]

orden = "dame las imagenes de esos dos sensores"
orden_l = orden.lower()

es_peticion_imagenes_sensores = any(w in orden_l for w in [
    "imagen", "imágenes", "imagenes", "foto", "fotos", "fichas", "ficha visual",
    "ver los sensores", "ver esos", "enséñame", "enseñame", "muestra las fotos",
    "muestra las imagenes", "muestra los sensores"
]) and any(w in orden_l for w in ["sensor", "sensores", "componente", "componentes", "modulo", "módulo", "dispositivo", "esos dos", "estos dos", "esos"])

print("es_peticion_imagenes_sensores:", es_peticion_imagenes_sensores)

sensores_objetivo = buscar_sensores_en_texto(orden)
if len(sensores_objetivo) < 2 and historial:
    for m in reversed(historial):
        if m["rol"] == "asistente":
            s_hist = buscar_sensores_en_texto(m["texto"])
            for sh in s_hist:
                if not any(so["nombre"] == sh["nombre"] for so in sensores_objetivo):
                    sensores_objetivo.append(sh)
            if sensores_objetivo:
                break

print("Sensores encontrados:", [s["nombre"] for s in sensores_objetivo])
nombres_txt = " y del ".join([f"**{s['nombre']}**" for s in sensores_objetivo])
respuesta = f"¡A sus órdenes, Jefe! Aquí tiene las fichas tácticas, esquemas vectoriales de pines y especificaciones de taller del {nombres_txt}."
print("Respuesta:", respuesta)

# Verify that renderizar_artifacts_interactivos will find them in respuesta
detectados_en_respuesta = buscar_sensores_en_texto(respuesta)
print("Detectados para renderizar en UI:", [s["nombre"] for s in detectados_en_respuesta])
