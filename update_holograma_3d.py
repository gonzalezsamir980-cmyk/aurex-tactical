# -*- coding: utf-8 -*-
"""
Script para generar plantillas/holograma_3d.py con soporte dual:
- Actuador Servo-Industrial
- Brazo Robótico Articulado 6-DOF con Pinza (Gripper)
"""

code = '''"""
LABORATORIO HOLOGRÁFICO 3D INTERACTIVO - ESTILO TONY STARK & HIRO HAMADA
Motor Three.js WebGL integrado para AUREX / Isabella.
Soporte para:
- 🦾 Brazo Robótico Articulado 6-DOF con Pinza Paralela (Gripper)
- ⚙️ Actuador Servo-Industrial con Tren Planetario y Rodamiento 608ZZ
Permite:
- Desarme y ensamble en tiempo real con interpolación suave.
- Modo Holograma Wireframe (Cian Neón estilo Big Hero 6).
- Selección de piezas con HUD lateral de datos técnicos y tolerancias ISO/DIN.
- Control de cámara 360° orbital con ratón o táctil.
- Selector de modelo en tiempo real (Brazo Robótico ↔ Actuador).
"""

def generar_laboratorio_holografico_3d(modelo_inicial="brazo"):
    return f"""```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HoloLab 3D · Laboratorio Táctico de Ensamble</title>
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
  #canvas-container {{
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
  }}

  /* HUD SUPERIOR TÁCTICO (ESTILO J.A.R.V.I.S. / BIG HERO 6) */
  .hud-top {{
    position: absolute;
    top: 14px;
    left: 18px;
    right: 18px;
    z-index: 10;
    display: flex;
    justify-content: space-between;
    align-items: center;
    pointer-events: none;
    flex-wrap: wrap;
    gap: 10px;
  }}
  .hud-title-box {{
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-left: 4px solid #38bdf8;
    backdrop-filter: blur(8px);
    padding: 8px 16px;
    border-radius: 4px;
    pointer-events: auto;
  }}
  .hud-title-box h1 {{
    font-size: 0.95rem;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: 2px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .hud-title-box p {{
    font-size: 0.68rem;
    color: #94a3b8;
    letter-spacing: 0.8px;
  }}
  .holo-indicator {{
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #00f0ff;
    border-radius: 50%;
    box-shadow: 0 0 10px #00f0ff;
    animation: pulse 1.5s infinite;
  }}
  @keyframes pulse {{ 0%, 100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: 0.4; transform: scale(0.85); }} }}

  /* SELECTOR DE MODELO 3D (BRAZO VS ACTUADOR) */
  .model-selector {{
    display: flex;
    gap: 6px;
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 4px;
    border-radius: 6px;
    backdrop-filter: blur(8px);
    pointer-events: auto;
  }}
  .model-btn {{
    background: transparent;
    border: 1px solid transparent;
    color: #94a3b8;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .model-btn:hover {{
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
  }}
  .model-btn.active {{
    background: rgba(14, 165, 233, 0.25);
    border-color: #38bdf8;
    color: #00f0ff;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
  }}

  /* TARJETA LATERAL FLOTANTE DE INSPECCIÓN (DATA HUD) */
  .hud-inspect {{
    position: absolute;
    top: 75px;
    right: 18px;
    width: 290px;
    background: rgba(10, 17, 33, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.4);
    box-shadow: 0 8px 32px rgba(0, 240, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 8px;
    padding: 14px;
    z-index: 10;
    transition: all 0.3s ease;
  }}
  .hud-inspect-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    padding-bottom: 6px;
    margin-bottom: 8px;
  }}
  .hud-inspect-header .tag {{
    font-size: 0.65rem;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }}
  .hud-part-name {{
    font-size: 0.95rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 6px;
  }}
  .hud-part-desc {{
    font-size: 0.73rem;
    color: #94a3b8;
    line-height: 1.35;
    margin-bottom: 10px;
  }}
  .hud-specs-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    background: rgba(15, 23, 42, 0.6);
    padding: 8px;
    border-radius: 6px;
    border: 1px solid rgba(56, 189, 248, 0.15);
    margin-bottom: 10px;
  }}
  .spec-item .lbl {{
    font-size: 0.6rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .spec-item .val {{
    font-size: 0.72rem;
    font-weight: 600;
    color: #38bdf8;
  }}
  .hud-instruction {{
    font-size: 0.7rem;
    color: #86efac;
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    padding: 8px;
    border-radius: 4px;
    line-height: 1.3;
  }}

  /* CONTROLES INFERIORES HOLOGRÁFICOS */
  .hud-bottom-bar {{
    position: absolute;
    bottom: 18px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 10;
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(10, 17, 33, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.35);
    box-shadow: 0 4px 20px rgba(0, 240, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 8px 14px;
    border-radius: 30px;
  }}
  .holo-btn {{
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(56, 189, 248, 0.4);
    color: #e2e8f0;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 8px 14px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .holo-btn:hover {{
    background: rgba(56, 189, 248, 0.2);
    border-color: #00f0ff;
    color: #00f0ff;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    transform: translateY(-1px);
  }}
  .holo-btn:active {{
    transform: translateY(0);
  }}
  .slider-box {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0 8px;
    border-left: 1px solid rgba(56, 189, 248, 0.2);
    border-right: 1px solid rgba(56, 189, 248, 0.2);
  }}
  .slider-box span {{
    font-size: 0.72rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
  }}
  input[type="range"] {{
    width: 105px;
    accent-color: #00f0ff;
    cursor: pointer;
    height: 4px;
    background: #334155;
    border-radius: 4px;
  }}

  /* AYUDA DE NAVEGACIÓN EN PANTALLA */
  .hint-nav {{
    position: absolute;
    bottom: 68px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.68rem;
    color: #64748b;
    pointer-events: none;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    background: rgba(15, 23, 42, 0.6);
    padding: 4px 12px;
    border-radius: 12px;
    border: 1px solid rgba(56, 189, 248, 0.15);
  }}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

<div class="hud-top">
  <div class="hud-title-box">
    <h1 id="topModelTitle"><span class="holo-indicator"></span> BRAZO ROBÓTICO 6-DOF CON PINZA</h1>
    <p id="topModelSubtitle">MODELO HOLOGRÁFICO ARTICULADO · LABORATORIO TÁCTICO</p>
  </div>
  
  <div class="model-selector">
    <button class="model-btn" id="btnSwitchArm" onclick="activarModelo('brazo')">🦾 Brazo Robótico 6-DOF</button>
    <button class="model-btn" id="btnSwitchActuator" onclick="activarModelo('actuador')">⚙️ Actuador Servo</button>
  </div>
</div>

<!-- TARJETA LATERAL DE DATOS DE LA PIEZA SELECCIONADA -->
<div class="hud-inspect" id="hudInspect">
  <div class="hud-inspect-header">
    <span class="tag" id="hudTag">ID: COMP-01</span>
    <span style="font-size:0.65rem; color:#22c55e;">ESTADO: LISTO</span>
  </div>
  <div class="hud-part-name" id="hudPartName">Pinza Paralela Servoaccionada (Gripper)</div>
  <div class="hud-part-desc" id="hudPartDesc">
    Efector final de precisión accionado por micro-servomotor y husillo bilateral. Dispone de mordazas desmontables con almohadillas de elastómero.
  </div>
  <div class="hud-specs-grid">
    <div class="spec-item"><div class="lbl">Material</div><div class="val" id="hudMat">Al 7075-T6</div></div>
    <div class="spec-item"><div class="lbl">Fuerza / Tol</div><div class="val" id="hudTol">65 N · ±0.01mm</div></div>
    <div class="spec-item"><div class="lbl">Carga Máx</div><div class="val" id="hudLoad">1.5 kg Útil</div></div>
    <div class="spec-item"><div class="lbl">Carrera</div><div class="val" id="hudMod">0 - 50 mm</div></div>
  </div>
  <div class="hud-instruction" id="hudInstruct">
    💡 <strong>Instrucción de Ensamble:</strong> Acoplar a la brida ISO 9409-1 de la muñeca apretando los 4 pernos Allen M3 a 1.4 N·m.
  </div>
</div>

<div class="hint-nav">
  🖱️ Clic izquierdo + Arrastrar: Rotar 360° · Rueda: Zoom · Clic en cualquier pieza: Inspeccionar ficha técnica
</div>

<!-- CONTROLES INFERIORES HOLOGRÁFICOS -->
<div class="hud-bottom-bar">
  <button class="holo-btn" id="btnDisassemble">🔓 Desarmar</button>
  <button class="holo-btn" id="btnAssemble">🔒 Ensamblar</button>
  <button class="holo-btn" id="btnStep">➡️ Paso a Paso</button>
  
  <div class="slider-box">
    <span>Explosión</span>
    <input type="range" id="explodeSlider" min="0" max="100" value="0">
  </div>

  <button class="holo-btn" id="btnWireframe">👁️ Rayos X</button>
  <button class="holo-btn" id="btnRotate">🔄 Auto Giro</button>
</div>

<div id="canvas-container"></div>

<script>
(function() {{
  const container = document.getElementById('canvas-container');
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x020617, 0.032);

  const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
  camera.position.set(7.5, 5.5, 9);

  const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  container.appendChild(renderer.domElement);

  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.maxDistance = 25;
  controls.minDistance = 2.5;
  controls.target.set(0, 0.5, 0);

  // Iluminación táctica neón
  const ambientLight = new THREE.AmbientLight(0x0f172a, 1.8);
  scene.add(ambientLight);

  const dirLight1 = new THREE.DirectionalLight(0x00f0ff, 2.5);
  dirLight1.position.set(6, 12, 8);
  scene.add(dirLight1);

  const dirLight2 = new THREE.DirectionalLight(0x3b82f6, 1.8);
  dirLight2.position.set(-6, -4, -6);
  scene.add(dirLight2);

  // Rejilla y anillos concéntricos en el suelo
  const gridHelper = new THREE.GridHelper(18, 36, 0x00f0ff, 0x1e3a5f);
  gridHelper.position.y = -2.5;
  scene.add(gridHelper);

  const ringGeo = new THREE.RingGeometry(2.5, 2.55, 64);
  const ringMat = new THREE.MeshBasicMaterial({{ color: 0x00f0ff, side: THREE.DoubleSide, transparent: true, opacity: 0.35 }});
  const ringMesh = new THREE.Mesh(ringGeo, ringMat);
  ringMesh.rotation.x = Math.PI / 2;
  ringMesh.position.y = -2.48;
  scene.add(ringMesh);

  // ─────────────────────────────────────────────────────────────
  //  MATERIALES HOLOGRÁFICOS Y REALISTAS
  // ─────────────────────────────────────────────────────────────
  const matAlDark = new THREE.MeshStandardMaterial({{ color: 0x0f172a, metalness: 0.85, roughness: 0.25 }});
  const matCyan = new THREE.MeshStandardMaterial({{ color: 0x0284c7, emissive: 0x00f0ff, emissiveIntensity: 0.35, metalness: 0.9, roughness: 0.2 }});
  const matCarbon = new THREE.MeshStandardMaterial({{ color: 0x1e293b, metalness: 0.9, roughness: 0.4 }});
  const matChrome = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.95, roughness: 0.1 }});
  const matGold = new THREE.MeshStandardMaterial({{ color: 0xca8a04, metalness: 0.9, roughness: 0.3, emissive: 0x422006 }});
  const matCopper = new THREE.MeshStandardMaterial({{ color: 0xb45309, metalness: 0.8, roughness: 0.35 }});

  // Raíces de grupos de modelos
  const groupArm = new THREE.Group();
  const groupActuator = new THREE.Group();
  scene.add(groupArm);
  scene.add(groupActuator);

  const armParts = [];
  const actuatorParts = [];
  let currentParts = armParts;

  function registrarPiezaEn(lista, grupo, mesh, info, deltaY, deltaX = 0, deltaZ = 0) {{
    mesh.userData = {{
      ...info,
      origPos: mesh.position.clone(),
      deltaPos: new THREE.Vector3(deltaX, deltaY, deltaZ)
    }};
    lista.push(mesh);
    grupo.add(mesh);
    return mesh;
  }}

  // ─────────────────────────────────────────────────────────────
  //  A. MODELO 1: BRAZO ROBÓTICO ARTICULADO 6-DOF CON PINZA
  // ─────────────────────────────────────────────────────────────

  // 1. Base y Pedestal de Fijación J1
  const bGeo = new THREE.CylinderGeometry(1.6, 1.9, 0.45, 32);
  const bMesh = new THREE.Mesh(bGeo, matAlDark);
  bMesh.position.set(0, -2.25, 0);
  registrarPiezaEn(armParts, groupArm, bMesh, {{
    id: "J1-BASE",
    nombre: "Base de Anclaje & Pedestal J1",
    desc: "Placa base de fundición pesada con 4 perforaciones normalizadas ISO 9409-1 para anclaje rígido a la bancada o celda robotizada.",
    mat: "Acero G25",
    tol: "±0.02 mm",
    load: "150 kg Estática",
    mod: "Brida ISO",
    instruct: "Fijar con 4 pernos M8 grado 10.9 a la celda de trabajo aplicando torque de 35 N·m en cruz."
  }}, 0, 0, 0);

  // 2. Torreta Giratoria Azimutal 360° J1
  const tGeo = new THREE.CylinderGeometry(1.3, 1.35, 0.65, 32);
  const tMesh = new THREE.Mesh(tGeo, matCyan);
  tMesh.position.set(0, -1.7, 0);
  registrarPiezaEn(armParts, groupArm, tMesh, {{
    id: "J1-TURRET",
    nombre: "Torreta Giratoria J1 (Eje Azimutal)",
    desc: "Unidad rotatoria continua 360° con rodamiento de rodillos cruzados para soportar momentos volcadores combinados.",
    mat: "Al 7075-T6 Anodizado",
    tol: "±0.005 mm",
    load: "180°/s · 19-Bit",
    mod: "Giro 360°",
    instruct: "Verificar precarga del rodamiento cruzado antes de cerrar la tapa inferior de engrase."
  }}, 0.7, 0, 0);

  // 3. Articulación de Hombro J2 (Harmonic Drive)
  const shGroup = new THREE.Group();
  const shBody = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.9, 1.1), matAlDark);
  const shPivot = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.55, 1.3, 24), matChrome);
  shPivot.rotation.z = Math.PI / 2;
  shGroup.add(shBody);
  shGroup.add(shPivot);
  shGroup.position.set(0, -0.9, 0);
  registrarPiezaEn(armParts, groupArm, shGroup, {{
    id: "J2-SHOULDER",
    nombre: "Hombro Articulado J2 (Elevación)",
    desc: "Articulación de alto par equipada con reductor armónico (Harmonic Drive 1:100) y freno electromagnético de seguridad en caso de corte eléctrico.",
    mat: "Al 6061-T6 CNC",
    tol: "< 1 arc-min",
    load: "48 N·m Continuo",
    mod: "Harmonic 1:100",
    instruct: "Conectar el cable del freno de seguridad de 24V y purgar el reductor armónico con grasa sintética 4B."
  }}, 1.6, -0.3, 0);

  // 4. Eslabón Primario L1 (Brazo de Fibra de Carbono)
  const l1Group = new THREE.Group();
  const l1Tube = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.32, 2.2, 20), matCarbon);
  l1Tube.rotation.z = -0.4;
  l1Tube.position.set(0.4, 0.25, 0);
  l1Group.add(l1Tube);
  l1Group.position.set(0, -0.3, 0);
  registrarPiezaEn(armParts, groupArm, l1Group, {{
    id: "LINK-L1",
    nombre: "Brazo Principal Eslabón L1",
    desc: "Tubo estructural de fibra de carbono aeroespacial de alta rigidez torsional y bajo momento de inercia dinámico.",
    mat: "Fibra Carbono / Ti",
    tol: "Rigidez 140 GPa",
    load: "350 mm Long.",
    mod: "Estructural",
    instruct: "Insertar los extremos en los casquillos de titanio y apretar los collares de apriete cónico."
  }}, 2.5, 0.6, 0);

  // 5. Articulación de Codo J3 (Flexión)
  const elGroup = new THREE.Group();
  const elMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 1.1, 24), matCyan);
  elMesh.rotation.z = Math.PI / 2;
  elGroup.add(elMesh);
  elGroup.position.set(0.9, 1.0, 0);
  registrarPiezaEn(armParts, groupArm, elGroup, {{
    id: "J3-ELBOW",
    nombre: "Codo Articulado J3 (Flexión)",
    desc: "Módulo integrado de flexión angular con encoder magnético absoluto multivuelta y sensor térmico integrado.",
    mat: "Aluminio 7075-T6",
    tol: "±0.01 mm",
    load: "28 N·m Torque",
    mod: "Rango -170°/+45°",
    instruct: "Guiar el bus de cables interno por el pasaje central hueco para evitar torsión de mangueras."
  }}, 3.4, 1.2, 0);

  // 6. Eslabón Secundario L2 (Antebrazo)
  const l2Mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.28, 1.8, 18), matCarbon);
  l2Mesh.rotation.z = 0.5;
  l2Mesh.position.set(0.4, 1.85, 0);
  registrarPiezaEn(armParts, groupArm, l2Mesh, {{
    id: "LINK-L2",
    nombre: "Antebrazo Eslabón L2",
    desc: "Brazo secundario estilizado con canaletas blindadas contra interferencias electromagnéticas (EMI) para buses de datos CAN/RS485.",
    mat: "Al-Mg-Si / Fibra",
    tol: "280 mm Long.",
    load: "1.8 kg Carga",
    mod: "Canalizado",
    instruct: "Verificar el radio mínimo de curvatura del cableado de señal para evitar microfracturas por flexión."
  }}, 4.3, 1.8, 0);

  // 7. Muñeca Esférica 2-Ejes J4/J5
  const wrGroup = new THREE.Group();
  const wrBody = new THREE.Mesh(new THREE.SphereGeometry(0.38, 20, 20), matChrome);
  const wrFlange = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.2, 24), matCyan);
  wrFlange.position.y = 0.35;
  wrGroup.add(wrBody);
  wrGroup.add(wrFlange);
  wrGroup.position.set(-0.2, 2.65, 0);
  registrarPiezaEn(armParts, groupArm, wrGroup, {{
    id: "J4-J5-WRIST",
    nombre: "Muñeca Esférica Biaxial J4/J5",
    desc: "Módulo ultracompacto de orientación angular con 2 micro-servomotores brushless y micro-reductores cicloidales.",
    mat: "Acero / Al CNC",
    tol: "±0.02 mm Repet.",
    load: "8.5 N·m Torque",
    mod: "Pitch ±110° · Roll 360°",
    instruct: "Montar con pernos M3 fijados con Loctite 242 y comprobar juego axial antes de instalar la pinza."
  }}, 5.2, 2.2, 0);

  // 8. Cuerpo de Pinza Paralela J6 (Gripper)
  const grGroup = new THREE.Group();
  const grBody = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.35, 0.5), matAlDark);
  grGroup.add(grBody);
  grGroup.position.set(-0.2, 3.15, 0);
  registrarPiezaEn(armParts, groupArm, grGroup, {{
    id: "J6-GRIPPER-BODY",
    nombre: "Cuerpo de Pinza Paralela J6",
    desc: "Chasis maestro de la pinza con husillo de rosca inversa y sensor de corriente para control adaptativo de fuerza de agarre.",
    mat: "Al 7075-T6",
    tol: "±0.005 mm",
    load: "Fuerza 10 - 65 N",
    mod: "Carrera 50 mm",
    instruct: "Conectar conector M8 de 4 pines y calibrar la corriente de agarre para objetos frágiles."
  }}, 6.0, 2.5, 0);

  // 9. Dedo Mordaza Izquierdo (Gripper Jaw Left)
  const jawLeft = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.5, 0.25), matCyan);
  jawLeft.position.set(-0.5, 3.55, 0);
  registrarPiezaEn(armParts, groupArm, jawLeft, {{
    id: "JAW-LEFT",
    nombre: "Mordaza Izquierda con Goma Táctil",
    desc: "Dedo mecanizado con almohadilla de elastómero de poliuretano 70A que maximiza el coeficiente de fricción.",
    mat: "Al 6061 / Poliuretano",
    tol: "±0.01 mm",
    load: "65 N Agarre",
    mod: "Dedo Táctil",
    instruct: "Alinear con el carro de guía lineal y apretar los 2 tornillos M2.5 de retención."
  }}, 6.7, 1.8, 0);

  // 10. Dedo Mordaza Derecho (Gripper Jaw Right)
  const jawRight = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.5, 0.25), matCyan);
  jawRight.position.set(0.1, 3.55, 0);
  registrarPiezaEn(armParts, groupArm, jawRight, {{
    id: "JAW-RIGHT",
    nombre: "Mordaza Derecha con Sensor de Carga",
    desc: "Dedo instrumentado con celda piezoeléctrica miniatura para retroalimentación de fuerza háptica en tiempo real.",
    mat: "Al 6061 / Galga",
    tol: "Resolución 0.05 N",
    load: "65 N Agarre",
    mod: "Sensor Háptico",
    instruct: "Calibrar el cero del sensor de fuerza antes de iniciar el ciclo de agarre autónomo."
  }}, 6.7, 3.2, 0);

  // ─────────────────────────────────────────────────────────────
  //  B. MODELO 2: ACTUADOR ROBÓTICO SERVO-INDUSTRIAL
  // ─────────────────────────────────────────────────────────────

  // 1. Carcasa Base
  const actBase = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.8, 0.7, 32), matAlDark);
  actBase.position.set(0, -1.8, 0);
  registrarPiezaEn(actuatorParts, groupActuator, actBase, {{
    id: "COMP-01",
    nombre: "Carcasa Base de Aluminio",
    desc: "Cuerpo estructural mecanizado CNC en aleación 6061-T6 con aletas de anclaje para montaje.",
    mat: "Al 6061-T6",
    tol: "±0.01 mm",
    load: "Carga Base",
    mod: "Métrico",
    instruct: "Fijar con cuatro pernos Allen M4 a la placa de montaje aplicando 3.2 N·m de torque."
  }}, 0);

  // 2. Driver PCB
  const actPcb = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 0.08, 32), new THREE.MeshStandardMaterial({{ color: 0x064e3b, metalness: 0.5, roughness: 0.4 }}));
  actPcb.position.set(0, -1.35, 0);
  registrarPiezaEn(actuatorParts, groupActuator, actPcb, {{
    id: "COMP-02",
    nombre: "Placa Lógica & Driver H-Bridge",
    desc: "PCB de cuatro capas con microcontrolador embebido de 32 bits y MOSFETs para conmutación PWM.",
    mat: "FR4 4-Capas",
    tol: "IPC-Class 3",
    load: "4.5 A Pico",
    mod: "32-Bit FOC",
    instruct: "Conectar arnés CAN/UART y verificar continuidad a masa antes de energizar a 24V."
  }}, -0.7);

  // 3. Estator con Bobinas
  const actStator = new THREE.Group();
  actStator.add(new THREE.Mesh(new THREE.CylinderGeometry(1.45, 1.45, 0.9, 16), new THREE.MeshStandardMaterial({{ color: 0x334155, metalness: 0.7 }})));
  for (let i = 0; i < 8; i++) {{
    const ang = (i / 8) * Math.PI * 2;
    const c = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.8, 0.5), matCopper);
    c.position.set(Math.cos(ang) * 1.05, 0, Math.sin(ang) * 1.05);
    c.rotation.y = -ang;
    actStator.add(c);
  }}
  actStator.position.set(0, -0.85, 0);
  registrarPiezaEn(actuatorParts, groupActuator, actStator, {{
    id: "COMP-03",
    nombre: "Estator Magnético con 8 Polos",
    desc: "Núcleo de acero al silicio laminado con devanados de cobre clase H (180°C) trifásicos.",
    mat: "Acero / Cobre",
    tol: "±0.02 mm",
    load: "120 W Continua",
    mod: "Trifásico",
    instruct: "Insertar concéntricamente guiando los terminales por la ranura lateral."
  }}, 0.8);

  // 4. Rotor Neodimio N52
  const actRotor = new THREE.Group();
  actRotor.add(new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 3.2, 24), matChrome));
  actRotor.add(new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 0.8, 24), new THREE.MeshStandardMaterial({{ color: 0x1e3a5f, metalness: 0.9, roughness: 0.2 }})));
  actRotor.position.set(0, -0.65, 0);
  registrarPiezaEn(actuatorParts, groupActuator, actRotor, {{
    id: "COMP-04",
    nombre: "Rotor de Neodimio NdFeB & Eje",
    desc: "Conjunto rotativo con imanes N52 balanceado dinámicamente hasta 12,000 RPM sin vibraciones.",
    mat: "NdFeB / Acero 304",
    tol: "G 2.5 Dinámico",
    load: "12,000 RPM",
    mod: "8 Polos N-S",
    instruct: "Introducir con precaución en el estator cuidando la atracción magnética brusca."
  }}, 1.9);

  // 5. Rodamiento 608ZZ
  const actBearing = new THREE.Mesh(new THREE.TorusGeometry(0.65, 0.18, 16, 32), matChrome);
  actBearing.rotation.x = Math.PI / 2;
  actBearing.position.set(0, 0.15, 0);
  registrarPiezaEn(actuatorParts, groupActuator, actBearing, {{
    id: "COMP-05",
    nombre: "Rodamiento de Bolas Radial 608ZZ",
    desc: "Rodamiento rectificado con sellos antipolvo. Tolerancia recomendada de eje: k5 (+1 a +7 µm) para evitar patinado.",
    mat: "Acero Cromo 100Cr6",
    tol: "ABEC-7 · Eje k5",
    load: "3,300 N Dinámica",
    mod: "Ø8x22x7 mm",
    instruct: "Embutir en prensa manual apoyando únicamente sobre el anillo exterior para no dañar las pistas."
  }}, 2.9);

  // 6. Tren Planetario
  const actGears = new THREE.Group();
  actGears.add(new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.3, 20), matGold));
  for (let i = 0; i < 3; i++) {{
    const a = (i / 3) * Math.PI * 2;
    const p = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.25, 20), matGold);
    p.position.set(Math.cos(a) * 0.8, 0, Math.sin(a) * 0.8);
    actGears.add(p);
  }}
  actGears.position.set(0, 0.55, 0);
  registrarPiezaEn(actuatorParts, groupActuator, actGears, {{
    id: "COMP-06",
    nombre: "Tren Reductor de Engranajes Planetarios",
    desc: "Sistema epicicloidal que multiplica el torque por 1:4.8 reduciendo la velocidad y holgura.",
    mat: "Acero 42CrMo4",
    tol: "DIN 6 (Precisión)",
    load: "1:4.8 Reducción",
    mod: "M 0.8 Dientes",
    instruct: "Alinear los 3 satélites en fase con la corona y lubricar con grasa sintética de litio."
  }}, 3.8);

  // 7. Tapa Superior
  const actTop = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.6, 0.35, 32), matCyan);
  actTop.position.set(0, 0.95, 0);
  registrarPiezaEn(actuatorParts, groupActuator, actTop, {{
    id: "COMP-07",
    nombre: "Tapa Superior de Sellado CNC",
    desc: "Cúpula de cierre con ranura para junta tórica O-ring de protección IP65 contra polvo.",
    mat: "Aluminio 6061-T6",
    tol: "±0.01 mm",
    load: "Sellado IP65",
    mod: "Cierre Frontal",
    instruct: "Verificar el O-ring limpio y apretar en cruz los 4 tornillos de fijación."
  }}, 4.7);

  // 8. Tornillos M3
  const actScrews = new THREE.Group();
  for (let i = 0; i < 4; i++) {{
    const a = (i / 4) * Math.PI * 2 + Math.PI / 4;
    const sc = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.45, 12), matChrome);
    sc.position.set(Math.cos(a) * 1.35, 0, Math.sin(a) * 1.35);
    actScrews.add(sc);
  }}
  actScrews.position.set(0, 1.25, 0);
  registrarPiezaEn(actuatorParts, groupActuator, actScrews, {{
    id: "COMP-08",
    nombre: "Tornillos Allen M3 de Precisión",
    desc: "Tornillería métrica de acero grado 12.9 de alta resistencia a tracción DIN 912.",
    mat: "Acero Grado 12.9",
    tol: "DIN 912",
    load: "Torque 1.5 N·m",
    mod: "Paso 0.5 mm",
    instruct: "Aplicar una gota de fijador de roscas Loctite 242 y apretar con llave hexagonal de 2.5 mm."
  }}, 5.5);

  // ─────────────────────────────────────────────────────────────
  //  ACTIVACIÓN Y SWITCHING DE MODELO EN TIEMPO REAL
  // ─────────────────────────────────────────────────────────────
  window.activarModelo = function(tipo) {{
    const btnArm = document.getElementById('btnSwitchArm');
    const btnAct = document.getElementById('btnSwitchActuator');
    const title = document.getElementById('topModelTitle');
    const sub = document.getElementById('topModelSubtitle');

    if (tipo === 'brazo') {{
      groupArm.visible = true;
      groupActuator.visible = false;
      currentParts = armParts;
      btnArm.classList.add('active');
      btnAct.classList.remove('active');
      title.innerHTML = '<span class="holo-indicator"></span> BRAZO ROBÓTICO 6-DOF CON PINZA';
      sub.innerText = 'MODELO HOLOGRÁFICO ARTICULADO · LABORATORIO TÁCTICO';
      camera.position.set(7.5, 5.5, 9);
      controls.target.set(0, 0.5, 0);
      actualizarHUD(armParts[7].userData); // Pinza
    }} else {{
      groupArm.visible = false;
      groupActuator.visible = true;
      currentParts = actuatorParts;
      btnAct.classList.add('active');
      btnArm.classList.remove('active');
      title.innerHTML = '<span class="holo-indicator"></span> ACTUADOR ROBÓTICO SERVO-INDUSTRIAL';
      sub.innerText = 'MODELO HOLOGRÁFICO 3D EN TIEMPO REAL · LABORATORIO TÁCTICO';
      camera.position.set(7, 5, 8);
      controls.target.set(0, 0, 0);
      actualizarHUD(actuatorParts[4].userData); // Rodamiento 608ZZ
    }}
    setExplosion(0);
  }};

  // ─────────────────────────────────────────────────────────────
  //  CONTROL DE EXPLOSIÓN Y ANIMACIÓN INTERPOLADA
  // ─────────────────────────────────────────────────────────────
  let explosionFactor = 0;
  let targetExplosion = 0;
  let isWireframe = false;
  let autoRotate = false;

  function setExplosion(val) {{
    targetExplosion = Math.max(0, Math.min(1, val));
    document.getElementById('explodeSlider').value = targetExplosion * 100;
  }}

  // Raycaster para clics e inspección
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();

  window.addEventListener('click', (e) => {{
    if (e.target.closest('.hud-bottom-bar') || e.target.closest('.hud-inspect') || e.target.closest('.model-selector')) return;

    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(currentParts, true);

    if (intersects.length > 0) {{
      let topObj = intersects[0].object;
      while (topObj.parent && topObj.parent !== groupArm && topObj.parent !== groupActuator && topObj.parent !== scene) {{
        topObj = topObj.parent;
      }}
      if (topObj.userData && topObj.userData.nombre) {{
        actualizarHUD(topObj.userData);
        resaltarPieza(topObj);
      }}
    }}
  }});

  function actualizarHUD(data) {{
    document.getElementById('hudTag').innerText = data.id || "COMP-OK";
    document.getElementById('hudPartName').innerText = data.nombre;
    document.getElementById('hudPartDesc').innerText = data.desc;
    document.getElementById('hudMat').innerText = data.mat;
    document.getElementById('hudTol').innerText = data.tol;
    document.getElementById('hudLoad').innerText = data.load;
    document.getElementById('hudMod').innerText = data.mod;
    document.getElementById('hudInstruct').innerHTML = `💡 <strong>Instrucción de Ensamble:</strong> ${{data.instruct}}`;

    const hud = document.getElementById('hudInspect');
    hud.style.borderColor = "#00f0ff";
    hud.style.boxShadow = "0 8px 32px rgba(0, 240, 255, 0.4)";
    setTimeout(() => {{
      hud.style.borderColor = "rgba(56, 189, 248, 0.4)";
      hud.style.boxShadow = "0 8px 32px rgba(0, 240, 255, 0.15)";
    }}, 400);
  }}

  function resaltarPieza(obj) {{
    obj.position.y += 0.25;
    setTimeout(() => {{
      obj.position.y -= 0.25;
    }}, 200);
  }}

  // Event Listeners de Botones
  document.getElementById('btnDisassemble').addEventListener('click', () => setExplosion(1.0));
  document.getElementById('btnAssemble').addEventListener('click', () => setExplosion(0.0));
  
  let stepIndex = 0;
  document.getElementById('btnStep').addEventListener('click', () => {{
    stepIndex = (stepIndex + 1) % 5;
    setExplosion(stepIndex / 4);
  }});

  document.getElementById('explodeSlider').addEventListener('input', (e) => {{
    setExplosion(parseFloat(e.target.value) / 100);
  }});

  document.getElementById('btnWireframe').addEventListener('click', () => {{
    isWireframe = !isWireframe;
    scene.traverse((child) => {{
      if (child.isMesh && child !== gridHelper && child !== ringMesh) {{
        child.material.wireframe = isWireframe;
        if (isWireframe) {{
          child.material.color.setHex(0x00f0ff);
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

  // Inicializar modelo activo según parámetro
  activarModelo('{modelo_inicial}');

  // Bucle de renderizado 60 FPS
  function animate() {{
    requestAnimationFrame(animate);

    // Interpolación suave del factor de explosión
    explosionFactor += (targetExplosion - explosionFactor) * 0.08;

    // Aplicar desplazamiento a cada pieza del modelo activo
    for (let i = 0; i < currentParts.length; i++) {{
      const p = currentParts[i];
      if (p.userData && p.userData.origPos && p.userData.deltaPos) {{
        p.position.x = p.userData.origPos.x + p.userData.deltaPos.x * explosionFactor;
        p.position.y = p.userData.origPos.y + p.userData.deltaPos.y * explosionFactor;
        p.position.z = p.userData.origPos.z + p.userData.deltaPos.z * explosionFactor;
      }}
    }}

    if (autoRotate) {{
      groupArm.rotation.y += 0.008;
      groupActuator.rotation.y += 0.008;
    }}

    controls.update();
    renderer.render(scene, camera);
  }}
  animate();

  window.addEventListener('resize', () => {{
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }});
}})();
</script>
</body>
</html>
```"""
'''

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\plantillas\holograma_3d.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("plantillas/holograma_3d.py updated successfully!")
