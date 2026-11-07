' SCRIPT SILENCIOSO DE INICIO EN SEGUNDO PLANO PARA AUREX WAKE WORD
' No abre ventanas de consola negra. Se ejecuta de forma 100% invisible.
Set WshShell = CreateObject("WScript.Shell")
pythonwPath = "C:\Users\samir\AppData\Local\Programs\Python\Python311\pythonw.exe"
scriptPath = "C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\aurex_wake_listener.py"

WshShell.Run """" & pythonwPath & """ """ & scriptPath & """", 0, False
