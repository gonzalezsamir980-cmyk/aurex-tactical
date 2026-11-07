with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
'''                    "laboratorio", "desarme"
                ])''',
'''                    "laboratorio", "desarme"
                ]))'''
)

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py', 'w', encoding='utf-8') as f:
    f.write(content)

import subprocess
res = subprocess.run(["python", "-m", "py_compile", r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py"], capture_output=True, text=True)
if res.returncode == 0:
    print("[SUCCESS] app.py syntax is 100% VALID!")
else:
    print("[ERROR] Syntax error:\n", res.stderr)
