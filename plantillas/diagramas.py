def generar_diagrama_esp32_hcsr04():
    return """```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Diagrama ESP32 Ultrasónico - Referencia Táctica</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0b1120;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #e2e8f0;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .card {
    background: #ffffff;
    border-radius: 20px;
    padding: 24px 26px 18px 26px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    max-width: 860px;
    width: 100%;
    position: relative;
  }
  .header-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
    padding: 0 16px;
  }
  .pill-title {
    background: #1c385c;
    color: #ffffff;
    font-weight: 700;
    font-size: 1.15rem;
    padding: 7px 28px;
    border-radius: 8px;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.18);
  }
  svg {
    width: 100%;
    height: auto;
    display: block;
  }
  .details-box {
    max-width: 860px;
    width: 100%;
    margin-top: 20px;
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 20px 24px;
  }
  .details-box p {
    font-size: 1rem;
    color: #e5e7eb;
    margin-bottom: 14px;
  }
  .details-box h3 {
    font-size: 1.1rem;
    color: #38bdf8;
    margin-bottom: 12px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 16px;
  }
  th, td {
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid #1f2937;
    font-size: 0.95rem;
  }
  th {
    color: #9ca3af;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    background: #0f172a;
  }
  .tag-warn {
    display: inline-block;
    background: #c2410c;
    color: #ffffff;
    font-size: 0.75rem;
    font-weight: bold;
    padding: 2px 8px;
    border-radius: 12px;
    margin-right: 6px;
    text-transform: uppercase;
  }
  .warn-box {
    background: rgba(234, 88, 12, 0.12);
    border-left: 4px solid #f97316;
    padding: 12px 16px;
    border-radius: 4px;
    color: #fed7aa;
    font-size: 0.92rem;
    line-height: 1.5;
    margin-bottom: 14px;
  }
</style>
</head>
<body>

<div class="card">
  <div class="header-row">
    <div class="pill-title" style="margin-left: 20px;">ESP32</div>
    <div class="pill-title" style="margin-right: 40px;">Sensor Ultrasónico HC-SR04</div>
  </div>

  <svg viewBox="0 0 830 410" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <!-- Blindaje metálico ESP32 -->
      <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#e4e4e7"/>
        <stop offset="50%" stop-color="#a1a1aa"/>
        <stop offset="100%" stop-color="#71717a"/>
      </linearGradient>
      <!-- Bisel metálico transductores HC-SR04 -->
      <linearGradient id="metalBevel" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#ffffff"/>
        <stop offset="40%" stop-color="#cbd5e1"/>
        <stop offset="70%" stop-color="#94a3b8"/>
        <stop offset="100%" stop-color="#475569"/>
      </linearGradient>
      <!-- Rejilla acústica de los transductores -->
      <radialGradient id="meshGrad" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#18181b"/>
        <stop offset="75%" stop-color="#27272a"/>
        <stop offset="90%" stop-color="#52525b"/>
        <stop offset="100%" stop-color="#cbd5e1"/>
      </radialGradient>
      <!-- Conector USB metálico -->
      <linearGradient id="usbGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#f4f4f5"/>
        <stop offset="50%" stop-color="#d4d4d8"/>
        <stop offset="100%" stop-color="#a1a1aa"/>
      </linearGradient>
    </defs>

    <!-- ══════════════════════════════════════════════════════════ -->
    <!--  CABLES MANHATTAN (RUTAS TOTALMENTE DESPEJADAS)             -->
    <!-- ══════════════════════════════════════════════════════════ -->

    <!-- CABLE ROJO: ESP32 3V3 (x=70, y=248) -> HC-SR04 VCC (x=495, y=128) -->
    <path d="M 70 248 L 48 248 L 48 350 L 495 350 L 495 128" 
          fill="none" stroke="#ef4444" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- CABLE NEGRO: ESP32 GND (x=70, y=278) -> HC-SR04 GND (x=570, y=128) -->
    <path d="M 70 278 L 36 278 L 36 370 L 570 370 L 570 128" 
          fill="none" stroke="#111827" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- CABLE VERDE: ESP32 GPIO 5 (x=196, y=134) -> HC-SR04 TRIG (x=520, y=128) -->
    <path d="M 196 134 L 350 134 L 350 326 L 520 326 L 520 128" 
          fill="none" stroke="#16a34a" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- CABLE AZUL: ESP32 GPIO 18 (x=196, y=168) -> HC-SR04 ECHO (x=545, y=128) -->
    <path d="M 196 168 L 375 168 L 375 304 L 545 304 L 545 128" 
          fill="none" stroke="#2563eb" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- ══════════════════════════════════════════════════════════ -->
    <!--  ESP32 DEVKIT V1 (PCB NEGRA CON COMPONENTES REALISTAS)     -->
    <!-- ══════════════════════════════════════════════════════════ -->
    <g transform="translate(58, 12)">
      <!-- PCB negra con bordes redondeados -->
      <rect x="0" y="0" width="150" height="295" rx="14" fill="#18181b" stroke="#27272a" stroke-width="2"/>
      
      <!-- Zona de antena WiFi (negro mate + trazas doradas) -->
      <path d="M 24 8 L 126 8 Q 130 8 130 12 L 130 32 L 20 32 L 20 12 Q 20 8 24 8 Z" fill="#09090b"/>
      <path d="M 28 22 L 34 22 L 34 14 L 42 14 L 42 22 L 50 22 L 50 14 L 58 14 L 58 22 L 66 22 L 66 14 L 74 14 L 74 22 L 82 22 L 82 14 L 90 14 L 90 22 L 98 22 L 98 14 L 106 14 L 106 22 L 114 22 L 114 14 L 122 14" 
            fill="none" stroke="#ca8a04" stroke-width="1.8" stroke-linecap="round"/>

      <!-- Blindaje metálico RF grabado -->
      <rect x="22" y="38" width="106" height="102" rx="4" fill="url(#shieldGrad)" stroke="#52525b" stroke-width="1.2"/>
      <text x="75" y="78" text-anchor="middle" fill="#27272a" font-size="10.5" font-family="'Segoe UI', sans-serif" font-weight="700">ESP-WROOM-32</text>
      <text x="75" y="104" text-anchor="middle" fill="#3f3f46" font-size="17" font-family="'Segoe UI', sans-serif" font-weight="bold">CE</text>

      <!-- Puerto Micro USB metálico inferior -->
      <rect x="50" y="274" width="50" height="24" rx="3" fill="url(#usbGrad)" stroke="#71717a" stroke-width="1.2"/>
      <rect x="59" y="283" width="32" height="10" rx="2" fill="#27272a"/>

      <!-- Pulsadores táctiles EN y BOOT -->
      <rect x="18" y="260" width="16" height="16" rx="3" fill="#3f3f46" stroke="#71717a"/>
      <circle cx="26" cy="268" r="4.5" fill="#18181b"/>
      <text x="26" y="253" text-anchor="middle" fill="#a1a1aa" font-size="8" font-family="sans-serif" font-weight="bold">EN</text>

      <rect x="116" y="260" width="16" height="16" rx="3" fill="#3f3f46" stroke="#71717a"/>
      <circle cx="124" cy="268" r="4.5" fill="#18181b"/>
      <text x="124" y="253" text-anchor="middle" fill="#a1a1aa" font-size="8" font-family="sans-serif" font-weight="bold">BOOT</text>

      <!-- Pines dorados Header Izquierdo (15 pines) -->
      <g fill="#ca8a04" stroke="#78350f" stroke-width="0.8">
        <circle cx="12" cy="46" r="3"/><circle cx="12" cy="62" r="3"/><circle cx="12" cy="78" r="3"/>
        <circle cx="12" cy="94" r="3"/><circle cx="12" cy="110" r="3"/><circle cx="12" cy="126" r="3"/>
        <circle cx="12" cy="142" r="3"/><circle cx="12" cy="158" r="3"/><circle cx="12" cy="174" r="3"/>
        <circle cx="12" cy="190" r="3"/><circle cx="12" cy="206" r="3"/><circle cx="12" cy="222" r="3"/>
        <!-- 3V3 Pin destacado -->
        <circle cx="12" cy="236" r="4.2" fill="#ef4444" stroke="#ffffff" stroke-width="1.5"/>
        <!-- GND Pin destacado -->
        <circle cx="12" cy="266" r="4.2" fill="#111827" stroke="#ffffff" stroke-width="1.5"/>
      </g>

      <!-- Pines dorados Header Derecho (15 pines) -->
      <g fill="#ca8a04" stroke="#78350f" stroke-width="0.8">
        <circle cx="138" cy="46" r="3"/><circle cx="138" cy="62" r="3"/><circle cx="138" cy="78" r="3"/>
        <circle cx="138" cy="94" r="3"/><circle cx="138" cy="110" r="3"/>
        <!-- GPIO 5 destacado -->
        <circle cx="138" cy="122" r="4.2" fill="#16a34a" stroke="#ffffff" stroke-width="1.5"/>
        <circle cx="138" cy="138" r="3"/>
        <!-- GPIO 18 destacado -->
        <circle cx="138" cy="156" r="4.2" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"/>
        <circle cx="138" cy="172" r="3"/><circle cx="138" cy="188" r="3"/><circle cx="138" cy="204" r="3"/>
        <circle cx="138" cy="220" r="3"/><circle cx="138" cy="236" r="3"/><circle cx="138" cy="252" r="3"/>
        <circle cx="138" cy="268" r="3"/>
      </g>
    </g>

    <!-- ══════════════════════════════════════════════════════════ -->
    <!--  BADGES INDICADORES DE PINES ESP32                         -->
    <!-- ══════════════════════════════════════════════════════════ -->

    <!-- Badge 3V3 (Rojo) -->
    <rect x="14" y="236" width="46" height="24" rx="12" fill="#ef4444" stroke="#ffffff" stroke-width="1.5"/>
    <text x="37" y="252" text-anchor="middle" fill="#ffffff" font-size="11" font-family="sans-serif" font-weight="bold">3V3</text>

    <!-- Badge GND (Negro) -->
    <rect x="10" y="266" width="50" height="24" rx="12" fill="#1f2937" stroke="#ffffff" stroke-width="1.5"/>
    <text x="35" y="282" text-anchor="middle" fill="#ffffff" font-size="11" font-family="sans-serif" font-weight="bold">GND</text>

    <!-- Badge GPIO 5 (Trig) - Verde -->
    <g transform="translate(206, 114)">
      <rect x="0" y="0" width="76" height="34" rx="8" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.8"/>
      <text x="38" y="15" text-anchor="middle" fill="#15803d" font-size="10.5" font-family="sans-serif" font-weight="bold">GPIO 5</text>
      <text x="38" y="28" text-anchor="middle" fill="#16a34a" font-size="9" font-family="sans-serif" font-weight="600">(Trig)</text>
    </g>

    <!-- Badge GPIO 18 (Echo) - Azul -->
    <g transform="translate(206, 154)">
      <rect x="0" y="0" width="76" height="34" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="1.8"/>
      <text x="38" y="15" text-anchor="middle" fill="#1d4ed8" font-size="10.5" font-family="sans-serif" font-weight="bold">GPIO 18</text>
      <text x="38" y="28" text-anchor="middle" fill="#2563eb" font-size="9" font-family="sans-serif" font-weight="600">(Echo)</text>
    </g>

    <!-- ══════════════════════════════════════════════════════════ -->
    <!--  SENSOR ULTRASÓNICO HC-SR04 (PCB AZUL + TRANSDUCTORES)     -->
    <!-- ══════════════════════════════════════════════════════════ -->
    <g transform="translate(440, 22)">
      <!-- PCB azul brillante HC-SR04 -->
      <rect x="0" y="0" width="225" height="106" rx="8" fill="#0284c7" stroke="#0369a1" stroke-width="2"/>
      
      <!-- Cristal oscilador metálico -->
      <rect x="96" y="4" width="33" height="13" rx="3" fill="url(#shieldGrad)" stroke="#52525b"/>

      <!-- Serigrafía HC-SR04 -->
      <text x="112" y="38" text-anchor="middle" fill="#ffffff" font-size="11" font-family="'Segoe UI', sans-serif" font-weight="bold">HC-SR04</text>

      <!-- Transductor Izquierdo (Emisor T) -->
      <circle cx="54" cy="53" r="38" fill="url(#metalBevel)" stroke="#475569" stroke-width="1.5"/>
      <circle cx="54" cy="53" r="32" fill="url(#meshGrad)"/>
      <circle cx="54" cy="53" r="16" fill="#18181b" stroke="#71717a" stroke-dasharray="2,2"/>
      <circle cx="54" cy="53" r="5" fill="#27272a"/>

      <!-- Transductor Derecho (Receptor R) -->
      <circle cx="171" cy="53" r="38" fill="url(#metalBevel)" stroke="#475569" stroke-width="1.5"/>
      <circle cx="171" cy="53" r="32" fill="url(#meshGrad)"/>
      <circle cx="171" cy="53" r="16" fill="#18181b" stroke="#71717a" stroke-dasharray="2,2"/>
      <circle cx="171" cy="53" r="5" fill="#27272a"/>

      <!-- 4 Pines Header metálicos apuntando hacia abajo -->
      <!-- VCC(55), Trig(80), Echo(105), GND(130) -->
      <rect x="53" y="102" width="4" height="22" fill="#e2e8f0" stroke="#64748b" stroke-width="0.8"/>
      <rect x="78" y="102" width="4" height="22" fill="#e2e8f0" stroke="#64748b" stroke-width="0.8"/>
      <rect x="103" y="102" width="4" height="22" fill="#e2e8f0" stroke="#64748b" stroke-width="0.8"/>
      <rect x="128" y="102" width="4" height="22" fill="#e2e8f0" stroke="#64748b" stroke-width="0.8"/>

      <!-- Etiquetas serigrafiadas de los 4 pines -->
      <text x="55" y="96" text-anchor="middle" fill="#ffffff" font-size="8.5" font-family="sans-serif" font-weight="bold">VCC</text>
      <text x="80" y="96" text-anchor="middle" fill="#ffffff" font-size="8.5" font-family="sans-serif" font-weight="bold">Trig</text>
      <text x="105" y="96" text-anchor="middle" fill="#ffffff" font-size="8.5" font-family="sans-serif" font-weight="bold">Echo</text>
      <text x="130" y="96" text-anchor="middle" fill="#ffffff" font-size="8.5" font-family="sans-serif" font-weight="bold">GND</text>
    </g>

    <!-- ══════════════════════════════════════════════════════════ -->
    <!--  CUADRO LEYENDA "CONEXIONES" (ESPACIO TOTALMENTE DESPEJADO)-->
    <!-- ══════════════════════════════════════════════════════════ -->
    <g transform="translate(600, 260)">
      <rect x="0" y="0" width="205" height="124" rx="8" fill="#1c385c" stroke="#2563eb" stroke-width="1.2" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.2))"/>
      
      <text x="102" y="23" text-anchor="middle" fill="#ffffff" font-size="12.5" font-family="'Segoe UI', sans-serif" font-weight="bold">Conexiones</text>
      
      <!-- Fila Rojo -->
      <line x1="12" y1="44" x2="34" y2="44" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
      <text x="40" y="47" fill="#f8fafc" font-size="9.5" font-family="sans-serif">ESP32 3V3 &rarr; HC-SR04 VCC</text>

      <!-- Fila Verde -->
      <line x1="12" y1="65" x2="34" y2="65" stroke="#16a34a" stroke-width="3" stroke-linecap="round"/>
      <text x="40" y="68" fill="#f8fafc" font-size="9.5" font-family="sans-serif">ESP32 GPIO 5 &rarr; HC-SR04 Trig</text>

      <!-- Fila Azul -->
      <line x1="12" y1="86" x2="34" y2="86" stroke="#2563eb" stroke-width="3" stroke-linecap="round"/>
      <text x="40" y="89" fill="#f8fafc" font-size="9.5" font-family="sans-serif">ESP32 GPIO 18 &rarr; HC-SR04 Echo</text>

      <!-- Fila Negro -->
      <line x1="12" y1="107" x2="34" y2="107" stroke="#111827" stroke-width="3" stroke-linecap="round"/>
      <text x="40" y="110" fill="#f8fafc" font-size="9.5" font-family="sans-serif">ESP32 GND &rarr; HC-SR04 GND</text>
    </g>
  </svg>
</div>

<div class="details-box">
  <p>Aquí tienes el diagrama de conexión del <strong>ESP32</strong> con el <strong>sensor ultrasónico HC-SR04</strong>.</p>

  <h3>Conexiones:</h3>
  <table>
    <thead>
      <tr>
        <th>ESP32</th>
        <th>HC-SR04</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>3V3</strong></td>
        <td><strong>VCC</strong></td>
      </tr>
      <tr>
        <td><strong>GPIO 5</strong></td>
        <td><strong>TRIG</strong></td>
      </tr>
      <tr>
        <td><strong>GPIO 18</strong></td>
        <td><strong>ECHO</strong></td>
      </tr>
      <tr>
        <td><strong>GND</strong></td>
        <td><strong>GND</strong></td>
      </tr>
    </tbody>
  </table>

  <div class="warn-box">
    <span class="tag-warn">Importante</span>
    El pin ECHO del HC-SR04 puede entregar 5 V y el ESP32 trabaja con lógica de 3.3 V. Utiliza un divisor de voltaje entre ECHO y GPIO 18 para proteger el ESP32.
  </div>

  <p style="margin-bottom: 0; color: #94a3b8;">También puedo prepararte el código Arduino IDE para medir distancias con este circuito.</p>
</div>

</body>
</html>
```"""
