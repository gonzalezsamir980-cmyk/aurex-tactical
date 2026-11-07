import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\plantillas\holograma_3d.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the model selector HTML to add the 3rd button
OLD_BUTTONS = '''    <button class="view-btn active" id="btnSwitchArm" onclick="activarModelo(\'brazo\')">🦾 Brazo 6-DOF</button>
    <button class="view-btn" id="btnSwitchActuator" onclick="activarModelo(\'actuador\')">⚙️ Actuador</button>'''

NEW_BUTTONS = '''    <button class="view-btn active" id="btnSwitchArm" onclick="activarModelo(\'brazo\')">🦾 Brazo 6-DOF</button>
    <button class="view-btn" id="btnSwitchActuator" onclick="activarModelo(\'actuador\')">⚙️ Actuador</button>
    <button class="view-btn" id="btnSwitchSensors" onclick="activarModelo(\'sensores\')">🧪 Sensores 3D (TDS + OLED)</button>'''

if OLD_BUTTONS in content:
    content = content.replace(OLD_BUTTONS, NEW_BUTTONS)
    print("[OK] Button 3 (Sensores 3D) added to model selector HTML")
else:
    print("[ERROR] OLD_BUTTONS not found")

# 2. Add groupPhysSensors and groupDigSensors declarations
OLD_GROUPS = '''  // Grupos en escena física
  const groupPhysArm = new THREE.Group();
  const groupPhysAct = new THREE.Group();
  scenePhys.add(groupPhysArm);
  scenePhys.add(groupPhysAct);

  // Grupos en escena digital
  const groupDigArm = new THREE.Group();
  const groupDigAct = new THREE.Group();
  sceneDig.add(groupDigArm);
  sceneDig.add(groupDigAct);

  const digArmParts = [];
  const digActParts = [];
  let currentDigParts = digArmParts;'''

NEW_GROUPS = '''  // Grupos en escena física
  const groupPhysArm = new THREE.Group();
  const groupPhysAct = new THREE.Group();
  const groupPhysSensors = new THREE.Group();
  scenePhys.add(groupPhysArm);
  scenePhys.add(groupPhysAct);
  scenePhys.add(groupPhysSensors);

  // Grupos en escena digital
  const groupDigArm = new THREE.Group();
  const groupDigAct = new THREE.Group();
  const groupDigSensors = new THREE.Group();
  sceneDig.add(groupDigArm);
  sceneDig.add(groupDigAct);
  sceneDig.add(groupDigSensors);

  const digArmParts = [];
  const digActParts = [];
  const digSensorsParts = [];
  let currentDigParts = digArmParts;'''

if OLD_GROUPS in content:
    content = content.replace(OLD_GROUPS, NEW_GROUPS)
    print("[OK] groupPhysSensors and groupDigSensors groups created")
else:
    print("[ERROR] OLD_GROUPS not found")

# 3. Add the buildSensorsPhysical and buildSensorsDigital functions
SENSORS_BUILDER_CODE = '''
  // ─────────────────────────────────────────────────────────────
  //  MODELO C: BANCO DE SENSORES 3D (TDS, OLED, HC-SR04, ESP32)
  // ─────────────────────────────────────────────────────────────
  // Materiales específicos para sensores
  const matPcbGreen = new THREE.MeshStandardMaterial({{ color: 0x065f46, roughness: 0.4 }});
  const matPcbBlue = new THREE.MeshStandardMaterial({{ color: 0x1d4ed8, roughness: 0.4 }});
  const matWater = new THREE.MeshStandardMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.55, roughness: 0.1 }});
  const matGlass = new THREE.MeshStandardMaterial({{ color: 0x0f172a, roughness: 0.1, metalness: 0.8 }});

  function buildSensorsPhysical() {{
    // 1. Base Protoboard de taller
    const baseBench = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.25, 3.4), matPhysAlum);
    baseBench.position.set(0, -0.9, 0);
    groupPhysSensors.add(baseBench);

    // 2. Sensor TDS de Calidad de Agua (Sonda + Vaso)
    const beaker = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.65, 1.4, 24), matWater);
    beaker.position.set(-1.6, -0.15, 0.2);
    groupPhysSensors.add(beaker);

    const tdsProbe = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.26, 1.2, 20), matPhysBlack);
    tdsProbe.position.set(-1.6, 0.5, 0.2);
    groupPhysSensors.add(tdsProbe);

    const elec1 = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.5, 12), matPhysChrome);
    elec1.position.set(-1.68, 0.0, 0.2);
    groupPhysSensors.add(elec1);
    const elec2 = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.5, 12), matPhysChrome);
    elec2.position.set(-1.52, 0.0, 0.2);
    groupPhysSensors.add(elec2);

    // 3. Pantalla Gráfica OLED 0.96" I2C
    const oledPcb = new THREE.Mesh(new THREE.BoxGeometry(1.3, 1.1, 0.08), matPhysBlack);
    oledPcb.position.set(0, 0.0, 0.5);
    oledPcb.rotation.x = -Math.PI / 6;
    groupPhysSensors.add(oledPcb);

    const oledGlass = new THREE.Mesh(new THREE.BoxGeometry(1.05, 0.7, 0.04), matGlass);
    oledGlass.position.set(0, 0.03, 0.55);
    oledGlass.rotation.x = -Math.PI / 6;
    groupPhysSensors.add(oledGlass);

    // 4. Sensor Ultrasónico HC-SR04
    const sonarPcb = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.8, 0.08), matPcbBlue);
    sonarPcb.position.set(1.5, 0.2, 0.2);
    groupPhysSensors.add(sonarPcb);

    const cylT = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.45, 20), matPhysChrome);
    cylT.rotation.x = Math.PI / 2;
    cylT.position.set(1.15, 0.2, 0.45);
    groupPhysSensors.add(cylT);

    const cylR = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.45, 20), matPhysChrome);
    cylR.rotation.x = Math.PI / 2;
    cylR.position.set(1.85, 0.2, 0.45);
    groupPhysSensors.add(cylR);

    // 5. Placa ESP32 Microcontrolador
    const espPcb = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.08, 1.9), matPhysBlack);
    espPcb.position.set(0, -0.7, -0.7);
    groupPhysSensors.add(espPcb);

    const espShield = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.12, 1.0), matPhysChrome);
    espShield.position.set(0, -0.62, -0.85);
    groupPhysSensors.add(espShield);
  }}
  buildSensorsPhysical();

  function buildSensorsDigital() {{
    // 1. Base Bench Digital
    const baseBench = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.25, 3.4), matDigDark);
    baseBench.position.set(0, -0.9, 0);
    registrarPiezaDigital(digSensorsParts, groupDigSensors, baseBench, {{
      id: "LAB-BENCH", nombre: "Banco de Pruebas Táctico", desc: "Plataforma de instrumentación mecatrónica para pruebas de laboratorio.",
      mat: "ABS Aislante V0", tol: "Paso 2.54 mm", load: "500V Aislamiento", mod: "Bench 830pts", instruct: "Compartir masa común (GND) entre sensores."
    }}, 0);

    // 2. Sensor TDS Calidad de Agua Digital
    const tdsGroup = new THREE.Group();
    const beaker = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.65, 1.4, 24), matDigWire);
    beaker.position.set(0, -0.65, 0);
    tdsGroup.add(beaker);
    const tdsProbe = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.26, 1.2, 20), matDigDark);
    tdsProbe.position.set(0, 0.1, 0);
    tdsGroup.add(tdsProbe);
    const elec1 = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.5, 12), matDigCyan);
    elec1.position.set(-0.08, -0.4, 0);
    tdsGroup.add(elec1);
    const elec2 = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.5, 12), matDigCyan);
    elec2.position.set(0.08, -0.4, 0);
    tdsGroup.add(elec2);
    tdsGroup.position.set(-1.6, 0.4, 0.2);

    registrarPiezaDigital(digSensorsParts, groupDigSensors, tdsGroup, {{
      id: "SENS-TDS", nombre: "Sensor Calidad de Agua TDS (Titanio)", desc: "Mide conductividad eléctrica e iones disueltos (0 - 1000 ppm) con excitación AC.",
      mat: "Titanio Grado Médico", tol: "±10% F.S. @ 25°C", load: "3 a 6 mA", mod: "Salida Analógica 0~2.3V", instruct: "Sumergir solo puntas metálicas. Compensar con sensor de temp DS18B20."
    }}, 1.4, -0.4, 0);

    // 3. Pantalla OLED 0.96" Digital
    const oledGroup = new THREE.Group();
    const oledPcb = new THREE.Mesh(new THREE.BoxGeometry(1.3, 1.1, 0.08), matDigDark);
    oledGroup.add(oledPcb);
    const oledGlass = new THREE.Mesh(new THREE.BoxGeometry(1.05, 0.7, 0.04), matDigCyan);
    oledGlass.position.set(0, 0.03, 0.05);
    oledGroup.add(oledGlass);
    oledGroup.position.set(0, 0.0, 0.5);
    oledGroup.rotation.x = -Math.PI / 6;

    registrarPiezaDigital(digSensorsParts, groupDigSensors, oledGroup, {{
      id: "DISP-OLED", nombre: "Pantalla OLED 0.96\\" I2C (SSD1306)", desc: "Display gráfico monocromático 128x64 con alto contraste y píxeles auto-emisivos.",
      mat: "Cristal OLED + FR4", tol: "Resolución 128x64", load: "20 mA @ 3.3V", mod: "Bus I2C (0x3C)", instruct: "Verificar mapa GND-VCC del lote antes de alimentar a 5V."
    }}, 1.2, 0, 0.6);

    // 4. Sensor Ultrasónico HC-SR04 Digital
    const sonarGroup = new THREE.Group();
    const sonarPcb = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.8, 0.08), matDigDark);
    sonarGroup.add(sonarPcb);
    const cylT = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.45, 20), matDigCyan);
    cylT.rotation.x = Math.PI / 2;
    cylT.position.set(-0.35, 0, 0.25);
    sonarGroup.add(cylT);
    const cylR = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 0.45, 20), matDigCyan);
    cylR.rotation.x = Math.PI / 2;
    cylR.position.set(0.35, 0, 0.25);
    sonarGroup.add(cylR);
    sonarGroup.position.set(1.5, 0.2, 0.2);

    registrarPiezaDigital(digSensorsParts, groupDigSensors, sonarGroup, {{
      id: "SENS-HCSR04", nombre: "Sensor Ultrasónico HC-SR04", desc: "Sonar de ecolocalización con transductor emisor (T) y receptor (R) a 40 kHz.",
      mat: "Cápsula Al 6063", tol: "Precisión 3 mm", load: "15 mA @ 5V", mod: "Rango 2 - 400 cm", instruct: "Usar divisor resistivo en pin ECHO si se conecta a micro de 3.3V (ESP32)."
    }}, 1.1, 0.5, 0.3);

    // 5. Microcontrolador ESP32 Digital
    const espGroup = new THREE.Group();
    const espPcb = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.08, 1.9), matDigDark);
    espGroup.add(espPcb);
    const espShield = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.12, 1.0), matDigCyan);
    espShield.position.set(0, 0.08, -0.15);
    espGroup.add(espShield);
    espGroup.position.set(0, -0.7, -0.7);

    registrarPiezaDigital(digSensorsParts, groupDigSensors, espGroup, {{
      id: "MCU-ESP32", nombre: "SoC ESP32 NodeMCU-32S", desc: "Procesador de 32 bits Dual-Core a 240 MHz con conectividad WiFi y BLE integrada.",
      mat: "Silicio + Blindaje RF", tol: "38 Pines GPIO", load: "80 - 240 mA", mod: "Xtensa LX6 32-Bit", instruct: "Nivel lógico estricto de 3.3V. Pines NO toleran 5V directo."
    }}, 1.3, 0, -0.6);
  }}
  buildSensorsDigital();
'''

# Find where buildActuatorDigital ends (around line 770)
idx_act_end = content.find('  buildActuatorDigital();')
if idx_act_end >= 0:
    insert_pos = idx_act_end + len('  buildActuatorDigital();')
    content = content[:insert_pos] + SENSORS_BUILDER_CODE + content[insert_pos:]
    print("[OK] buildSensorsPhysical and buildSensorsDigital inserted successfully!")
else:
    print("[ERROR] buildActuatorDigital call not found")

# 4. Update activarModelo to support 'sensores'
OLD_ACTIVAR = '''  window.activarModelo = function(tipo) {{
    const btnArm = document.getElementById('btnSwitchArm');
    const btnAct = document.getElementById('btnSwitchActuator');
    const title = document.getElementById('topModelTitle');

    if (tipo === 'brazo') {{
      groupPhysArm.visible = true;
      groupPhysAct.visible = false;
      groupDigArm.visible = true;
      groupDigAct.visible = false;
      currentDigParts = digArmParts;
      btnArm.classList.add('active');
      btnAct.classList.remove('active');
      title.innerHTML = '<span class="dot-cyan pulse-dot"></span> GEMELO DIGITAL: BRAZO ROBÓTICO 6-DOF';
      camera.position.set(7.5, 5.5, 9);
      controlsPhys.target.set(0, 0.5, 0);
      controlsDig.target.set(0, 0.5, 0);
      actualizarHUD(digArmParts[7].userData); // Pinza
    }} else {{
      groupPhysArm.visible = false;
      groupPhysAct.visible = true;
      groupDigArm.visible = false;
      groupDigAct.visible = true;
      currentDigParts = digActParts;
      btnAct.classList.add('active');
      btnArm.classList.remove('active');
      title.innerHTML = '<span class="dot-cyan pulse-dot"></span> GEMELO DIGITAL: ACTUADOR INDUSTRIAL';
      camera.position.set(7, 5, 8);
      controlsPhys.target.set(0, 0, 0);
      controlsDig.target.set(0, 0, 0);
      actualizarHUD(digActParts[4].userData); // Rodamiento 608ZZ
    }}
    setExplosion(0);
  }};'''

NEW_ACTIVAR = '''  window.activarModelo = function(tipo) {{
    const btnArm = document.getElementById('btnSwitchArm');
    const btnAct = document.getElementById('btnSwitchActuator');
    const btnSens = document.getElementById('btnSwitchSensors');
    const title = document.getElementById('topModelTitle');

    if (btnArm) btnArm.classList.remove('active');
    if (btnAct) btnAct.classList.remove('active');
    if (btnSens) btnSens.classList.remove('active');

    if (tipo === 'brazo') {{
      groupPhysArm.visible = true;
      groupPhysAct.visible = false;
      groupPhysSensors.visible = false;
      groupDigArm.visible = true;
      groupDigAct.visible = false;
      groupDigSensors.visible = false;
      currentDigParts = digArmParts;
      if (btnArm) btnArm.classList.add('active');
      title.innerHTML = '<span class="dot-cyan pulse-dot"></span> GEMELO DIGITAL: BRAZO ROBÓTICO 6-DOF';
      camera.position.set(7.5, 5.5, 9);
      controlsPhys.target.set(0, 0.5, 0);
      controlsDig.target.set(0, 0.5, 0);
      actualizarHUD(digArmParts[7].userData);
    }} else if (tipo === 'actuador') {{
      groupPhysArm.visible = false;
      groupPhysAct.visible = true;
      groupPhysSensors.visible = false;
      groupDigArm.visible = false;
      groupDigAct.visible = true;
      groupDigSensors.visible = false;
      currentDigParts = digActParts;
      if (btnAct) btnAct.classList.add('active');
      title.innerHTML = '<span class="dot-cyan pulse-dot"></span> GEMELO DIGITAL: ACTUADOR INDUSTRIAL';
      camera.position.set(7, 5, 8);
      controlsPhys.target.set(0, 0, 0);
      controlsDig.target.set(0, 0, 0);
      actualizarHUD(digActParts[4].userData);
    }} else if (tipo === 'sensores') {{
      groupPhysArm.visible = false;
      groupPhysAct.visible = false;
      groupPhysSensors.visible = true;
      groupDigArm.visible = false;
      groupDigAct.visible = false;
      groupDigSensors.visible = true;
      currentDigParts = digSensorsParts;
      if (btnSens) btnSens.classList.add('active');
      title.innerHTML = '<span class="dot-cyan pulse-dot"></span> GEMELO DIGITAL: SENSORES 3D (TDS + OLED + SONAR)';
      camera.position.set(7.5, 5.5, 8.5);
      controlsPhys.target.set(0, 0, 0);
      controlsDig.target.set(0, 0, 0);
      actualizarHUD(digSensorsParts[1].userData); // Sensor TDS
    }}
    setExplosion(0);
  }};'''

if OLD_ACTIVAR in content:
    content = content.replace(OLD_ACTIVAR, NEW_ACTIVAR)
    print("[OK] activarModelo updated with 3 models: brazo, actuador, sensores")
else:
    print("[ERROR] OLD_ACTIVAR not found")

# 5. Raycasting check in holograma_3d.py
OLD_RAYCAST = 'while (topObj.parent && topObj.parent !== groupDigArm && topObj.parent !== groupDigAct && topObj.parent !== sceneDig)'
NEW_RAYCAST = 'while (topObj.parent && topObj.parent !== groupDigArm && topObj.parent !== groupDigAct && topObj.parent !== groupDigSensors && topObj.parent !== sceneDig)'

if OLD_RAYCAST in content:
    content = content.replace(OLD_RAYCAST, NEW_RAYCAST)
    print("[OK] Raycasting updated to include groupDigSensors")

# 6. Auto-rotation check in holograma_3d.py
OLD_AUTOROT = '''      groupPhysAct.rotation.y += 0.008;
      groupDigAct.rotation.y += 0.008;'''
NEW_AUTOROT = '''      groupPhysAct.rotation.y += 0.008;
      groupDigAct.rotation.y += 0.008;
      groupPhysSensors.rotation.y += 0.008;
      groupDigSensors.rotation.y += 0.008;'''

if OLD_AUTOROT in content:
    content = content.replace(OLD_AUTOROT, NEW_AUTOROT)
    print("[OK] Auto-rotation updated for groupPhysSensors and groupDigSensors")

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\plantillas\holograma_3d.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Syntax check
import subprocess
res = subprocess.run(["python", "-m", "py_compile", r"C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\plantillas\holograma_3d.py"], capture_output=True, text=True)
if res.returncode == 0:
    print("[SUCCESS] plantillas/holograma_3d.py compiled 100%!")
else:
    print("[ERROR] Syntax error in holograma_3d.py:\n", res.stderr)
