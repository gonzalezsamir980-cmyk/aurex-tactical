# -*- coding: utf-8 -*-
path = r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """### 🦾 Guía del Laboratorio Holográfico (Ensamble & Desarme 3D):
- **Selector de Modelo en Vivo:** Puedes alternar en cualquier momento entre el **🦾 Brazo Robótico 6-DOF** y el **⚙️ Actuador Servo** con los botones tácticos superiores.
- **Desarmar / Ensamblar en Tiempo Real:** Pulsa **🔓 Desarmar** para ver todas las piezas separarse en el aire a lo largo de su eje de extracción, o arrastra el control de **Explosión**.
- **Modo Ensamble ("Pon esa pieza"):** Pulsa **➡️ Paso a Paso** o **🔒 Ensamblar** para ver cómo cada componente encaja en su lugar milimétricamente con animación fluida.
- **Inspección Táctica ("¿Qué es y cómo funciona?"):** Haz **clic sobre cualquier pieza** en el espacio 3D (el rotor, los engranajes, el rodamiento, el estator) para abrir su ficha técnica con tolerancias, materiales e instrucciones de montaje en el HUD lateral.
- **Modo Rayos X (Big Hero 6):** Pulsa **👁️ Rayos X** para activar la malla wireframe neón transparente igual que en la película.
- **Control Total 360°:** Arrastra con el ratón para rotar el mecanismo en cualquier ángulo o usa la rueda para hacer zoom."""

replacement = """### 🦾 Guía del Gemelo Digital (Objeto Físico Real ↔ Modelo 3D):
- **◫ Vista Dividida (Split Screen):** En la pantalla izquierda tienes el **Objeto Físico Real** montado en el banco de taller con materiales industriales PBR. En la derecha tienes el **Gemelo Digital 3D** desarmable.
- **🔄 Rotación Sincronizada 360°:** Arrastra con el ratón en cualquiera de los dos lados para rotar ambos objetos a la vez y comparar cada detalle físico con el diseño digital.
- **🎛️ Modos de Pantalla:** Puedes alternar con los botones superiores entre **◫ Físico + 3D**, **📷 Objeto Físico** a pantalla completa o **🌐 Modelo 3D**.
- **🔓 Desarmar / Explosión 3D:** Pulsa **Desarmar 3D** o mueve el slider para ver cómo el gemelo digital se separa en el aire mientras el objeto físico permanece armado como referencia visual.
- **🔍 Inspección Táctica:** Haz clic en cualquier pieza del 3D para ver su material, tolerancia y procedimiento de montaje en el HUD lateral.
- **🦾 Selector de Mecanismo:** Alterna entre el **Brazo Robótico 6-DOF** y el **Actuador Servo** con los botones superiores."""

if target in text:
    text = text.replace(target, replacement, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("app.py guide updated successfully!")
else:
    print("Target not found in app.py")
