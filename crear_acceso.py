import os
import shutil

desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
bat_src = r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\iniciar_aurex.bat"
bat_dst = os.path.join(desktop, "INICIAR_AUREX.bat")

try:
    shutil.copy2(bat_src, bat_dst)
    print("COPIADO_OK:", bat_dst)
except Exception as e:
    print("ERROR:", e)
