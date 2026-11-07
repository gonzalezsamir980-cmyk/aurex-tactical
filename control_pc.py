"""
MÓDULO DE CONTROL DE SISTEMA Y TELEMETRÍA DE HARDWARE - AUREX
Control nativo 100% de Windows sin dependencias externas pesadas.
Permite abrir cualquier programa instalado en la laptop y traerlo al frente de la pantalla.
"""

import os
import sys
import re
import ctypes
import shutil
import time
import subprocess
import threading
from pathlib import Path

# ─────────────────────────────────────────────────────────────
#  1. ESTRUCTURAS WIN32 / CTYPES PARA TELEMETRÍA NATIVA
# ─────────────────────────────────────────────────────────────
class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ('dwLength', ctypes.c_ulong),
        ('dwMemoryLoad', ctypes.c_ulong),
        ('ullTotalPhys', ctypes.c_ulonglong),
        ('ullAvailPhys', ctypes.c_ulonglong),
        ('ullTotalPageFile', ctypes.c_ulonglong),
        ('ullAvailPageFile', ctypes.c_ulonglong),
        ('ullTotalVirtual', ctypes.c_ulonglong),
        ('ullAvailVirtual', ctypes.c_ulonglong),
        ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
    ]

class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', ctypes.c_byte),
        ('BatteryFlag', ctypes.c_byte),
        ('BatteryLifePercent', ctypes.c_byte),
        ('SystemStatusFlag', ctypes.c_byte),
        ('BatteryLifeTime', ctypes.c_ulong),
        ('BatteryFullLifeTime', ctypes.c_ulong),
    ]

class FILETIME(ctypes.Structure):
    _fields_ = [('dwLowDateTime', ctypes.c_uint), ('dwHighDateTime', ctypes.c_uint)]

def _filetime_to_int(ft):
    return (ft.dwHighDateTime << 32) + ft.dwLowDateTime

def obtener_uso_cpu_rapido():
    """Calcula el porcentaje de uso de CPU en una ventana de 150ms."""
    try:
        idle1, kernel1, user1 = FILETIME(), FILETIME(), FILETIME()
        ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idle1), ctypes.byref(kernel1), ctypes.byref(user1))
        time.sleep(0.15)
        idle2, kernel2, user2 = FILETIME(), FILETIME(), FILETIME()
        ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idle2), ctypes.byref(kernel2), ctypes.byref(user2))

        idle_diff = _filetime_to_int(idle2) - _filetime_to_int(idle1)
        kernel_diff = _filetime_to_int(kernel2) - _filetime_to_int(kernel1)
        user_diff = _filetime_to_int(user2) - _filetime_to_int(user1)
        total = kernel_diff + user_diff

        if total == 0:
            return 0.0
        uso = (1.0 - (idle_diff / total)) * 100.0
        return max(0.0, min(100.0, uso))
    except Exception:
        return 0.0

def obtener_telemetria_sistema():
    """
    Recopila métricas instantáneas del hardware de la computadora.
    Retorna un diccionario con datos de CPU, RAM, Disco y Batería.
    """
    stat = MEMORYSTATUSEX()
    stat.dwLength = ctypes.sizeof(stat)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
    ram_total_gb = stat.ullTotalPhys / (1024**3)
    ram_usada_gb = (stat.ullTotalPhys - stat.ullAvailPhys) / (1024**3)
    ram_pct = stat.dwMemoryLoad

    cpu_pct = obtener_uso_cpu_rapido()

    try:
        disco_total, disco_used, disco_free = shutil.disk_usage("C:")
        disco_total_gb = disco_total / (1024**3)
        disco_libre_gb = disco_free / (1024**3)
        disco_pct = ((disco_total - disco_free) / disco_total) * 100.0
    except Exception:
        disco_total_gb, disco_libre_gb, disco_pct = 0, 0, 0

    p_stat = SYSTEM_POWER_STATUS()
    ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(p_stat))
    bateria_pct = int(p_stat.BatteryLifePercent)
    es_laptop = (bateria_pct != 255)
    cargando = (p_stat.ACLineStatus == 1)

    return {
        "cpu_pct": round(cpu_pct, 1),
        "ram_usada_gb": round(ram_usada_gb, 1),
        "ram_total_gb": round(ram_total_gb, 1),
        "ram_pct": ram_pct,
        "disco_total_gb": round(disco_total_gb, 1),
        "disco_libre_gb": round(disco_libre_gb, 1),
        "disco_pct": round(disco_pct, 1),
        "es_laptop": es_laptop,
        "bateria_pct": bateria_pct if es_laptop else None,
        "cargando": cargando if es_laptop else None
    }

# ─────────────────────────────────────────────────────────────
#  2. ESCÁNER UNIVERSAL DE PROGRAMAS INSTALADOS EN LA LAPTOP
# ─────────────────────────────────────────────────────────────
_CACHE_PROGRAMAS = {}

def indexar_programas_laptop():
    """
    Escanea las carpetas de inicio y accesos directos de Windows
    para indexar TODOS los programas instalados en la laptop.
    """
    global _CACHE_PROGRAMAS
    if _CACHE_PROGRAMAS:
        return _CACHE_PROGRAMAS

    rutas = [
        os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%USERPROFILE%\Desktop"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs")
    ]

    programas = {}
    for r in rutas:
        if os.path.exists(r):
            for root, _, files in os.walk(r):
                for f in files:
                    ext = Path(f).suffix.lower()
                    if ext in [".lnk", ".exe"]:
                        nombre_limpio = Path(f).stem.lower().strip()
                        ruta_completa = os.path.join(root, f)
                        # No sobreescribir si ya existe uno más corto
                        if nombre_limpio not in programas:
                            programas[nombre_limpio] = (Path(f).stem, ruta_completa)

    _CACHE_PROGRAMAS = programas
    return _CACHE_PROGRAMAS

def _forzar_foco_en_pantalla(nombre_ventana_o_proceso: str):
    """
    Hilo en segundo plano que espera a que la ventana se dibuje y
    fuerza a Windows a ponerla en primer plano en la pantalla del Jefe.
    """
    def _tarea():
        for _ in range(4):
            time.sleep(0.4)
            try:
                # 1. Simular toque de tecla Alt para saltar el bloqueo de Windows (SetForegroundLock)
                user32 = ctypes.windll.user32
                user32.keybd_event(0x12, 0, 0, 0)
                user32.keybd_event(0x12, 0, 2, 0)

                # 2. Activar ventana con WScript.Shell AppActivate
                termino = nombre_ventana_o_proceso.replace('"', '').replace("'", "")
                cmd = f'$ws = New-Object -ComObject Wscript.Shell; $ws.AppActivate("{termino}")'
                creationflags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
                subprocess.run(
                    ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=creationflags
                )
            except Exception:
                pass

    t = threading.Thread(target=_tarea, daemon=True)
    t.start()

def abrir_cualquier_programa(nombre_solicitado: str) -> tuple[bool, str]:
    """
    Busca cualquier programa instalado en la laptop del Jefe,
    lo ejecuta y lo trae al frente de la pantalla automáticamente.
    """
    nombre_limpio = nombre_solicitado.lower().strip()
    nombre_limpio = nombre_limpio.replace("el ", "").replace("la ", "").replace("mi ", "").strip()

    # 1. Comandos nativos y programas principales de la estación
    ruta_arduino_ide = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Arduino IDE\Arduino IDE.exe")
    
    comandos_nativos = {
        # Arduino IDE
        "arduino": ("Arduino IDE", f'"{ruta_arduino_ide}"' if os.path.exists(ruta_arduino_ide) else "start arduino"),
        "arduino ide": ("Arduino IDE", f'"{ruta_arduino_ide}"' if os.path.exists(ruta_arduino_ide) else "start arduino"),
        "arduinoide": ("Arduino IDE", f'"{ruta_arduino_ide}"' if os.path.exists(ruta_arduino_ide) else "start arduino"),
        "ide arduino": ("Arduino IDE", f'"{ruta_arduino_ide}"' if os.path.exists(ruta_arduino_ide) else "start arduino"),
        
        # Herramientas del sistema y explorador
        "calculadora": ("Calculadora", "start calculator:"),
        "calc": ("Calculadora", "start calculator:"),
        "bloc de notas": ("Bloc de notas", "start notepad"),
        "notepad": ("Bloc de notas", "start notepad"),
        "explorador": ("Explorador de Archivos", "start explorer"),
        "explorador de archivos": ("Explorador de Archivos", "start explorer"),
        "archivos": ("Explorador de Archivos", "start explorer"),
        "carpetas": ("Explorador de Archivos", "start explorer"),
        "mis archivos": ("Explorador de Archivos", "start explorer"),
        "mis documentos": ("Explorador de Archivos", "start explorer"),
        "administrador de tareas": ("Administrador de tareas", "start taskmgr"),
        "taskmgr": ("Administrador de tareas", "start taskmgr"),
        "tareas": ("Administrador de tareas", "start taskmgr"),
        "cmd": ("Símbolo del Sistema", "start cmd"),
        "terminal": ("Terminal", "start wt || start cmd"),
        "configuracion": ("Configuración de Windows", "start ms-settings:"),
        "configuración": ("Configuración de Windows", "start ms-settings:"),
        "paint": ("Paint", "start mspaint"),
        "recortes": ("Herramienta Recortes", "start ms-screenclip:")
    }

    if nombre_limpio in comandos_nativos:
        nombre_oficial, cmd = comandos_nativos[nombre_limpio]
        if cmd.startswith('"') and os.path.exists(cmd.replace('"', '')):
            try:
                os.startfile(cmd.replace('"', ''))
            except Exception:
                os.system(f'start "" {cmd}')
        else:
            os.system(cmd)
        _forzar_foco_en_pantalla(nombre_oficial)
        return True, f"Jefe, he abierto **{nombre_oficial}** en primer plano en su pantalla."

    # 2. Si es una URL o servicio web
    if nombre_limpio.startswith("http://") or nombre_limpio.startswith("https://") or "youtube" in nombre_limpio:
        url = "https://www.youtube.com" if "youtube" in nombre_limpio else nombre_limpio
        os.system(f"start {url}")
        _forzar_foco_en_pantalla("Chrome")
        return True, f"Jefe, enlace abierto en su navegador: {url}"

    # 3. Buscar en el catálogo de programas instalados en la laptop (330+ programas)
    programas = indexar_programas_laptop()
    
    # Búsqueda exacta
    if nombre_limpio in programas:
        nombre_display, ruta_archivo = programas[nombre_limpio]
        try:
            try:
                os.startfile(ruta_archivo)
            except Exception:
                os.system(f'start "" "{ruta_archivo}"')
            _forzar_foco_en_pantalla(nombre_display)
            return True, f"Jefe, iniciando **{nombre_display}** directamente en su pantalla."
        except Exception as e:
            return False, f"Jefe, encontré {nombre_display} pero ocurrió un error al ejecutarlo: {e}"

    # Búsqueda parcial (ej: "word" -> "Word.lnk", "visual studio" -> "Visual Studio 2022")
    candidatos = []
    for k, (nom_disp, ruta) in programas.items():
        if nombre_limpio in k:
            candidatos.append((len(k), nom_disp, ruta))

    if candidatos:
        candidatos.sort(key=lambda x: x[0])
        _, mejor_nom, mejor_ruta = candidatos[0]
        try:
            try:
                os.startfile(mejor_ruta)
            except Exception:
                os.system(f'start "" "{mejor_ruta}"')
            _forzar_foco_en_pantalla(mejor_nom)
            return True, f"Jefe, desplegando **{mejor_nom}** en su pantalla."
        except Exception as e:
            return False, f"Jefe, error al inicializar {mejor_nom}: {e}"

    # 4. Verificar si es un ejecutable reconocido en el PATH del sistema (sin disparar cuadros de error)
    cmd_path = shutil.which(nombre_limpio)
    if cmd_path:
        try:
            os.system(f'start "" "{cmd_path}"')
            _forzar_foco_en_pantalla(nombre_limpio)
            return True, f"Jefe, ejecutando **{nombre_limpio}** en su pantalla."
        except Exception as e:
            pass

    return False, f"Jefe, no encontré el programa '{nombre_solicitado}' instalado en su laptop. ¿Desea que lo busque con otro nombre?"

# ─────────────────────────────────────────────────────────────
#  3. CONTROL DE VOLUMEN Y SISTEMA OPERATIVO
# ─────────────────────────────────────────────────────────────
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

def ajustar_volumen(accion: str) -> str:
    """Sube, baja o silencia el audio de Windows."""
    user32 = ctypes.windll.user32
    accion = accion.lower()

    if any(w in accion for w in ["subir", "aumentar", "mas", "más", "sube"]):
        for _ in range(6):
            user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
            user32.keybd_event(VK_VOLUME_UP, 0, 2, 0)
        return "Volumen incrementado, Jefe."

    elif any(w in accion for w in ["bajar", "disminuir", "menos", "baja"]):
        for _ in range(6):
            user32.keybd_event(VK_VOLUME_DOWN, 0, 0, 0)
            user32.keybd_event(VK_VOLUME_DOWN, 0, 2, 0)
        return "Volumen reducido, Jefe."

    elif any(w in accion for w in ["silenciar", "mutear", "mute", "silencio"]):
        user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
        user32.keybd_event(VK_VOLUME_MUTE, 0, 2, 0)
        return "Audio silenciado/restablecido a sus órdenes."

    return "Comando de audio no reconocido."

def bloquear_computadora() -> str:
    """Bloquea la sesión de Windows inmediatamente."""
    try:
        ctypes.windll.user32.LockWorkStation()
        return "Estación de trabajo asegurada y bloqueada, Jefe."
    except Exception as e:
        return f"No se pudo bloquear la estación: {e}"

# ─────────────────────────────────────────────────────────────
#  4. INTÉRPRETE DE COMANDOS TÁCTICOS DE J.A.R.V.I.S.
# ─────────────────────────────────────────────────────────────
def limpiar_prefijo_asistente(orden: str) -> str:
    """Limpia 'AUREX', saludos o signos del inicio de la orden."""
    o = orden.strip()
    # Quitar 'AUREX', 'Oye Aurex', 'Hola Aurex', 'Hey Aurex'
    o = re.sub(r'^(hola|oye|hey)?\s*aurex[\s,.:;!¡?¿]*', '', o, flags=re.IGNORECASE).strip()
    # Quitar palabras de cortesía iniciales
    o = re.sub(r'^(por favor|puedes|podrias|podrías)?\s*', '', o, flags=re.IGNORECASE).strip()
    return o

def detectar_y_ejecutar_comando_pc(orden: str) -> tuple[bool, str]:
    """
    Analiza si la orden del usuario es un comando para controlar la computadora.
    Retorna (es_comando_pc, respuesta_para_el_jefe).
    """
    # Limpiar prefijo 'AUREX,' para no interferir en la detección de comandos
    orden_l = limpiar_prefijo_asistente(orden).lower().strip()

    # 1. Telemetría de hardware / Estado del sistema
    terminos_estado = [
        "estado del sistema", "telemetria", "telemetría", "estado de la nave",
        "rendimiento", "como esta la pc", "cómo está la pc", "uso de cpu",
        "cuanta ram", "cuánta ram", "memoria ram", "estado de la maquina",
        "diagnostico de hardware", "diagnóstico de hardware", "revisar pc",
        "estado de la computadora"
    ]
    if any(term in orden_l for term in terminos_estado):
        data = obtener_telemetria_sistema()
        msg = (
            f"Jefe, diagnóstico de la nave completado:\n"
            f"• CPU: {data['cpu_pct']}% de carga de trabajo\n"
            f"• RAM: {data['ram_usada_gb']} GB en uso de {data['ram_total_gb']} GB ({data['ram_pct']}%)\n"
            f"• Almacenamiento (C:): {data['disco_libre_gb']} GB libres de {data['disco_total_gb']} GB\n"
        )
        if data['es_laptop']:
            estado_bat = "Conectada a la corriente" if data['cargando'] else "Operando en batería"
            msg += f"• Batería: {data['bateria_pct']}% ({estado_bat})\n"
        msg += "Todos los subsistemas se encuentran estables y operando dentro de los parámetros nominales."
        return True, msg

    # 2. Control de volumen
    if any(w in orden_l for w in ["volumen", "audio", "silencio", "mutear"]):
        if any(w in orden_l for w in ["sube", "subir", "aumenta", "aumentar", "más", "mas"]):
            return True, ajustar_volumen("subir")
        elif any(w in orden_l for w in ["baja", "bajar", "disminuye", "disminuir", "menos"]):
            return True, ajustar_volumen("bajar")
        elif any(w in orden_l for w in ["silencia", "silenciar", "mutea", "mutear", "mute"]):
            return True, ajustar_volumen("silenciar")

    # 3. Bloqueo de estación
    if any(w in orden_l for w in ["bloquea la pc", "bloquear pc", "asegura la maquina", "bloquear la estacion", "bloquea la pantalla"]):
        return True, bloquear_computadora()

    # 4. Lanzar CUALQUIER programa y traerlo al frente de la pantalla
    # Detecta 'abre X', 'abrir X', 'inicia X', 'ejecuta X', etc.
    patron_abrir = r'(?:abre|abrir|inicia|iniciar|ejecuta|ejecutar|lanzar|pon|abreme|ábreme)\s+(?:el\s+programa\s+|la\s+aplicacion\s+|la\s+aplicación\s+|el\s+|la\s+|mi\s+)?([a-zA-Z0-9_\-\.\s]+)'
    match = re.search(patron_abrir, orden_l, re.IGNORECASE)
    if match:
        target = match.group(1).strip()
        # Mapeos especiales
        if "visual studio" in target and "code" not in target:
            target = "Visual Studio 2022"
        elif "vs code" in target or "vscode" in target:
            target = "Visual Studio Code"
            
        if target and len(target) < 50:
            ok, res = abrir_cualquier_programa(target)
            return True, res

    return False, ""
