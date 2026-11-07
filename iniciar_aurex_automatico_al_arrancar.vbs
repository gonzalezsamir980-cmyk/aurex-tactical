' AUTO-ARRANQUE DE AUREX AL INICIAR SESIÓN EN WINDOWS
' Lanza el servidor en segundo plano y abre la ventana en su pantalla inmediatamente.
Set WshShell = CreateObject("WScript.Shell")
pythonwPath = "C:\Users\samir\AppData\Local\Programs\Python\Python311\pythonw.exe"
scriptPath = "C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\desplegar_aurex.py"

WshShell.Run """" & pythonwPath & """ """ & scriptPath & """", 0, False
