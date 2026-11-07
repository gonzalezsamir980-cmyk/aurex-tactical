# -*- coding: utf-8 -*-
path = r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """                        if es_holograma_3d:
                            from plantillas.holograma_3d import generar_laboratorio_holografico_3d
                            pers_act = config_global.get("personalidad_activa", "isabella")
                            nombre_ia = "Isabella" if pers_act == "isabella" else "AUREX"
                            respuesta = f\"\"\"¡Protocolo holográfico en línea, Jefe! He desplegado el **Laboratorio 3D Interactivo** estilo Hiro Hamada / Tony Stark:

{generar_laboratorio_holografico_3d()}

### 🦾 Guía del Laboratorio Holográfico (Ensamble & Desarme 3D):"""

replacement = """                        if es_holograma_3d:
                            from plantillas.holograma_3d import generar_laboratorio_holografico_3d
                            pers_act = config_global.get("personalidad_activa", "isabella")
                            nombre_ia = "Isabella" if pers_act == "isabella" else "AUREX"
                            es_modelo_brazo = any(b in orden_l for b in ["brazo", "arm", "articulad", "robotico", "robótico", "pinza", "gripper"])
                            modelo_ini = "brazo" if es_modelo_brazo else "actuador"
                            nombre_mecanismo = "Brazo Robótico Articulado 6-DOF con Pinza (Gripper)" if es_modelo_brazo else "Actuador Robótico Servo-Industrial"
                            respuesta = f\"\"\"¡Protocolo holográfico en línea, Jefe! He desplegado el **Laboratorio 3D Interactivo** del **{nombre_mecanismo}** estilo Hiro Hamada / Tony Stark:

{generar_laboratorio_holografico_3d(modelo_inicial=modelo_ini)}

### 🦾 Guía del Laboratorio Holográfico (Ensamble & Desarme 3D):
- **Selector de Modelo en Vivo:** Puedes alternar en cualquier momento entre el **🦾 Brazo Robótico 6-DOF** y el **⚙️ Actuador Servo** con los botones tácticos superiores."""

if target in text:
    text = text.replace(target, replacement, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("app.py updated with dynamic robot arm 3D detection!")
else:
    print("Target not found in app.py!")
