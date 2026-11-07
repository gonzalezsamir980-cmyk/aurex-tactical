# Script to generate new sensors_data.py with rich data, SVG blueprints, and water sensors

import sys
sys.stdout.reconfigure(encoding='utf-8')

SVG_FLOTADOR = """<svg viewBox="0 0 200 160" width="100%" height="130" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="stemGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="50%" stop-color="#94a3b8"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
    <linearGradient id="floatGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="50%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
  </defs>
  <!-- Background -->
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <!-- Rosca superior -->
  <rect x="85" y="12" width="30" height="16" rx="2" fill="#64748b" stroke="#94a3b8" stroke-width="1"/>
  <line x1="85" y1="16" x2="115" y2="16" stroke="#334155" stroke-width="1"/>
  <line x1="85" y1="20" x2="115" y2="20" stroke="#334155" stroke-width="1"/>
  <line x1="85" y1="24" x2="115" y2="24" stroke="#334155" stroke-width="1"/>
  <!-- Cables -->
  <path d="M 94 12 Q 94 2 80 2" stroke="#38bdf8" stroke-width="2.5" fill="none"/>
  <path d="M 106 12 Q 106 2 120 2" stroke="#f59e0b" stroke-width="2.5" fill="none"/>
  <circle cx="80" cy="2" r="2.5" fill="#38bdf8"/>
  <circle cx="120" cy="2" r="2.5" fill="#f59e0b"/>
  <!-- Eje de acero / plástico -->
  <rect x="94" y="28" width="12" height="110" rx="2" fill="url(#stemGrad)"/>
  <!-- Tope inferior -->
  <ellipse cx="100" cy="138" rx="10" ry="4" fill="#64748b"/>
  <!-- Ondas de agua -->
  <path d="M 20 105 Q 40 100 60 105 T 100 105 T 140 105 T 180 105" stroke="#0ea5e9" stroke-width="1.5" fill="none" opacity="0.4"/>
  <path d="M 20 115 Q 40 110 60 115 T 100 115 T 140 115 T 180 115" stroke="#0ea5e9" stroke-width="1.5" fill="none" opacity="0.6"/>
  <!-- Flotador móvil (Boya cilíndrica) -->
  <rect x="74" y="70" width="52" height="34" rx="6" fill="url(#floatGrad)" stroke="#7dd3fc" stroke-width="1.5"/>
  <ellipse cx="100" cy="74" rx="20" ry="3" fill="#38bdf8" opacity="0.8"/>
  <!-- Indicador magnético reed switch -->
  <rect x="98" y="78" width="4" height="18" fill="#facc15" rx="1"/>
  <text x="100" y="91" fill="#0b1329" font-size="7" font-weight="bold" text-anchor="middle">N-S</text>
  <!-- Flechas de movimiento -->
  <path d="M 140 76 L 140 98" stroke="#38bdf8" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="148" y="90" fill="#38bdf8" font-size="8" font-family="sans-serif">Flotabilidad</text>
  <text x="100" y="153" fill="#94a3b8" font-size="8.5" font-family="sans-serif" font-weight="bold" text-anchor="middle">BOYA MAGNÉTICA (ON/OFF)</text>
</svg>"""

SVG_TDS = """<svg viewBox="0 0 200 160" width="100%" height="130" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <!-- Módulo amplificador PCB -->
  <rect x="18" y="20" width="80" height="110" rx="4" fill="#065f46" stroke="#10b981" stroke-width="1.5"/>
  <text x="58" y="34" fill="#a7f3d0" font-size="7.5" font-weight="bold" text-anchor="middle">TDS METER V1.0</text>
  <!-- Chip señal -->
  <rect x="42" y="44" width="32" height="24" rx="2" fill="#0f172a" stroke="#334155"/>
  <circle cx="47" cy="49" r="1.5" fill="#10b981"/>
  <!-- Potenciómetro azul -->
  <rect x="26" y="76" width="18" height="18" rx="2" fill="#0284c7"/>
  <circle cx="35" cy="85" r="4" fill="#f8fafc"/>
  <!-- Pines de salida -->
  <rect x="24" y="112" width="28" height="14" fill="#0f172a" stroke="#475569"/>
  <circle cx="28" cy="119" r="2" fill="#ef4444"/>
  <circle cx="35" cy="119" r="2" fill="#64748b"/>
  <circle cx="42" cy="119" r="2" fill="#38bdf8"/>
  <text x="28" y="134" fill="#ef4444" font-size="6" text-anchor="middle">VCC</text>
  <text x="35" y="134" fill="#94a3b8" font-size="6" text-anchor="middle">GND</text>
  <text x="42" y="134" fill="#38bdf8" font-size="6" text-anchor="middle">AOUT</text>
  <!-- Cable de sonda -->
  <path d="M 85 75 C 105 75 110 50 135 50" stroke="#0f172a" stroke-width="4" fill="none"/>
  <path d="M 85 75 C 105 75 110 50 135 50" stroke="#475569" stroke-width="2" fill="none"/>
  <!-- Sonda TDS cilíndrica -->
  <rect x="135" y="38" width="45" height="24" rx="3" fill="#1e293b" stroke="#64748b"/>
  <rect x="140" y="62" width="35" height="55" rx="2" fill="#0f172a" stroke="#475569"/>
  <!-- Agujas / electrodos de titanio -->
  <rect x="148" y="117" width="4" height="22" fill="#cbd5e1" stroke="#94a3b8"/>
  <rect x="163" y="117" width="4" height="22" fill="#cbd5e1" stroke="#94a3b8"/>
  <!-- Rayos de corriente entre electrodos -->
  <line x1="152" y1="128" x2="163" y2="128" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="2,2"/>
  <text x="157.5" y="148" fill="#38bdf8" font-size="7" font-weight="bold" text-anchor="middle">TITANIO</text>
  <text x="58" y="152" fill="#6ee7b7" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">SENSOR TDS (CALIDAD AGUA)</text>
</svg>"""

print("SVGs formatted correctly")
