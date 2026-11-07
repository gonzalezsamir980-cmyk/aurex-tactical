import sys
sys.path.append(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local')
from sensores_data import CATALOGO_SENSORES

s = CATALOGO_SENSORES["sensor-nivel-flotador"]

pines_html = "".join([
    f'<span style="background:#1e293b; color:{color}; padding:3px 8px; border-radius:4px; font-weight:bold; font-size:0.8rem; margin-right:6px; border:1px solid #334155;">'
    f'{pin}: <span style="color:#e2e8f0; font-weight:normal;">{desc}</span></span> '
    for pin, desc, color in s.get("pines", [])
])

html = f"""
<div style="background: linear-gradient(135deg, #0b1329 0%, #030712 100%); border: 1px solid #38bdf8; border-radius: 14px; padding: 16px; margin: 14px 0; box-shadow: 0 4px 20px rgba(56, 189, 248, 0.15);">
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:8px; margin-bottom:12px;">
        <div>
            <span style="font-size:0.75rem; letter-spacing:1px; color:#38bdf8; text-transform:uppercase; font-weight:bold;">{s.get('categoria', 'Componente')} · FICHA TÉCNICA</span>
            <h4 style="margin:2px 0 0 0; color:#f8fafc; font-size:1.15rem;">{s.get('nombre')}</h4>
        </div>
        <span style="background:#0284c7; color:#fff; font-size:0.75rem; padding:3px 8px; border-radius:12px; font-weight:bold;">{s.get('voltaje', '5V')}</span>
    </div>
    <div style="display:flex; gap:16px; flex-wrap:wrap;">
        <div style="flex:1; min-width:200px; max-width:260px; text-align:center; background:#0f172a; padding:10px; border-radius:10px; border:1px solid #1e293b;">
            {s.get('svg_diagrama', '')}
            <div style="font-size:0.72rem; color:#38bdf8; margin-top:5px; font-weight:bold; letter-spacing:0.5px;">📐 BLUEPRINT TÁCTICO & PINES</div>
        </div>
        <div style="flex:2; min-width:260px; font-size:0.9rem; line-height:1.5;">
            <p style="margin:0 0 8px 0; color:#cbd5e1;">{s.get('descripcion')}</p>
            <div style="margin:8px 0;">
                <div style="font-size:0.75rem; color:#38bdf8; font-weight:bold; margin-bottom:4px;">🔌 MAPA DE PINES (PINOUT):</div>
                <div style="display:flex; flex-wrap:wrap; gap:4px;">{pines_html}</div>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:10px; font-size:0.8rem; background:#0f172a; padding:8px 10px; border-radius:6px;">
                <div><b style="color:#94a3b8;">Consumo:</b> <span style="color:#f1f5f9;">{s.get('consumo', 'N/D')}</span></div>
                <div><b style="color:#94a3b8;">Protocolo:</b> <span style="color:#f1f5f9;">{s.get('protocolo', 'Digital')}</span></div>
                <div style="grid-column: span 2;"><b style="color:#94a3b8;">Rango:</b> <span style="color:#f1f5f9;">{s.get('rango', 'N/D')}</span></div>
            </div>
            <div style="margin-top:10px; background:#451a03; border-left:3px solid #f59e0b; padding:6px 10px; border-radius:4px; font-size:0.78rem; color:#fde68a;">
                ⚠️ <b>Directiva de Taller:</b> {s.get('advertencia')}
            </div>
        </div>
    </div>
</div>
"""

clean_html = "\n".join([line.strip() for line in html.split("\n") if line.strip()])
print("Clean HTML length:", len(clean_html))
print("Any line with 4 spaces at start?", any(l.startswith("    ") for l in clean_html.split("\n")))
print("First 3 lines:\n", "\n".join(clean_html.split("\n")[:3]))
