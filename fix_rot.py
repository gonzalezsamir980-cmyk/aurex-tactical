with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\plantillas\holograma_3d.py', 'r', encoding='utf-8') as f:
    content = f.read()

OLD_ROT = '''    if (autoRotate) {{
      groupPhysArm.rotation.y += 0.008;
      groupPhysAct.rotation.y += 0.008;
      groupDigArm.rotation.y += 0.008;
      groupDigAct.rotation.y += 0.008;
    }}'''

NEW_ROT = '''    if (autoRotate) {{
      groupPhysArm.rotation.y += 0.008;
      groupPhysAct.rotation.y += 0.008;
      groupPhysSensors.rotation.y += 0.008;
      groupDigArm.rotation.y += 0.008;
      groupDigAct.rotation.y += 0.008;
      groupDigSensors.rotation.y += 0.008;
    }}'''

if OLD_ROT in content:
    content = content.replace(OLD_ROT, NEW_ROT)
    with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\plantillas\holograma_3d.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Auto-rotation updated for 3D sensors!")
else:
    print("OLD_ROT not found")
