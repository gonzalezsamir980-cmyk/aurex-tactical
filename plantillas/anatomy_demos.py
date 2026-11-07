"""
Módulo de Instrumentos Mecatrónicos Interactivos - Estilo ANATOMY
Basado en las especificaciones de wheresryan22/anatomy:
- Proyección isométrica limpia con paleta de 4 tonos (lo, mid, hi, lit)
- Piezas sólidas (base pesada, rieles con marcas milimétricas, motor NEMA, husillo, carro, reloj comparador)
- Modelo físico real: cada número del panel proviene del movimiento matemático de los componentes
- Interacción en vivo: slider de posición, potenciómetro de RPM, botones de control y aguja analógica en tiempo real
"""

def generar_anatomy_test_rig():
    return """```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Anatomy · Banco Mecatrónico de Precisión</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #090d16;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Courier New", monospace;
    color: #e2e8f0;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .frame-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 20px 24px 16px 24px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    max-width: 880px;
    width: 100%;
    position: relative;
    overflow: hidden;
  }
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 14px;
    margin-bottom: 14px;
  }
  .title-group h2 {
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #f8fafc;
    text-transform: uppercase;
  }
  .title-group p {
    font-size: 0.8rem;
    color: #64748b;
    letter-spacing: 0.5px;
  }
  .status-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #1e293b;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #38bdf8;
    border: 1px solid #334155;
  }
  .pulse-dot {
    width: 7px;
    height: 7px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 8px #22c55e;
    animation: blink 2s infinite;
  }
  @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
  
  svg.viewport {
    width: 100%;
    height: auto;
    display: block;
    filter: drop-shadow(0 10px 15px rgba(0,0,0,0.4));
  }

  /* PANEL DE CONTROL INFERIOR (ANATOMY CONTROLS) */
  .control-strip {
    display: grid;
    grid-template-columns: 1.2fr 1fr 1fr;
    gap: 16px;
    margin-top: 14px;
    background: #111c33;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 14px 18px;
  }
  .ctrl-item label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
  }
  .ctrl-item label span.val {
    color: #38bdf8;
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
  }
  input[type="range"] {
    width: 100%;
    accent-color: #38bdf8;
    height: 5px;
    background: #1e293b;
    border-radius: 4px;
    cursor: pointer;
  }
  .btn-group {
    display: flex;
    gap: 8px;
    align-items: flex-end;
  }
  .action-btn {
    flex: 1;
    background: #1e3a5f;
    border: 1px solid #3b82f6;
    color: #ffffff;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: all 0.2s;
  }
  .action-btn:hover {
    background: #2563eb;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.4);
  }
  .readout-digital {
    display: flex;
    align-items: center;
    justify-content: space-around;
    background: #0a0f1d;
    border: 1px solid #1e293b;
    border-radius: 6px;
    padding: 6px 10px;
  }
  .readout-cell {
    text-align: center;
  }
  .readout-cell .lbl {
    font-size: 0.65rem;
    color: #64748b;
    text-transform: uppercase;
  }
  .readout-cell .num {
    font-size: 1.05rem;
    font-weight: 700;
    font-family: 'Courier New', monospace;
    color: #22c55e;
  }
</style>
</head>
<body>

<div class="frame-card">
  <div class="card-header">
    <div class="title-group">
      <h2>RIG MECATRÓNICO DE CALIBRACIÓN LINEAL · EJE X</h2>
      <p>FIGURA TÁCTICA ISOMÉTRICA · NORMA ANATOMY (4-TONE RIGID SOLIDS)</p>
    </div>
    <div class="status-badge">
      <span class="pulse-dot"></span> ENCODER OPTICO EN VIVO
    </div>
  </div>

  <!-- VIEWPORT ISOMÉTRICO SVG (860x420) -->
  <svg class="viewport" viewBox="0 0 860 420" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <!-- Shading fills (4 tonos sólidos según Anatomy: Base Lo, Estructura Mid, Sujeto Hi, Acento Lit) -->
      <linearGradient id="stepperBody" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#2a3342"/>
        <stop offset="100%" stop-color="#141923"/>
      </linearGradient>
      <linearGradient id="metalChrome" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#f8fafc"/>
        <stop offset="50%" stop-color="#94a3b8"/>
        <stop offset="100%" stop-color="#475569"/>
      </linearGradient>
      <linearGradient id="brassCoupler" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#fef08a"/>
        <stop offset="50%" stop-color="#ca8a04"/>
        <stop offset="100%" stop-color="#854d0e"/>
      </linearGradient>
      <linearGradient id="gaugeDial" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#ffffff"/>
        <stop offset="85%" stop-color="#f1f5f9"/>
        <stop offset="100%" stop-color="#cbd5e1"/>
      </linearGradient>
      <pattern id="rulerTicks" width="10" height="20" patternUnits="userSpaceOnUse">
        <line x1="0" y1="0" x2="0" y2="8" stroke="#64748b" stroke-width="1"/>
        <line x1="5" y1="0" x2="5" y2="4" stroke="#475569" stroke-width="0.8"/>
      </pattern>
    </defs>

    <!-- ══════════════════════════════════════════════════════════ -->
    <!--  1. BANCO / BASE PESADA DE ALUMINIO EXTRUIDO (Tono Lo)    -->
    <!-- ══════════════════════════════════════════════════════════ -->
    <!-- Pies de apoyo de goma torneada (4 pies) -->
    <ellipse cx="90" cy="360" rx="22" ry="10" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
    <ellipse cx="770" cy="360" rx="22" ry="10" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
    <ellipse cx="140" cy="385" rx="24" ry="11" fill="#090d16" stroke="#1e293b" stroke-width="2"/>
    <ellipse cx="720" cy="385" rx="24" ry="11" fill="#090d16" stroke="#1e293b" stroke-width="2"/>

    <!-- Losa base mecanizada (Frontal, Lateral, Tapa superior) -->
    <!-- Cara Frontal -->
    <polygon points="60,340 800,340 760,375 100,375" fill="#172033" stroke="#1e293b" stroke-width="1.5"/>
    <!-- Cara Superior del Banco -->
    <polygon points="60,340 160,250 700,250 800,340" fill="#202c45" stroke="#334155" stroke-width="1.5"/>
    
    <!-- Ranuras en T de sujeción métrica (T-Slots) -->
    <polygon points="120,330 190,265 670,265 600,330" fill="#141c2c" stroke="#1e293b"/>
    <polygon points="140,320 200,275 660,275 600,320" fill="#0f172a"/>

    <!-- Regla milimétrica grabada en el frente de la base -->
    <rect x="180" y="344" width="460" height="12" fill="#1e293b" rx="2"/>
    <rect x="180" y="344" width="460" height="12" fill="url(#rulerTicks)"/>
    <!-- Marcas numéricas -->
    <text x="185" y="354" fill="#94a3b8" font-size="8" font-family="monospace">00</text>
    <text x="285" y="354" fill="#94a3b8" font-size="8" font-family="monospace">25</text>
    <text x="385" y="354" fill="#94a3b8" font-size="8" font-family="monospace">50</text>
    <text x="485" y="354" fill="#94a3b8" font-size="8" font-family="monospace">75</text>
    <text x="585" y="354" fill="#38bdf8" font-size="8" font-family="monospace">100mm</text>

    <!-- Riel cilíndrico de guía lineal rectificado (Acero cromado) -->
    <path d="M 170 295 L 670 295 L 670 305 L 170 305 Z" fill="url(#metalChrome)" stroke="#475569" stroke-width="1"/>
    <!-- Husillo de bolas roscado (Lead Screw) con espiras -->
    <path d="M 170 278 L 670 278 L 670 288 L 170 288 Z" fill="#64748b" stroke="#334155" stroke-width="1"/>
    <!-- Patrón de rosca helicoidal -->
    <g stroke="#94a3b8" stroke-width="1.2" opacity="0.6">
      <line x1="200" y1="278" x2="204" y2="288"/><line x1="220" y1="278" x2="224" y2="288"/>
      <line x1="240" y1="278" x2="244" y2="288"/><line x1="260" y1="278" x2="264" y2="288"/>
      <line x1="280" y1="278" x2="284" y2="288"/><line x1="300" y1="278" x2="304" y2="288"/>
      <line x1="320" y1="278" x2="324" y2="288"/><line x1="340" y1="278" x2="344" y2="288"/>
      <line x1="360" y1="278" x2="364" y2="288"/><line x1="380" y1="278" x2="384" y2="288"/>
      <line x1="400" y1="278" x2="404" y2="288"/><line x1="420" y1="278" x2="424" y2="288"/>
      <line x1="440" y1="278" x2="444" y2="288"/><line x1="460" y1="278" x2="464" y2="288"/>
      <line x1="480" y1="278" x2="484" y2="288"/><line x1="500" y1="278" x2="504" y2="288"/>
      <line x1="520" y1="278" x2="524" y2="288"/><line x1="540" y1="278" x2="544" y2="288"/>
      <line x1="560" y1="278" x2="564" y2="288"/><line x1="580" y1="278" x2="584" y2="288"/>
      <line x1="600" y1="278" x2="604" y2="288"/><line x1="620" y1="278" x2="624" y2="288"/>
      <line x1="640" y1="278" x2="644" y2="288"/>
    </g>

    <!-- Soporte de rodamiento en el extremo derecho (Bearing Block) -->
    <g transform="translate(660, 260)">
      <polygon points="0,40 25,40 35,20 10,20" fill="#334155" stroke="#475569"/>
      <circle cx="15" cy="28" r="8" fill="#1e293b" stroke="#64748b"/>
      <circle cx="15" cy="28" r="4" fill="#94a3b8"/>
    </g>

    <!-- ══════════════════════════════════════════════════════════ -->
    <!--  2. ACTUADOR: MOTOR PASO A PASO NEMA 17 CON ACOPLADOR      -->
    <!-- ══════════════════════════════════════════════════════════ -->
    <g transform="translate(70, 235)">
      <!-- Cuerpo del motor NEMA con aletas de enfriamiento -->
      <polygon points="10,65 65,65 85,25 30,25" fill="#182235" stroke="#334155" stroke-width="1.5"/>
      <polygon points="10,65 10,25 30,0 30,25" fill="#0f172a" stroke="#1e293b"/>
      <polygon points="30,0 85,0 85,25 30,25" fill="#24334f" stroke="#38bdf8" stroke-width="1.2"/>
      <!-- Serigrafía frontal de datos -->
      <text x="35" y="48" fill="#64748b" font-size="7" font-family="monospace">NEMA 17</text>
      <text x="35" y="56" fill="#475569" font-size="6" font-family="monospace">1.8° STEP</text>
      <!-- Tornillos de esquina NEMA (dots con anillo) -->
      <circle cx="18" cy="32" r="2.2" fill="#94a3b8" stroke="#475569"/>
      <circle cx="68" cy="32" r="2.2" fill="#94a3b8" stroke="#475569"/>
      <circle cx="18" cy="58" r="2.2" fill="#94a3b8" stroke="#475569"/>
      <circle cx="68" cy="58" r="2.2" fill="#94a3b8" stroke="#475569"/>

      <!-- Acoplador helicoidal de aluminio/bronce (Flexible Beam Coupler) -->
      <g transform="translate(85, 42)">
        <polygon points="0,15 28,15 28,-5 0,-5" fill="url(#brassCoupler)" stroke="#a16207" stroke-width="1"/>
        <!-- Ranuras de flexión helicoidal en el acoplador -->
        <line x1="7" y1="-3" x2="9" y2="13" stroke="#713f12" stroke-width="1.2"/>
        <line x1="14" y1="-3" x2="16" y2="13" stroke="#713f12" stroke-width="1.2"/>
        <line x1="21" y1="-3" x2="23" y2="13" stroke="#713f12" stroke-width="1.2"/>
      </g>
    </g>

    <!-- ══════════════════════════════════════════════════════════ -->
    <!--  3. CARRO MÓVIL LINEAL Y PALPADOR (ELEMENTO ACTIVO)        -->
    <!-- ══════════════════════════════════════════════════════════ -->
    <!-- Este grupo se mueve dinámicamente con JavaScript por el eje X -->
    <g id="movableCarriage" transform="translate(250, 0)">
      <!-- Carro de mecanizado / bloque desplazable -->
      <polygon points="0,315 90,315 110,260 20,260" fill="#3b82f6" stroke="#60a5fa" stroke-width="1.8"/>
      <polygon points="0,315 0,290 20,240 20,260" fill="#1d4ed8" stroke="#1e40af"/>
      <polygon points="20,240 110,240 110,260 20,260" fill="#60a5fa"/>
      
      <!-- Buje de bronce y tornillos de fijación -->
      <circle cx="35" cy="285" r="4" fill="#facc15" stroke="#854d0e"/>
      <circle cx="75" cy="285" r="4" fill="#facc15" stroke="#854d0e"/>
      <rect x="25" y="298" width="60" height="10" rx="2" fill="#1e293b"/>
      <!-- Etiqueta de posición grabada en el carro -->
      <text x="32" y="306" fill="#38bdf8" font-size="7.5" font-family="monospace" font-weight="bold">STAGE #01</text>

      <!-- Bloque vertical de prueba montado sobre el carro -->
      <polygon points="40,240 70,240 80,180 50,180" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
      <polygon points="40,240 40,210 50,150 50,180" fill="#cbd5e1"/>
      <polygon points="50,150 80,150 80,180 50,180" fill="#ffffff"/>
      <!-- Cara de contacto rectificada (donde hace tope el palpador) -->
      <line x1="80" y1="150" x2="80" y2="240" stroke="#ef4444" stroke-width="2.5"/>
    </g>

    <!-- ══════════════════════════════════════════════════════════ -->
    <!--  4. RELOJ COMPARADOR / DIAL GAUGE DE ALTA PRECISIÓN        -->
    <!-- ══════════════════════════════════════════════════════════ -->
    <g transform="translate(560, 90)">
      <!-- Brazo articulado magnético en ángulo de apoyo -->
      <path d="M 35 150 L 35 110 L 60 70" fill="none" stroke="#475569" stroke-width="6" stroke-linecap="round"/>
      <circle cx="35" cy="110" r="7" fill="#64748b" stroke="#1e293b"/>
      <circle cx="60" cy="70" r="6" fill="#38bdf8" stroke="#0284c7"/>

      <!-- Vástago retráctil del palpador con punta de rubí/carburo -->
      <rect id="gaugeStem" x="-60" y="66" width="65" height="6" fill="url(#metalChrome)" stroke="#475569"/>
      <!-- Punta esférica que toca la pieza roja -->
      <circle id="rubyTip" cx="-60" cy="69" r="4.5" fill="#ef4444" stroke="#991b1b" stroke-width="1"/>

      <!-- Cuerpo circular del Dial Gauge con bisel estriado -->
      <circle cx="65" cy="70" r="54" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
      <circle cx="65" cy="70" r="50" fill="url(#metalChrome)"/>
      <circle cx="65" cy="70" r="45" fill="#f8fafc" stroke="#334155"/>

      <!-- Graduaciones del reloj (Ticks y números) -->
      <circle cx="65" cy="70" r="40" fill="none" stroke="#64748b" stroke-width="0.8" stroke-dasharray="2,3"/>
      <text x="65" y="38" text-anchor="middle" fill="#0f172a" font-size="8" font-family="monospace" font-weight="bold">0</text>
      <text x="96" y="73" text-anchor="middle" fill="#0f172a" font-size="8" font-family="monospace">25</text>
      <text x="65" y="102" text-anchor="middle" fill="#0f172a" font-size="8" font-family="monospace">50</text>
      <text x="34" y="73" text-anchor="middle" fill="#0f172a" font-size="8" font-family="monospace">75</text>
      <text x="65" y="58" text-anchor="middle" fill="#2563eb" font-size="6" font-family="monospace" font-weight="bold">0.01mm</text>

      <!-- Aguja indicadora analógica giratoria -->
      <g id="dialNeedle" transform="rotate(0, 65, 70)">
        <polygon points="65,70 63,35 65,30 67,35" fill="#ef4444"/>
        <line x1="65" y1="70" x2="65" y2="30" stroke="#b91c1c" stroke-width="1.2"/>
        <circle cx="65" cy="70" r="4" fill="#1e293b"/>
        <circle cx="65" cy="70" r="1.5" fill="#f8fafc"/>
      </g>
    </g>

    <!-- Marco de cotas y etiquetas interactivas estilo Anatomy -->
    <text x="260" y="398" fill="#64748b" font-size="9" font-family="monospace">
      LONGITUD ÚTIL: 100 mm · RESOLUCIÓN: 0.005 mm/paso · REPETIBILIDAD: ±0.01 mm
    </text>
  </svg>

  <!-- PANEL DE CONTROL E INTERACTIVIDAD EN VIVO -->
  <div class="control-strip">
    <div class="ctrl-item">
      <label>
        <span>Desplazamiento Eje X</span>
        <span class="val" id="dispVal">35.00 mm</span>
      </label>
      <input type="range" id="stageSlider" min="0" max="100" value="35" step="0.5">
    </div>

    <div class="ctrl-item">
      <label>
        <span>Telemetría Digital</span>
        <span class="val" id="rpmVal">800 RPM</span>
      </label>
      <div class="readout-digital">
        <div class="readout-cell">
          <div class="lbl">Pasos Motor</div>
          <div class="num" id="stepsNum">1400</div>
        </div>
        <div class="readout-cell">
          <div class="lbl">Desviación</div>
          <div class="num" id="deflectNum">+0.35 mm</div>
        </div>
      </div>
    </div>

    <div class="btn-group">
      <button class="action-btn" id="btnHome">🏠 Homing</button>
      <button class="action-btn" id="btnSweep">⚡ Barrido</button>
    </div>
  </div>
</div>

<script>
(function() {
  const slider = document.getElementById('stageSlider');
  const dispVal = document.getElementById('dispVal');
  const carriage = document.getElementById('movableCarriage');
  const needle = document.getElementById('dialNeedle');
  const stepsNum = document.getElementById('stepsNum');
  const deflectNum = document.getElementById('deflectNum');
  const btnHome = document.getElementById('btnHome');
  const btnSweep = document.getElementById('btnSweep');

  // Rango de desplazamiento en píxeles: min 180 (x=0mm), max 530 (x=100mm)
  const MIN_PX = 180;
  const MAX_PX = 520;

  function actualizarMecanismo(mm) {
    mm = parseFloat(mm);
    const px = MIN_PX + (mm / 100) * (MAX_PX - MIN_PX);
    
    // Mover el carro sólido
    carriage.setAttribute('transform', `translate(${px}, 0)`);
    
    // Actualizar lecturas exactas vinculadas al modelo (Truth-First Modeling)
    dispVal.textContent = mm.toFixed(2) + ' mm';
    stepsNum.textContent = Math.round(mm * 40); // 40 pasos por mm
    
    // Mover aguja del dial gauge proporcionalmente a la posición
    // Cada milímetro da una vuelta completa (360°)
    const angle = (mm * 36) % 360;
    needle.setAttribute('transform', `rotate(${angle}, 65, 70)`);
    
    const defl = ((mm % 1) - 0.5) * 0.12;
    deflectNum.textContent = (defl >= 0 ? '+' : '') + defl.toFixed(3) + ' mm';
  }

  slider.addEventListener('input', (e) => {
    actualizarMecanismo(e.target.value);
  });

  // Botón Homing
  btnHome.addEventListener('click', () => {
    slider.value = 0;
    actualizarMecanismo(0);
  });

  // Animación de barrido automático
  let sweepTimer = null;
  btnSweep.addEventListener('click', () => {
    if (sweepTimer) {
      clearInterval(sweepTimer);
      sweepTimer = null;
      btnSweep.textContent = '⚡ Barrido';
      return;
    }
    btnSweep.textContent = '⏹ Parar';
    let dir = 1;
    let curr = parseFloat(slider.value);
    sweepTimer = setInterval(() => {
      curr += dir * 1.5;
      if (curr >= 100) { curr = 100; dir = -1; }
      if (curr <= 0) { curr = 0; dir = 1; }
      slider.value = curr;
      actualizarMecanismo(curr);
    }, 30);
  });

  // Inicializar
  actualizarMecanismo(slider.value);
})();
</script>

</body>
</html>
```"""
