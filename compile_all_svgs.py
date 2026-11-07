import sys
sys.stdout.reconfigure(encoding='utf-8')

SVG_L298N = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <!-- Placa PCB roja clásica L298N -->
  <rect x="25" y="20" width="150" height="115" rx="5" fill="#7f1d1d" stroke="#ef4444" stroke-width="1.5"/>
  <!-- Disipador de calor de aluminio negro grande -->
  <rect x="65" y="32" width="70" height="42" rx="3" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
  <line x1="75" y1="32" x2="75" y2="74" stroke="#0f172a" stroke-width="2"/>
  <line x1="85" y1="32" x2="85" y2="74" stroke="#0f172a" stroke-width="2"/>
  <line x1="95" y1="32" x2="95" y2="74" stroke="#0f172a" stroke-width="2"/>
  <line x1="105" y1="32" x2="105" y2="74" stroke="#0f172a" stroke-width="2"/>
  <line x1="115" y1="32" x2="115" y2="74" stroke="#0f172a" stroke-width="2"/>
  <line x1="125" y1="32" x2="125" y2="74" stroke="#0f172a" stroke-width="2"/>
  <!-- Chip L298 fijado al disipador -->
  <text x="100" y="58" fill="#f8fafc" font-size="9" font-weight="bold" font-family="sans-serif" text-anchor="middle">L298N DUAL</text>
  <!-- Bloques de terminales azules (Motores) -->
  <rect x="15" y="52" width="18" height="34" rx="2" fill="#0284c7" stroke="#38bdf8"/>
  <circle cx="24" cy="61" r="3" fill="#0f172a"/>
  <circle cx="24" cy="77" r="3" fill="#0f172a"/>
  <text x="18" y="96" fill="#38bdf8" font-size="7" font-weight="bold">OUT1/2</text>
  <rect x="167" y="52" width="18" height="34" rx="2" fill="#0284c7" stroke="#38bdf8"/>
  <circle cx="176" cy="61" r="3" fill="#0f172a"/>
  <circle cx="176" cy="77" r="3" fill="#0f172a"/>
  <text x="165" y="96" fill="#38bdf8" font-size="7" font-weight="bold">OUT3/4</text>
  <!-- Bloque de alimentación abajo izquierda -->
  <rect x="35" y="112" width="40" height="18" rx="2" fill="#0284c7" stroke="#38bdf8"/>
  <circle cx="43" cy="121" r="2.5" fill="#ef4444"/>
  <circle cx="55" cy="121" r="2.5" fill="#64748b"/>
  <circle cx="67" cy="121" r="2.5" fill="#10b981"/>
  <text x="43" y="140" fill="#ef4444" font-size="6" text-anchor="middle">12V</text>
  <text x="55" y="140" fill="#94a3b8" font-size="6" text-anchor="middle">GND</text>
  <text x="67" y="140" fill="#10b981" font-size="6" text-anchor="middle">5V</text>
  <!-- Pines de control lógica (ENA, IN1-IN4, ENB) -->
  <rect x="95" y="116" width="65" height="14" fill="#0f172a" stroke="#475569"/>
  <circle cx="102" cy="123" r="2" fill="#38bdf8"/>
  <circle cx="111" cy="123" r="2" fill="#f59e0b"/>
  <circle cx="120" cy="123" r="2" fill="#f59e0b"/>
  <circle cx="129" cy="123" r="2" fill="#f59e0b"/>
  <circle cx="138" cy="123" r="2" fill="#f59e0b"/>
  <circle cx="147" cy="123" r="2" fill="#38bdf8"/>
  <text x="128" y="140" fill="#f59e0b" font-size="6.5" font-weight="bold" text-anchor="middle">IN1 IN2 IN3 IN4</text>
  <text x="100" y="153" fill="#fca5a5" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">DRIVER PUENTE H DUAL L298N (2A)</text>
</svg>"""

SVG_MG996R = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <!-- Cuerpo negro del servomotor -->
  <rect x="45" y="38" width="110" height="75" rx="4" fill="#0f172a" stroke="#475569" stroke-width="1.5"/>
  <!-- Pestañas de fijación con agujeros de goma -->
  <rect x="25" y="65" width="20" height="22" rx="2" fill="#1e293b" stroke="#334155"/>
  <circle cx="35" cy="76" r="3.5" fill="#0b1329" stroke="#64748b"/>
  <rect x="155" y="65" width="20" height="22" rx="2" fill="#1e293b" stroke="#334155"/>
  <circle cx="165" cy="76" r="3.5" fill="#0b1329" stroke="#64748b"/>
  <!-- Etiqueta superior dorada MG996R -->
  <rect x="55" y="60" width="90" height="30" rx="2" fill="#b45309" stroke="#f59e0b"/>
  <text x="100" y="75" fill="#fef3c7" font-size="9" font-weight="bold" font-family="sans-serif" text-anchor="middle">TOWER PRO</text>
  <text x="100" y="86" fill="#ffffff" font-size="8.5" font-weight="bold" font-family="sans-serif" text-anchor="middle">MG996R METAL GEAR</text>
  <!-- Eje superior dentado de latón/cobre -->
  <circle cx="75" cy="38" r="14" fill="#d97706" stroke="#fbbf24" stroke-width="1.5"/>
  <circle cx="75" cy="38" r="6" fill="#92400e"/>
  <!-- Brazo de servo plástico blanco -->
  <rect x="68" y="10" width="14" height="28" rx="6" fill="#f1f5f9" stroke="#cbd5e1"/>
  <circle cx="75" cy="16" r="2.5" fill="#0f172a"/>
  <!-- Cable de 3 hilos -->
  <path d="M 130 113 Q 130 135 155 135" stroke="#78350f" stroke-width="2.5" fill="none"/>
  <path d="M 134 113 Q 134 135 159 135" stroke="#dc2626" stroke-width="2.5" fill="none"/>
  <path d="M 138 113 Q 138 135 163 135" stroke="#f59e0b" stroke-width="2.5" fill="none"/>
  <text x="100" y="152" fill="#fcd34d" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">SERVO METÁLICO 11 KG·CM (TORQUE)</text>
</svg>"""

SVG_SG90 = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <!-- Cuerpo azul translúcido SG90 -->
  <rect x="55" y="42" width="90" height="68" rx="4" fill="#0284c7" stroke="#38bdf8" stroke-width="1.5" opacity="0.9"/>
  <!-- Pestañas de montaje -->
  <rect x="38" y="66" width="17" height="20" rx="2" fill="#0369a1"/>
  <circle cx="46" cy="76" r="3" fill="#0b1329"/>
  <rect x="145" y="66" width="17" height="20" rx="2" fill="#0369a1"/>
  <circle cx="154" cy="76" r="3" fill="#0b1329"/>
  <!-- Texto etiqueta -->
  <rect x="65" y="62" width="70" height="26" fill="#0f172a" rx="2"/>
  <text x="100" y="75" fill="#38bdf8" font-size="8" font-weight="bold" text-anchor="middle">Tower Pro</text>
  <text x="100" y="84" fill="#f8fafc" font-size="7.5" font-weight="bold" text-anchor="middle">SG90 9g Micro</text>
  <!-- Eje y horn -->
  <circle cx="80" cy="42" r="11" fill="#f8fafc" stroke="#94a3b8"/>
  <rect x="75" y="16" width="10" height="26" rx="5" fill="#f8fafc" stroke="#94a3b8"/>
  <circle cx="80" cy="22" r="2" fill="#0f172a"/>
  <!-- Cables -->
  <path d="M 125 110 Q 125 132 145 132" stroke="#78350f" stroke-width="2" fill="none"/>
  <path d="M 128 110 Q 128 132 148 132" stroke="#ef4444" stroke-width="2" fill="none"/>
  <path d="M 131 110 Q 131 132 151 132" stroke="#f59e0b" stroke-width="2" fill="none"/>
  <text x="100" y="152" fill="#7dd3fc" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">MICRO SERVO SG90 (9 GRAMOS / 180°)</text>
</svg>"""

SVG_ESP32 = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <!-- Placa negra ESP32 -->
  <rect x="42" y="15" width="116" height="125" rx="5" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
  <!-- Pines laterales dorados -->
  <rect x="36" y="22" width="6" height="110" fill="#f59e0b"/>
  <rect x="158" y="22" width="6" height="110" fill="#f59e0b"/>
  <!-- Blindaje metálico ESP-WROOM-32 -->
  <rect x="58" y="42" width="84" height="64" rx="3" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1.2"/>
  <!-- Logo y texto grabado -->
  <text x="100" y="64" fill="#0f172a" font-size="10" font-weight="bold" font-family="sans-serif" text-anchor="middle">ESP-WROOM-32</text>
  <text x="100" y="78" fill="#334155" font-size="7" font-weight="bold" font-family="sans-serif" text-anchor="middle">WiFi + Bluetooth SoC</text>
  <text x="100" y="90" fill="#0284c7" font-size="7.5" font-weight="bold" font-family="sans-serif" text-anchor="middle">240 MHz Dual-Core</text>
  <!-- Antena PCB arriba -->
  <path d="M 65 34 L 75 34 L 75 25 L 85 25 L 85 34 L 95 34 L 95 25 L 105 25 L 105 34 L 115 34 L 115 25 L 125 25 L 125 34 L 135 34" stroke="#f59e0b" stroke-width="2" fill="none"/>
  <!-- Botones EN y BOOT -->
  <rect x="52" y="118" width="10" height="8" rx="1" fill="#475569"/>
  <text x="57" y="115" fill="#94a3b8" font-size="5" text-anchor="middle">EN</text>
  <rect x="138" y="118" width="10" height="8" rx="1" fill="#475569"/>
  <text x="143" y="115" fill="#94a3b8" font-size="5" text-anchor="middle">BOOT</text>
  <!-- Puerto micro USB -->
  <rect x="88" y="128" width="24" height="12" rx="2" fill="#94a3b8" stroke="#475569"/>
  <text x="100" y="153" fill="#38bdf8" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">ESP32 DEVKIT V1 (38 PINES)</text>
</svg>"""

SVG_OLED = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <rect x="35" y="25" width="130" height="105" rx="4" fill="#0f172a" stroke="#0284c7" stroke-width="1.5"/>
  <!-- Pantalla OLED negra brillante -->
  <rect x="48" y="45" width="104" height="65" rx="3" fill="#030712" stroke="#1e293b"/>
  <!-- Gráfica de telemetría simulada en cian -->
  <polyline points="55,95 70,85 85,90 100,65 115,75 130,55 145,60" fill="none" stroke="#38bdf8" stroke-width="1.8"/>
  <text x="55" y="60" fill="#facc15" font-size="7" font-weight="bold">TEMP: 24.5 C</text>
  <text x="55" y="70" fill="#38bdf8" font-size="7" font-weight="bold">AUREX 128x64</text>
  <!-- 4 Pines arriba -->
  <rect x="70" y="18" width="60" height="14" fill="#1e293b" rx="2"/>
  <circle cx="78" cy="25" r="2.5" fill="#64748b"/>
  <circle cx="92" cy="25" r="2.5" fill="#ef4444"/>
  <circle cx="107" cy="25" r="2.5" fill="#38bdf8"/>
  <circle cx="122" cy="25" r="2.5" fill="#a855f7"/>
  <text x="78" y="38" fill="#94a3b8" font-size="5.5" text-anchor="middle">GND</text>
  <text x="92" y="38" fill="#ef4444" font-size="5.5" text-anchor="middle">VCC</text>
  <text x="107" y="38" fill="#38bdf8" font-size="5.5" text-anchor="middle">SCL</text>
  <text x="122" y="38" fill="#a855f7" font-size="5.5" text-anchor="middle">SDA</text>
  <text x="100" y="152" fill="#7dd3fc" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">PANTALLA OLED 0.96\" I2C (SSD1306)</text>
</svg>"""

SVG_MPU6050 = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <!-- Placa GY-521 azul -->
  <rect x="40" y="25" width="120" height="100" rx="4" fill="#0369a1" stroke="#38bdf8" stroke-width="1.5"/>
  <!-- Chip MPU-6050 QFN central -->
  <rect x="80" y="55" width="40" height="40" rx="2" fill="#0f172a" stroke="#334155"/>
  <circle cx="87" cy="62" r="2" fill="#38bdf8"/>
  <text x="100" y="74" fill="#e2e8f0" font-size="6.5" font-weight="bold" text-anchor="middle">MPU-6050</text>
  <text x="100" y="84" fill="#94a3b8" font-size="6" text-anchor="middle">6-DOF IMU</text>
  <!-- Cruz de ejes X Y Z -->
  <line x1="135" y1="75" x2="150" y2="75" stroke="#ef4444" stroke-width="2"/>
  <text x="154" y="78" fill="#ef4444" font-size="7" font-weight="bold">X</text>
  <line x1="135" y1="75" x2="135" y2="60" stroke="#22c55e" stroke-width="2"/>
  <text x="135" y="55" fill="#22c55e" font-size="7" font-weight="bold" text-anchor="middle">Y</text>
  <!-- Pines inferiores -->
  <rect x="48" y="115" width="104" height="12" fill="#0f172a"/>
  <circle cx="56" cy="121" r="2" fill="#ef4444"/>
  <circle cx="68" cy="121" r="2" fill="#64748b"/>
  <circle cx="80" cy="121" r="2" fill="#38bdf8"/>
  <circle cx="92" cy="121" r="2" fill="#a855f7"/>
  <text x="56" y="136" fill="#ef4444" font-size="5" text-anchor="middle">VCC</text>
  <text x="68" y="136" fill="#94a3b8" font-size="5" text-anchor="middle">GND</text>
  <text x="80" y="136" fill="#38bdf8" font-size="5" text-anchor="middle">SCL</text>
  <text x="92" y="136" fill="#a855f7" font-size="5" text-anchor="middle">SDA</text>
  <text x="100" y="152" fill="#bae6fd" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">MPU-6050 (ACELERÓMETRO + GIROSCOPIO)</text>
</svg>"""

SVG_ARDUINO = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <!-- Placa azul/verde Arduino Uno -->
  <rect x="30" y="20" width="140" height="110" rx="6" fill="#0284c7" stroke="#38bdf8" stroke-width="1.5"/>
  <!-- Puerto USB-B plateado -->
  <rect x="22" y="32" width="28" height="24" rx="2" fill="#cbd5e1" stroke="#64748b"/>
  <!-- Jack de barril DC negro -->
  <rect x="22" y="80" width="28" height="28" rx="2" fill="#1e293b" stroke="#0f172a"/>
  <!-- Chip ATmega328P DIP-28 -->
  <rect x="80" y="65" width="60" height="22" rx="2" fill="#0f172a" stroke="#334155"/>
  <text x="110" y="78" fill="#f8fafc" font-size="7.5" font-weight="bold" font-family="sans-serif" text-anchor="middle">ATmega328P</text>
  <!-- Headers de pines superior e inferior -->
  <rect x="75" y="22" width="85" height="8" fill="#0f172a"/>
  <rect x="75" y="118" width="85" height="8" fill="#0f172a"/>
  <!-- Botón de Reset rojo -->
  <circle cx="62" cy="38" r="4" fill="#ef4444" stroke="#991b1b"/>
  <!-- Texto UNO -->
  <text x="115" y="52" fill="#ffffff" font-size="12" font-weight="bold" font-family="sans-serif">UNO</text>
  <text x="115" y="105" fill="#bae6fd" font-size="7" font-family="sans-serif">ITALY R3</text>
  <text x="100" y="152" fill="#7dd3fc" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">ARDUINO UNO R3 (ATMEGA328P)</text>
</svg>"""

SVG_RELE = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <!-- Placa PCB azul del relé -->
  <rect x="35" y="22" width="130" height="110" rx="4" fill="#0369a1" stroke="#38bdf8" stroke-width="1.5"/>
  <!-- Cubo azul del relé Songle -->
  <rect x="50" y="42" width="65" height="70" rx="3" fill="#1d4ed8" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="82.5" y="66" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">SONGLE</text>
  <text x="82.5" y="78" fill="#bae6fd" font-size="7" text-anchor="middle">10A 250VAC</text>
  <text x="82.5" y="90" fill="#bae6fd" font-size="7" text-anchor="middle">10A 30VDC</text>
  <text x="82.5" y="102" fill="#facc15" font-size="7.5" font-weight="bold" text-anchor="middle">5V COIL</text>
  <!-- Bloque de terminales verde alta potencia a la derecha -->
  <rect x="135" y="48" width="22" height="58" rx="2" fill="#15803d" stroke="#22c55e"/>
  <circle cx="146" cy="58" r="3" fill="#0f172a"/>
  <circle cx="146" cy="77" r="3" fill="#0f172a"/>
  <circle cx="146" cy="96" r="3" fill="#0f172a"/>
  <text x="146" y="118" fill="#86efac" font-size="6" text-anchor="middle">NO COM NC</text>
  <!-- Pines de entrada abajo -->
  <rect x="45" y="122" width="28" height="10" fill="#0f172a"/>
  <circle cx="50" cy="127" r="2" fill="#ef4444"/>
  <circle cx="58" cy="127" r="2" fill="#38bdf8"/>
  <circle cx="66" cy="127" r="2" fill="#64748b"/>
  <text x="50" y="142" fill="#ef4444" font-size="5" text-anchor="middle">VCC</text>
  <text x="58" y="142" fill="#38bdf8" font-size="5" text-anchor="middle">IN</text>
  <text x="66" y="142" fill="#94a3b8" font-size="5" text-anchor="middle">GND</text>
  <text x="100" y="152" fill="#7dd3fc" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">MÓDULO RELÉ 5V OPTOACOPLADO (10A)</text>
</svg>"""

SVG_TCRT = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <!-- Placa seguidor de línea -->
  <rect x="40" y="25" width="120" height="105" rx="4" fill="#0369a1" stroke="#38bdf8" stroke-width="1.5"/>
  <!-- Par emisor/receptor óptico (azul y negro) -->
  <rect x="80" y="32" width="40" height="25" rx="3" fill="#0f172a" stroke="#475569"/>
  <circle cx="90" cy="44" r="6" fill="#38bdf8" opacity="0.8"/>
  <circle cx="110" cy="44" r="6" fill="#0f172a" stroke="#64748b"/>
  <!-- Potenciómetro azul de sensibilidad -->
  <rect x="85" y="68" width="30" height="20" rx="2" fill="#0284c7"/>
  <circle cx="100" cy="78" r="4" fill="#f8fafc"/>
  <!-- Pines de conexión abajo -->
  <rect x="65" y="118" width="70" height="12" fill="#0f172a"/>
  <circle cx="75" cy="124" r="2" fill="#ef4444"/>
  <circle cx="90" cy="124" r="2" fill="#64748b"/>
  <circle cx="105" cy="124" r="2" fill="#38bdf8"/>
  <circle cx="120" cy="124" r="2" fill="#a855f7"/>
  <text x="75" y="139" fill="#ef4444" font-size="5.5" text-anchor="middle">VCC</text>
  <text x="90" y="139" fill="#94a3b8" font-size="5.5" text-anchor="middle">GND</text>
  <text x="105" y="139" fill="#38bdf8" font-size="5.5" text-anchor="middle">D0</text>
  <text x="120" y="139" fill="#a855f7" font-size="5.5" text-anchor="middle">A0</text>
  <text x="100" y="152" fill="#7dd3fc" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">TCRT5000 ÓPTICO SEGUIDOR DE LÍNEA</text>
</svg>"""

print("All 9 SVGs compiled successfully!")
