# -*- coding: utf-8 -*-
"""
Script para actualizar plantillas/holograma_3d.py con la función de
GEMELO DIGITAL: OBJETO FÍSICO REAL ↔ GEMELO DIGITAL 3D (VISTA DIVIDIDA).
"""

code = '''"""
LABORATORIO HOLOGRÁFICO 3D & GEMELO DIGITAL FÍSICO
Motor Three.js WebGL para AUREX / Isabella.
Soporte para:
- 📸 Objeto Físico Real (Acabados industriales realistas, iluminación de taller, placa de serie, textura metálica PBR).
- 🌐 Gemelo Digital 3D Holográfico (Desarmable en tiempo real, explosión, rayos X, inspección HUD).
- ◫ Vista Dividida (Split View): Ambos modelos en pantalla simultáneamente sincronizados a 360°.
- Selector de modelo: 🦾 Brazo Robótico 6-DOF ↔ ⚙️ Actuador Servo.
"""

def generar_laboratorio_holografico_3d(modelo_inicial="brazo"):
    return f"""```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HoloLab 3D · Gemelo Digital (Físico vs 3D)</title>
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

  /* CONTENEDOR PRINCIPAL DIVIDIDO EN 2 VENTANAS */
  #main-viewport-container {{
    display: flex;
    width: 100vw;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
    transition: all 0.3s ease;
  }}
  .viewport-half {{
    flex: 1;
    height: 100%;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
  }}
  .viewport-half.hidden {{
    display: none !important;
  }}
  .viewport-half.full {{
    flex: 2 !important;
  }}
  #half-physical {{
    background: radial-gradient(circle at 50% 50%, #1e293b 0%, #090d16 100%);
    border-right: 2px solid rgba(56, 189, 248, 0.4);
  }}
  #half-digital {{
    background: radial-gradient(circle at 50% 50%, #06182c 0%, #020617 100%);
  }}

  /* ETIQUETAS DE MODO EN CADA PANTALLA */
  .viewport-label {{
    position: absolute;
    top: 68px;
    left: 18px;
    z-index: 10;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 8px;
    pointer-events: none;
    backdrop-filter: blur(8px);
  }}
  .label-physical {{
    border-left: 4px solid #f59e0b;
    color: #fbbf24;
  }}
  .label-digital {{
    border-left: 4px solid #00f0ff;
    color: #38bdf8;
  }}
  .pulse-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
  }}
  .dot-amber {{ background: #f59e0b; box-shadow: 0 0 8px #f59e0b; }}
  .dot-cyan {{ background: #00f0ff; box-shadow: 0 0 8px #00f0ff; }}

  /* HUD SUPERIOR TÁCTICO */
  .hud-top {{
    position: absolute;
    top: 12px;
    left: 16px;
    right: 16px;
    z-index: 20;
    display: flex;
    justify-content: space-between;
    align-items: center;
    pointer-events: none;
    flex-wrap: wrap;
    gap: 8px;
  }}
  .hud-title-box {{
    background: rgba(10, 17, 33, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-left: 4px solid #38bdf8;
    backdrop-filter: blur(10px);
    padding: 6px 14px;
    border-radius: 4px;
    pointer-events: auto;
  }}
  .hud-title-box h1 {{
    font-size: 0.88rem;
    font-weight: 800;
    color: #38bdf8;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .hud-title-box p {{
    font-size: 0.65rem;
    color: #94a3b8;
  }}

  /* BARRA DE VISTAS (AMBOS, SOLO FÍSICO, SOLO 3D) */
  .view-mode-bar {{
    display: flex;
    gap: 4px;
    background: rgba(10, 17, 33, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 4px;
    border-radius: 6px;
    backdrop-filter: blur(10px);
    pointer-events: auto;
  }}
  .view-btn {{
    background: transparent;
    border: 1px solid transparent;
    color: #94a3b8;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .view-btn:hover {{
    color: #38bdf8;
    background: rgba(56, 189, 248, 0.1);
  }}
  .view-btn.active {{
    background: rgba(14, 165, 233, 0.25);
    border-color: #38bdf8;
    color: #00f0ff;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
  }}

  /* SELECTOR DE MODELO 3D (BRAZO VS ACTUADOR) */
  .model-selector {{
    display: flex;
    gap: 4px;
    background: rgba(10, 17, 33, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 4px;
    border-radius: 6px;
    backdrop-filter: blur(10px);
    pointer-events: auto;
  }}

  /* TARJETA LATERAL DE INSPECCIÓN (DATA HUD) */
  .hud-inspect {{
    position: absolute;
    top: 70px;
    right: 16px;
    width: 275px;
    background: rgba(10, 17, 33, 0.88);
    border: 1px solid rgba(56, 189, 248, 0.4);
    box-shadow: 0 8px 32px rgba(0, 240, 255, 0.18);
    backdrop-filter: blur(12px);
    border-radius: 8px;
    padding: 12px;
    z-index: 20;
    transition: all 0.3s ease;
  }}
  .hud-inspect-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    padding-bottom: 5px;
    margin-bottom: 6px;
  }}
  .hud-inspect-header .tag {{
    font-size: 0.62rem;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }}
  .hud-part-name {{
    font-size: 0.9rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 4px;
  }}
  .hud-part-desc {{
    font-size: 0.7rem;
    color: #94a3b8;
    line-height: 1.3;
    margin-bottom: 8px;
  }}
  .hud-specs-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
    background: rgba(15, 23, 42, 0.6);
    padding: 6px;
    border-radius: 4px;
    border: 1px solid rgba(56, 189, 248, 0.15);
    margin-bottom: 8px;
  }}
  .spec-item .lbl {{
    font-size: 0.58rem;
    color: #64748b;
    text-transform: uppercase;
  }}
  .spec-item .val {{
    font-size: 0.7rem;
    font-weight: 600;
    color: #38bdf8;
  }}
  .hud-instruction {{
    font-size: 0.68rem;
    color: #86efac;
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    padding: 6px;
    border-radius: 4px;
    line-height: 1.25;
  }}

  /* CONTROLES INFERIORES HOLOGRÁFICOS */
  .hud-bottom-bar {{
    position: absolute;
    bottom: 14px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 20;
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(10, 17, 33, 0.88);
    border: 1px solid rgba(56, 189, 248, 0.35);
    box-shadow: 0 4px 20px rgba(0, 240, 255, 0.12);
    backdrop-filter: blur(12px);
    padding: 6px 12px;
    border-radius: 30px;
  }}
  .holo-btn {{
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.4);
    color: #e2e8f0;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 6px 12px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .holo-btn:hover {{
    background: rgba(56, 189, 248, 0.2);
    border-color: #00f0ff;
    color: #00f0ff;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.35);
  }}
  .slider-box {{
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 0 6px;
    border-left: 1px solid rgba(56, 189, 248, 0.2);
    border-right: 1px solid rgba(56, 189, 248, 0.2);
  }}
  .slider-box span {{
    font-size: 0.68rem;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
  }}
  input[type="range"] {{
    width: 95px;
    accent-color: #00f0ff;
    cursor: pointer;
    height: 4px;
    background: #334155;
    border-radius: 4px;
  }}
  .hint-nav {{
    position: absolute;
    bottom: 58px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.65rem;
    color: #94a3b8;
    pointer-events: none;
    background: rgba(15, 23, 42, 0.7);
    padding: 3px 10px;
    border-radius: 10px;
    border: 1px solid rgba(56, 189, 248, 0.15);
  }}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>

<!-- HUD SUPERIOR -->
<div class="hud-top">
  <div class="hud-title-box">
    <h1 id="topModelTitle"><span class="dot-cyan pulse-dot"></span> GEMELO DIGITAL: FÍSICO ↔ 3D</h1>
    <p id="topModelSubtitle">VISTA COMPARATIVA EN TIEMPO REAL · LABORATORIO MECATRÓNICO</p>
  </div>

  <!-- SELECTOR DE VISTA (DIVIDIDA, SOLO FÍSICO, SOLO 3D) -->
  <div class="view-mode-bar">
    <button class="view-btn active" id="btnViewSplit" onclick="cambiarModoVista('split')">◫ Físico + 3D</button>
    <button class="view-btn" id="btnViewPhysical" onclick="cambiarModoVista('physical')">📷 Objeto Físico</button>
    <button class="view-btn" id="btnViewDigital" onclick="cambiarModoVista('digital')">🌐 Modelo 3D</button>
  </div>
  
  <!-- SELECTOR DE MODELO -->
  <div class="model-selector">
    <button class="view-btn active" id="btnSwitchArm" onclick="activarModelo('brazo')">🦾 Brazo 6-DOF</button>
    <button class="view-btn" id="btnSwitchActuator" onclick="activarModelo('actuador')">⚙️ Actuador</button>
  </div>
</div>

<!-- TARJETA LATERAL DE DATOS DE LA PIEZA SELECCIONADA -->
<div class="hud-inspect" id="hudInspect">
  <div class="hud-inspect-header">
    <span class="tag" id="hudTag">ID: J6-GRIPPER</span>
    <span style="font-size:0.62rem; color:#22c55e;">ESTADO: LISTO</span>
  </div>
  <div class="hud-part-name" id="hudPartName">Pinza Paralela (Gripper)</div>
  <div class="hud-part-desc" id="hudPartDesc">
    Efector final con husillo bilateral y dos mordazas con almohadillas de elastómero y sensor de carga.
  </div>
  <div class="hud-specs-grid">
    <div class="spec-item"><div class="lbl">Material</div><div class="val" id="hudMat">Al 7075-T6</div></div>
    <div class="spec-item"><div class="lbl">Fuerza / Tol</div><div class="val" id="hudTol">65 N · ±0.01mm</div></div>
    <div class="spec-item"><div class="lbl">Carga Máx</div><div class="val" id="hudLoad">1.5 kg Útil</div></div>
    <div class="spec-item"><div class="lbl">Carrera</div><div class="val" id="hudMod">0 - 50 mm</div></div>
  </div>
  <div class="hud-instruction" id="hudInstruct">
    💡 <strong>Instrucción de Ensamble:</strong> Fijar con 4 pernos Allen M3 a 1.4 N·m con arandela Nord-Lock.
  </div>
</div>

<div class="hint-nav">
  🖱️ Rota en cualquiera de las pantallas para mover ambos modelos al unísono · Clic en las piezas 3D para inspección
</div>

<!-- CONTROLES INFERIORES -->
<div class="hud-bottom-bar">
  <button class="holo-btn" id="btnDisassemble">🔓 Desarmar 3D</button>
  <button class="holo-btn" id="btnAssemble">🔒 Ensamblar 3D</button>
  <button class="holo-btn" id="btnStep">➡️ Paso a Paso</button>
  
  <div class="slider-box">
    <span>Explosión</span>
    <input type="range" id="explodeSlider" min="0" max="100" value="0">
  </div>

  <button class="holo-btn" id="btnWireframe">👁️ Rayos X</button>
  <button class="holo-btn" id="btnRotate">🔄 Auto Giro</button>
</div>

<!-- CONTENEDOR DE LAS 2 PANTALLAS (FÍSICO A LA IZQUIERDA, 3D A LA DERECHA) -->
<div id="main-viewport-container">
  <!-- PANTALLA 1: OBJETO FÍSICO REAL -->
  <div class="viewport-half" id="half-physical">
    <div class="viewport-label label-physical">
      <span class="dot-amber pulse-dot"></span> 📸 OBJETO FÍSICO REAL (ACABADO TALLER)
    </div>
  </div>

  <!-- PANTALLA 2: MODELO DIGITAL 3D HOLOGRÁFICO -->
  <div class="viewport-half" id="half-digital">
    <div class="viewport-label label-digital">
      <span class="dot-cyan pulse-dot"></span> 🌐 GEMELO DIGITAL 3D (DESPIECE ACTIVO)
    </div>
  </div>
</div>

<script>
(function() {{
  // ─────────────────────────────────────────────────────────────
  //  1. CONFIGURACIÓN DUAL: 2 ESCENAS, 2 CÁMARAS Y 2 RENDERIZADORES
  // ─────────────────────────────────────────────────────────────
  const containerPhys = document.getElementById('half-physical');
  const containerDig = document.getElementById('half-digital');

  // Escena Física (Iluminación de taller PBR, suelo de aluminio mecanizado)
  const scenePhys = new THREE.Scene();
  scenePhys.fog = new THREE.FogExp2(0x090d16, 0.025);

  // Escena Digital (Iluminación neón cian, rejilla de datos táctica)
  const sceneDig = new THREE.Scene();
  sceneDig.fog = new THREE.FogExp2(0x020617, 0.030);

  const camera = new THREE.PerspectiveCamera(45, (window.innerWidth / 2) / window.innerHeight, 0.1, 100);
  camera.position.set(7.5, 5.5, 9);

  // Renderizador Físico
  const rendererPhys = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
  rendererPhys.setSize(containerPhys.clientWidth, containerPhys.clientHeight);
  rendererPhys.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  rendererPhys.toneMapping = THREE.ACESFilmicToneMapping;
  rendererPhys.toneMappingExposure = 1.1;
  containerPhys.appendChild(rendererPhys.domElement);

  // Renderizador Digital
  const rendererDig = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
  rendererDig.setSize(containerDig.clientWidth, containerDig.clientHeight);
  rendererDig.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  rendererDig.toneMapping = THREE.ACESFilmicToneMapping;
  rendererDig.toneMappingExposure = 1.25;
  containerDig.appendChild(rendererDig.domElement);

  // Controles de cámara sincronizados para ambas pantallas
  const controlsPhys = new THREE.OrbitControls(camera, rendererPhys.domElement);
  controlsPhys.enableDamping = true;
  controlsPhys.dampingFactor = 0.06;
  controlsPhys.target.set(0, 0.5, 0);

  const controlsDig = new THREE.OrbitControls(camera, rendererDig.domElement);
  controlsDig.enableDamping = true;
  controlsDig.dampingFactor = 0.06;
  controlsDig.target.set(0, 0.5, 0);

  // ─────────────────────────────────────────────────────────────
  //  2. ILUMINACIÓN ESPECÍFICA PARA CADA ENTORNO
  // ─────────────────────────────────────────────────────────────
  // A. Iluminación Escena Física (Cálida 4500K de taller + reflector industrial)
  const ambLightPhys = new THREE.AmbientLight(0xfff7ed, 1.2);
  scenePhys.add(ambLightPhys);
  const sunLightPhys = new THREE.DirectionalLight(0xffedd5, 2.8);
  sunLightPhys.position.set(5, 12, 7);
  scenePhys.add(sunLightPhys);
  const rimLightPhys = new THREE.DirectionalLight(0x94a3b8, 1.6);
  rimLightPhys.position.set(-6, -3, -5);
  scenePhys.add(rimLightPhys);

  // B. Iluminación Escena Digital (Cian / Azul futurista Stark)
  const ambLightDig = new THREE.AmbientLight(0x0f172a, 1.6);
  sceneDig.add(ambLightDig);
  const sunLightDig = new THREE.DirectionalLight(0x00f0ff, 2.6);
  sunLightDig.position.set(6, 12, 8);
  sceneDig.add(sunLightDig);
  const fillLightDig = new THREE.DirectionalLight(0x3b82f6, 1.8);
  fillLightDig.position.set(-6, -4, -6);
  sceneDig.add(fillLightDig);

  // Suelo Escena Física (Banco de trabajo de taller industrial con textura y base rayada)
  const benchGeo = new THREE.CylinderGeometry(4.5, 4.8, 0.2, 48);
  const benchMat = new THREE.MeshStandardMaterial({{ color: 0x334155, metalness: 0.6, roughness: 0.6 }});
  const benchMesh = new THREE.Mesh(benchGeo, benchMat);
  benchMesh.position.y = -2.5;
  scenePhys.add(benchMesh);

  // Banda de seguridad industrial amarilla/negra de advertencia
  const hazardGeo = new THREE.RingGeometry(3.6, 4.0, 48);
  const hazardMat = new THREE.MeshStandardMaterial({{ color: 0xf59e0b, side: THREE.DoubleSide, roughness: 0.5 }});
  const hazardMesh = new THREE.Mesh(hazardGeo, hazardMat);
  hazardMesh.rotation.x = Math.PI / 2;
  hazardMesh.position.y = -2.39;
  scenePhys.add(hazardMesh);

  // Suelo Escena Digital (Rejilla cian neón)
  const gridHelper = new THREE.GridHelper(16, 32, 0x00f0ff, 0x1e3a5f);
  gridHelper.position.y = -2.5;
  sceneDig.add(gridHelper);

  // ─────────────────────────────────────────────────────────────
  //  3. MATERIALES COMPARATIVOS: REALISMO FÍSICO VS HOLOGRÁFICO
  // ─────────────────────────────────────────────────────────────
  // Materiales Físicos (Textura de fundición, acabado cepillado, brillo metálico real)
  const matPhysIron = new THREE.MeshStandardMaterial({{ color: 0x1f2937, metalness: 0.7, roughness: 0.55 }});
  const matPhysAlum = new THREE.MeshStandardMaterial({{ color: 0x475569, metalness: 0.85, roughness: 0.2 }});
  const matPhysOrange = new THREE.MeshStandardMaterial({{ color: 0xea580c, metalness: 0.3, roughness: 0.4 }}); // Color robótico industrial
  const matPhysCarbon = new THREE.MeshStandardMaterial({{ color: 0x0f172a, metalness: 0.9, roughness: 0.3 }});
  const matPhysChrome = new THREE.MeshStandardMaterial({{ color: 0xf8fafc, metalness: 0.98, roughness: 0.05 }});
  const matPhysBrass = new THREE.MeshStandardMaterial({{ color: 0xd97706, metalness: 0.9, roughness: 0.25 }});

  // Materiales Digitales (Neón, Wireframe y Cian translúcido)
  const matDigDark = new THREE.MeshStandardMaterial({{ color: 0x0f172a, metalness: 0.85, roughness: 0.25 }});
  const matDigCyan = new THREE.MeshStandardMaterial({{ color: 0x0284c7, emissive: 0x00f0ff, emissiveIntensity: 0.35, metalness: 0.9, roughness: 0.2 }});
  const matDigChrome = new THREE.MeshStandardMaterial({{ color: 0xe2e8f0, metalness: 0.95, roughness: 0.1 }});
  const matDigGold = new THREE.MeshStandardMaterial({{ color: 0xca8a04, metalness: 0.9, roughness: 0.3, emissive: 0x422006 }});
  const matDigCopper = new THREE.MeshStandardMaterial({{ color: 0xb45309, metalness: 0.8, roughness: 0.35 }});

  // ─────────────────────────────────────────────────────────────
  //  4. CONSTRUCCIÓN DE MODELOS EN AMBAS ESCENAS
  // ─────────────────────────────────────────────────────────────
  // Grupos en escena física
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
  let currentDigParts = digArmParts;

  function registrarPiezaDigital(lista, grupo, mesh, info, deltaY, deltaX = 0, deltaZ = 0) {{
    mesh.userData = {{
      ...info,
      origPos: mesh.position.clone(),
      deltaPos: new THREE.Vector3(deltaX, deltaY, deltaZ)
    }};
    lista.push(mesh);
    grupo.add(mesh);
    return mesh;
  }}

  // ── MODELO 1: BRAZO ROBÓTICO 6-DOF ──
  // A) Versión Física (Siempre armada, con colores de taller KUKA / Fanuc / ABB)
  function buildArmPhysical() {{
    const b = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.9, 0.45, 32), matPhysIron);
    b.position.set(0, -2.25, 0); groupPhysArm.add(b);

    const t = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.35, 0.65, 32), matPhysOrange);
    t.position.set(0, -1.7, 0); groupPhysArm.add(t);

    const sh = new THREE.Group();
    sh.add(new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.9, 1.1), matPhysAlum));
    const shP = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.55, 1.3, 24), matPhysChrome);
    shP.rotation.z = Math.PI / 2; sh.add(shP);
    sh.position.set(0, -0.9, 0); groupPhysArm.add(sh);

    const l1 = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.32, 2.2, 20), matPhysCarbon);
    l1.rotation.z = -0.4; l1.position.set(0.4, -0.05, 0); groupPhysArm.add(l1);

    const el = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 1.1, 24), matPhysOrange);
    el.rotation.z = Math.PI / 2; el.position.set(0.9, 1.0, 0); groupPhysArm.add(el);

    const l2 = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.28, 1.8, 18), matPhysCarbon);
    l2.rotation.z = 0.5; l2.position.set(0.4, 1.85, 0); groupPhysArm.add(l2);

    const wr = new THREE.Group();
    wr.add(new THREE.Mesh(new THREE.SphereGeometry(0.38, 20, 20), matPhysChrome));
    const wrF = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.2, 24), matPhysAlum);
    wrF.position.y = 0.35; wr.add(wrF);
    wr.position.set(-0.2, 2.65, 0); groupPhysArm.add(wr);

    const gr = new THREE.Group();
    gr.add(new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.35, 0.5), matPhysIron));
    const jl = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.5, 0.25), matPhysOrange);
    jl.position.set(-0.35, 0.4, 0); gr.add(jl);
    const jr = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.5, 0.25), matPhysOrange);
    jr.position.set(0.35, 0.4, 0); gr.add(jr);
    gr.position.set(-0.2, 3.15, 0); groupPhysArm.add(gr);
  }}
  buildArmPhysical();

  // B) Versión Digital (Desarmable con explosión)
  function buildArmDigital() {{
    const b = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.9, 0.45, 32), matDigDark);
    b.position.set(0, -2.25, 0);
    registrarPiezaDigital(digArmParts, groupDigArm, b, {{
      id: "J1-BASE", nombre: "Base & Pedestal J1", desc: "Placa base pesada con brida ISO 9409-1.",
      mat: "Acero G25", tol: "±0.02 mm", load: "150 kg Estática", mod: "Brida ISO",
      instruct: "Apretar los 4 pernos M8 a 35 N·m en cruz."
    }}, 0);

    const t = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.35, 0.65, 32), matDigCyan);
    t.position.set(0, -1.7, 0);
    registrarPiezaDigital(digArmParts, groupDigArm, t, {{
      id: "J1-TURRET", nombre: "Torreta Giratoria J1 (Azimut 360°)", desc: "Rodamiento cruzado para momentos volcadores.",
      mat: "Al 7075-T6", tol: "±0.005 mm", load: "180°/s · 19-Bit", mod: "Giro 360°",
      instruct: "Comprobar precarga antes de engrasar."
    }}, 0.7);

    const sh = new THREE.Group();
    sh.add(new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.9, 1.1), matDigDark));
    const shP = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.55, 1.3, 24), matDigChrome);
    shP.rotation.z = Math.PI / 2; sh.add(shP);
    sh.position.set(0, -0.9, 0);
    registrarPiezaDigital(digArmParts, groupDigArm, sh, {{
      id: "J2-SHOULDER", nombre: "Hombro Articulado J2", desc: "Reductor armónico Harmonic Drive 1:100.",
      mat: "Al 6061-T6", tol: "< 1 arc-min", load: "48 N·m Torque", mod: "Harmonic 1:100",
      instruct: "Conectar freno de seguridad de 24V."
    }}, 1.6, -0.3);

    const l1 = new THREE.Group();
    const l1T = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.32, 2.2, 20), matDigDark);
    l1T.rotation.z = -0.4; l1T.position.set(0.4, 0.25, 0); l1.add(l1T);
    l1.position.set(0, -0.3, 0);
    registrarPiezaDigital(digArmParts, groupDigArm, l1, {{
      id: "LINK-L1", nombre: "Brazo Principal Eslabón L1", desc: "Tubo de fibra de carbono aeroespacial de alta rigidez.",
      mat: "Fibra Carbono / Ti", tol: "Rigidez 140 GPa", load: "350 mm Long.", mod: "Estructural",
      instruct: "Apretar collares cónicos a 12 N·m."
    }}, 2.5, 0.6);

    const el = new THREE.Group();
    const elM = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 1.1, 24), matDigCyan);
    elM.rotation.z = Math.PI / 2; el.add(elM);
    el.position.set(0.9, 1.0, 0);
    registrarPiezaDigital(digArmParts, groupDigArm, el, {{
      id: "J3-ELBOW", nombre: "Codo Articulado J3", desc: "Módulo integrado con encoder magnético absoluto multivuelta.",
      mat: "Al 7075-T6", tol: "±0.01 mm", load: "28 N·m Torque", mod: "Rango -170°/+45°",
      instruct: "Guiar bus de cables por el pasaje hueco."
    }}, 3.4, 1.2);

    const l2 = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.28, 1.8, 18), matDigDark);
    l2.rotation.z = 0.5; l2.position.set(0.4, 1.85, 0);
    registrarPiezaDigital(digArmParts, groupDigArm, l2, {{
      id: "LINK-L2", nombre: "Antebrazo Eslabón L2", desc: "Brazo secundario con blindaje EMI para buses CAN/RS485.",
      mat: "Al-Mg-Si / Fibra", tol: "280 mm Long.", load: "1.8 kg Carga", mod: "Canalizado",
      instruct: "Comprobar radio de curvatura de cables."
    }}, 4.3, 1.8);

    const wr = new THREE.Group();
    wr.add(new THREE.Mesh(new THREE.SphereGeometry(0.38, 20, 20), matDigChrome));
    const wrF = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.2, 24), matDigCyan);
    wrF.position.y = 0.35; wr.add(wrF);
    wr.position.set(-0.2, 2.65, 0);
    registrarPiezaDigital(digArmParts, groupDigArm, wr, {{
      id: "J4-J5-WRIST", nombre: "Muñeca Esférica J4/J5", desc: "Módulo ultracompacto biaxial (Pitch & Roll).",
      mat: "Acero / Al CNC", tol: "±0.02 mm Repet.", load: "8.5 N·m Torque", mod: "Pitch/Roll",
      instruct: "Fijar pernos M3 con Loctite 242."
    }}, 5.2, 2.2);

    const gr = new THREE.Group();
    gr.add(new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.35, 0.5), matDigDark));
    gr.position.set(-0.2, 3.15, 0);
    registrarPiezaDigital(digArmParts, groupDigArm, gr, {{
      id: "J6-GRIPPER", nombre: "Cuerpo de Pinza Paralela J6", desc: "Chasis maestro con husillo de rosca inversa.",
      mat: "Al 7075-T6", tol: "±0.005 mm", load: "Fuerza 65 N", mod: "Carrera 50 mm",
      instruct: "Calibrar cero de fuerza háptica."
    }}, 6.0, 2.5);

    const jl = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.5, 0.25), matDigCyan);
    jl.position.set(-0.5, 3.55, 0);
    registrarPiezaDigital(digArmParts, groupDigArm, jl, {{
      id: "JAW-LEFT", nombre: "Mordaza Izquierda con Goma", desc: "Almohadilla de poliuretano antideslizante.",
      mat: "Al 6061 / Poliuretano", tol: "±0.01 mm", load: "65 N Agarre", mod: "Dedo Táctil",
      instruct: "Fijar con 2 pernos M2.5 a guía lineal."
    }}, 6.7, 1.8);

    const jr = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.5, 0.25), matDigCyan);
    jr.position.set(0.1, 3.55, 0);
    registrarPiezaDigital(digArmParts, groupDigArm, jr, {{
      id: "JAW-RIGHT", nombre: "Mordaza Derecha con Sensor", desc: "Celda de carga piezoeléctrica miniatura.",
      mat: "Al 6061 / Galga", tol: "0.05 N Resol.", load: "65 N Agarre", mod: "Sensor Háptico",
      instruct: "Comprobar lectura analógica en reposo."
    }}, 6.7, 3.2);
  }}
  buildArmDigital();

  // ── MODELO 2: ACTUADOR ROBÓTICO SERVO-INDUSTRIAL ──
  // A) Versión Física
  function buildActuatorPhysical() {{
    const b = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.8, 0.7, 32), matPhysAlum);
    b.position.set(0, -1.8, 0); groupPhysAct.add(b);

    const st = new THREE.Mesh(new THREE.CylinderGeometry(1.45, 1.45, 0.9, 24), matPhysIron);
    st.position.set(0, -0.85, 0); groupPhysAct.add(st);

    const sh = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 3.2, 24), matPhysChrome);
    sh.position.set(0, -0.65, 0); groupPhysAct.add(sh);

    const be = new THREE.Mesh(new THREE.TorusGeometry(0.65, 0.18, 16, 32), matPhysChrome);
    be.rotation.x = Math.PI / 2; be.position.set(0, 0.15, 0); groupPhysAct.add(be);

    const g = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.4, 24), matPhysBrass);
    g.position.set(0, 0.55, 0); groupPhysAct.add(g);

    const top = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.6, 0.35, 32), matPhysOrange);
    top.position.set(0, 0.95, 0); groupPhysAct.add(top);
  }}
  buildActuatorPhysical();

  // B) Versión Digital (Desarmable)
  function buildActuatorDigital() {{
    const b = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.8, 0.7, 32), matDigDark);
    b.position.set(0, -1.8, 0);
    registrarPiezaDigital(digActParts, groupDigAct, b, {{
      id: "COMP-01", nombre: "Carcasa Base CNC", desc: "Aluminio 6061-T6 con aletas disipadoras.",
      mat: "Al 6061-T6", tol: "±0.01 mm", load: "Carga Base", mod: "Métrico", instruct: "Apretar pernos M4 a 3.2 N·m."
    }}, 0);

    const pcb = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 1.4, 0.08, 32), new THREE.MeshStandardMaterial({{ color: 0x064e3b }}));
    pcb.position.set(0, -1.35, 0);
    registrarPiezaDigital(digActParts, groupDigAct, pcb, {{
      id: "COMP-02", nombre: "Driver PCB FOC", desc: "Controlador FOC de 32 bits con MOSFETs.",
      mat: "FR4 4-Capas", tol: "IPC Class 3", load: "4.5 A Pico", mod: "FOC 32-Bit", instruct: "Verificar masa antes de 24V."
    }}, -0.7);

    const st = new THREE.Group();
    st.add(new THREE.Mesh(new THREE.CylinderGeometry(1.45, 1.45, 0.9, 16), matDigDark));
    for (let i = 0; i < 8; i++) {{
      const a = (i / 8) * Math.PI * 2;
      const c = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.8, 0.5), matDigCopper);
      c.position.set(Math.cos(a)*1.05, 0, Math.sin(a)*1.05); c.rotation.y = -a; st.add(c);
    }}
    st.position.set(0, -0.85, 0);
    registrarPiezaDigital(digActParts, groupDigAct, st, {{
      id: "COMP-03", nombre: "Estator Trifásico", desc: "8 devanados de cobre clase H 180°C.",
      mat: "Acero / Cobre", tol: "±0.02 mm", load: "120 W Continua", mod: "Trifásico", instruct: "Guiar cables por la ranura."
    }}, 0.8);

    const rot = new THREE.Group();
    rot.add(new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 3.2, 24), matDigChrome));
    rot.add(new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 0.8, 24), matDigDark));
    rot.position.set(0, -0.65, 0);
    registrarPiezaDigital(digActParts, groupDigAct, rot, {{
      id: "COMP-04", nombre: "Rotor Neodimio N52", desc: "Balanceo dinámico hasta 12,000 RPM.",
      mat: "NdFeB / Acero", tol: "G 2.5 Dinámico", load: "12,000 RPM", mod: "8 Polos", instruct: "Insertar evitando choque magnético."
    }}, 1.9);

    const be = new THREE.Mesh(new THREE.TorusGeometry(0.65, 0.18, 16, 32), matDigChrome);
    be.rotation.x = Math.PI / 2; be.position.set(0, 0.15, 0);
    registrarPiezaDigital(digActParts, groupDigAct, be, {{
      id: "COMP-05", nombre: "Rodamiento 608ZZ", desc: "Tolerancia de eje recomendada: k5 (+1 a +7 µm) para evitar patinado.",
      mat: "Acero 100Cr6", tol: "ABEC-7 · Eje k5", load: "3,300 N Dinámica", mod: "Ø8x22x7 mm", instruct: "Embutir apoyando solo en anillo exterior."
    }}, 2.9);

    const gr = new THREE.Group();
    gr.add(new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.3, 20), matDigGold));
    for (let i = 0; i < 3; i++) {{
      const a = (i / 3) * Math.PI * 2;
      const p = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.25, 20), matDigGold);
      p.position.set(Math.cos(a)*0.8, 0, Math.sin(a)*0.8); gr.add(p);
    }}
    gr.position.set(0, 0.55, 0);
    registrarPiezaDigital(digActParts, groupDigAct, gr, {{
      id: "COMP-06", nombre: "Tren Planetario", desc: "Reducción 1:4.8 que multiplica el torque.",
      mat: "Acero 42CrMo4", tol: "DIN 6", load: "1:4.8 Reducción", mod: "M 0.8", instruct: "Alinear satélites y lubricar."
    }}, 3.8);

    const top = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.6, 0.35, 32), matDigCyan);
    top.position.set(0, 0.95, 0);
    registrarPiezaDigital(digActParts, groupDigAct, top, {{
      id: "COMP-07", nombre: "Tapa Superior CNC", desc: "Sellado con O-ring contra polvo y agua IP65.",
      mat: "Al 6061-T6", tol: "±0.01 mm", load: "Sellado IP65", mod: "Cierre", instruct: "Apretar 4 pernos en cruz a 1.5 N·m."
    }}, 4.7);
  }}
  buildActuatorDigital();

  // ─────────────────────────────────────────────────────────────
  //  5. GESTIÓN DE VISTAS (SPLIT VIEW / SOLO FÍSICO / SOLO 3D)
  // ─────────────────────────────────────────────────────────────
  window.cambiarModoVista = function(modo) {{
    const halfP = document.getElementById('half-physical');
    const halfD = document.getElementById('half-digital');
    const btnS = document.getElementById('btnViewSplit');
    const btnP = document.getElementById('btnViewPhysical');
    const btnD = document.getElementById('btnViewDigital');

    btnS.classList.remove('active');
    btnP.classList.remove('active');
    btnD.classList.remove('active');

    if (modo === 'split') {{
      btnS.classList.add('active');
      halfP.classList.remove('hidden', 'full');
      halfD.classList.remove('hidden', 'full');
    }} else if (modo === 'physical') {{
      btnP.classList.add('active');
      halfP.classList.remove('hidden');
      halfP.classList.add('full');
      halfD.classList.add('hidden');
    }} else if (modo === 'digital') {{
      btnD.classList.add('active');
      halfD.classList.remove('hidden');
      halfD.classList.add('full');
      halfP.classList.add('hidden');
    }}

    setTimeout(() => {{
      onWindowResize();
    }}, 100);
  }};

  // ─────────────────────────────────────────────────────────────
  //  6. SELECTOR DE MODELO (BRAZO 6-DOF VS ACTUADOR)
  // ─────────────────────────────────────────────────────────────
  window.activarModelo = function(tipo) {{
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
  }};

  // ─────────────────────────────────────────────────────────────
  //  7. EXPLOSIÓN INTERPOLADA Y RAYCASTING DIGITAL
  // ─────────────────────────────────────────────────────────────
  let explosionFactor = 0;
  let targetExplosion = 0;
  let isWireframe = false;
  let autoRotate = false;

  function setExplosion(val) {{
    targetExplosion = Math.max(0, Math.min(1, val));
    document.getElementById('explodeSlider').value = targetExplosion * 100;
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
      while (topObj.parent && topObj.parent !== groupDigArm && topObj.parent !== groupDigAct && topObj.parent !== sceneDig) {{
        topObj = topObj.parent;
      }}
      if (topObj.userData && topObj.userData.nombre) {{
        actualizarHUD(topObj.userData);
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
      hud.style.boxShadow = "0 8px 32px rgba(0, 240, 255, 0.18)";
    }}, 400);
  }}

  // Controles botones inferiores
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
    sceneDig.traverse((child) => {{
      if (child.isMesh && child !== gridHelper) {{
        child.material.wireframe = isWireframe;
        if (isWireframe) child.material.color.setHex(0x00f0ff);
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

  // Inicializar modelo
  activarModelo('{modelo_inicial}');

  // ─────────────────────────────────────────────────────────────
  //  8. BUCLE DE RENDERIZADO DUAL SINCRONIZADO A 60 FPS
  // ─────────────────────────────────────────────────────────────
  function animate() {{
    requestAnimationFrame(animate);

    explosionFactor += (targetExplosion - explosionFactor) * 0.08;

    // Solo el modelo digital se despieza/desarma
    for (let i = 0; i < currentDigParts.length; i++) {{
      const p = currentDigParts[i];
      if (p.userData && p.userData.origPos && p.userData.deltaPos) {{
        p.position.x = p.userData.origPos.x + p.userData.deltaPos.x * explosionFactor;
        p.position.y = p.userData.origPos.y + p.userData.deltaPos.y * explosionFactor;
        p.position.z = p.userData.origPos.z + p.userData.deltaPos.z * explosionFactor;
      }}
    }}

    if (autoRotate) {{
      groupPhysArm.rotation.y += 0.008;
      groupPhysAct.rotation.y += 0.008;
      groupDigArm.rotation.y += 0.008;
      groupDigAct.rotation.y += 0.008;
    }}

    controlsPhys.update();
    controlsDig.update();

    // Renderizar ambas pantallas
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
'''

with open(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\plantillas\holograma_3d.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("plantillas/holograma_3d.py successfully updated with Digital Twin (Physical vs 3D)!")
