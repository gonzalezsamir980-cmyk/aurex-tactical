import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Marker 1: near es_peticion_diagrama definition
TARGET_DEF = '''                # Detectar petición explícita de desplegar o abrir un diagrama / 3D
                es_peticion_diagrama = (not es_pregunta_o_consulta) and any(k in orden_l for k in ['''

REPLACEMENT_DEF = '''                # ── DETECCIÓN EXPLÍCITA DE IMÁGENES O FICHAS DE SENSORES ──
                es_peticion_imagenes_sensores = any(w in orden_l for w in [
                    "imagen", "imágenes", "imagenes", "foto", "fotos", "fichas", "ficha visual",
                    "ver los sensores", "ver esos", "enséñame", "enseñame", "muestra las fotos",
                    "muestra las imagenes", "muestra los sensores", "dame las imagenes", "dame las imágenes"
                ]) and any(w in orden_l for w in ["sensor", "sensores", "componente", "componentes", "modulo", "módulo", "dispositivo", "esos dos", "estos dos", "esos", "estos", "agua"])

                sensores_objetivo = []
                if es_peticion_imagenes_sensores:
                    sensores_objetivo = buscar_sensores_en_texto(orden)
                    if len(sensores_objetivo) < 2 and st.session_state.historial:
                        for m in reversed(st.session_state.historial):
                            if m.get("rol") in ["ia", "asistente"]:
                                s_hist = buscar_sensores_en_texto(m["texto"])
                                for sh in s_hist:
                                    if not any(so["nombre"] == sh["nombre"] for so in sensores_objetivo):
                                        sensores_objetivo.append(sh)
                                if sensores_objetivo:
                                    break

                # Detectar petición explícita de desplegar o abrir un diagrama / 3D
                es_peticion_diagrama = (es_peticion_imagenes_sensores and bool(sensores_objetivo)) or ((not es_pregunta_o_consulta) and any(k in orden_l for k in ['''

if TARGET_DEF in content:
    content = content.replace(TARGET_DEF, REPLACEMENT_DEF)
    print("[OK] es_peticion_imagenes_sensores definition added")
else:
    print("[ERROR] TARGET_DEF not found")

# Marker 2: inside if es_peticion_diagrama: handling
TARGET_BRANCH = '''                        elif es_ultrasonico:
                            from plantillas.diagramas import generar_diagrama_esp32_hcsr04
                            respuesta = f"""Aquí tienes el diagrama de conexión del **ESP32** con el **sensor ultrasónico HC-SR04**, Jefe:

{generar_diagrama_esp32_hcsr04()}

### Conexiones:
| ESP32 | HC-SR04 |
| :--- | :--- |
| **3V3** | **VCC** |
| **GPIO 5** | **TRIG** |
| **GPIO 18** | **ECHO** |
| **GND** | **GND** |

> ⚠️ **Importante:** El pin ECHO del HC-SR04 entrega 5 V y el ESP32 opera con lógica de 3.3 V. Utiliza un divisor de voltaje (1kΩ y 2kΩ) entre ECHO y GPIO 18 para proteger el microcontrolador.

También puedo prepararte el código Arduino IDE para medir distancias con este circuito."""'''

REPLACEMENT_BRANCH = '''                        elif es_peticion_imagenes_sensores and sensores_objetivo:
                            pers_act = config_global.get("personalidad_activa", "isabella")
                            nombre_ia = "Isabella" if pers_act == "isabella" else "AUREX"
                            nombres_txt = " y del ".join([f"**{s['nombre']}**" for s in sensores_objetivo])
                            respuesta = f"¡A sus órdenes, Jefe! Aquí tiene las **fichas tácticas, esquemas vectoriales de pines (pinouts) y especificaciones técnicas completas** del {nombres_txt}:\n\nPuede consultar abajo los diagramas de cableado y directivas de taller para cada uno."

                        elif es_ultrasonico:
                            from plantillas.diagramas import generar_diagrama_esp32_hcsr04
                            respuesta = f"""Aquí tienes el diagrama de conexión del **ESP32** con el **sensor ultrasónico HC-SR04**, Jefe:

{generar_diagrama_esp32_hcsr04()}

### Conexiones:
| ESP32 | HC-SR04 |
| :--- | :--- |
| **3V3** | **VCC** |
| **GPIO 5** | **TRIG** |
| **GPIO 18** | **ECHO** |
| **GND** | **GND** |

> ⚠️ **Importante:** El pin ECHO del HC-SR04 entrega 5 V y el ESP32 opera con lógica de 3.3 V. Utiliza un divisor de voltaje (1kΩ y 2kΩ) entre ECHO y GPIO 18 para proteger el microcontrolador.

También puedo prepararte el código Arduino IDE para medir distancias con este circuito."""'''

if TARGET_BRANCH in content:
    content = content.replace(TARGET_BRANCH, REPLACEMENT_BRANCH)
    print("[OK] es_peticion_imagenes_sensores branch added")
else:
    print("[ERROR] TARGET_BRANCH not found")

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Syntax check
import subprocess
res = subprocess.run(["python", "-m", "py_compile", r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py"], capture_output=True, text=True)
if res.returncode == 0:
    print("[SUCCESS] app.py syntax check PASSED!")
else:
    print("[ERROR] Syntax error in app.py:\n", res.stderr)
