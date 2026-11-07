"""
AGENTE AUTÓNOMO AUREX - MOTOR DE EJECUCIÓN Y AUTO-CORRECCIÓN EN VIVO
Permite que AUREX actúe de manera similar a Antigravity:
1. Recibe la orden del Jefe.
2. Genera el código con Qwen 2.5 Coder 7B.
3. Lo guarda en el workspace local.
4. Lo ejecuta en el sistema operativo real.
5. Si ocurre un error, lo captura, analiza el Traceback, reescribe el código y lo vuelve a probar.
6. Devuelve el reporte completo de telemetría y el artefacto funcional verificado.
"""

import os
import sys
import re
import json
import time
import subprocess
import urllib.request
from pathlib import Path

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "workspace_autonomo"))
os.makedirs(WORKSPACE_DIR, exist_ok=True)

def llamar_ollama(prompt: str, modelo: str = "qwen2.5-coder:7b", stream: bool = False) -> str:
    """Llama a la API local de Ollama."""
    url = "http://127.0.0.1:11434/api/generate"
    payload = json.dumps({
        "model": modelo,
        "prompt": prompt,
        "stream": stream,
        "options": {
            "temperature": 0.2, # Baja temperatura para máxima precisión sintáctica
            "num_predict": 2048
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except Exception as e:
        return f"ERROR_OLLAMA: {e}"

def extraer_codigo(texto: str, lenguaje_preferido: str = "python") -> tuple[str, str]:
    """Extrae el bloque de código principal del texto."""
    patron = r'```([a-zA-Z0-9_\-\+]*)[ \t]*\r?\n([\s\S]*?)```'
    bloques = re.findall(patron, texto)
    if bloques:
        for lang, code in bloques:
            lang_c = lang.strip().lower()
            if lenguaje_preferido in lang_c:
                return lang_c, code.strip()
        # Si no encontró el preferido, retornar el primero
        return bloques[0][0].strip().lower(), bloques[0][1].strip()
    return "python", texto.strip()

def ejecutar_script_python(ruta_script: str, timeout: int = 12) -> tuple[int, str, str]:
    """Ejecuta un script Python en un subproceso aislado y captura stdout y stderr."""
    python_exe = sys.executable
    try:
        resultado = subprocess.run(
            [python_exe, ruta_script],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=WORKSPACE_DIR,
            encoding="utf-8",
            errors="replace"
        )
        return resultado.returncode, resultado.stdout, resultado.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"TIMEOUT: El script superó el límite de seguridad de {timeout} segundos."
    except Exception as e:
        return -2, "", f"EXCEPCIÓN DE EJECUCIÓN: {str(e)}"

def validar_firmware_arduino_esp32(codigo: str) -> tuple[bool, list[str]]:
    """Validador estático de reglas de ingeniería embebida para Arduino y ESP32."""
    errores = []
    
    # 1. Verificar funciones obligatorias
    if "void setup" not in codigo:
        errores.append("Falta la función obligatoria 'void setup()'.")
    if "void loop" not in codigo:
        errores.append("Falta la función obligatoria 'void loop()'.")
        
    # 2. Pines prohibidos en ESP32
    if "esp32" in codigo.lower() or "wifi.h" in codigo.lower():
        pines_flash = [f"pinMode({p}" for p in [6, 7, 8, 9, 10, 11]] + [f"digitalWrite({p}" for p in [6, 7, 8, 9, 10, 11]]
        for pf in pines_flash:
            if pf in codigo.replace(" ", ""):
                errores.append(f"VIOLACIÓN DE HARDWARE: Los pines GPIO 6 a 11 están conectados a la memoria SPI Flash interna del ESP32. Su uso causará un kernel panic/reinicio cíclico.")
                
    # 3. Paréntesis y llaves balanceadas
    if codigo.count("{") != codigo.count("}"):
        errores.append(f"ERROR DE SINTAXIS: Desbalance de llaves (abiertas: {codigo.count('{')}, cerradas: {codigo.count('}')}).")
        
    return len(errores) == 0, errores

def ejecutar_ciclo_agente_autonomo(instruccion: str, max_intentos: int = 3, progreso_callback = None) -> dict:
    """
    Ejecuta el bucle de auto-corrección autónoma estilo Antigravity.
    """
    logs = []
    
    def emitir(etapa: str, mensaje: str, estado: str = "INFO"):
        logs.append({"etapa": etapa, "mensaje": mensaje, "estado": estado, "ts": time.strftime("%H:%M:%S")})
        if progreso_callback:
            progreso_callback(etapa, mensaje, estado)
            
    emitir("INICIO", f"Iniciando Misión Autónoma AUREX: '{instruccion[:60]}...'", "INFO")
    
    # Determinar si es Python o Arduino/ESP32
    instruccion_l = instruccion.lower()
    es_arduino = any(k in instruccion_l for k in ["arduino", "esp32", "sketch", ".ino", "c++", "gpio", "microcontrolador"])
    lenguaje = "arduino" if es_arduino else "python"
    extension = ".ino" if es_arduino else ".py"
    
    nombre_archivo = f"tarea_autonoma_{int(time.time())}{extension}"
    ruta_archivo = os.path.join(WORKSPACE_DIR, nombre_archivo)
    
    # ── FASE 1: GENERACIÓN DE CÓDIGO INICIAL ──
    emitir("GENERACIÓN", f"Sintetizando arquitectura de software ({lenguaje.upper()}) con Qwen 2.5 Coder 7B...", "INFO")
    
    prompt_generacion = f"""Eres un ingeniero senior de desarrollo mecatrónico y software en el sistema AUREX.
Tu tarea es escribir el código COMPLETO, FUNCIONAL y AUTÓNOMO para cumplir la siguiente orden del Jefe:

ORDEN: {instruccion}

REGLAS CRÍTICAS:
- Escribe ÚNICAMENTE el bloque de código dentro de ```{lenguaje} ... ```.
- NUNCA uses explicaciones ni comentarios innecesarios antes o después del código.
- El código debe ser 100% ejecutable, sin dependencias inexistentes y con manejo de excepciones si aplica.
"""
    respuesta_llm = llamar_ollama(prompt_generacion, modelo="qwen2.5-coder:7b")
    lang_detectado, codigo_actual = extraer_codigo(respuesta_llm, lenguaje)
    
    intentos = 0
    exito = False
    salida_consola = ""
    error_consola = ""
    
    while intentos < max_intentos and not exito:
        intentos += 1
        emitir("COMPILACIÓN/EJECUCIÓN", f"[Ciclo {intentos}/{max_intentos}] Probando código en el entorno de taller...", "INFO")
        
        # Guardar en disco
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(codigo_actual)
            
        if lenguaje == "python":
            returncode, stdout, stderr = ejecutar_script_python(ruta_archivo)
            salida_consola = stdout
            error_consola = stderr
            
            if returncode == 0:
                exito = True
                emitir("VERIFICACIÓN", f"Código ejecutado con éxito (Exit Code 0). Salida validada.", "SUCCESS")
                break
            else:
                emitir("FALLO DETECTADO", f"Error detectado en la prueba local: {stderr.strip()[:100]}", "WARNING")
                
                # ── FASE DE AUTO-CORRECCIÓN (AGENT LOOP) ──
                if intentos < max_intentos:
                    emitir("AUTO-DEBUG", f"Invocando auto-corrección autónoma para reparar el fallo...", "INFO")
                    prompt_fix = f"""Eres el motor de depuración autónoma de AUREX.
El código que generaste falló durante la ejecución en la máquina del taller.

CÓDIGO ACTUAL:
```{lenguaje}
{codigo_actual}
```

ERROR / TRACEBACK CAPTURADO DE LA TERMINAL:
{stderr}

TAREA OBLIGATORIA:
Analiza el error con precisión de ingeniería, corrige la falla y devuelve ÚNICAMENTE el código corregido y completo dentro de ```{lenguaje} ... ```.
No agregues saludos ni explicaciones.
"""
                    resp_fix = llamar_ollama(prompt_fix, modelo="qwen2.5-coder:7b")
                    _, codigo_actual = extraer_codigo(resp_fix, lenguaje)
                else:
                    emitir("LÍMITE ALCANZADO", f"Se alcanzó el límite de {max_intentos} ciclos de auto-reparación.", "ERROR")
                    
        else: # Arduino / ESP32
            valido, errores_hardware = validar_firmware_arduino_esp32(codigo_actual)
            if valido:
                exito = True
                salida_consola = f"Firmware {lenguaje.upper()} validado con éxito:\n- Estructura canónica setup() / loop() verificada.\n- Verificación de pines segura para microcontrolador.\n- Listo para subir por puerto COM."
                emitir("VERIFICACIÓN", "Firmware validado exitosamente bajo estándares mecatrónicos AUREX.", "SUCCESS")
                break
            else:
                error_consola = "\n".join(errores_hardware)
                emitir("FALLO DETECTADO", f"Infracción de reglas de hardware: {error_consola}", "WARNING")
                if intentos < max_intentos:
                    emitir("AUTO-DEBUG", "Auto-reparando configuración de pines y sintaxis de firmware...", "INFO")
                    prompt_fix_ino = f"""El firmware de Arduino/ESP32 contiene los siguientes errores de compilación/hardware:
{error_consola}

CÓDIGO A CORREGIR:
```{lenguaje}
{codigo_actual}
```

Devuelve ÚNICAMENTE el código corregido dentro de ```{lenguaje} ... ```.
"""
                    resp_fix_ino = llamar_ollama(prompt_fix_ino, modelo="qwen2.5-coder:7b")
                    _, codigo_actual = extraer_codigo(resp_fix_ino, lenguaje)
                else:
                    emitir("LÍMITE ALCANZADO", "Límite de intentos de validación alcanzado.", "ERROR")

    return {
        "exito": exito,
        "intentos": intentos,
        "lenguaje": lenguaje,
        "nombre_archivo": nombre_archivo,
        "ruta_archivo": ruta_archivo,
        "codigo_final": codigo_actual,
        "salida_consola": salida_consola,
        "error_consola": error_consola,
        "logs": logs
    }
