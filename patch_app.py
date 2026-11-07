import re

path = r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

old_block = """                # Detectar tipo de petición
                es_peticion_diagrama = any(k in orden.lower() for k in [
                    "diagrama", "conexion", "conexión", "cableado", "wiring", "esquema",
                    "esquemático", "circuito", "pinout", "conectar", "haz un diagrama",
                    "haz el diagrama", "muestra el diagrama", "visualiza", "anatomy",
                    "despiece", "isometric", "isométric", "mecanismo", "máquina", "maquina", "rig",
                    "holograma", "3d", "desarmar", "desensambl", "ensambl", "hiro", "stark",
                    "big hero", "pelicula", "película", "rayos x", "wireframe", "pon eso", "pon pieza",
                    "laboratorio", "desarme"
                ])"""

new_block = """                # Detectar si el usuario está haciendo una pregunta o consulta técnica
                orden_l = orden.lower()
                es_pregunta_o_consulta = any(q in orden_l for q in [
                    "?", "¿", "dime", "por que", "por qué", "como ", "cómo ", "cual", "cuál", 
                    "que ", "qué ", "cuanto", "cuánto", "calcula", "tolerancia", "ajuste", 
                    "recomiend", "explica", "analiza", "duda", "revis", "porqué", "cuántos", "cuantos",
                    "para que", "para qué", "sirve", "falla", "avería", "averia"
                ])

                # Detectar petición explícita de desplegar o abrir un diagrama / 3D
                es_peticion_diagrama = (not es_pregunta_o_consulta) and any(k in orden_l for k in [
                    "diagrama", "conexion", "conexión", "cableado", "wiring", "esquema",
                    "esquemático", "circuito", "pinout", "conectar", "haz un diagrama",
                    "haz el diagrama", "muestra el diagrama", "visualiza", "anatomy",
                    "despiece", "isometric", "isométric", "mecanismo", "máquina", "maquina", "rig",
                    "holograma", "3d", "desarmar", "desensambl", "ensambl", "hiro", "stark",
                    "big hero", "pelicula", "película", "rayos x", "wireframe", "pon eso", "pon pieza",
                    "laboratorio", "desarme"
                ])"""

if old_block in text:
    text = text.replace(old_block, new_block, 1)
    print("Successfully replaced old_block!")
else:
    print("old_block not found exactly!")

# Also enhance orden_efectiva with 3D mechanism telemetry if asking about it
target_orden = "                orden_efectiva = orden"
replacement_orden = """                orden_efectiva = orden
                # Inyección táctica de telemetría si pregunta por componentes del actuador robótico 3D
                if any(p in orden_l for p in ["rodamiento", "608zz", "rotor", "estator", "engranaje", "planetario", "tolerancia", "holograma", "eje", "bobina"]):
                    orden_efectiva += \"\"\"

(DIRECTIVA DE TELEMETRÍA TÉCNICA - ACTUADOR ROBÓTICO 3D:
Tienes en pantalla el Actuador Robótico Servo-Industrial con 8 piezas:
1. Rodamiento de Bolas Radial 608ZZ:
   - Medidas: Diámetro interior d=8 mm, exterior D=22 mm, espesor B=7 mm.
   - Material: Acero cromo 100Cr6, tolerancia de precisión ABEC-7, Carga máx 3,300 N.
   - TOLERANCIA DE AJUSTE DEL EJE RECOMENDADA: k5 (+1 µm a +7 µm). Es un ajuste con apriete o interferencia ligera para eje giratorio bajo carga dinámica, lo que evita por completo el deslizamiento y desgaste por frotamiento (fretting corrosion).
   - ¿Por qué NO g6?: g6 (-5 a -14 µm) es un ajuste con juego que patinaría inmediatamente bajo torque.
   - ¿Por qué NO h6?: h6 (0 a -9 µm) es deslizante/transición; si no se usa adhesivo anaeróbico Loctite 641, terminará aflojándose con las vibraciones.
   - Alojamiento exterior en la carcasa: H7 (0 a +15 µm).
2. Engranajes planetarios: Relación 1:4.8, acero 42CrMo4, módulo 0.8.
3. Rotor magnético Neodimio N52 con 14 polos permanentes.
4. Estator con 8 devanados de cobre clase H 180°C.
5. Tornillería M3 DIN 912 clase 12.9, torque 1.5 N·m.
Responde de forma técnica, empática, profesional y directa dirigiéndote siempre al usuario como 'Jefe'.)\"\"\""""

if target_orden in text:
    text = text.replace(target_orden, replacement_orden, 1)
    print("Successfully replaced orden_efectiva!")
else:
    print("target_orden not found!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("File written successfully.")
