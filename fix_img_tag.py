with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\artifacts_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

OLD_IMG = '<img src="{sensor.get(\'imagen_url\', \'\')}" alt="{sensor.get(\'nombre\')}" style="max-width:100%; max-height:90px; object-fit:contain; border-radius:4px; background:#fff; padding:2px; margin-top:6px;" onerror="this.style.display=\'none\'"/>'

if OLD_IMG in content:
    content = content.replace(OLD_IMG, '')
    with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\artifacts_helper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Broken img tag removed from artifacts_helper.py!")
else:
    print("OLD_IMG not found")

import subprocess
res = subprocess.run(["python", "-m", "py_compile", r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\artifacts_helper.py"], capture_output=True, text=True)
if res.returncode == 0:
    print("[SUCCESS] artifacts_helper.py compiled 100%!")
else:
    print("[ERROR] Syntax error:\n", res.stderr)
