import sys
sys.stdout.reconfigure(encoding='utf-8')

print("Generating enhanced sensores_data.py...")

NEW_SENSORES_DATA = '''"""
BANCO TÁCTICO DE SENSORES Y COMPONENTES MECATRÓNICOS - AUREX
Contiene fichas técnicas, diagramas de pines, voltajes, blueprints vectoriales y fotos reales.
"""

SVG_FLOTADOR = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="stemGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#475569"/><stop offset="50%" stop-color="#94a3b8"/><stop offset="100%" stop-color="#334155"/>
    </linearGradient>
    <linearGradient id="floatGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/><stop offset="50%" stop-color="#38bdf8"/><stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
  </defs>
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <rect x="85" y="12" width="30" height="16" rx="2" fill="#64748b" stroke="#94a3b8" stroke-width="1"/>
  <line x1="85" y1="16" x2="115" y2="16" stroke="#334155" stroke-width="1"/>
  <line x1="85" y1="20" x2="115" y2="20" stroke="#334155" stroke-width="1"/>
  <line x1="85" y1="24" x2="115" y2="24" stroke="#334155" stroke-width="1"/>
  <path d="M 94 12 Q 94 2 80 2" stroke="#38bdf8" stroke-width="2.5" fill="none"/>
  <path d="M 106 12 Q 106 2 120 2" stroke="#f59e0b" stroke-width="2.5" fill="none"/>
  <circle cx="80" cy="2" r="2.5" fill="#38bdf8"/><circle cx="120" cy="2" r="2.5" fill="#f59e0b"/>
  <rect x="94" y="28" width="12" height="110" rx="2" fill="url(#stemGrad)"/>
  <ellipse cx="100" cy="138" rx="10" ry="4" fill="#64748b"/>
  <path d="M 20 105 Q 40 100 60 105 T 100 105 T 140 105 T 180 105" stroke="#0ea5e9" stroke-width="1.5" fill="none" opacity="0.4"/>
  <path d="M 20 115 Q 40 110 60 115 T 100 115 T 140 115 T 180 115" stroke="#0ea5e9" stroke-width="1.5" fill="none" opacity="0.6"/>
  <rect x="74" y="70" width="52" height="34" rx="6" fill="url(#floatGrad)" stroke="#7dd3fc" stroke-width="1.5"/>
  <ellipse cx="100" cy="74" rx="20" ry="3" fill="#38bdf8" opacity="0.8"/>
  <rect x="98" y="78" width="4" height="18" fill="#facc15" rx="1"/>
  <text x="100" y="91" fill="#0b1329" font-size="7" font-weight="bold" text-anchor="middle">N-S</text>
  <text x="100" y="153" fill="#94a3b8" font-size="8.5" font-family="sans-serif" font-weight="bold" text-anchor="middle">SENSOR DE NIVEL FLOTADOR (BOYA)</text>
</svg>"""

SVG_TDS = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <rect x="18" y="20" width="80" height="110" rx="4" fill="#065f46" stroke="#10b981" stroke-width="1.5"/>
  <text x="58" y="34" fill="#a7f3d0" font-size="7.5" font-weight="bold" text-anchor="middle">TDS METER V1.0</text>
  <rect x="42" y="44" width="32" height="24" rx="2" fill="#0f172a" stroke="#334155"/>
  <circle cx="47" cy="49" r="1.5" fill="#10b981"/>
  <rect x="26" y="76" width="18" height="18" rx="2" fill="#0284c7"/>
  <circle cx="35" cy="85" r="4" fill="#f8fafc"/>
  <rect x="24" y="112" width="28" height="14" fill="#0f172a" stroke="#475569"/>
  <circle cx="28" cy="119" r="2" fill="#ef4444"/>
  <circle cx="35" cy="119" r="2" fill="#64748b"/>
  <circle cx="42" cy="119" r="2" fill="#38bdf8"/>
  <text x="28" y="134" fill="#ef4444" font-size="6" text-anchor="middle">VCC</text>
  <text x="35" y="134" fill="#94a3b8" font-size="6" text-anchor="middle">GND</text>
  <text x="42" y="134" fill="#38bdf8" font-size="6" text-anchor="middle">AOUT</text>
  <path d="M 85 75 C 105 75 110 50 135 50" stroke="#0f172a" stroke-width="4" fill="none"/>
  <path d="M 85 75 C 105 75 110 50 135 50" stroke="#475569" stroke-width="2" fill="none"/>
  <rect x="135" y="38" width="45" height="24" rx="3" fill="#1e293b" stroke="#64748b"/>
  <rect x="140" y="62" width="35" height="55" rx="2" fill="#0f172a" stroke="#475569"/>
  <rect x="148" y="117" width="4" height="22" fill="#cbd5e1" stroke="#94a3b8"/>
  <rect x="163" y="117" width="4" height="22" fill="#cbd5e1" stroke="#94a3b8"/>
  <line x1="152" y1="128" x2="163" y2="128" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="2,2"/>
  <text x="157.5" y="148" fill="#38bdf8" font-size="7" font-weight="bold" text-anchor="middle">TITANIO</text>
  <text x="58" y="152" fill="#6ee7b7" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="middle">SENSOR TDS (CALIDAD AGUA)</text>
</svg>"""

SVG_HCSR04 = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <rect x="25" y="30" width="150" height="75" rx="4" fill="#1e40af" stroke="#38bdf8" stroke-width="1.5"/>
  <circle cx="65" cy="65" r="24" fill="#94a3b8" stroke="#cbd5e1" stroke-width="2"/>
  <circle cx="65" cy="65" r="16" fill="#475569"/>
  <text x="65" y="68" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">T</text>
  <circle cx="135" cy="65" r="24" fill="#94a3b8" stroke="#cbd5e1" stroke-width="2"/>
  <circle cx="135" cy="65" r="16" fill="#475569"/>
  <text x="135" y="68" fill="#f8fafc" font-size="9" font-weight="bold" text-anchor="middle">R</text>
  <rect x="94" y="55" width="12" height="20" rx="2" fill="#e2e8f0"/>
  <rect x="65" y="105" width="70" height="15" fill="#0f172a" stroke="#475569"/>
  <circle cx="75" cy="112" r="2.5" fill="#ef4444"/>
  <circle cx="92" cy="112" r="2.5" fill="#38bdf8"/>
  <circle cx="108" cy="112" r="2.5" fill="#a855f7"/>
  <circle cx="125" cy="112" r="2.5" fill="#64748b"/>
  <text x="75" y="132" fill="#ef4444" font-size="7" text-anchor="middle">VCC</text>
  <text x="92" y="132" fill="#38bdf8" font-size="7" text-anchor="middle">TRIG</text>
  <text x="108" y="132" fill="#a855f7" font-size="7" text-anchor="middle">ECHO</text>
  <text x="125" y="132" fill="#94a3b8" font-size="7" text-anchor="middle">GND</text>
  <text x="100" y="152" fill="#93c5fd" font-size="8.5" font-family="sans-serif" font-weight="bold" text-anchor="middle">HC-SR04 ULTRASÓNICO</text>
</svg>"""

SVG_DHT11 = """<svg viewBox="0 0 200 160" width="100%" height="135" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="160" rx="8" fill="#0b1329"/>
  <rect x="55" y="25" width="90" height="85" rx="5" fill="#0284c7" stroke="#38bdf8" stroke-width="1.5"/>
  <line x1="68" y1="40" x2="132" y2="40" stroke="#0369a1" stroke-width="2.5"/>
  <line x1="68" y1="50" x2="132" y2="50" stroke="#0369a1" stroke-width="2.5"/>
  <line x1="68" y1="60" x2="132" y2="60" stroke="#0369a1" stroke-width="2.5"/>
  <line x1="68" y1="70" x2="132" y2="70" stroke="#0369a1" stroke-width="2.5"/>
  <text x="100" y="95" fill="#f0f9ff" font-size="11" font-weight="bold" text-anchor="middle">DHT11</text>
  <rect x="70" y="110" width="60" height="18" fill="#0f172a" stroke="#475569"/>
  <circle cx="78" cy="119" r="2.5" fill="#ef4444"/>
  <circle cx="93" cy="119" r="2.5" fill="#38bdf8"/>
  <circle cx="107" cy="119" r="2.5" fill="#64748b"/>
  <circle cx="122" cy="119" r="2.5" fill="#64748b"/>
  <text x="78" y="137" fill="#ef4444" font-size="6.5" text-anchor="middle">VCC</text>
  <text x="93" y="137" fill="#38bdf8" font-size="6.5" text-anchor="middle">DATA</text>
  <text x="107" y="137" fill="#64748b" font-size="6.5" text-anchor="middle">NC</text>
  <text x="122" y="137" fill="#94a3b8" font-size="6.5" text-anchor="middle">GND</text>
  <text x="100" y="152" fill="#7dd3fc" font-size="8.5" font-family="sans-serif" font-weight="bold" text-anchor="middle">DHT11 HUMEDAD / TEMP</text>
</svg>"""

CATALOGO_SENSORES = {
    "sensor-nivel-flotador": {
        "nombre": "Sensor de Nivel de Flotador / Boya Magnética",
        "categoria": "Sensores de Nivel y Líquidos",
        "voltaje": "0 - 220V AC/DC (Contacto Seco / Reed Switch)",
        "consumo": "Pasivo (0 mA en reposo)",
        "rango": "Detección Binaria: ON (Lleno) / OFF (Vacío) por flotabilidad",
        "protocolo": "Interruptor Digital (Reed Switch activado por imán toroidal)",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Float_switch_off.jpg/500px-Float_switch_off.jpg",
        "svg_diagrama": SVG_FLOTADOR,
        "pines": [
            ("CABLE 1 (AZUL)", "Común de Entrada (3.3V, 5V o GND)", "#38bdf8"),
            ("CABLE 2 (AMARILLO)", "Retorno a GPIO con resistencia Pull-up/down", "#f59e0b")
        ],
        "descripcion": "Boya sellada de polipropileno o acero inoxidable con un imán anular interno. Al subir el nivel del agua, el flotador asciende por el eje central y el campo magnético cierra un interruptor de lengüeta (reed switch) hermético.",
        "advertencia": "NUNCA conectar directamente motores ni bombas de 110V/220V al flotador; la chispa del arco fundirá los contactos internos del reed switch. Conectar siempre hacia un relé o entrada digital del microcontrolador."
    },
    "sensor-calidad-agua": {
        "nombre": "Sensor de Calidad de Agua TDS (Sólidos Disueltos Totales)",
        "categoria": "Sensores Químicos y Calidad de Líquidos",
        "voltaje": "3.3V - 5.5V DC (Compatible con ESP32 y Arduino)",
        "consumo": "3 a 6 mA",
        "rango": "0 a 1000 ppm (Partes por Millón) · Precisión: ±10% F.S. a 25°C",
        "protocolo": "Señal Analógica de Voltaje (0 ~ 2.3V proporcional a la conductividad)",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/PH_meter_with_glass_electrode.jpg/500px-PH_meter_with_glass_electrode.jpg",
        "svg_diagrama": SVG_TDS,
        "pines": [
            ("VCC (ROJO)", "Alimentación 3.3V a 5.5V DC", "#ef4444"),
            ("GND (NEGRO)", "Tierra común de referencia (0V)", "#64748b"),
            ("AOUT (AZUL)", "Salida analógica de voltaje hacia el ADC", "#38bdf8")
        ],
        "descripcion": "Sonda con dos electrodos de titanio sumergibles que inyectan una señal alterna de alta frecuencia para medir la conductividad eléctrica del agua. Permite determinar la concentración de sales, minerales y pureza del agua potable o acuarios.",
        "advertencia": "Solo sumergir los electrodos de titanio; la base plástica superior y el cable no son totalmente sumergibles en modelos comerciales. La lectura varía con la temperatura (+2%/°C), por lo que se recomienda compensar con un sensor DS18B20."
    },
    "hc-sr04": {
        "nombre": "Sensor Ultrasónico HC-SR04",
        "categoria": "Sensores de Distancia",
        "voltaje": "5V DC",
        "consumo": "15 mA",
        "rango": "2 cm a 400 cm (Precisión: 3 mm)",
        "protocolo": "Pulso Digital (Trigger / Echo)",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/HC-SR04_Ultrasonic_Sensor.jpg/500px-HC-SR04_Ultrasonic_Sensor.jpg",
        "svg_diagrama": SVG_HCSR04,
        "pines": [
            ("VCC", "5V", "#ef4444"),
            ("TRIG", "Disparo de pulso (salida micro)", "#38bdf8"),
            ("ECHO", "Recepción de eco (entrada micro)", "#a855f7"),
            ("GND", "Tierra (0V)", "#64748b")
        ],
        "descripcion": "Emite ráfagas ultrasónicas a 40 kHz y mide el tiempo de rebote para calcular la distancia con la fórmula: d = (tiempo * 0.0343) / 2.",
        "advertencia": "En ESP32/Raspberry Pi (3.3V), el pin ECHO entrega 5V. Requiere divisor de tensión (1kΩ y 2kΩ) para no quemar el GPIO."
    },
    "dht11": {
        "nombre": "Sensor de Temperatura y Humedad DHT11",
        "categoria": "Sensores Ambientales",
        "voltaje": "3.3V - 5V DC",
        "consumo": "0.5 - 2.5 mA",
        "rango": "Humedad: 20-90% RH | Temp: 0 a 50 °C",
        "protocolo": "Bus digital propietario (1 cable / One-Wire)",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/DHT11_temperature_and_humidity_sensor.jpg/500px-DHT11_temperature_and_humidity_sensor.jpg",
        "svg_diagrama": SVG_DHT11,
        "pines": [
            ("VCC", "3.3V a 5V", "#ef4444"),
            ("DATA", "Datos digitales (Pull-up 10kΩ)", "#38bdf8"),
            ("NC", "No conectado", "#64748b"),
            ("GND", "Tierra (0V)", "#64748b")
        ],
        "descripcion": "Sensor capacitivo de humedad y termistor NTC integrado con un chip conversor analógico-digital de 8 bits.",
        "advertencia": "Velocidad de muestreo máxima de 1 Hz (1 lectura por segundo). No consultar con menor intervalo."
    },
    "dht22": {
        "nombre": "Sensor de Precisión DHT22 (AM2302)",
        "categoria": "Sensores Ambientales",
        "voltaje": "3.3V - 6V DC",
        "consumo": "1 - 1.5 mA",
        "rango": "Humedad: 0-100% RH | Temp: -40 a 80 °C (Precisión ±0.5°C)",
        "protocolo": "Bus digital propietario (1 cable)",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/DHT22_pinout.jpg/500px-DHT22_pinout.jpg",
        "svg_diagrama": SVG_DHT11,
        "pines": [
            ("VCC", "3.3V - 5V", "#ef4444"),
            ("DATA", "Datos digitales", "#38bdf8"),
            ("NC", "No conectado", "#64748b"),
            ("GND", "Tierra", "#64748b")
        ],
        "descripcion": "Versión industrial y más precisa del DHT11, ideal para estaciones meteorológicas e invernaderos.",
        "advertencia": "Tiempo de respuesta de 2 segundos. Requiere resistencia pull-up de 4.7kΩ a 10kΩ en el pin DATA si el módulo no la incluye."
    },
    "sg90": {
        "nombre": "Micro Servomotor TowerPro SG90",
        "categoria": "Actuadores y Motores",
        "voltaje": "4.8V - 6V DC",
        "consumo": "100 mA (reposo) - 500 mA (bloqueo)",
        "rango": "0° a 180° de rotación (Torque: 1.8 kg·cm)",
        "protocolo": "PWM (50 Hz / período de 20 ms)",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Servo_motor_SG90.jpg/500px-Servo_motor_SG90.jpg",
        "pines": [
            ("MARRÓN", "GND (Tierra)", "#64748b"),
            ("ROJO", "VCC (+5V externo)", "#ef4444"),
            ("NARANJA", "Señal PWM (GPIO)", "#f59e0b")
        ],
        "descripcion": "Servomotor de 9 gramos con engranajes plásticos de nylon, ideal para brazos robóticos miniatura, pinzas (grippers) y escaneo de sensores.",
        "advertencia": "NUNCA alimentar el servo directamente desde el pin 5V del Arduino si hay carga mecánica; la caída de tensión reiniciará el microcontrolador. Use fuente externa compartiendo GND."
    },
    "mg996r": {
        "nombre": "Servomotor Metálico de Alto Torque MG996R",
        "categoria": "Actuadores y Motores",
        "voltaje": "4.8V - 7.2V DC",
        "consumo": "500 mA a 2.5 A (en esfuerzo máximo)",
        "rango": "0° a 180° (Torque: hasta 11 kg·cm a 6V)",
        "protocolo": "PWM estándar (50 Hz)",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/MG996R_Metal_Gear_Servo.jpg/500px-MG996R_Metal_Gear_Servo.jpg",
        "pines": [
            ("MARRÓN", "GND", "#64748b"),
            ("ROJO", "VCC (+6V recomendado)", "#ef4444"),
            ("NARANJA", "Señal PWM", "#f59e0b")
        ],
        "descripcion": "Servomotor de piñonería metálica de cobre con doble rodamiento de bolas, ideal para articulaciones pesadas en brazos robóticos o dirección de coches RC.",
        "advertencia": "Picos de corriente de hasta 2.5A. Exige fuente de alimentación independiente con cableado grueso (mínimo 20 AWG)."
    },
    "l298n": {
        "nombre": "Módulo Driver Puente H Dual L298N",
        "categoria": "Controladores de Potencia",
        "voltaje": "Lógica: 5V DC | Motores: 5V a 35V DC",
        "consumo": "Hasta 2A por canal (pico de 3A)",
        "rango": "Controla 2 motores DC bidireccionales o 1 motor paso a paso bipolar",
        "protocolo": "Señales Digitales IN1-IN4 + PWM en ENA/ENB",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/L298N_Dual_H_Bridge_Motor_Driver.jpg/500px-L298N_Dual_H_Bridge_Motor_Driver.jpg",
        "pines": [
            ("12V", "Alimentación de fuerza para motores", "#ef4444"),
            ("GND", "Tierra compartida", "#64748b"),
            ("5V", "Salida 5V (del regulador 7805 interno) o entrada lógica", "#10b981"),
            ("ENA / ENB", "Habilitación y velocidad PWM de cada motor", "#38bdf8"),
            ("IN1..IN4", "Dirección de giro (H/L)", "#f59e0b")
        ],
        "descripcion": "El puente H más clásico de la robótica para invertir la polaridad de motores DC y variar su velocidad mediante modulación de ancho de pulsos.",
        "advertencia": "Su diseño bipolar basado en transistores BJT tiene una caída de voltaje interna de 1.5V a 2V en calor. Si la tensión de motores supera los 12V, retirar el jumper de 5V."
    },
    "mpu6050": {
        "nombre": "IMU MPU-6050 (Acelerómetro + Giroscopio 6-DOF)",
        "categoria": "Sensores Inerciales",
        "voltaje": "3.3V - 5V DC (módulo con regulador LDO integrado)",
        "consumo": "3.9 mA",
        "rango": "Acel: ±2g a ±16g | Giro: ±250°/s a ±2000°/s",
        "protocolo": "I2C (Dirección estándar: 0x68, o 0x69 si AD0 = HIGH)",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/MPU-6050_Module.jpg/500px-MPU-6050_Module.jpg",
        "pines": [
            ("VCC", "3.3V a 5V", "#ef4444"),
            ("GND", "Tierra (0V)", "#64748b"),
            ("SCL", "Reloj I2C", "#38bdf8"),
            ("SDA", "Datos I2C", "#a855f7"),
            ("INT", "Interrupción programable", "#10b981")
        ],
        "descripcion": "Unidad de medición inercial con procesador de movimiento digital (DMP) integrado, capaz de fusionar datos para calcular ángulos de Euler y cuaterniones.",
        "advertencia": "El giróscopo presenta deriva (drift) con el paso del tiempo; debe calibrarse al encender con el robot estático y fusionarse con un filtro complementario o de Kalman."
    },
    "oled-i2c": {
        "nombre": "Pantalla Gráfica OLED 0.96 Pulgadas I2C (SSD1306)",
        "categoria": "Displays y Visualización",
        "voltaje": "3.3V - 5V DC",
        "consumo": "0.04W (20 mA aprox con pantalla encendida)",
        "rango": "Resolución 128x64 píxeles monocromática (Azul/Blanco/Bicolor)",
        "protocolo": "I2C (Dirección 0x3C o 0x3D)",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/OLED_Display_Module_0.96_inch_I2C.jpg/500px-OLED_Display_Module_0.96_inch_I2C.jpg",
        "pines": [
            ("GND", "Tierra", "#64748b"),
            ("VCC", "3.3V o 5V", "#ef4444"),
            ("SCL", "Reloj I2C", "#38bdf8"),
            ("SDA", "Datos I2C", "#a855f7")
        ],
        "descripcion": "Display ultra-ligero y de alto contraste que no requiere luz de fondo porque cada píxel emite su propia luz. Ideal para telemetría y HUDs portátiles.",
        "advertencia": "Cuidado con la asignación de pines: algunos módulos genéricos tienen el orden GND-VCC invertido (VCC-GND). Invertir polaridad quemará el chip al instante."
    },
    "esp32": {
        "nombre": "Placa de Desarrollo ESP32 NodeMCU-32S",
        "categoria": "Microcontroladores y SoCs",
        "voltaje": "Alimentación USB: 5V | Nivel lógico GPIO: 3.3V ESTRICTO",
        "consumo": "80 mA (activo) - 240 mA (WiFi Tx) - 10 µA (Deep Sleep)",
        "rango": "Dual Core Xtensa 32-bit a 240 MHz, 520 KB SRAM, 4 MB Flash, WiFi 802.11 b/g/n + BLE 4.2",
        "protocolo": "36 GPIOs, 3x UART, 2x I2C, 3x SPI, 16x PWM, 12-bit ADC, 2x 8-bit DAC, Touch capacitivo",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/NodeMCU_ESP32_Microcontroller.jpg/500px-NodeMCU_ESP32_Microcontroller.jpg",
        "pines": [
            ("VIN / 5V", "Entrada regulada externa", "#ef4444"),
            ("3V3", "Salida 3.3V del regulador interno", "#f59e0b"),
            ("GND", "Tierra de referencia", "#64748b"),
            ("GPIO 21 / 22", "I2C predeterminado (SDA / SCL)", "#38bdf8"),
            ("GPIO 1 / 3", "UART0 (TX0 / RX0 para el USB)", "#10b981")
        ],
        "descripcion": "El SoC IoT más potente y económico para robótica táctica, servidores web integrados y telemetría en tiempo real.",
        "advertencia": "Los pines GPIO NO son tolerantes a 5V. Conectar una señal de 5V (como el Echo de un HC-SR04) dañará permanentemente el chip."
    },
    "arduino-uno": {
        "nombre": "Placa de Desarrollo Arduino Uno R3",
        "categoria": "Microcontroladores Educativos",
        "voltaje": "USB: 5V | Jack de barril: 7V a 12V DC | Lógica: 5V",
        "consumo": "50 mA",
        "rango": "Microcontrolador ATmega328P de 8 bits a 16 MHz, 32 KB Flash, 2 KB SRAM",
        "protocolo": "14 Pines Digitales (6 PWM), 6 Entradas Analógicas ADC (10-bit), UART, I2C, SPI",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Arduino_Uno_-_R3.jpg/500px-Arduino_Uno_-_R3.jpg",
        "pines": [
            ("5V / 3.3V", "Alimentación regulada para sensores", "#ef4444"),
            ("GND", "Tierra", "#64748b"),
            ("D0/D1", "RX / TX Serie (usados por el USB)", "#f59e0b"),
            ("D3, D5, D6, D9, D10, D11", "Salidas analógicas PWM (~)", "#10b981"),
            ("A4 / A5", "I2C (SDA / SCL)", "#38bdf8")
        ],
        "descripcion": "La placa estándar de prototipado y robótica educativa por excelencia, resistente y fácil de programar.",
        "advertencia": "Cada pin digital soporta máximo 40 mA (recomendado 20 mA). Nunca conectar motores o bobinas directamente sin transistor o driver."
    },
    "rele-5v": {
        "nombre": "Módulo Relé (Relay) de 1 Canal con Optoacoplador",
        "categoria": "Interruptores y Potencia",
        "voltaje": "Bobina: 5V DC | Contactos: hasta 250VAC 10A o 30VDC 10A",
        "consumo": "70 mA al activarse",
        "rango": "Aislamiento galvánico por optoacoplador PC817",
        "protocolo": "Señal Digital (Activo en LOW o HIGH según jumper)",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Relay_module_for_Arduino.jpg/500px-Relay_module_for_Arduino.jpg",
        "pines": [
            ("VCC", "+5V", "#ef4444"),
            ("GND", "Tierra", "#64748b"),
            ("IN", "Señal digital de disparo", "#38bdf8"),
            ("COM", "Común del relé", "#f59e0b"),
            ("NO / NC", "Normalmente Abierto / Normalmente Cerrado", "#10b981")
        ],
        "descripcion": "Permite a un microcontrolador de 5V encender y apagar artefactos de alta potencia como focos de 110V/220V, bombas de agua o solenoides.",
        "advertencia": "Al manipular voltajes de red eléctrica (110V/220V AC), aislar perfectamente la parte inferior de la placa para evitar electrocución."
    },
    "tcrt5000": {
        "nombre": "Sensor Óptico Reflectivo TCRT5000 (Seguidor de Línea)",
        "categoria": "Sensores Ópticos",
        "voltaje": "3.3V - 5V DC",
        "consumo": "10 - 20 mA",
        "rango": "0.2 mm a 15 mm de distancia de detección",
        "protocolo": "Salida Digital (DO por comparador LM393) y Analógica (AO)",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/TCRT5000_Reflective_Optical_Sensor.jpg/500px-TCRT5000_Reflective_Optical_Sensor.jpg",
        "pines": [
            ("VCC", "3.3V a 5V", "#ef4444"),
            ("GND", "Tierra", "#64748b"),
            ("DO", "Salida digital (detecta línea negra/blanca)", "#38bdf8"),
            ("AO", "Salida analógica del fototransistor", "#a855f7")
        ],
        "descripcion": "Combina un diodo emisor infrarrojo con un fototransistor para detectar contraste de color y líneas en robots seguidores de trayectoria.",
        "advertencia": "Ajustar el potenciómetro de sensibilidad azul integrado según la altura del chasis respecto a la pista."
    }
}

def buscar_sensores_en_texto(texto: str):
    """
    Detecta si en una pregunta, respuesta o historial se hace referencia a algún sensor conocido.
    Retorna una lista de fichas de sensores encontrados (sin duplicados).
    """
    texto_l = texto.lower()
    coincidencias = []
    claves_encontradas = set()
    
    mapeo_claves = {
        "sensor-nivel-flotador": [
            "flotador", "boya", "nivel de flotador", "sensor de flotador", "float switch", 
            "sensor de nivel", "nivel de agua", "nivel del agua", "tanque de agua"
        ],
        "sensor-calidad-agua": [
            "calidad del agua", "calidad de agua", "tds", "sólidos disueltos", "solidos disueltos",
            "pureza del agua", "conductividad", "sensor tds", "agua limpia", "contaminantes en el agua"
        ],
        "hc-sr04": ["hc-sr04", "hcsr04", "ultrasonico", "ultrasónico", "sensor de distancia", "sensor ultrasonido"],
        "dht11": ["dht11", "dht-11", "temperatura y humedad dht11"],
        "dht22": ["dht22", "dht-22", "am2302", "sensor dht22"],
        "sg90": ["sg90", "sg-90", "micro servo", "microservo", "servomotor pequeño"],
        "mg996r": ["mg996r", "mg996", "servo metalico", "servo metálico", "servo de torque"],
        "l298n": ["l298n", "l298", "puente h", "driver de motor", "controlador de motores"],
        "mpu6050": ["mpu6050", "mpu-6050", "giroscopio", "giróscopo", "acelerometro", "acelerómetro", "imu"],
        "oled-i2c": ["oled", "ssd1306", "pantalla oled", "pantalla i2c", "display oled"],
        "esp32": ["esp32", "esp-32", "nodemcu esp32", "placa esp32"],
        "arduino-uno": ["arduino uno", "arduino", "atmega328", "placa arduino"],
        "rele-5v": ["rele", "relé", "relay", "modulo rele", "módulo relé"],
        "tcrt5000": ["tcrt5000", "tcrt", "seguidor de linea", "seguidor de línea", "sensor infrarrojo de linea"]
    }
    
    for clave, terminos in mapeo_claves.items():
        if any(term in texto_l for term in terminos):
            if clave in CATALOGO_SENSORES and clave not in claves_encontradas:
                claves_encontradas.add(clave)
                coincidencias.append(CATALOGO_SENSORES[clave])
                
    return coincidencias
'''

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\sensores_data.py', 'w', encoding='utf-8') as f:
    f.write(NEW_SENSORES_DATA)

print("sensores_data.py written successfully!")
