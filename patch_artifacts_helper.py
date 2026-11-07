import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\artifacts_helper.py', 'r', encoding='utf-8') as f:
    content = f.read()

OLD_CARD = '''        <div style="display:flex; gap:16px; flex-wrap:wrap;">
            <div style="flex:1; min-width:180px; max-width:240px; text-align:center; background:#0f172a; padding:10px; border-radius:10px; border:1px solid #1e293b;">
                <img src="{sensor.get('imagen_url')}" alt="{sensor.get('nombre')}" style="max-width:100%; height:140px; object-fit:contain; border-radius:6px; background:#fff; padding:4px;" onerror="this.style.display='none'"/>
                <div style="font-size:0.72rem; color:#94a3b8; margin-top:6px;">Foto técnica de referencia</div>
            </div>'''

NEW_CARD = '''        <div style="display:flex; gap:16px; flex-wrap:wrap;">
            <div style="flex:1; min-width:200px; max-width:260px; text-align:center; background:#0f172a; padding:10px; border-radius:10px; border:1px solid #1e293b;">
                {sensor.get('svg_diagrama', '')}
                <div style="font-size:0.72rem; color:#38bdf8; margin-top:5px; font-weight:bold; letter-spacing:0.5px;">📐 BLUEPRINT TÁCTICO & PINES</div>
                <img src="{sensor.get('imagen_url', '')}" alt="{sensor.get('nombre')}" style="max-width:100%; max-height:90px; object-fit:contain; border-radius:4px; background:#fff; padding:2px; margin-top:6px;" onerror="this.style.display='none'"/>
            </div>'''

if OLD_CARD in content:
    content = content.replace(OLD_CARD, NEW_CARD)
    with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\artifacts_helper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("artifacts_helper.py updated successfully!")
else:
    print("Could not find OLD_CARD in artifacts_helper.py")
    idx = content.find("Foto técnica de referencia")
    if idx >= 0:
        print("Context:", content[idx-150:idx+150])
