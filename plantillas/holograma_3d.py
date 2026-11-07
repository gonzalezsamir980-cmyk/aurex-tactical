"""
LABORATORIO HOLOGRÁFICO 3D UNIVERSAL & GEMELO DIGITAL FÍSICO
Motor Three.js WebGL para AUREX / Isabella.
Capaz de sintetizar y renderizar en 3D en tiempo real:
- Sensor de Flujo de Agua YF-S201 (cuerpo de válvula roscado G 1/2", cámara de turbina, rotor de paletas magnético, sensor Hall)
- SoC ESP32 NodeMCU-32S (blindaje RF WROOM-32, antena PCB 2.4GHz, 38 GPIOs, USB y botones)
- Placa Arduino Uno R3 (ATmega328P DIP-28, USB Tipo-B, Jack DC, cristal 16MHz y headers)
- Motor Paso a Paso Bipolar NEMA 17 (estator negro, brida frontal CNC, eje 5mm D-cut y conector JST)
- Sensor de Nivel Tipo Boya / Flotador (vástago con tope mecánico, flotador toroidal magnético y reed switch)
- Módulo Relé de Potencia 5V (cubo azul Songle, bornera de tornillos de 3 terminales y optoacoplador)
- Micro Servomotor SG90 (engranajes, cruceta/horn y cable trifilar)
- Controlador de Potencia Puente H L298N (disipador aleteado de aluminio y borneras)
- Brazo Robótico Industrial 6-DOF con pinza paralela (Gripper)
- Actuador Robótico Servo-Industrial (rodamiento 608ZZ y reductora planetaria)
- Banco de Sensores TDS y Sonar (sonda de titanio TDS, display OLED y HC-SR04)
- GENERADOR PROCEDURAL PARAMÉTRICO para CUALQUIER OTRO OBJETO que pida el Jefe ("lo que sea").
"""

def generar_laboratorio_holografico_3d(modelo_inicial="flujo", objeto_personalizado="", *args, **kwargs):
    # Detectar modelo a partir del texto solicitado
    m_init = str(modelo_inicial).lower().strip()
    obj_txt = str(objeto_personalizado).lower().strip()
    prompt = f"{m_init} {obj_txt}"

    # Detección específica prioritaria (sin falsos positivos con 'sensor' o 'agua')
    if any(k in prompt for k in ["flujo", "caudal", "caudalimetro", "caudalímetro", "yf-s201", "yfs201"]):
        modelo_detectado = "flujo"
        titulo_obj = "Sensor de Flujo de Agua YF-S201"
    elif any(k in prompt for k in ["flotador", "boya", "float switch", "nivel de flotador"]):
        modelo_detectado = "flotador"
        titulo_obj = "Sensor de Nivel de Flotador (Boya)"
    elif any(k in prompt for k in ["rele", "relé", "relay"]):
        modelo_detectado = "rele"
        titulo_obj = "Módulo Relé de Potencia 5V"
    elif any(k in prompt for k in ["esp32", "esp-32", "wroom", "nodemcu"]):
        modelo_detectado = "esp32"
        titulo_obj = "SoC ESP32 NodeMCU-32S"
    elif any(k in prompt for k in ["nema", "stepper", "paso a paso", "motor a pasos"]):
        modelo_detectado = "nema17"
        titulo_obj = "Motor Paso a Paso NEMA 17"
    elif any(k in prompt for k in ["arduino", "atmega", "uno", "placa arduino"]):
        modelo_detectado = "arduino"
        titulo_obj = "Placa Arduino Uno R3"
    elif any(k in prompt for k in ["servo", "sg90", "mg996", "servomotor"]):
        modelo_detectado = "servo"
        titulo_obj = "Micro Servomotor SG90"
    elif any(k in prompt for k in ["l298", "puente h", "driver"]):
        modelo_detectado = "l298n"
        titulo_obj = "Controlador Puente H L298N"
    elif any(k in prompt for k in ["brazo", "gripper", "pinza", "articulad"]):
        modelo_detectado = "brazo"
        titulo_obj = "Brazo Robótico 6-DOF con Pinza"
    elif any(k in prompt for k in ["actuador", "rotor", "608zz"]):
        modelo_detectado = "actuador"
        titulo_obj = "Actuador Servo-Industrial 608ZZ"
    elif any(k in prompt for k in ["tds", "conductividad", "sonar", "ultrason", "hc-sr04"]):
        modelo_detectado = "sensores"
        titulo_obj = "Banco de Sensores (TDS + Sonar)"
    else:
        # CUALQUIER OTRO OBJETO SOLICITADO ("LO QUE SEA"): Activación procedural paramétrica
        modelo_detectado = "custom"
        titulo_obj = objeto_personalizado.strip().title() if objeto_personalizado.strip() else modelo_inicial.strip().title()

    return f"""```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HoloLab 3D Universal – Gemelo Digital</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
  body {{
    background: #020617;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, "Courier New", monospace;
    color: #e2e8f0;
    overflow: hidden;
    width: 100vw;
    height: 100vh;
  }}

  #main-viewport-container {{
    display: flex;
    width: 100vw;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 0;
  }}

  .viewport-half {{
    position: relative;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }}
  .viewport-half.full {{ width: 100%; }}
  .viewport-half.hidden {{ width: 0%; display: none; }}

  #half-physical {{
    background: radial-gradient(circle at 50% 30%, #1e293b 0%, #090d16 100%);
    border-right: 2px solid rgba(56, 189, 248, 0.3);
  }}
  #half-digital {{
    background: radial-gradient(circle at 50% 30%, #082f49 0%, #020617 100%);
  }}

  .scene-canvas-container {{
    width: 100%;
    height: 100%;
    display: block;
    cursor: grab;
  }}
  .scene-canvas-container:active {{ cursor: grabbing; }}

  .top-hud-bar {{
    position: absolute;
    top: 14px;
    left: 20px;
    right: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    pointer-events: none;
    z-index: 20;
  }}
  .top-title-card {{
    background: rgba(15, 23, 42, 0.9);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(56, 189, 248, 0.45);
    border-radius: 8px;
    padding: 8px 18px;
    pointer-events: auto;
  }}
  .top-title-card h1 {{
    font-size: 0.92rem;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }}

  .view-controls {{
    display: flex;
    gap: 6px;
    background: rgba(15, 23, 42, 0.9);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 8px;
    padding: 4px;
    pointer-events: auto;
  }}
  .view-btn {{
    background: transparent;
    border: 1px solid transparent;
    color: #94a3b8;
    font-size: 0.72rem;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
  }}
  .view-btn:hover {{ color: #38bdf8; background: rgba(56, 189, 248, 0.1); }}
  .view-btn.active {{
    background: rgba(14, 165, 233, 0.25);
    border-color: #00f0ff;
    color: #00f0ff;
    box-shadow: 0 0 12px rgba(0, 240, 255, 0.3);
  }}

  .hud-inspect {{
    position: absolute;
    top: 75px;
    right: 20px;
    width: 320px;
    background: rgba(15, 23, 42, 0.94);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(56, 189, 248, 0.45);
    border-radius: 10px;
    padding: 14px 16px;
    z-index: 20;
    box-shadow: 0 8px 32px rgba(0, 240, 255, 0.2);
    transition: all 0.3s ease;
  }}
  .hud-inspect-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(56, 189, 248, 0.25);
    padding-bottom: 8px;
    margin-bottom: 10px;
  }}
  .hud-inspect .tag {{
    font-size: 0.65rem;
    font-family: monospace;
    color: #00f0ff;
    background: rgba(0, 240, 255, 0.12);
    padding: 2px 7px;
    border-radius: 4px;
    border: 1px solid rgba(0, 240, 255, 0.3);
  }}
  .hud-part-name {{
    font-size: 0.95rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 4px;
  }}
  .hud-part-desc {{
    font-size: 0.72rem;
    color: #94a3b8;
    line-height: 1.35;
    margin-bottom: 10px;
  }}
  .hud-specs-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    margin-bottom: 10px;
  }}
  .spec-item {{
    background: rgba(30, 41, 59, 0.6);
    border-radius: 6px;
    padding: 5px 7px;
    border: 1px solid rgba(148, 163, 184, 0.15);
  }}
  .spec-item .lbl {{ font-size: 0.58rem; color: #64748b; text-transform: uppercase; }}
  .spec-item .val {{ font-size: 0.72rem; font-family: monospace; color: #38bdf8; font-weight: 600; }}
  .hud-instruction {{
    font-size: 0.7rem;
    color: #e2e8f0;
    background: rgba(6, 78, 59, 0.35);
    border-left: 3px solid #10b981;
    padding: 6px 10px;
    border-radius: 4px;
    line-height: 1.3;
  }}

  .bottom-telemetry-bar {{
    position: absolute;
    bottom: 16px;
    left: 20px;
    right: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(15, 23, 42, 0.92);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 8px;
    padding: 8px 16px;
    z-index: 20;
  }}
  .action-btn-group {{
    display: flex;
    gap: 8px;
    align-items: center;
  }}
  .action-btn {{
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(56, 189, 248, 0.4);
    color: #e2e8f0;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s;
  }}
  .action-btn:hover {{
    background: rgba(56, 189, 248, 0.2);
    border-color: #00f0ff;
    color: #00f0ff;
  }}
  .slider-control {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.72rem;
    color: #94a3b8;
  }}
  .slider-control input[type=range] {{
    width: 140px;
    accent-color: #00f0ff;
    cursor: pointer;
  }}
  .dot-cyan {{
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #00f0ff;
    box-shadow: 0 0 8px #00f0ff;
    margin-right: 6px;
  }}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

<div id="main-viewport-container">
  <!-- 1. VENTANA FÍSICA REAL -->
  <div class="viewport-half" id="half-physical">
    <div class="scene-canvas-container" id="canvas-physical"></div>
    <div style="position:absolute; top:70px; left:20px; font-size:0.68rem; font-family:monospace; color:#94a3b8; background:rgba(15,23,42,0.85); padding:4px 8px; border-radius:4px; border:1px solid rgba(148,163,184,0.3); pointer-events:none;">
      🏭 OBJETO FÍSICO REAL (ACABADO TALLER PBR)
    </div>
  </div>

  <!-- 2. VENTANA HOLOGRÁFICA 3D -->
  <div class="viewport-half" id="half-digital">
    <div class="scene-canvas-container" id="canvas-digital"></div>
    <div style="position:absolute; top:70px; left:20px; font-size:0.68rem; font-family:monospace; color:#00f0ff; background:rgba(15,23,42,0.85); padding:4px 8px; border-radius:4px; border:1px solid rgba(0,240,255,0.4); pointer-events:none;">
      🌐 GEMELO DIGITAL 3D (DESPIECE & TELEMETRÍA)
    </div>
  </div>
</div>

<!-- BARRA SUPERIOR -->
<div class="top-hud-bar">
  <div class="top-title-card">
    <h1 id="topModelTitle"><span class="dot-cyan"></span> GEMELO DIGITAL: {titulo_obj.upper()}</h1>
  </div>
  
  <div class="view-controls">
    <button class="view-btn active" id="btnViewSplit" onclick="cambiarModoVista('split')">◫ Físico + 3D</button>
    <button class="view-btn" id="btnViewPhysical" onclick="cambiarModoVista('physical')">🏭 Solo Físico</button>
    <button class="view-btn" id="btnViewDigital" onclick="cambiarModoVista('digital')">🌐 Solo 3D</button>
  </div>
</div>

<!-- TARJETA LATERAL DE DATOS DE LA PIEZA SELECCIONADA -->
<div class="hud-inspect" id="hudInspect">
  <div class="hud-inspect-header">
    <span class="tag" id="hudTag">ID: PART-01</span>
    <span style="font-size:0.62rem; color:#22c55e;">ESTADO: LISTO</span>
  </div>
  <div class="hud-part-name" id="hudPartName">{titulo_obj}</div>
  <div class="hud-part-desc" id="hudPartDesc">
    Inspección holográfica en tiempo real del componente mecatrónico seleccionado.
  </div>
  <div class="hud-specs-grid">
    <div class="spec-item"><div class="lbl">Material</div><div class="val" id="hudMat">Nylon PA66 / Al 6061</div></div>
    <div class="spec-item"><div class="lbl">Tolerancia</div><div class="val" id="hudTol">±0.05 mm</div></div>
    <div class="spec-item"><div class="lbl">Carga / VCC</div><div class="val" id="hudLoad">5V - 18V DC</div></div>
    <div class="spec-item"><div class="lbl">Protocolo / I/O</div><div class="val" id="hudMod">Pulsos Hall / PWM</div></div>
  </div>
  <div class="hud-instruction" id="hudInstruct">
    💡 <strong>Instrucción de Ensamble:</strong> Seleccione cualquier pieza con clic para inspección individual.
  </div>
</div>

<!-- BARRA INFERIOR DE ACCIONES Y TELEMETRÍA -->
<div class="bottom-telemetry-bar">
  <div class="action-btn-group">
    <button class="action-btn" id="btnDisassemble">💥 Desarmar (100%)</button>
    <button class="action-btn" id="btnAssemble">🧩 Ensamblar</button>
    <button class="action-btn" id="btnStep">⏭ Paso a Paso</button>
    <button class="action-btn" id="btnRotate">🔄 Rotación 360°</button>
    <button class="action-btn" id="btnWireframe">📐 Rayos X (Wireframe)</button>
  </div>

  <div class="slider-control">
    <span>Despiece (Explosión):</span>
    <input type="range" id="explodeSlider" min="0" max="100" value="0">
    <span id="explodeVal">0%</span>
  </div>
</div>

<script>
(function() {{
  const containerPhys = document.getElementById('canvas-physical');
  const containerDig = document.getElementById('canvas-digital');

  // Escenas
  const scenePhys = new THREE.Scene();
  const sceneDig = new THREE.Scene();
  scenePhys.background = new THREE.Color(0x0a0f1d);
  sceneDig.background = new THREE.Color(0x030712);
  scenePhys.fog = new THREE.FogExp2(0x0a0f1d, 0.025);
  sceneDig.fog = new THREE.FogExp2(0x030712, 0.025);

  // Cámara centrada directamente en el objeto
  const camera = new THREE.PerspectiveCamera(45, (window.innerWidth * 0.5) / window.innerHeight, 0.1, 100);
  camera.position.set(5.5, 4.2, 6.0);

  // Renderers
  const rendererPhys = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
  rendererPhys.setSize(containerPhys.clientWidth, containerPhys.clientHeight);
  rendererPhys.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  rendererPhys.shadowMap.enabled = true;
  rendererPhys.shadowMap.type = THREE.PCFSoftShadowMap;
  containerPhys.appendChild(rendererPhys.domElement);

  const rendererDig = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
  rendererDig.setSize(containerDig.clientWidth, containerDig.clientHeight);
  rendererDig.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  containerDig.appendChild(rendererDig.domElement);

  // Controles Orbit centrados en origen (0, 0, 0)
  const controlsPhys = new THREE.OrbitControls(camera, rendererPhys.domElement);
  controlsPhys.enableDamping = true;
  controlsPhys.dampingFactor = 0.08;
  controlsPhys.target.set(0, 0, 0);

  const controlsDig = new THREE.OrbitControls(camera, rendererDig.domElement);
  controlsDig.enableDamping = true;
  controlsDig.dampingFactor = 0.08;
  controlsDig.target.set(0, 0, 0);

  // Luces Físicas PBR
  scenePhys.add(new THREE.AmbientLight(0xffffff, 0.75));
  const dirLight1 = new THREE.DirectionalLight(0xffeedd, 1.3);
  dirLight1.position.set(8, 12, 8);
  dirLight1.castShadow = true;
  scenePhys.add(dirLight1);
  const dirLight2 = new THREE.DirectionalLight(0x38bdf8, 0.6);
  dirLight2.position.set(-8, 5, -8);
  scenePhys.add(dirLight2);

  // Luces Digitales Holográficas
  sceneDig.add(new THREE.AmbientLight(0x00f0ff, 0.45));
  const dLightDig = new THREE.DirectionalLight(0x00f0ff, 1.4);
  dLightDig.position.set(6, 10, 6);
  sceneDig.add(dLightDig);
  const pLightDig = new THREE.PointLight(0x38bdf8, 1.2, 25);
  pLightDig.position.set(0, 4, 0);
  sceneDig.add(pLightDig);

  // Rejilla Neón Digital
  const gridHelper = new THREE.GridHelper(16, 32, 0x00f0ff, 0x1e3a5f);
  gridHelper.position.y = -2.2;
  sceneDig.add(gridHelper);

  // Suelo Físico
  const hazardGeo = new THREE.RingGeometry(3.6, 4.0, 48);
  const hazardMat = new THREE.MeshStandardMaterial({{ color: 0xf59e0b, side: THREE.DoubleSide, roughness: 0.5 }});
  const hazardMesh = new THREE.Mesh(hazardGeo, hazardMat);
  hazardMesh.rotation.x = Math.PI / 2;
  hazardMesh.position.y = -2.19;
  scenePhys.add(hazardMesh);

  // Materiales de alta fidelidad
  const matPhysBlack = new THREE.MeshStandardMaterial({{ color: 0x111827, roughness: 0.6, metalness: 0.2 }});
  const matPhysChrome = new THREE.MeshStandardMaterial({{ color: 0xf8fafc, metalness: 0.98, roughness: 0.05 }});
  const matPhysBrass = new THREE.MeshStandardMaterial({{ color: 0xd97706, metalness: 0.9, roughness: 0.25 }});
  const matPhysAlum = new THREE.MeshStandardMaterial({{ color: 0x64748b, metalness: 0.85, roughness: 0.2 }});
  const matPhysOrange = new THREE.MeshStandardMaterial({{ color: 0xea580c, metalness: 0.3, roughness: 0.4 }});
  const matPcbBlue = new THREE.MeshStandardMaterial({{ color: 0x0284c7, roughness: 0.4 }});
  const matWater = new THREE.MeshStandardMaterial({{ color: 0x38bdf8, transparent: true, opacity: 0.55, roughness: 0.1 }});
  const matGlass = new THREE.MeshStandardMaterial({{ color: 0x0f172a, roughness: 0.1, metalness: 0.8 }});

  const matDigDark = new THREE.MeshStandardMaterial({{ color: 0x0f172a, metalness: 0.85, roughness: 0.25 }});
  const matDigCyan = new THREE.MeshStandardMaterial({{ color: 0x0284c7, emissive: 0x00f0ff, emissiveIntensity: 0.4, metalness: 0.9, roughness: 0.2 }});
  const matDigChrome = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.95, roughness: 0.1 }});
  const matDigGold = new THREE.MeshStandardMaterial({{ color: 0xca8a04, metalness: 0.9, roughness: 0.3, emissive: 0x422006 }});
  const matDigWire = new THREE.MeshStandardMaterial({{ color: 0x38bdf8, wireframe: true, transparent: true, opacity: 0.7 }});

  // Grupos maestros
  const groupPhys = new THREE.Group();
  const groupDig = new THREE.Group();
  scenePhys.add(groupPhys);
  sceneDig.add(groupDig);
  const currentDigParts = [];

  function registrarPiezaDigital(lista, grupo, mesh, info, deltaY, deltaX = 0, deltaZ = 0) {{
    mesh.userData = {{
      ...info,
      origPos: mesh.position.clone(),
      deltaPos: new THREE.Vector3(deltaX, deltaY, deltaZ)
    }};
    grupo.add(mesh);
    lista.push(mesh);
  }}

  // ─────────────────────────────────────────────────────────────
  //  CONSTRUCTOR SEGÚN MODELO SELECCIONADO
  // ─────────────────────────────────────────────────────────────
  const modeloActivo = "{modelo_detectado}";

  if (modeloActivo === "flujo") {{
    // ══════════════════════════════════════════════════════════
    //  SENSOR DE FLUJO DE AGUA YF-S201 (TURBINA + EFECTO HALL)
    // ══════════════════════════════════════════════════════════
    // FÍSICO
    // 1. Tubo horizontal roscado G 1/2"
    const pipeF = new THREE.Mesh(new THREE.CylinderGeometry(0.75, 0.75, 4.4, 28), matPhysBlack);
    pipeF.rotation.z = Math.PI / 2;
    groupPhys.add(pipeF);

    // Boquillas con rosca
    const thread1F = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.6, 24), matPhysBrass);
    thread1F.rotation.z = Math.PI / 2;
    thread1F.position.set(-2.0, 0, 0);
    groupPhys.add(thread1F);
    const thread2F = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.6, 24), matPhysBrass);
    thread2F.rotation.z = Math.PI / 2;
    thread2F.position.set(2.0, 0, 0);
    groupPhys.add(thread2F);

    // 2. Cámara central cilíndrica de la turbina
    const chamberF = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.3, 1.4, 32), matPhysBlack);
    chamberF.position.set(0, 0.5, 0);
    groupPhys.add(chamberF);

    // 3. Tapa superior con sensor Hall
    const capF = new THREE.Mesh(new THREE.CylinderGeometry(1.35, 1.35, 0.35, 32), matPhysBlack);
    capF.position.set(0, 1.3, 0);
    groupPhys.add(capF);

    const hallChipF = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.35, 0.5), matPhysChrome);
    hallChipF.position.set(0, 1.5, 0);
    groupPhys.add(hallChipF);

    // 4. Cable trifilar (Rojo, Negro, Amarillo)
    const cableF = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 1.5, 16), matPhysOrange);
    cableF.position.set(0, 1.8, -0.6);
    cableF.rotation.x = -0.5;
    groupPhys.add(cableF);

    // DIGITAL (DESPIECE HOLOGRAMA)
    // 1. Cuerpo de Válvula / Tubería
    const pipeD = new THREE.Group();
    const pipeMeshD = new THREE.Mesh(new THREE.CylinderGeometry(0.75, 0.75, 4.4, 28), matDigDark);
    pipeMeshD.rotation.z = Math.PI / 2;
    pipeD.add(pipeMeshD);
    const th1D = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.6, 24), matDigGold);
    th1D.rotation.z = Math.PI / 2; th1D.position.set(-2.0, 0, 0);
    pipeD.add(th1D);
    const th2D = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.6, 24), matDigGold);
    th2D.rotation.z = Math.PI / 2; th2D.position.set(2.0, 0, 0);
    pipeD.add(th2D);

    registrarPiezaDigital(currentDigParts, groupDig, pipeD, {{
      id: "BODY-VALVE-G12", nombre: "Cuerpo de Flujo Rosca G 1/2 Pulgadas (Macho)", desc: "Cuerpo hidráulico en nylon reforzado con fibra para tubería estándar de 1/2 pulgada. Presión máxima admisible: 1.75 MPa.",
      mat: "Nylon PA66 + 30% Fibra Vidrio", tol: "Rosca G 1/2 Pulgadas (ISO 228)", load: "Presión ≤ 1.75 MPa (17.5 bar)", mod: "Caudal: 1 a 30 L/min", instruct: "Aplicar 5-6 vueltas de cinta de teflón en sentido de las agujas del reloj sobre las roscas."
    }}, 0);

    // 2. Rotor de Turbina con Imanes de Neodimio
    const turbineD = new THREE.Group();
    const hubD = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.8, 16), matDigCyan);
    turbineD.add(hubD);
    for (let i = 0; i < 6; i++) {{
      const a = (i / 6) * Math.PI * 2;
      const blade = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.7, 0.08), matDigCyan);
      blade.position.set(Math.cos(a)*0.6, 0, Math.sin(a)*0.6);
      blade.rotation.y = -a;
      turbineD.add(blade);
    }}
    turbineD.position.set(0, 0.5, 0);

    registrarPiezaDigital(currentDigParts, groupDig, turbineD, {{
      id: "ROTOR-TURBINE", nombre: "Rueda de Paletas (Turbina con Imán NdFeB)", desc: "Rotor de 6 alabes de poliacetal con núcleo magnético de neodimio que gira al paso del caudal de agua.",
      mat: "POM Poliacetal + Imán NdFeB", tol: "Eje Inox SUS304", load: "Frecuencia: F = 7.5 × Q", mod: "6 Paletas Radiales", instruct: "Verificar libre giro del rotor. Las impurezas sólidas requieren filtro previo de 50 micras."
    }}, 1.8, 0, 0);

    // 3. Sensor de Efecto Hall Encapsulado
    const hallD = new THREE.Group();
    const capMeshD = new THREE.Mesh(new THREE.CylinderGeometry(1.35, 1.35, 0.35, 32), matDigDark);
    hallD.add(capMeshD);
    const chipD = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.35, 0.5), matDigCyan);
    chipD.position.set(0, 0.25, 0);
    hallD.add(chipD);
    hallD.position.set(0, 1.3, 0);

    registrarPiezaDigital(currentDigParts, groupDig, hallD, {{
      id: "SENS-HALL-EFFECT", nombre: "Módulo Sensor de Efecto Hall (Pulsos NPN)", desc: "Detecta cada paso del polo magnético del rotor generando un pulso digital de 5V. Cada litro equivale a aprox. 450 pulsos.",
      mat: "Sensor Hall + Resina Epoxi", tol: "Precisión ±3%", load: "4.5V a 18V DC (15 mA)", mod: "Salida Onda Cuadrada NPN", instruct: "Conectar cable Rojo a 5V, Negro a GND, y Amarillo al pin de interrupción externa (ej. GPIO 2 o 4) con pull-up."
    }}, 3.2, 0, 0);

  }} else if (modeloActivo === "esp32") {{
    // ══════════════════════════════════════════════════════════
    //  SoC ESP32 NODEMCU-32S DEDICADO
    // ══════════════════════════════════════════════════════════
    const pcbF = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.16, 5.2), matPhysBlack);
    groupPhys.add(pcbF);
    const shieldF = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.22, 1.8), matPhysChrome);
    shieldF.position.set(0, 0.18, 0.4);
    groupPhys.add(shieldF);
    const antF = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.04, 0.7), matPhysBrass);
    antF.position.set(0, 0.1, 2.0);
    groupPhys.add(antF);
    const usbF = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.45, 0.75), matPhysChrome);
    usbF.position.set(0, 0.28, -2.5);
    groupPhys.add(usbF);
    const hdrLF = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.65, 4.8), matPhysBlack);
    hdrLF.position.set(-1.25, 0.38, 0);
    groupPhys.add(hdrLF);
    const hdrRF = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.65, 4.8), matPhysBlack);
    hdrRF.position.set(1.25, 0.38, 0);
    groupPhys.add(hdrRF);

    // DIGITAL
    const pcbD = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.16, 5.2), matDigDark);
    registrarPiezaDigital(currentDigParts, groupDig, pcbD, {{
      id: "PCB-ESP32-38PIN", nombre: "Placa Base FR4 ESP32 NodeMCU-32S", desc: "PCB multicapa con plano de tierra continuo para filtrado RF 2.4 GHz y distribución de energía en estrella.",
      mat: "FR4 Negro Mate + Oro Químico", tol: "±0.05 mm", load: "Rigidez dieléctrica 20 kV/mm", mod: "28 x 52 mm", instruct: "Fijar con espaciadores de nylon aislados M2.5."
    }}, 0);

    const shieldD = new THREE.Group();
    shieldD.add(new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.22, 1.8), matDigCyan));
    shieldD.position.set(0, 0.18, 0.4);
    registrarPiezaDigital(currentDigParts, groupDig, shieldD, {{
      id: "SOC-ESP32-WROOM", nombre: "SoC ESP-WROOM-32 (Xtensa Dual-Core 240MHz)", desc: "Microcontrolador de 32 bits a 240 MHz con 520 KB SRAM, 4 MB Flash, transceptor WiFi 802.11 b/g/n y Bluetooth 4.2 BLE.",
      mat: "Silicio Xtensa LX6 + Blindaje RF", tol: "Reloj 240 MHz", load: "Consumo: 80 - 240 mA", mod: "Xtensa 32-Bit", instruct: "Nivel lógico estricto de 3.3V. Pines GPIO NO son tolerantes a 5V directo."
    }}, 2.2, 0, 0);

    const antD = new THREE.Group();
    antD.add(new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.04, 0.7), matDigGold));
    antD.position.set(0, 0.1, 2.0);
    registrarPiezaDigital(currentDigParts, groupDig, antD, {{
      id: "ANT-PCB-2.4GHZ", nombre: "Antena Inverted-F PCB 2.4 GHz", desc: "Antena integrada sintonizada a 2400-2484 MHz con ganancia de +2 dBi para comunicaciones WiFi y Bluetooth.",
      mat: "Cobre Estañado en Microstrip", tol: "Impedancia 50Ω", load: "+20 dBm Potencia RF", mod: "Banda ISM 2.4 GHz", instruct: "Mantener libre de objetos metálicos a menos de 15 mm para evitar atenuación de señal."
    }}, 1.4, 0, 0.8);

  }} else if (modeloActivo === "arduino") {{
    // ══════════════════════════════════════════════════════════
    //  ARDUINO UNO R3 DEDICADO
    // ══════════════════════════════════════════════════════════
    const pcbF = new THREE.Mesh(new THREE.BoxGeometry(5.4, 0.2, 3.8), matPcbBlue);
    groupPhys.add(pcbF);
    const usbF = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.05, 1.15), matPhysChrome);
    usbF.position.set(-2.1, 0.6, -1.1); groupPhys.add(usbF);
    const jackF = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.95, 1.1), matPhysBlack);
    jackF.position.set(-2.05, 0.55, 1.15); groupPhys.add(jackF);
    const mcuF = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.22, 0.75), matPhysBlack);
    mcuF.position.set(0.6, 0.32, 0.4); groupPhys.add(mcuF);

    const pcbD = new THREE.Mesh(new THREE.BoxGeometry(5.4, 0.2, 3.8), matDigDark);
    registrarPiezaDigital(currentDigParts, groupDig, pcbD, {{
      id: "PCB-ARDUINO-UNO", nombre: "Placa Base FR4 Arduino Uno R3", desc: "Circuito impreso de 2 capas con máscara azul, serigrafía técnica y pistas de distribución de potencia.",
      mat: "FR4 Cobre 1oz", tol: "±0.05 mm", load: "Rigidez 20 kV/mm", mod: "53.4 x 68.6 mm", instruct: "Fijar con 4 pernos métrica M3 con aislador dieléctrico."
    }}, 0);

    const mcuD = new THREE.Group();
    mcuD.add(new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.22, 0.75), matDigCyan));
    mcuD.position.set(0.6, 0.32, 0.4);
    registrarPiezaDigital(currentDigParts, groupDig, mcuD, {{
      id: "MCU-ATMEGA328P", nombre: "Microcontrolador ATmega328P (DIP-28)", desc: "Cerebro AVR de 8 bits a 16 MHz, 32 KB Flash, 2 KB SRAM y 1 KB EEPROM interna con arquitectura RISC.",
      mat: "Silicio + Zócalo DIP", tol: "16.000 MHz Cristal", load: "40 mA máx por pin", mod: "Arquitectura AVR", instruct: "Orientar muesca semicircular hacia el puerto USB. Respetar 200 mA de corriente total."
    }}, 2.2, 0, 0);

  }} else if (modeloActivo === "nema17") {{
    // ══════════════════════════════════════════════════════════
    //  MOTOR PASO A PASO NEMA 17 DEDICADO
    // ══════════════════════════════════════════════════════════
    const bodyF = new THREE.Mesh(new THREE.BoxGeometry(4.2, 3.8, 4.2), matPhysBlack);
    groupPhys.add(bodyF);
    const flangeF = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.7, 4.2), matPhysAlum);
    flangeF.position.set(0, 2.25, 0); groupPhys.add(flangeF);
    const shaftF = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 2.4, 24), matPhysChrome);
    shaftF.position.set(0, 3.8, 0); groupPhys.add(shaftF);

    const bodyD = new THREE.Mesh(new THREE.BoxGeometry(4.2, 3.8, 4.2), matDigDark);
    registrarPiezaDigital(currentDigParts, groupDig, bodyD, {{
      id: "STATOR-NEMA17", nombre: "Estator Bobinado Bipolar NEMA 17", desc: "Núcleo de chapas de acero al silicio con 8 polos dentados y devanado de cobre esmaltado clase H.",
      mat: "Acero al Silicio + Cobre", tol: "Aislamiento Clase B", load: "1.5A / Fase (Resistencia 1.5Ω)", mod: "42BYGH Bipolar", instruct: "Conectar a las salidas 1A, 1B, 2A, 2B del driver de potencia (A4988/TMC2209)."
    }}, 0);

    const shaftD = new THREE.Group();
    shaftD.add(new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 2.4, 24), matDigCyan));
    shaftD.position.set(0, 3.8, 0);
    registrarPiezaDigital(currentDigParts, groupDig, shaftD, {{
      id: "ROTOR-SHAFT-5MM", nombre: "Eje de Salida Ø 5 mm (D-Cut) + Rotor NdFeB", desc: "Eje de acero templado rectificado con cara plana en D (D-cut) para acople sin deslizamiento y rotor de neodimio.",
      mat: "Acero C45 Rectificado + Imán NdFeB", tol: "H7 (±0.005 mm)", load: "Torque: 45 N·cm", mod: "Ø 5 mm x 24 mm", instruct: "Alinear el tornillo prisionero del acople flexible exactamente sobre la cara plana del eje."
    }}, 2.5, 0, 0);

  }} else if (modeloActivo === "brazo") {{
    // ══════════════════════════════════════════════════════════
    //  BRAZO ROBÓTICO 6-DOF
    // ══════════════════════════════════════════════════════════
    const bF = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.9, 0.45, 32), matPhysIron);
    bF.position.set(0, -2.25, 0); groupPhys.add(bF);
    const grF = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.35, 0.5), matPhysIron);
    grF.position.set(-0.2, 3.15, 0); groupPhys.add(grF);

    const bD = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.9, 0.45, 32), matDigDark);
    bD.position.set(0, -2.25, 0);
    registrarPiezaDigital(currentDigParts, groupDig, bD, {{
      id: "J0-BASE", nombre: "Base Fija de Anclaje J0", desc: "Plataforma de fundición con corona dentada interna para el giro de azimut (J1).",
      mat: "Fundición Gris GG-25", tol: "±0.02 mm", load: "Fuerza Axial 2800 N", mod: "Base 320mm", instruct: "Apretar 4 pernos M12 a 85 N·m en cruz."
    }}, 0);

    const grD = new THREE.Group();
    grD.add(new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.35, 0.5), matDigCyan));
    grD.position.set(-0.2, 3.15, 0);
    registrarPiezaDigital(currentDigParts, groupDig, grD, {{
      id: "J6-GRIPPER", nombre: "Pinza Paralela (Gripper Robot)", desc: "Efector final con husillo bilateral y mordazas con almohadillas de elastómero y sensor de carga.",
      mat: "Al 7075-T6", tol: "±0.005 mm", load: "65 N Fuerza", mod: "Carrera 50 mm", instruct: "Fijar con 4 pernos Allen M3 a 1.4 N·m."
    }}, 2.2, 0, 0);

  }} else if (modeloActivo === "sensores") {{
    // ══════════════════════════════════════════════════════════
    //  BANCO DE SENSORES (TDS + SONAR)
    // ══════════════════════════════════════════════════════════
    const benchF = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.25, 3.4), matPhysAlum);
    benchF.position.set(0, -0.9, 0); groupPhys.add(benchF);
    const beakerF = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.65, 1.4, 24), matWater);
    beakerF.position.set(-1.6, -0.15, 0.2); groupPhys.add(beakerF);

    const benchD = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.25, 3.4), matDigDark);
    benchD.position.set(0, -0.9, 0);
    registrarPiezaDigital(currentDigParts, groupDig, benchD, {{
      id: "LAB-BENCH", nombre: "Banco de Instrumentación Táctico", desc: "Plataforma de instrumentación mecatrónica para pruebas de laboratorio.",
      mat: "ABS Aislante V0", tol: "Paso 2.54 mm", load: "500V Aislamiento", mod: "Bench 830pts", instruct: "Compartir masa común (GND) entre sensores."
    }}, 0);

    const tdsD = new THREE.Group();
    tdsD.add(new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.26, 1.2, 20), matDigCyan));
    tdsD.position.set(-1.6, 0.4, 0.2);
    registrarPiezaDigital(currentDigParts, groupDig, tdsD, {{
      id: "SENS-TDS", nombre: "Sensor Calidad de Agua TDS (Titanio)", desc: "Mide conductividad eléctrica e iones disueltos (0 - 1000 ppm) con excitación AC.",
      mat: "Titanio Grado Médico", tol: "±10% F.S.", load: "3 a 6 mA", mod: "Salida 0~2.3V", instruct: "Sumergir solo puntas metálicas. Compensar con sensor de temp DS18B20."
    }}, 1.4, -0.4, 0);

  }} else {{
    // ══════════════════════════════════════════════════════════
    //  GENERADOR PROCEDURAL DINÁMICO UNIVERSAL ("LO QUE SEA")
    // ══════════════════════════════════════════════════════════
    const chasisF = new THREE.Mesh(new THREE.BoxGeometry(3.6, 1.2, 3.6), matPhysAlum);
    groupPhys.add(chasisF);
    const coreF = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 1.6, 28), matPhysOrange);
    coreF.position.set(0, 1.2, 0); groupPhys.add(coreF);
    const pinF = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.35, 0.7), matPhysBlack);
    pinF.position.set(0, -0.7, 0); groupPhys.add(pinF);

    const chasisD = new THREE.Mesh(new THREE.BoxGeometry(3.6, 1.2, 3.6), matDigDark);
    registrarPiezaDigital(currentDigParts, groupDig, chasisD, {{
      id: "MOD-CHASIS", nombre: "Chasis Estructural: {titulo_obj}", desc: "Estructura portante de alta rigidez torsional y disipación térmica integrada.",
      mat: "Aluminio Al 7075-T6 / FR4", tol: "±0.01 mm CNC", load: "Carga dinámica nominal", mod: "Chasis Modular", instruct: "Fijar con pernos Allen métrica M3 con arandela Nord-Lock."
    }}, 0);

    const coreD = new THREE.Group();
    coreD.add(new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 1.6, 28), matDigCyan));
    coreD.position.set(0, 1.2, 0);
    registrarPiezaDigital(currentDigParts, groupDig, coreD, {{
      id: "CORE-ACTUATOR", nombre: "Núcleo Operativo: {titulo_obj}", desc: "Unidad funcional principal de accionamiento, detección electromagnética o conversión de energía.",
      mat: "Silicio + Aleación Magnética", tol: "DIN Grado 6", load: "Operación Continua", mod: "Unidad Central", instruct: "Mantener dentro de los rangos térmicos especificados (máx 75°C)."
    }}, 2.2, 0, 0);

    const pinD = new THREE.Group();
    pinD.add(new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.4, 0.8), matDigGold));
    pinD.position.set(0, -0.7, 0);
    registrarPiezaDigital(currentDigParts, groupDig, pinD, {{
      id: "CONN-TERMINAL", nombre: "Terminales de Interconexión y Bus I/O", desc: "Pines de alimentación (VCC, GND) y líneas de señalización digital y analógica.",
      mat: "Bronce Fosforado Dorado", tol: "Paso estándar 2.54 mm", load: "Hasta 2A por contacto", mod: "Bus I/O", instruct: "Verificar polaridad antes de energizar la etapa de potencia."
    }}, -1.5, 0, 0);
  }}

  // Actualizar HUD inicial con la primera pieza activa
  if (currentDigParts.length > 0) {{
    const initialPart = currentDigParts.length > 1 ? currentDigParts[1] : currentDigParts[0];
    if (initialPart.userData) {{
      actualizarHUD(initialPart.userData);
    }}
  }}

  // ─────────────────────────────────────────────────────────────
  //  GESTIÓN DE VISTAS (SPLIT / FISICO / DIGITAL)
  // ─────────────────────────────────────────────────────────────
  window.cambiarModoVista = function(modo) {{
    const halfP = document.getElementById('half-physical');
    const halfD = document.getElementById('half-digital');
    const btnS = document.getElementById('btnViewSplit');
    const btnP = document.getElementById('btnViewPhysical');
    const btnD = document.getElementById('btnViewDigital');

    if (btnS) btnS.classList.remove('active');
    if (btnP) btnP.classList.remove('active');
    if (btnD) btnD.classList.remove('active');

    if (modo === 'split') {{
      if (btnS) btnS.classList.add('active');
      halfP.classList.remove('hidden', 'full');
      halfD.classList.remove('hidden', 'full');
    }} else if (modo === 'physical') {{
      if (btnP) btnP.classList.add('active');
      halfP.classList.remove('hidden');
      halfP.classList.add('full');
      halfD.classList.add('hidden');
    }} else if (modo === 'digital') {{
      if (btnD) btnD.classList.add('active');
      halfD.classList.remove('hidden');
      halfD.classList.add('full');
      halfP.classList.add('hidden');
    }}
    setTimeout(onWindowResize, 50);
  }};

  // ─────────────────────────────────────────────────────────────
  //  EXPLOSIÓN Y RAYCASTING
  // ─────────────────────────────────────────────────────────────
  let explosionFactor = 0;
  let targetExplosion = 0;
  let isWireframe = false;
  let autoRotate = false;

  function setExplosion(val) {{
    targetExplosion = Math.max(0, Math.min(1, val));
    document.getElementById('explodeSlider').value = targetExplosion * 100;
    document.getElementById('explodeVal').innerText = Math.round(targetExplosion * 100) + '%';
  }}

  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();

  containerDig.addEventListener('click', (e) => {{
    const rect = containerDig.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(currentDigParts, true);

    if (intersects.length > 0) {{
      let topObj = intersects[0].object;
      while (topObj.parent && topObj.parent !== groupDig && topObj.parent !== sceneDig) {{
        topObj = topObj.parent;
      }}
      if (topObj.userData && topObj.userData.nombre) {{
        actualizarHUD(topObj.userData);
      }}
    }}
  }});

  function actualizarHUD(data) {{
    document.getElementById('hudTag').innerText = data.id || "PART-OK";
    document.getElementById('hudPartName').innerText = data.nombre || "{titulo_obj}";
    document.getElementById('hudPartDesc').innerText = data.desc || "";
    document.getElementById('hudMat').innerText = data.mat || "Aluminio / FR4";
    document.getElementById('hudTol').innerText = data.tol || "±0.02 mm";
    document.getElementById('hudLoad').innerText = data.load || "Nominal";
    document.getElementById('hudMod').innerText = data.mod || "Estándar";
    document.getElementById('hudInstruct').innerHTML = `💡 <strong>Instrucción de Ensamble:</strong> ${{data.instruct || "Verificar conexionado."}}`;

    const hud = document.getElementById('hudInspect');
    hud.style.borderColor = "#00f0ff";
    hud.style.boxShadow = "0 8px 32px rgba(0, 240, 255, 0.4)";
    setTimeout(() => {{
      hud.style.borderColor = "rgba(56, 189, 248, 0.4)";
      hud.style.boxShadow = "0 8px 32px rgba(0, 240, 255, 0.18)";
    }}, 400);
  }}

  // Botones
  document.getElementById('btnDisassemble').addEventListener('click', () => setExplosion(1.0));
  document.getElementById('btnAssemble').addEventListener('click', () => setExplosion(0.0));
  
  let stepIdx = 0;
  document.getElementById('btnStep').addEventListener('click', () => {{
    stepIdx = (stepIdx + 1) % 5;
    setExplosion(stepIdx / 4);
  }});

  document.getElementById('explodeSlider').addEventListener('input', (e) => {{
    setExplosion(parseFloat(e.target.value) / 100);
  }});

  document.getElementById('btnWireframe').addEventListener('click', () => {{
    isWireframe = !isWireframe;
    groupDig.traverse((child) => {{
      if (child.isMesh && child.material) {{
        if (Array.isArray(child.material)) {{
          child.material.forEach(m => m.wireframe = isWireframe);
        }} else {{
          child.material.wireframe = isWireframe;
        }}
      }}
    }});
    document.getElementById('btnWireframe').style.color = isWireframe ? '#00f0ff' : '#e2e8f0';
    document.getElementById('btnWireframe').style.borderColor = isWireframe ? '#00f0ff' : 'rgba(56, 189, 248, 0.4)';
  }});

  document.getElementById('btnRotate').addEventListener('click', () => {{
    autoRotate = !autoRotate;
    document.getElementById('btnRotate').style.color = autoRotate ? '#00f0ff' : '#e2e8f0';
    document.getElementById('btnRotate').style.borderColor = autoRotate ? '#00f0ff' : 'rgba(56, 189, 248, 0.4)';
  }});

  // ─────────────────────────────────────────────────────────────
  //  BUCLE DE RENDERIZADO DUAL 60 FPS
  // ─────────────────────────────────────────────────────────────
  function animate() {{
    requestAnimationFrame(animate);

    explosionFactor += (targetExplosion - explosionFactor) * 0.08;

    for (let i = 0; i < currentDigParts.length; i++) {{
      const p = currentDigParts[i];
      if (p.userData && p.userData.origPos && p.userData.deltaPos) {{
        p.position.x = p.userData.origPos.x + p.userData.deltaPos.x * explosionFactor;
        p.position.y = p.userData.origPos.y + p.userData.deltaPos.y * explosionFactor;
        p.position.z = p.userData.origPos.z + p.userData.deltaPos.z * explosionFactor;
      }}
    }}

    if (autoRotate) {{
      groupPhys.rotation.y += 0.008;
      groupDig.rotation.y += 0.008;
    }}

    controlsPhys.update();
    controlsDig.update();

    if (containerPhys.clientWidth > 0 && containerPhys.clientHeight > 0) {{
      rendererPhys.render(scenePhys, camera);
    }}
    if (containerDig.clientWidth > 0 && containerDig.clientHeight > 0) {{
      rendererDig.render(sceneDig, camera);
    }}
  }}
  animate();

  function onWindowResize() {{
    const wP = containerPhys.clientWidth;
    const hP = containerPhys.clientHeight;
    if (wP > 0 && hP > 0) {{
      rendererPhys.setSize(wP, hP);
    }}

    const wD = containerDig.clientWidth;
    const hD = containerDig.clientHeight;
    if (wD > 0 && hD > 0) {{
      rendererDig.setSize(wD, hD);
      camera.aspect = wD / hD;
      camera.updateProjectionMatrix();
    }}
  }}
  window.addEventListener('resize', onWindowResize);
}})();
</script>
</body>
</html>
```"""
