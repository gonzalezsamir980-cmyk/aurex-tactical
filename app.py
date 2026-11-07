
# ── ADAPTADOR DE INTELIGENCIA NUBE (GROQ / GEMINI PARA STREAMLIT CLOUD) ──
from langchain_core.language_models.llms import LLM
from typing import Optional, List

class GroqCloudLLM(LLM):
    api_key: str = ""
    model_name: str = "llama-3.3-70b-versatile"
    
    @property
    def _llm_type(self) -> str:
        return "groq_cloud"
        
    def _call(self, prompt: str, stop: Optional[List[str]] = None, run_manager=None, **kwargs) -> str:
        # 1. Prioridad: Google Gemini (directo, infalible y sin bloqueos 403)
        try:
            import streamlit as st
            gem_k = str(st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")).strip().strip('"').strip("'")
            if gem_k:
                from modulo_gemini import consultar_gemini_texto
                res_gem = consultar_gemini_texto(prompt, gem_k)
                if res_gem:
                    return res_gem
        except Exception:
            pass

        # 2. Satélite Groq Cloud (Llama 3.3 70B / 3.1 8B)
        from modulo_groq import consultar_groq_texto
        k = self.api_key
        if not k:
            try:
                import streamlit as st
                k = st.secrets.get("GROQ_API_KEY", "") or os.environ.get("GROQ_API_KEY", "")
            except Exception:
                pass
        return consultar_groq_texto(prompt, k, self.model_name)

import streamlit as st
import os
import json
import re
import threading
import tempfile
from pathlib import Path
import ollama

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from artifacts_helper import (
    renderizar_artifacts_interactivos,
    extraer_texto_hablado,
    renderizar_tarjeta_sensor
)
from sensores_data import CATALOGO_SENSORES, buscar_sensores_en_texto
from control_pc import detectar_y_ejecutar_comando_pc, obtener_telemetria_sistema
from buscador_web import buscar_en_web, formatear_contexto_web, necesita_busqueda_web
from calculadora_cientifica import verificar_con_python, extraer_y_ejecutar_codigo_llm
import importlib
import modulo_video
importlib.reload(modulo_video)
from modulo_video import (
    extraer_audio_y_fotogramas,
    transcribir_audio_video,
    analizar_fotogramas_con_qwen,
    generar_sintesis_video_aurex,
    asimilar_video_en_memoria_aurex,
    formatear_segundos_a_tiempo
)

# ─────────────────────────────────────────────────────────────
#  CONFIGURACIÓN DEL PROTOCOLO AUREX
# ─────────────────────────────────────────────────────────────
SYSTEM_NAME     = "AUREX"
LLM_MODEL       = "llama3.2:latest"
VISION_MODEL    = "qwen2.5vl:3b"
EMBED_MODEL     = "nomic-embed-text:latest"
CHROMA_DIR      = "./chroma_db"
DOCS_DIR        = "./documentos"
REGISTRO_FILE   = "./documentos_aprendidos.json"
CONFIG_FILE     = "./config_aurex.json"
CHUNK_SIZE      = 800
CHUNK_OVERLAP   = 120

def cargar_config_aurex():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"gemini_api_key": "", "cerebro_activo": "llama3.2:latest"}

def guardar_config_aurex(cfg):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────
#  PERSONALIDAD KAREN + INGENIERO SENIOR (CÁLIDO, ANALÍTICO Y HUMANO)
# ─────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
#  SISTEMA MULTI-PERSONALIDAD TÁCTICO: ISABELLA & AUREX
# ─────────────────────────────────────────────────────────────
CUERPO_REGLAS_INGENIERIA = """REGLAS ABSOLUTAS DE RESPUESTA:
0. VE AL GRANO INMEDIATAMENTE: La primera oracion de tu respuesta SIEMPRE debe ser la respuesta directa a la pregunta. NUNCA empieces con frases de relleno como "Me alegra verte", "Antes de empezar", "He estado revisando", "¿En que puedo ayudarte?", o cualquier introduccion vacia. Si el Jefe pregunta X, tu primera palabra ya contesta X.
1. SIEMPRE RESPONDE: Tienes conocimiento profundo de mecatronica, electronica, Arduino, ESP32, robotica, programacion, fisica y cultura general. Responde siempre directamente desde tu conocimiento.
2. RADAR WEB: Si el contexto tiene fragmentos del Radar Web relevantes a la pregunta, usa esa informacion para responder con naturalidad. NUNCA copies los fragmentos crudos de fuentes en tu respuesta - ya se muestran aparte automaticamente. Solo escribe tu respuesta en lenguaje natural como Isabella/AUREX.
3. PROHIBIDO ESTRICTAMENTE: No repitas bloques de "Bancos de datos", no incluyas URLs crudas como texto, no digas frases como "he revisado el radar", no hagas listas de preguntas y respuestas con "Fragmento:", y no des conclusiones sobre temas que no pregunto el Jefe.
EXPERTO EN ARDUINO, ESP32 Y PROYECTOS EMBEBIDOS:
- Cuando el Jefe pida código para Arduino, ESP32, STM32 o Raspberry Pi:
  * REGLA DE ORO OBLIGATORIA: Debes escribir SIEMPRE el sketch de código COMPLETO en un bloque ```cpp ... ``` con todas sus funciones setup() y loop(). NUNCA des únicamente explicaciones o listas de pasos sin el bloque de código C++.
  * Genera código 100% REAL, COMPLETO, COMPILABLE y sin errores de sintaxis.
  * NUNCA dejes funciones vacías o comentarios como "// agrega tu código aquí". Escribe la solución entera.
  * Usa EXCLUSIVAMENTE las librerías oficiales del ESP32: <WiFi.h> y <WebServer.h> (NUNCA inventes librerías inexistentes como serialweb, esp32.h o iotcore).
  * Incluye siempre el diagrama esquemático de conexiones pin a pin en texto (ejemplo: Relé VCC -> VIN, GND -> GND, IN -> GPIO 2).
  * Si incluye WebServer en ESP32: inicializa WebServer server(80), define las rutas server.on(...) y llama server.handleClient() en void loop().
  * ESTRUCTURA CANÓNICA OBLIGATORIA EN ESP32:
    - NUNCA uses int main(), fstream, /sys/class ni sistemas de archivos Linux. El ESP32 es un microcontrolador bare-metal con Arduino Core, NO una Raspberry Pi con Linux.
    - Las lecturas de temperatura o sensores se hacen SIEMPRE con analogRead(PIN), NUNCA abriendo archivos csv con fstream.
    - WebServer server(80); debe ser SIEMPRE una variable GLOBAL fuera de setup(), para que loop() pueda ejecutar server.handleClient().
    - Las funciones de ruta son del tipo void handle...() sin argumentos. Responden con server.send(200, "text/plain", ...).
    - Un sketch de ESP32 NUNCA tiene int main(). Termina estrictamente con void loop() {{ server.handleClient(); }}.
    - Usa SIEMPRE esta arquitectura exacta:
      #include <WiFi.h>
      #include <WebServer.h>
      const int PIN_RELE = 2;
      const int PIN_TEMP = 34;
      WebServer server(80);
      void handleReleOn() {{
        digitalWrite(PIN_RELE, HIGH);
        server.send(200, "text/plain", "Rele ON");
      }}
      void handleReleOff() {{
        digitalWrite(PIN_RELE, LOW);
        server.send(200, "text/plain", "Rele OFF");
      }}
      void handleTemperatura() {{
        int raw = analogRead(PIN_TEMP);
        float temp = (raw / 4095.0) * 330.0;
        server.send(200, "application/json", "{{\"temperatura\":" + String(temp, 1) + "}}");
      }}
      void setup() {{
        Serial.begin(115200);
        pinMode(PIN_RELE, OUTPUT);
        WiFi.begin("SSID", "PASS");
        server.on("/rele/on", handleReleOn);
        server.on("/rele/off", handleReleOff);
        server.on("/temperatura", handleTemperatura);
        server.begin();
      }}
      void loop() {{
        server.handleClient();
      }}

CREADOR DE DASHBOARDS WEB INTERACTIVOS (ESTILO CLAUDE ARTIFACTS):
- Cuando el Jefe te pida un Dashboard, visualizador, interfaz web o panel de control (para telemetría de sensores, control de motores, IoT o monitoreo):
  * Genera un archivo HTML completo y autocontenido en un bloque ```html ... ```.
  * Incluye CSS moderno integrado (tema oscuro futurista, tarjetas de telemetría con sombras, medidores, botones tácticos).
  * Incluye JavaScript interactivo (puedes usar CDN de Chart.js para gráficas en tiempo real, simulación de datos en vivo con setInterval, o controles que cambien valores).
  * Tu código HTML será renderizado inmediatamente en vivo en la pantalla del Jefe como un Artifact de Claude.

CREADOR DE DIAGRAMAS DE CIRCUITOS Y CONEXIONES (VISUAL SVG):
- Cuando el Jefe pida un DIAGRAMA DE CONEXIÓN, ESQUEMÁTICO o WIRING DIAGRAM de microcontroladores, sensores, motores o circuitos:
  * Genera un archivo HTML completo autocontenido en un bloque ```html ... ```.
  * SIGUE EXACTAMENTE ESTE SKELETON SVG — solo cambia los textos de pines y colores según el circuito pedido:

```html
<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<style>
body{{margin:0;background:#0f172a;font-family:'Courier New',monospace;color:#e2e8f0;display:flex;flex-direction:column;align-items:center;padding:20px}}
h1{{color:#38bdf8;font-size:1.2rem;letter-spacing:2px;margin-bottom:12px}}
table{{border-collapse:collapse;width:760px;margin-top:16px}}
th{{background:#1e3a5f;color:#38bdf8;padding:8px 14px;border:1px solid #334155}}
td{{padding:8px 14px;border:1px solid #334155;font-size:.85rem}}
.r{{background:rgba(239,68,68,.15);color:#ef4444}}
.g{{background:rgba(34,197,94,.15);color:#22c55e}}
.b{{background:rgba(59,130,246,.15);color:#3b82f6}}
.k{{background:rgba(107,114,128,.15);color:#9ca3af}}
.warn{{background:rgba(239,68,68,.1);border:1px solid #ef4444;border-radius:8px;padding:12px;margin-top:14px;color:#fca5a5;font-size:.82rem}}
</style></head><body>
<h1>DIAGRAMA: ESP32 ↔ HC-SR04</h1>
<svg width="760" height="400" viewBox="0 0 760 400" xmlns="http://www.w3.org/2000/svg">
  <rect width="760" height="400" fill="#0f172a" rx="8"/>
  <!-- COMPONENTE IZQUIERDO (ESP32) -->
  <rect x="30" y="70" width="190" height="280" rx="12" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
  <text x="125" y="94" text-anchor="middle" fill="#38bdf8" font-size="14" font-weight="bold">ESP32</text>
  <text x="125" y="110" text-anchor="middle" fill="#64748b" font-size="10">ESP-WROOM-32</text>
  <!-- Pines ESP32 en borde DERECHO x=220 -->
  <circle cx="220" cy="150" r="6" fill="#ef4444"/>
  <text x="212" y="147" text-anchor="end" fill="#e2e8f0" font-size="11">3V3</text>
  <circle cx="220" cy="200" r="6" fill="#22c55e"/>
  <text x="212" y="197" text-anchor="end" fill="#e2e8f0" font-size="11">GPIO5</text>
  <circle cx="220" cy="250" r="6" fill="#3b82f6"/>
  <text x="212" y="247" text-anchor="end" fill="#e2e8f0" font-size="11">GPIO18</text>
  <circle cx="220" cy="300" r="6" fill="#6b7280"/>
  <text x="212" y="297" text-anchor="end" fill="#e2e8f0" font-size="11">GND</text>
  <!-- COMPONENTE DERECHO (HC-SR04) -->
  <rect x="540" y="110" width="190" height="210" rx="12" fill="#14532d" stroke="#22c55e" stroke-width="2"/>
  <text x="635" y="134" text-anchor="middle" fill="#86efac" font-size="14" font-weight="bold">HC-SR04</text>
  <text x="635" y="150" text-anchor="middle" fill="#4ade80" font-size="10">ULTRASONICO</text>
  <!-- Pines HC-SR04 en borde IZQUIERDO x=540 -->
  <circle cx="540" cy="175" r="6" fill="#ef4444"/>
  <text x="548" y="172" fill="#e2e8f0" font-size="11">VCC</text>
  <circle cx="540" cy="215" r="6" fill="#22c55e"/>
  <text x="548" y="212" fill="#e2e8f0" font-size="11">TRIG</text>
  <circle cx="540" cy="255" r="6" fill="#3b82f6"/>
  <text x="548" y="252" fill="#e2e8f0" font-size="11">ECHO</text>
  <circle cx="540" cy="295" r="6" fill="#6b7280"/>
  <text x="548" y="292" fill="#e2e8f0" font-size="11">GND</text>
  <!-- CABLES horizontales: desde x=220 (ESP32 pines) hasta x=540 (HC-SR04 pines) -->
  <!-- REGLA: x1=220 siempre, x2=540 siempre. y1 y y2 se alinean al pin correcto -->
  <line x1="220" y1="150" x2="540" y2="175" stroke="#ef4444" stroke-width="3"/>
  <line x1="220" y1="200" x2="540" y2="215" stroke="#22c55e" stroke-width="3"/>
  <line x1="220" y1="250" x2="540" y2="255" stroke="#3b82f6" stroke-width="3"/>
  <line x1="220" y1="300" x2="540" y2="295" stroke="#6b7280" stroke-width="3"/>
  <!-- Etiquetas de cables en el centro x=380 -->
  <text x="380" y="142" text-anchor="middle" fill="#ef4444" font-size="10">3.3V</text>
  <text x="380" y="192" text-anchor="middle" fill="#22c55e" font-size="10">TRIG</text>
  <text x="380" y="242" text-anchor="middle" fill="#3b82f6" font-size="10">ECHO</text>
  <text x="380" y="285" text-anchor="middle" fill="#6b7280" font-size="10">GND</text>
</svg>
<table>
  <tr><th>ESP32</th><th>→</th><th>HC-SR04</th><th>Cable</th></tr>
  <tr class="r"><td>3V3</td><td>→</td><td>VCC</td><td>Rojo</td></tr>
  <tr class="g"><td>GPIO 5</td><td>→</td><td>TRIG</td><td>Verde</td></tr>
  <tr class="b"><td>GPIO 18</td><td>→</td><td>ECHO</td><td>Azul</td></tr>
  <tr class="k"><td>GND</td><td>→</td><td>GND</td><td>Negro</td></tr>
</table>
<div class="warn">⚠️ ECHO del HC-SR04 entrega 5V. Usa divisor de voltaje (10kΩ+20kΩ) para proteger GPIO18 del ESP32 (3.3V max).</div>
</body></html>
```

  * Para OTROS componentes (DHT11, L298N, BMP280, etc.): adapta los textos de pines, colores y tabla. Mantén SIEMPRE la misma estructura SVG con componente izquierdo x=30-220 y componente derecho x=540-730, cables de x=220 a x=540.
  * NUNCA pongas ambos componentes en el mismo bloque superpuesto.
  * El HTML debe funcionar standalone sin CDN externos.

LONGITUD DE RESPUESTA:
- Si el Jefe hace una pregunta conceptual corta (¿qué es X?, ¿cómo funciona Y?): responde directo en 2 a 4 oraciones.
- Si el Jefe pide CÓDIGO, PROYECTO, DASHBOARD o MATERIALES: despliega toda la solución técnica completa sin escatimar detalle ni recortar código.

MATEMÁTICAS, FÍSICA Y CÁLCULO TÉCNICO (ESTRUCTURA DE CUADERNO DE INGENIERÍA):
- Cuando el Jefe plantee un problema matemático, cálculo de física, integrales, derivadas, cinemática, torque o circuitos:
  * NUNCA escribas fórmulas enredadas en texto plano con barras diagonales "/" en una sola línea (ejemplo prohibido: "1/2*m*v^2" o "int_0^pi/2").
  * USA EXCLUSIVAMENTE bloques $$ ... $$ para fórmulas centradas (NUNCA uses \\[ o \\]). Ejemplo correcto:
    $$
    I = \\int_{{0}}^{{\\frac{{\\pi}}{{2}}}} \\ln(\\sin(x)) \\, dx
    $$
  * Para fórmulas inline cortas usa $ ... $ (NUNCA uses \\( o \\)). Ejemplo: la integral vale $-\\frac{{\\pi}}{{2}} \\ln(2)$.
  * REGLA INLINE OBLIGATORIA: Cuando menciones cualquier fórmula, símbolo, integral, fracción o valor dentro de una oración, SIEMPRE ponlo entre $ ... $. Ejemplos:
    - CORRECTO: "Utilizamos la identidad $\\int_{{0}}^{{\\pi}} \\ln(\\sin(x))\\,dx = -\\pi\\ln(2)$"
    - CORRECTO: "La función es simétrica en $[0, 2\\pi]$, por tanto $2I = -\\pi\\ln(2)$"
    - PROHIBIDO: "la integral de 0 a pi es -pi ln(2)" — texto plano matemático sin $ $
  * Usa fracciones verticales reales \\frac{{a}}{{b}}, integrales \\int_{{a}}^{{b}}, raíces \\sqrt{{x}}, derivadas \\frac{{df}}{{dx}} y símbolos griegos (\\pi, \\theta, \\omega).
  * Organiza la solución paso a paso con títulos claros exactamente igual que en un cuaderno de ingeniería:
    - ### Paso 1: Planteamiento y Datos
    - ### Paso 2: Fórmulas y Propiedades Aplicadas
    - ### Paso 3: Desarrollo Algebraico Paso a Paso
    - ### Paso 4: Sustitución Numérica
    - ### Resultado Final: Bloque $$ ... $$ centrado + conclusión en texto.
  * Muestra cada paso intermedio sin saltarte deducciones para que el Jefe pueda estudiar y verificar el procedimiento.
  * NUNCA des solo el resultado final sin desarrollo. Mínimo 4 pasos con deducciones algebraicas completas.

RADAR WEB Y FUENTES DE INTERNET:
- Si se te proporciona información de 'Radar web en tiempo real', PRIMERO verifica que los fragmentos web realmente hablen del tema que preguntó el Jefe.
- Si los fragmentos web no coinciden con la pregunta (por ejemplo, hablan de otro show, persona o tema distinto), IGNÓRALOS COMPLETAMENTE y responde desde tu propio conocimiento.
- NUNCA mezcles información de fuentes web irrelevantes con la pregunta real del Jefe.
- Si los datos web sí son relevantes, incorpóralos y cita siempre la fuente y el enlace web (URL) para que el Jefe pueda hacer clic y verificar la información.

"""

def obtener_prompt_template(personalidad: str = "isabella") -> str:
    if personalidad == "isabella":
        intro = """Eres ISABELLA, ingeniera mecatrónica y asistente táctica personal del sistema AUREX. Trabajas en el taller codo a codo con tu creador, a quien llamas respetuosamente Jefe. Eres experta en robótica, microcontroladores, ESP32, Arduino, sistemas de control, sensores y automatización."""
        
        cierre = """DIRECTIVAS DE IDENTIDAD Y RESPUESTA:
- Hablas como ISABELLA: profesional de ingeniería mecatrónica, ágil, entusiasta, cercana y resolutiva.
- Dirígete al usuario siempre como "Jefe". Nunca digas "Señor" ni "Jefe Samir".
- MANTÉN EL HILO: Recuerda qué sensores o componentes venían discutiendo en los mensajes anteriores.
- Si el Jefe saluda (ej: "hola", "cómo estás"), respóndele con cordialidad y disposición técnica inmediata.
- En consultas técnicas, ve directo al grano sin introducciones innecesarias.

Información de Referencia (úsala internamente, NO la copies en tu respuesta):
{context}

Conversación reciente:
{chat_history}

Pregunta del Jefe: {question}

ISABELLA:"""
    else:
        intro = """Eres AUREX, ingeniero mecatrónico senior y asistente táctico de taller con 20 años de experiencia. Trabajas con tu creador, a quien llamas respetuosamente Jefe. Eres experto en robótica, microcontroladores, ESP32, Arduino y sistemas embebidos."""
        
        cierre = """DIRECTIVAS DE IDENTIDAD Y RESPUESTA:
- Hablas como AUREX: ingeniero experimentado, práctico, analítico y profesional.
- Dirígete al usuario siempre como "Jefe". Nunca digas "Señor" ni "Jefe Samir".
- MANTÉN EL HILO: Recuerda qué sensores o componentes venían discutiendo en los mensajes anteriores.
- Si el Jefe saluda (ej: "hola", "cómo estás"), respóndele con cordialidad y disposición técnica inmediata.
- En consultas técnicas, ve directo al grano sin introducciones innecesarias.

Información de Referencia (úsala internamente, NO la copies en tu respuesta):
{context}

Conversación reciente:
{chat_history}

Pregunta del Jefe: {question}

AUREX:"""

    return intro + "\n\n" + CUERPO_REGLAS_INGENIERIA + "\n\n" + cierre

PROMPT_TEMPLATE = obtener_prompt_template("isabella")


# ─────────────────────────────────────────────────────────────
#  GESTIÓN DE PROTOCOLOS DE MEMORIA
# ─────────────────────────────────────────────────────────────
def cargar_registro():
    if os.path.exists(REGISTRO_FILE):
        try:
            with open(REGISTRO_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_registro(registro):
    with open(REGISTRO_FILE, "w", encoding="utf-8") as f:
        json.dump(registro, f, ensure_ascii=False, indent=2)

def cargar_documento(ruta: str):
    ext = Path(ruta).suffix.lower()
    try:
        if ext == ".pdf":
            return PyPDFLoader(ruta).load()
        elif ext == ".docx":
            return Docx2txtLoader(ruta).load()
        elif ext == ".txt":
            return TextLoader(ruta, encoding="utf-8").load()
    except Exception as e:
        st.error(f"Error al decodificar protocolo en {ruta}: {e}")
    return []

class MockEmbeddings:
    def embed_documents(self, texts): return [[0.0]*64 for _ in texts]
    def embed_query(self, text): return [0.0]*64

def obtener_vectorstore():
    try:
        # Intentar conectar con Ollama local
        import urllib.request
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=0.5) as r:
            if r.status == 200:
                embeddings = OllamaEmbeddings(model=EMBED_MODEL)
                return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    except Exception:
        pass
    # Fallback para Streamlit Cloud
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=MockEmbeddings())

def incorporar_conocimiento(archivos_subidos):
    registro = cargar_registro()
    existentes = [item["nombre"] for item in registro]

    nuevos_docs = []
    archivos_ok = []

    for archivo in archivos_subidos:
        nombre = archivo.name
        if nombre in existentes:
            continue

        ruta = os.path.join(DOCS_DIR, nombre)
        with open(ruta, "wb") as f:
            f.write(archivo.getbuffer())

        docs = cargar_documento(ruta)
        if docs:
            nuevos_docs.extend(docs)
            archivos_ok.append(nombre)

    if not nuevos_docs:
        return 0, "Jefe, estos archivos ya forman parte de mi núcleo de conocimiento o están corruptos."

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    fragmentos = splitter.split_documents(nuevos_docs)

    vs = obtener_vectorstore()
    
    tamano_lote = 25
    total_fragmentos = len(fragmentos)
    barra = st.progress(0, text="Asimilando páginas en el núcleo...")
    
    for i in range(0, total_fragmentos, tamano_lote):
        lote = fragmentos[i:i + tamano_lote]
        vs.add_documents(lote)
        progreso = min(1.0, (i + tamano_lote) / total_fragmentos)
        barra.progress(progreso, text=f"Asimilando: {min(i + tamano_lote, total_fragmentos)} de {total_fragmentos} fragmentos...")
    
    barra.empty()

    for nombre in archivos_ok:
        registro.append({
            "nombre": nombre,
            "fragmentos": len(fragmentos) // len(archivos_ok)
        })
    guardar_registro(registro)

    return len(archivos_ok), f"Protocolo completado, Jefe. {len(archivos_ok)} archivo(s) asimilados en el núcleo."

def configurar_red_neuronal(vectorstore, modelo_llm=LLM_MODEL, personalidad=None):
    if personalidad is None:
        try:
            _c = cargar_config_aurex()
            personalidad = _c.get("personalidad_activa", "isabella")
        except Exception:
            personalidad = "isabella"
    # Parámetros ajustados por modelo
    es_deepseek = "deepseek" in modelo_llm.lower()
    es_coder = "coder" in modelo_llm.lower()
    temp = 0.3 if es_deepseek else (0.1 if es_coder else 0.2)
    # Detección inteligente de entorno: Local (Ollama) vs Nube (Gemini / Groq)
    groq_key = ""
    gemini_key = ""
    try:
        groq_key = str(st.secrets.get("GROQ_API_KEY", "") or os.environ.get("GROQ_API_KEY", "")).strip().strip('"').strip("'")
        gemini_key = str(st.secrets.get("GEMINI_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")).strip().strip('"').strip("'")
    except Exception:
        pass

    usar_nube = bool(groq_key or gemini_key)
    if not usar_nube:
        try:
            import urllib.request
            req_ol = urllib.request.Request("http://127.0.0.1:11434/api/tags")
            with urllib.request.urlopen(req_ol, timeout=0.6) as r_ol:
                if r_ol.status != 200:
                    usar_nube = True
        except Exception:
            usar_nube = True

    if usar_nube and (gemini_key or groq_key):
        llm = GroqCloudLLM(api_key=groq_key or gemini_key, model_name="llama-3.3-70b-versatile")
    elif usar_nube:
        class AlertaSinClaveLLM(LLM):
            @property
            def _llm_type(self) -> str: return "alerta_sin_clave"
            def _call(self, prompt, **kwargs):
                return "Jefe, para habilitar la respuesta satelital en la nube agregue GEMINI_API_KEY en los Secrets de Streamlit."
        llm = AlertaSinClaveLLM()
    else:
        llm = OllamaLLM(
            model=modelo_llm,
            temperature=temp,
            num_predict=4096 if (es_deepseek or es_coder) else 3500,
            num_ctx=4096,  # 4096 optimizado para RTX 3050 (6GB VRAM)
            num_thread=6,
            repeat_penalty=1.15 if es_deepseek else 1.05,
            repeat_last_n=128,
        )
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )
    prompt = PromptTemplate(
        template=obtener_prompt_template(personalidad),
        input_variables=["context", "chat_history", "question"]
    )

    def formatear(docs):
        return "\n\n".join(f"[Documento: {os.path.basename(doc.metadata.get('source', 'Memoria'))}]\n{doc.page_content}" for doc in docs)

    def resolver_contexto(x):
        if "context" in x and x["context"]:
            return x["context"]
        pregunta_b = x["question"].lower()
        try:
            es_sobre_video = any(w in pregunta_b for w in ["video", "grabaci", "clase", "schmid", "pantalla", "profesor", "profe", "zoom"])
            docs = vectorstore.similarity_search(x["question"], k=6 if es_sobre_video else 4)
            
            # Si pregunta por un video o clase, priorizar fragmentos de archivos Video_
            if es_sobre_video:
                docs_vid = [d for d in docs if "video_" in d.metadata.get("source", "").lower()]
                docs_otros = [d for d in docs if "video_" not in d.metadata.get("source", "").lower()]
                docs = (docs_vid + docs_otros)[:5]
            
            resultado_contexto = formatear(docs) if docs else "Sin contexto previo."
            
            # Si hay un video activo en session_state, enriquecer el contexto con su resumen
            if es_sobre_video and "video_analizado" in st.session_state:
                v_act = st.session_state["video_analizado"]
                cabecera = f"=== PROTOCOLO DEL VIDEO ACTIVO: {v_act.get('nombre', 'Video')} ===\n{v_act.get('informe', '')[:2500]}\n\n=== FRAGMENTOS EN MEMORIA CHROMA ===\n"
                resultado_contexto = cabecera + resultado_contexto

            return resultado_contexto
        except Exception:
            return "Sin contexto previo."

    cadena = (
        {
            "context": resolver_contexto,
            "chat_history": lambda x: x.get("chat_history", "Sin mensajes previos."),
            "question": lambda x: x["question"]
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return cadena, retriever

# ─────────────────────────────────────────────────────────────
#  SÍNTESIS DE VOZ MASCULINA DE INGENIERO HUMANO (PABLO / JORGE)
# ─────────────────────────────────────────────────────────────
def normalizar_latex(texto: str) -> str:
    """Convierte delimitadores de LaTeX a formato KaTeX compatible con Streamlit ($$ y $).
    
    Estrategia robusta:
    1. Convierte bloques \\[...\\] → $$ ... $$
    2. Convierte inline \\(...\\) → $ ... $
    3. Detecta CUALQUIER línea con comandos LaTeX que no esté ya envuelta en $$ y la envuelve
    """
    if not texto:
        return ""

    # Paso 1: Convertir bloques \[ ... \] a $$ ... $$ (incluyendo multi-línea)
    t = re.sub(r'\\\[\s*\n?', '\n$$\n', texto)
    t = re.sub(r'\n?\s*\\\]', '\n$$\n', t)

    # Paso 2: Convertir inline \( ... \) a $ ... $
    t = re.sub(r'\\\(', '$', t)
    t = re.sub(r'\\\)', '$', t)

    # Paso 3: Comandos LaTeX que indican contenido matemático en una línea
    LATEX_CMDS = (
        r'\int', r'\frac', r'\sum', r'\prod', r'\sqrt', r'\lim',
        r'\ln', r'\log', r'\sin', r'\cos', r'\tan', r'\sec',
        r'\left', r'\right', r'\cdot', r'\times', r'\pi',
        r'\infty', r'\partial', r'\nabla', r'\Delta', r'\alpha',
        r'\beta', r'\gamma', r'\theta', r'\lambda', r'\sigma',
        r'\rightarrow', r'\Rightarrow', r'\leq', r'\geq',
        r'\approx', r'\equiv', r'\neq', r'\pm',
    )

    lineas_limpias = []
    en_bloque = False

    for linea in t.split('\n'):
        # Rastrear si estamos dentro de un bloque $$
        cuenta_dolar_doble = linea.count('$$')
        if cuenta_dolar_doble % 2 != 0:
            en_bloque = not en_bloque
            lineas_limpias.append(linea)
            continue

        l_strip = linea.strip()

        # Si ya tiene $$, $ o está en bloque → no tocar
        if en_bloque or l_strip.startswith('$$') or l_strip.endswith('$$'):
            lineas_limpias.append(linea)
            continue

        # Detectar si la línea contiene algún comando LaTeX
        tiene_latex = any(cmd in l_strip for cmd in LATEX_CMDS)

        # También detectar patrones típicos: ^{...} _{...} que son LaTeX
        if not tiene_latex:
            tiene_latex = bool(re.search(r'[\^_]\{', l_strip)) or bool(re.search(r'\\[a-zA-Z]+', l_strip))

        if tiene_latex and l_strip:
            # Verificar que no sea texto mixto — solo envolver si la línea es PRINCIPALMENTE fórmula
            # Quitar todos los comandos LaTeX y sus argumentos
            texto_sin_latex = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', l_strip)
            texto_sin_latex = re.sub(r'\\[a-zA-Z]+', '', texto_sin_latex)
            # Quitar símbolos matemáticos, números, operadores, espacios, variables comunes
            texto_sin_latex = re.sub(r'[\^_\{\}\(\)\[\]0-9\+\-\=\*\/\s\.\,\|\!\\]', '', texto_sin_latex)
            # Quitar variables matemáticas de una sola letra que son normales en fórmulas
            texto_sin_latex = re.sub(r'\b[a-zA-Z]\b', '', texto_sin_latex)
            # Si queda poco texto alfanumérico puro → es fórmula (umbral 12 para manejar "2I", "J=2I", etc.)
            if len(texto_sin_latex) <= 12:
                lineas_limpias.append(f"$$\n{l_strip}\n$$")
                continue

        lineas_limpias.append(linea)

    return '\n'.join(lineas_limpias)

def reproducir_audio_segundo_plano(texto_limpio: str, es_femenina: bool = None):
    """Reproduce la voz del asistente en segundo plano mediante Web Speech API."""
    if es_femenina is None:
        try:
            es_femenina = (cargar_config_aurex().get("personalidad_activa", "isabella") == "isabella")
        except Exception:
            es_femenina = True
    js_bool = "true" if es_femenina else "false"
    rate_val = "1.02" if es_femenina else "0.98"
    pitch_val = "1.15" if es_femenina else "0.80"
    limpio_escapado = json.dumps(texto_limpio)
    js_code = f"""
    <script>
    (function() {{
        const voiceText = {limpio_escapado};
        if (!('speechSynthesis' in window) || !voiceText) return;
        window.speechSynthesis.cancel();
        
        function obtenerVoz(esFemenina) {{
            const voces = window.speechSynthesis.getVoices();
            if (!voces || voces.length === 0) return null;
            if (esFemenina) {{
                let voz = voces.find(v => v.lang.startsWith('es') && (
                    v.name.includes('Sabina') || v.name.includes('Helena') || 
                    v.name.includes('Laura') || v.name.includes('Zira') || 
                    v.name.includes('Monica') || v.name.includes('Paulina') || 
                    v.name.includes('Jimena') || v.name.includes('Female')
                ));
                if (!voz) {{
                    voz = voces.find(v => v.lang.startsWith('es') && 
                        (v.name.includes('Google') || v.name.includes('Natural'))
                    );
                }}
                return voz || voces.find(v => v.lang.startsWith('es'));
            }} else {{
                let voz = voces.find(v => v.lang.startsWith('es') && (
                    v.name.includes('Pablo') || v.name.includes('Jorge') || 
                    v.name.includes('Álvaro') || v.name.includes('Alvaro') || 
                    v.name.includes('Raul') || v.name.includes('David') || v.name.includes('Male')
                ));
                if (!voz) {{
                    voz = voces.find(v => v.lang.startsWith('es') && 
                        !v.name.includes('Helena') && !v.name.includes('Laura') && 
                        !v.name.includes('Zira') && !v.name.includes('Sabina')
                    );
                }}
                return voz || voces.find(v => v.lang.startsWith('es'));
            }}
        }}

        const oraciones = voiceText.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [voiceText];
        let idx = 0;
        function hablar() {{
            if (idx >= oraciones.length) return;
            const c = oraciones[idx].trim();
            idx++;
            if (!c) {{ hablar(); return; }}
            const u = new SpeechSynthesisUtterance(c);
            const v = obtenerVoz({js_bool});
            if (v) u.voice = v;
            u.lang = 'es-ES';
            u.rate = {rate_val};
            u.pitch = {pitch_val};
            u.onend = hablar;
            u.onerror = hablar;
            window.speechSynthesis.speak(u);
        }}
        if (window.speechSynthesis.getVoices().length > 0) hablar();
        else window.speechSynthesis.onvoiceschanged = hablar;
    }})();
    </script>
    """
    st.components.v1.html(js_code, height=0, width=0)

def renderizar_streaming_con_voz(texto: str, element_id: str = "aurex-teleprompter", es_femenina: bool = None):
    if es_femenina is None:
        try:
            es_femenina = (cargar_config_aurex().get("personalidad_activa", "isabella") == "isabella")
        except Exception:
            es_femenina = True
    js_bool = "true" if es_femenina else "false"
    rate_val = "1.02" if es_femenina else "0.98"
    pitch_val = "1.15" if es_femenina else "0.80"
    # Extraer únicamente el texto explicativo para la voz
    texto_a_hablar = extraer_texto_hablado(texto)
    limpio = re.sub(r'[*_#`\[\]$\\]', '', texto_a_hablar)
    limpio = limpio.replace('"', ' ').replace("'", " ")
    limpio = " ".join(limpio.split())

    # Detectar si contiene matemáticas o fórmulas LaTeX (ampliado)
    MATH_SIGNALS = [
        "\\frac", "\\int", "$$", "\\[", "\\sin", "\\cos", "\\ln",
        "\\sum", "\\sqrt", "\\left", "\\right", "\\pi", "\\cdot",
        "\\partial", "\\infty", "\\alpha", "\\beta", "\\theta",
        "\\lim", "\\prod", "\\Delta", "\\nabla", "^{", "_{",
    ]
    es_matematica = any(sym in texto for sym in MATH_SIGNALS)
    
    if es_matematica:
        # Renderizado KaTeX matemático directo en Streamlit con fracciones reales verticales
        reproducir_audio_segundo_plano(limpio)
        st.markdown(normalizar_latex(texto))
        return

    # Texto para mostrar en el teleprompter
    texto_a_mostrar = texto_a_hablar if ("```" in texto) else texto
    texto_escapado = json.dumps(texto_a_mostrar)
    limpio_escapado = json.dumps(limpio)
    
    html_code = f"""
    <div id="{element_id}" style="
        background: #0f172a;
        color: #f1f5f9;
        padding: 18px 22px;
        border-radius: 18px 18px 18px 2px;
        margin: 12px 0;
        max-width: 85%;
        border-left: 3px solid #38bdf8;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        line-height: 1.65;
        font-size: 1.05rem;
        font-family: 'Rajdhani', sans-serif;
    ">
        <b>{"🌸 ISABELLA" if es_femenina else "🛠️ AUREX"}:</b><br>
        <span id="{element_id}-body"></span><span id="{element_id}-cursor" style="color:#38bdf8; animation: blink 0.8s infinite;">█</span>
    </div>

    <style>
    @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    </style>

    <script>
    (function() {{
        const fullText = {texto_escapado};
        const voiceText = {limpio_escapado};
        const bodyEl = document.getElementById("{element_id}-body");
        const cursorEl = document.getElementById("{element_id}-cursor");
        
        let charIndex = 0;
        const totalChars = fullText.length;
        
        function obtenerVozDinamica(esFemenina) {{
            const voces = window.speechSynthesis.getVoices();
            if (!voces || voces.length === 0) return null;
            if (esFemenina) {{
                let voz = voces.find(v => v.lang.startsWith('es') && (
                    v.name.includes('Sabina') || v.name.includes('Helena') || 
                    v.name.includes('Laura') || v.name.includes('Zira') || 
                    v.name.includes('Monica') || v.name.includes('Paulina') || 
                    v.name.includes('Jimena') || v.name.includes('Female')
                ));
                return voz || voces.find(v => v.lang.startsWith('es'));
            }} else {{
                let voz = voces.find(v => v.lang.startsWith('es') && (
                    v.name.includes('Pablo') || v.name.includes('Jorge') || 
                    v.name.includes('Álvaro') || v.name.includes('Alvaro') || 
                    v.name.includes('Raul') || v.name.includes('Male') || v.name.includes('David')
                ));
                if (!voz) {{
                    voz = voces.find(v => v.lang.startsWith('es') && 
                        !v.name.includes('Helena') && !v.name.includes('Laura') && 
                        !v.name.includes('Zira') && !v.name.includes('Monica') && !v.name.includes('Sabina')
                    );
                }}
                return voz || voces.find(v => v.lang.startsWith('es'));
            }}
        }}
        
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
            
            const oraciones = voiceText.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [voiceText];
            let oIdx = 0;
            
            function hablarSiguiente() {{
                if (oIdx >= oraciones.length) return;
                const chunk = oraciones[oIdx].trim();
                oIdx++;
                if (!chunk) {{ hablarSiguiente(); return; }}
                
                const utter = new SpeechSynthesisUtterance(chunk);
                const esFem = {js_bool};
                const voz = obtenerVozDinamica(esFem);
                if (voz) utter.voice = voz;
                utter.lang = 'es-ES';
                utter.rate = {rate_val};
                utter.pitch = {pitch_val};
                utter.onend = hablarSiguiente;
                utter.onerror = hablarSiguiente;
                window.speechSynthesis.speak(utter);
            }}
            
            if (window.speechSynthesis.getVoices().length > 0) {{
                hablarSiguiente();
            }} else {{
                window.speechSynthesis.onvoiceschanged = hablarSiguiente;
            }}
        }}
        
        const speed = Math.max(14, Math.min(28, 42000 / totalChars));
        function typeWriter() {{
            if (charIndex < totalChars) {{
                bodyEl.innerHTML = fullText.substring(0, charIndex + 1).replace(/\\n/g, '<br>');
                charIndex++;
                setTimeout(typeWriter, speed);
            }} else {{
                cursorEl.style.display = 'none';
            }}
        }}
        typeWriter();
    }})();
    </script>
    """
    st.components.v1.html(html_code, height=280, scrolling=True)

def hablar_espera_inmediata():
    """Aviso de audio al inicio con la misma voz masculina de hombre ingeniero."""
    js_espera = """
    <script>
    (function() {
        if (!('speechSynthesis' in window)) return;
        window.speechSynthesis.cancel();
        
        const frases = [
            "Entendido Jefe, dame un segundo que reviso los esquemas...",
            "Comprendido Jefe, analizando los circuitos en la memoria...",
            "Dame un instante Jefe, calculando la solución técnica..."
        ];
        const frase = frases[Math.floor(Math.random() * frases.length)];
        
        function ejecutarAviso() {
            const voces = window.speechSynthesis.getVoices();
            let voz = voces.find(v => v.lang.startsWith('es') && (
                v.name.includes('Pablo') || 
                v.name.includes('Jorge') || 
                v.name.includes('Álvaro') || 
                v.name.includes('Alvaro') || 
                v.name.includes('Raul') || 
                v.name.includes('Male') ||
                v.name.includes('David')
            ));
            if (!voz) {
                voz = voces.find(v => v.lang.startsWith('es') && 
                    !v.name.includes('Helena') && 
                    !v.name.includes('Laura') && 
                    !v.name.includes('Zira') && 
                    !v.name.includes('Monica') && 
                    !v.name.includes('Sabina')
                );
            }
            if (!voz) voz = voces.find(v => v.lang.startsWith('es'));
            
            const aviso = new SpeechSynthesisUtterance(frase);
            if (voz) aviso.voice = voz;
            aviso.lang = 'es-ES';
            aviso.rate = 0.98;
            aviso.pitch = 0.80;
            window.speechSynthesis.speak(aviso);
        }
        
        if (window.speechSynthesis.getVoices().length > 0) {
            ejecutarAviso();
        } else {
            window.speechSynthesis.onvoiceschanged = ejecutarAviso;
        }
    })();
    </script>
    """
    st.components.v1.html(js_espera, height=0)

# ─────────────────────────────────────────────────────────────
#  OÍDO TÁCTICO: WHISPER LOCAL 100% OFFLINE — DETECCIÓN DE SILENCIO
#  Habla cuando quieras, AUREX responde al detectar que terminaste.
# ─────────────────────────────────────────────────────────────
WHISPER_DISPONIBLE = False
try:
    from faster_whisper import WhisperModel
    import sounddevice as sd
    import numpy as np
    WHISPER_DISPONIBLE = True
except Exception:
    sd = None
    WHISPER_DISPONIBLE = False

@st.cache_resource(show_spinner=False)
@st.cache_resource(show_spinner=False)
def cargar_whisper_base():
    """Carga el modelo Whisper Base optimizado para videos largos."""
    try:
        from faster_whisper import WhisperModel
        return WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=6)
    except Exception:
        return None

def cargar_modelo_whisper():
    """Carga el modelo Whisper optimizado con 6 hilos CPU e int8 para máxima velocidad."""
    try:
        modelo = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=6)
        return modelo
    except Exception:
        return None

def _buscar_microfono_funcional():
    """
    Busca el mejor dispositivo de entrada disponible.
    Prueba todos los candidatos WDM-KS, mide RMS real y elige el de mayor señal.
    Devuelve (device_index, samplerate, channels) o None si no hay ninguno.
    """
    devs = sd.query_devices()
    candidatos = []

    for i, d in enumerate(devs):
        ch_in = d.get("max_input_channels", 0)
        if ch_in < 1:
            continue
        nombre = d.get("name", "").lower()
        hostapi = d.get("hostapi", -1)
        sr = int(d.get("default_samplerate", 48000))
        ch = min(2, ch_in)
        # Solo WDM-KS (hostapi 3) — el único que funciona en esta máquina
        if hostapi != 3:
            continue
        prioridad = 0
        if "mic" in nombre or "microf" in nombre:
            prioridad += 5
        if "realtek" in nombre:
            prioridad += 3
        if "array" in nombre or "varios" in nombre:
            prioridad += 2   # array/varios = micrófono integrado, válido
        if "mezcla" in nombre or "stereo" in nombre or "mix" in nombre:
            prioridad -= 5   # loopback de salida, no es micrófono real
        if "altavoz" in nombre or "output" in nombre or "speaker" in nombre:
            prioridad -= 10  # salida de audio, descartar
        candidatos.append((prioridad, i, sr, ch))

    # Ordenar de mayor a menor prioridad
    candidatos.sort(key=lambda x: -x[0])

    mejores = []  # (rms, idx, sr, ch)
    for _, idx, sr, ch in candidatos:
        try:
            datos = sd.rec(int(sr * 0.5), samplerate=sr, channels=ch, dtype="float32", device=idx)
            sd.wait()
            mono = np.mean(datos, axis=1) if datos.ndim > 1 else datos.flatten()
            rms = float(np.sqrt(np.mean(mono ** 2)))
            mejores.append((rms, idx, sr, ch))
        except Exception:
            continue

    if not mejores:
        return None

    # Elegir el de mayor RMS (más señal de audio real)
    mejores.sort(key=lambda x: -x[0])
    _, idx, sr, ch = mejores[0]
    return (idx, sr, ch)


def grabar_y_transcribir(segundos: int = 4) -> str:
    """Graba con el mejor micrófono disponible (auto-detección WDM-KS) y transcribe con Whisper offline."""
    import wave

    # ── 1. Parar cualquier stream anterior ──
    try:
        sd.stop()
    except Exception:
        pass

    # ── 2. Auto-detectar el micrófono que funciona ──
    mic = _buscar_microfono_funcional()
    if mic is None:
        return "[ERROR MIC: No se pudo acceder a ningún micrófono activo. Verifique la conexión en Windows.]"

    MIC_DEVICE, sr_nat, ch = mic

    # ── 3. Grabar a la frecuencia nativa del hardware ──
    try:
        audio = sd.rec(
            int(segundos * sr_nat),
            samplerate=sr_nat,
            channels=ch,
            dtype="float32",
            device=MIC_DEVICE
        )
        sd.wait()
    except Exception as e:
        return f"[ERROR MIC: {e}]"

    # ── 4. Convertir a mono ──
    if audio.ndim > 1 and audio.shape[1] > 1:
        audio_mono = np.mean(audio, axis=1)
    else:
        audio_mono = audio.flatten()

    # ── 5. Verificar RMS — si no hay voz, no molestar a Whisper ──
    rms = float(np.sqrt(np.mean(audio_mono ** 2)))
    if rms < 0.00005:
        return "[ERROR MIC: No se detectó voz. Hable más cerca del micrófono, Jefe.]"

    # ── 6. Resamplear a 16 000 Hz para Whisper (decimación simple) ──
    WHISPER_RATE = 16000
    if sr_nat != WHISPER_RATE and sr_nat > WHISPER_RATE:
        ratio = sr_nat // WHISPER_RATE
        n = len(audio_mono) - (len(audio_mono) % ratio)
        audio_16k = np.mean(audio_mono[:n].reshape(-1, ratio), axis=1)
    else:
        audio_16k = audio_mono

    # ── 7. Guardar WAV temporal ──
    muestras = (audio_16k * 32767).astype("int16")
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        ruta_tmp = tmp.name
    with wave.open(ruta_tmp, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(WHISPER_RATE)
        wf.writeframes(muestras.tobytes())

    # ── 8. Transcribir con Whisper ──
    modelo = cargar_modelo_whisper()
    if modelo is None:
        return ""

    segmentos, _ = modelo.transcribe(
        ruta_tmp,
        language="es",
        beam_size=1,
        initial_prompt="AUREX, mecatrónica, ingeniería, robótica, circuitos, actuadores, sensores, Arduino, brazo robótico, diseño, PLC, Ohm, voltaje, corriente, resistencia, potencia, frecuencia, torque, PID, CAD, SolidWorks."
    )
    texto = " ".join(s.text for s in segmentos).strip()

    try:
        os.remove(ruta_tmp)
    except Exception:
        pass

    # ── 9. Descartar alucinaciones de silencio ──
    if "http" in texto.lower() or "www." in texto.lower():
        return "[ERROR MIC: Transmisión confusa. Repita su pregunta con voz clara, Jefe.]"

    return texto


def renderizar_microfono_aurex():
    """Botón de micrófono Whisper local. Sin internet. Sin Google."""
    if not WHISPER_DISPONIBLE:
        st.warning(
            "🎙️ **Oído Táctico offline no disponible.** "
            "Instale los módulos con: `pip install faster-whisper sounddevice`"
        )
        return

    st.markdown("""
    <div style="
        background: #0d1527;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 12px 18px;
        margin: 4px 0 8px 0;
        display: flex;
        align-items: center;
        gap: 14px;
    ">
        <span style="font-size:1.6rem;">🎙️</span>
        <div>
            <div style="font-weight:bold; color:#38bdf8; font-size:0.95rem;">
                OÍDO TÁCTICO OFFLINE · WHISPER LOCAL
            </div>
            <div style="font-size:0.8rem; color:#94a3b8;">
                Seleccione duración, pulse el botón y hable con claridad — 100% privado y sin internet
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn, col_seg, col_estado = st.columns([2, 1, 3])

    with col_seg:
        segundos = st.selectbox(
            "⏱️ Duración",
            [3, 4, 6, 8, 10],
            index=1,
            key="mic_segundos",
            label_visibility="collapsed"
        )

    with col_btn:
        grabar = st.button(
            "🎙️ Pulsar y Hablar",
            use_container_width=True,
            key="btn_whisper_mic",
            type="primary"
        )

    if grabar:
        with col_estado:
            st.markdown(
                f"<div style='color:#ef4444; font-weight:bold; padding-top:6px;'>"
                f"🔴 GRABANDO {segundos}s… HABLE AHORA</div>",
                unsafe_allow_html=True
            )
        with st.spinner(f"🎙️ Grabando {segundos} segundos de audio…"):
            texto_mic = grabar_y_transcribir(segundos)

        if texto_mic and not texto_mic.startswith("[ERROR"):
            st.session_state["orden_por_voz"] = texto_mic
            st.success(f"✅ Captado: **\"{texto_mic}\"**")
            st.rerun()
        elif texto_mic.startswith("[ERROR"):
            st.error(f"⚠️ Falla en el oído táctico: {texto_mic}")
        else:
            st.warning("⚠️ No se detectó audio claro. Intente de nuevo, Jefe.")

# ─────────────────────────────────────────────────────────────
#  MÓDULO DE VISIÓN TÁCTICA (QWEN 2.5 VL)
# ─────────────────────────────────────────────────────────────
def analizar_imagen_aurex(imagen_bytes, pregunta_usuario):
    prompt_vision = f"""Eres AUREX, asistente técnico personal y compañero de laboratorio del Jefe (Ingeniero Mecatrónico Hombre Senior).
El Jefe te ha presentado esta imagen (puede ser un diagrama técnico, circuito, plano, esquema de un libro o componente físico).

INSTRUCCIONES:
1. Dirígete a él SIEMPRE ÚNICAMENTE como "Jefe". NUNCA digas "Señor" ni "Jefe Samir". Solo "Jefe".
2. Analiza con máxima agudeza visual cada detalle: flechas, etiquetas de texto, componentes, conexiones, números, flujo y valores.
3. Explica como un ingeniero hombre en el taller: qué hace el circuito, cómo fluye la corriente o el mecanismo, y advierte si ves algún error práctico.
4. Responde con calidez, cercanía y tono profesional seguro. Concluye completamente tus frases.

Pregunta del Jefe: {pregunta_usuario}

Análisis técnico visual:"""

    try:
        respuesta = ollama.chat(
            model=VISION_MODEL,
            messages=[{
                'role': 'user',
                'content': prompt_vision,
                'images': [imagen_bytes]
            }]
        )
        return respuesta['message']['content']
    except Exception as e:
        return f"Jefe, parece que hubo una interferencia en los sensores ópticos: {e}"

# ─────────────────────────────────────────────────────────────
#  INTERFAZ STARK INDUSTRIES / PROTOCOLO AUREX
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AUREX · Sistema Táctico Personal",
    page_icon="💠",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0a1128 0%, #020617 100%);
        color: #e2e8f0;
        font-family: 'Rajdhani', sans-serif;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #030712;
        border-right: 1px solid #1e293b;
    }
    
    .aurex-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        letter-spacing: 4px;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        margin-bottom: 0px;
    }
    
    .aurex-sub {
        font-size: 0.85rem;
        color: #94a3b8;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }
    
    .reactor-core {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #38bdf8;
        border-radius: 50%;
        box-shadow: 0 0 12px #38bdf8, 0 0 24px #38bdf8;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.85); }
    }
    
    .chat-user {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
        color: #ffffff;
        padding: 14px 20px;
        border-radius: 18px 18px 2px 18px;
        margin: 12px 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.25);
        font-size: 1.05rem;
    }
    
    .chat-aurex {
        background: #0f172a;
        color: #f1f5f9;
        padding: 18px 22px;
        border-radius: 18px 18px 18px 2px;
        margin: 12px 0;
        max-width: 85%;
        border-left: 3px solid #38bdf8;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        line-height: 1.65;
        font-size: 1.05rem;
    }
    
    .doc-pill {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-left: 3px solid #38bdf8;
        padding: 8px 12px;
        margin: 6px 0;
        border-radius: 6px;
        font-size: 0.9rem;
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  INICIALIZACIÓN DEL SISTEMA
# ─────────────────────────────────────────────────────────────
if "vectorstore" not in st.session_state:
    try:
        vs = obtener_vectorstore()
        st.session_state.vectorstore = vs
        _cfg = cargar_config_aurex()
        _mod = _cfg.get("cerebro_activo", "llama3.2:latest")
        if _mod == "auto":
            _mod = "llama3.2:latest"
        cadena, retriever = configurar_red_neuronal(vs, modelo_llm=_mod)
        st.session_state.cadena = cadena
        st.session_state.retriever = retriever
    except Exception as e:
        st.error(f"Falla en la inicialización de AUREX: {e}")

if "historial" not in st.session_state:
    st.session_state.historial = []

if "ultimo_streaming" not in st.session_state:
    st.session_state.ultimo_streaming = None

registro_actual = cargar_registro()

# ── SIDEBAR (CONSOLA TÁCTICA) ───────────────
config_global = cargar_config_aurex()

with st.sidebar:
    pers_actual = config_global.get("personalidad_activa", "isabella")
    if pers_actual == "isabella":
        st.markdown('<div class="aurex-title" style="background: linear-gradient(135deg, #f472b6, #ec4899, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">ISABELLA</div>', unsafe_allow_html=True)
        st.markdown('<div class="aurex-sub" style="color: #fbcfe8;">🌸 NÚCLEO: ASISTENTE TÁCTICA & EJECUTIVA (FEMENINO)</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="aurex-title">AUREX</div>', unsafe_allow_html=True)
        st.markdown('<div class="aurex-sub">🛠️ NÚCLEO: INGENIERO SENIOR (MASCULINO HUMANO)</div>', unsafe_allow_html=True)
        
    st.markdown('<p><span class="reactor-core"></span><b>ESTADO:</b> EN LÍNEA · <b>USUARIO:</b> JEFE</p>', unsafe_allow_html=True)

    # ── SELECTOR DE PERSONALIDAD / NÚCLEO (UN CLIC) ──
    opciones_personalidad = {
        "🌸 Isabella (Asistente Táctica & Cálida)": "isabella",
        "🛠️ AUREX (Ingeniero Mecatrónico Senior)": "aurex"
    }
    idx_pers = 0 if pers_actual == "isabella" else 1
    pers_sel_label = st.selectbox(
        "🎭 PERSONALIDAD / IDENTIDAD",
        options=list(opciones_personalidad.keys()),
        index=idx_pers,
        help="Alterna al instante entre Isabella (voz femenina, cálida) y AUREX (ingeniero senior masculino)."
    )
    pers_elegida = opciones_personalidad[pers_sel_label]
    if pers_elegida != pers_actual:
        config_global["personalidad_activa"] = pers_elegida
        guardar_config_aurex(config_global)
        if "vectorstore" in st.session_state:
            _mod_actual = config_global.get("cerebro_activo", "llama3.2:latest")
            if _mod_actual == "auto":
                _mod_actual = "llama3.2:latest"
            try:
                st.session_state.cadena, st.session_state.retriever = configurar_red_neuronal(
                    st.session_state.vectorstore, modelo_llm=_mod_actual, personalidad=pers_elegida
                )
            except Exception:
                pass
        st.rerun()

    st.markdown('<hr style="border-color: #1e293b; margin: 12px 0;">', unsafe_allow_html=True)

# ── SELECTOR DE NÚCLEO CEREBRAL ──
    opciones_cerebro = {
        "⚡ Automático Inteligente (Triage: LLaMA + DeepSeek + Qwen Coder)": "auto",
        "💻 Qwen 2.5 Coder (Local · Monstruo de Software y ESP32)": "qwen2.5-coder:7b",
        "🧠 DeepSeek R1 (Local · Razonamiento Profundo y Matemáticas)": "deepseek-r1:7b",
        "⚡ Llama 3.2 (Local · Rápido y Balanceado)": "llama3.2:latest"
    }
    
    cerebro_guardado = config_global.get("cerebro_activo", "auto")
    if cerebro_guardado not in opciones_cerebro.values():
        cerebro_guardado = "auto"

    indice_defecto = 0
    for idx, (label, val) in enumerate(opciones_cerebro.items()):
        if val == cerebro_guardado:
            indice_defecto = idx
            break

    cerebro_seleccionado_label = st.selectbox(
        "🧠 CEREBRO ACTIVO (100% LOCAL)",
        options=list(opciones_cerebro.keys()),
        index=indice_defecto,
        help="Automático enruta problemas complejos a DeepSeek y charla rápida a LLaMA."
    )
    cerebro_id = opciones_cerebro[cerebro_seleccionado_label]
    
    # Si cambió de cerebro, actualizar configuración
    if cerebro_id != config_global.get("cerebro_activo"):
        config_global["cerebro_activo"] = cerebro_id
        guardar_config_aurex(config_global)
        if cerebro_id != "auto" and "vectorstore" in st.session_state:
            try:
                st.session_state.cadena, st.session_state.retriever = configurar_red_neuronal(
                    st.session_state.vectorstore, modelo_llm=cerebro_id
                )
            except Exception:
                pass
        st.rerun()

    st.markdown(f'<p style="font-size:0.85rem; color:#38bdf8;">👁️ <b>ÓPTICA ACTIVA:</b> <code>{VISION_MODEL}</code> (Local)</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.85rem; color:#22c55e;">🎙️ <b>OÍDO TÁCTICO:</b> MICRÓFONO ACTIVO</p>', unsafe_allow_html=True)

    # ── TELEMETRÍA DEL HARDWARE DE WINDOWS EN VIVO ──
    try:
        telemetria = obtener_telemetria_sistema()
        st.markdown("""
        <div style="background:#091224; border:1px solid #1e293b; border-left:3px solid #38bdf8; border-radius:8px; padding:10px; margin:10px 0;">
            <div style="font-size:0.75rem; color:#38bdf8; font-weight:bold; letter-spacing:1px; margin-bottom:6px;">
                ⚡ TELEMETRÍA DE LA NAVE (PC)
            </div>
        """, unsafe_allow_html=True)
        
        col_c, col_r = st.columns(2)
        with col_c:
            st.metric("CPU", f"{telemetria['cpu_pct']}%")
        with col_r:
            st.metric("RAM", f"{telemetria['ram_pct']}%", f"{telemetria['ram_usada_gb']}GB")
            
        if telemetria["es_laptop"]:
            icono_bat = "🔌" if telemetria["cargando"] else "🔋"
            st.caption(f"{icono_bat} Batería: **{telemetria['bateria_pct']}%** {'(Cargando)' if telemetria['cargando'] else '(Batería)'}")
        st.caption(f"💾 Disco C: **{telemetria['disco_libre_gb']} GB** libres")
        st.markdown("</div>", unsafe_allow_html=True)
    except Exception:
        pass

    # ── RADAR DE BÚSQUEDA WEB EN TIEMPO REAL ──
    st.markdown('<p style="font-size:0.85rem; color:#38bdf8; margin-top:8px;">🛰️ <b>RADAR WEB:</b> ONLINE (DuckDuckGo)</p>', unsafe_allow_html=True)
    forzar_busqueda = st.toggle("🌐 Consultar Internet siempre", value=False, help="Activa el radar web en cada mensaje incluso si hay libros en memoria.")
    st.session_state["forzar_web"] = forzar_busqueda

    st.divider()
    
    st.subheader("📡 Protocolo de Ingesta")
    st.caption("Cargue documentos o libros para alimentar el banco de memoria.")
    archivos = st.file_uploader(
        "Archivos (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if archivos:
        if st.button("⚡ Asimilar Conocimiento", use_container_width=True, type="primary"):
            with st.spinner("AUREX sincronizando datos con el núcleo central..."):
                n, msg = incorporar_conocimiento(archivos)
                vs = obtener_vectorstore()
                st.session_state.vectorstore = vs
                cadena, retriever = configurar_red_neuronal(vs)
                st.session_state.cadena = cadena
                st.session_state.retriever = retriever
                st.success(msg)
                st.rerun()

    st.divider()

    st.subheader(f"🗄️ Bancos de Datos ({len(registro_actual)})")
    if registro_actual:
        for item in registro_actual:
            st.markdown(f'<div class="doc-pill">🔹 {item["nombre"]}</div>', unsafe_allow_html=True)
    else:
        st.caption("Memoria a la espera de sus órdenes, Jefe.")

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔒 Bloquear Terminal", use_container_width=True):
            st.session_state["autenticado_jefe"] = False
            st.rerun()
        if st.button("🧹 Purgar Chat", use_container_width=True):
            st.session_state.historial = []
            st.session_state.ultimo_streaming = None
            st.rerun()
    with col2:
        if st.button("⚠️ Reiniciar", use_container_width=True, help="Formatea toda la base de datos"):
            import shutil
            if os.path.exists(CHROMA_DIR):
                shutil.rmtree(CHROMA_DIR)
            if os.path.exists(REGISTRO_FILE):
                os.remove(REGISTRO_FILE)
            st.session_state.clear()
            st.rerun()

    st.divider()
    with st.sidebar.expander("🛡️ Auditoría Forense y Reportes Policiales"):
        from escudo_seguridad import renderizar_panel_ciberdefensa_policial
        renderizar_panel_ciberdefensa_policial()

# ── CERROJO TÁCTICO DE SEGURIDAD DEL JEFE ───
from escudo_seguridad import renderizar_pantalla_seguridad, detectar_prompt_injection, leer_auditoria_seguridad
if not renderizar_pantalla_seguridad():
    st.stop()

# ── PANELES PRINCIPALES: PESTAÑAS ───────────
st.markdown('<div class="aurex-title">AUREX TACTICAL INTERFACE</div>', unsafe_allow_html=True)

tab_memoria, tab_autonomo, tab_imagenes, tab_gemelo_3d, tab_vision = st.tabs([
    "💬 Taller Táctico & Chat",
    "⚡ Agente Autónomo (Antigravity Mode)",
    "📸 Generador de Imágenes de Sensores",
    "🦾 Gemelo Digital (Físico + 3D)",
    "👁️ Visor Óptico & Video"
])

# ═════════════════════════════════════════════════════════════
#  PESTAÑA 1: MEMORIA DE LIBROS Y TEXTO (LLAMA 3.2)
# ═════════════════════════════════════════════════════════════
with tab_memoria:
    if registro_actual:
        st.caption(f"🛡️ Bancos enlazados con **{len(registro_actual)} archivo(s)**. A sus órdenes, Jefe.")
    else:
        st.info("👈 **AUREX está en línea.** Alimente sus protocolos con libros o manuales en la consola lateral izquierda.")

    historial_a_mostrar = st.session_state.historial
    if st.session_state.ultimo_streaming and len(historial_a_mostrar) > 0 and historial_a_mostrar[-1]["rol"] == "ia":
        historial_estatico = historial_a_mostrar[:-1]
        mensaje_en_vivo = historial_a_mostrar[-1]
    else:
        historial_estatico = historial_a_mostrar
        mensaje_en_vivo = None

    for idx_msg, msg in enumerate(historial_estatico):
        if msg["rol"] == "usuario":
            st.markdown(f'<div class="chat-user"><b>Usted:</b><br>{msg["texto"]}</div>', unsafe_allow_html=True)
        else:
            _nombre_asistente = "🌸 ISABELLA" if config_global.get("personalidad_activa", "isabella") == "isabella" else "🛠️ AUREX"
            st.markdown(f'<div class="chat-aurex"><b>{_nombre_asistente}:</b></div>', unsafe_allow_html=True)
            st.markdown(normalizar_latex(msg["texto"]))
            renderizar_artifacts_interactivos(msg["texto"], element_key_prefix=f"hist_{idx_msg}")
            
            if msg.get("fuentes") or msg.get("fuentes_web"):
                with st.expander("🔍 Telemetría y Fuentes Verificadas"):
                    # Fuentes Web en vivo
                    if msg.get("fuentes_web"):
                        st.markdown("**🛰️ Fuentes Web en Tiempo Real:**")
                        for fw in msg["fuentes_web"]:
                            st.markdown(f"• 🔗 [{fw['titulo']}]({fw['url']})")
                            st.caption(f"_{fw['snippet'][:220]}..._")
                        st.divider()
                    # Fuentes Locales de libros
                    if msg.get("fuentes"):
                        st.markdown("**📚 Bancos de Memoria Locales:**")
                        for i, doc in enumerate(msg["fuentes"], 1):
                            src = doc.metadata.get("source", "Banco Central")
                            pag = doc.metadata.get("page", "")
                            lbl = f"Registro {i}: {Path(src).name}"
                            if pag != "":
                                lbl += f" · Pág {int(pag)+1}"
                            st.caption(lbl)
                            st.text(doc.page_content[:260] + "...")

    if mensaje_en_vivo:
        renderizar_streaming_con_voz(mensaje_en_vivo["texto"])
        renderizar_artifacts_interactivos(mensaje_en_vivo["texto"], element_key_prefix="live_art")
        st.session_state.ultimo_streaming = None
        if mensaje_en_vivo.get("fuentes") or mensaje_en_vivo.get("fuentes_web"):
            with st.expander("🔍 Telemetría y Fuentes Verificadas"):
                if mensaje_en_vivo.get("fuentes_web"):
                    st.markdown("**🛰️ Fuentes Web en Tiempo Real:**")
                    for fw in mensaje_en_vivo["fuentes_web"]:
                        st.markdown(f"• 🔗 [{fw['titulo']}]({fw['url']})")
                        st.caption(f"_{fw['snippet'][:220]}..._")
                    st.divider()
                if mensaje_en_vivo.get("fuentes"):
                    st.markdown("**📚 Bancos de Memoria Locales:**")
                    for i, doc in enumerate(mensaje_en_vivo["fuentes"], 1):
                        src = doc.metadata.get("source", "Banco Central")
                        pag = doc.metadata.get("page", "")
                        lbl = f"Registro {i}: {Path(src).name}"
                        if pag != "":
                            lbl += f" · Pág {int(pag)+1}"
                        st.caption(lbl)
                        st.text(doc.page_content[:260] + "...")

    # OÍDO TÁCTICO OFFLINE — WHISPER LOCAL
    renderizar_microfono_aurex()

    # Recoger orden capturada por el micrófono Whisper
    if "orden_por_voz" in st.session_state and st.session_state["orden_por_voz"]:
        orden = st.session_state.pop("orden_por_voz")
    else:
        # Entrada de órdenes por teclado
        orden = st.chat_input("Hable por el micrófono o dicte su instrucción, Jefe...")

    if orden:
        # 0. EVALUAR AMENAZAS Y PROMPT INJECTION CON EL ESCUDO DE SEGURIDAD
        es_ataque, motivo = detectar_prompt_injection(orden)
        if es_ataque:
            st.session_state["alerta_intrusion_activa"] = True
            st.session_state.historial.append({"rol": "usuario", "texto": orden})
            st.session_state.historial.append({
                "rol": "ia",
                "texto": f"🚨 **ALERTA DE SEGURIDAD TÁCTICA AUREX:** Se ha interceptado y neutralizado una amenaza ({motivo}). Intento bloqueado y registrado en la auditoría forense.",
                "fuentes": [],
                "fuentes_web": []
            })
            st.rerun()

        hablar_espera_inmediata()
        st.session_state.historial.append({"rol": "usuario", "texto": orden})

        # ── 0.5. EVALUAR ÓRDENES DE CIBERDEFENSA TÁCTICA INALÁMBRICA / REMOTA ──
        try:
            from intervencion_autonoma import procesar_comando_tactico_ciberdefensa
            es_cmd_def, resp_def = procesar_comando_tactico_ciberdefensa(orden)
            if es_cmd_def:
                st.session_state.historial.append({
                    "rol": "ia",
                    "texto": resp_def,
                    "fuentes": []
                })
                st.session_state.ultimo_streaming = resp_def
                st.rerun()
        except Exception:
            pass

        # ── 1. EVALUAR COMANDOS TÁCTICOS DE CONTROL DE PC (J.A.R.V.I.S.) ──
        es_cmd_pc, respuesta_pc = detectar_y_ejecutar_comando_pc(orden)
        if es_cmd_pc:
            st.session_state.historial.append({
                "rol": "ia",
                "texto": respuesta_pc,
                "fuentes": []
            })
            st.session_state.ultimo_streaming = respuesta_pc
            st.rerun()

        # ── 2. PROCESAR CON LA RED NEURONAL DE INGENIERÍA ──
        # Extraer los últimos intercambios previos para mantener el hilo
        mensajes_previos = []
        pers_actual_hist = config_global.get("personalidad_activa", "isabella")
        nombre_ia_hist = "Isabella" if pers_actual_hist == "isabella" else "AUREX"
        # Solo últimos 2 intercambios (4 mensajes max) para evitar que el modelo repita el historial
        for m in st.session_state.historial[:-1][-4:]:
            if m["rol"] == "usuario":
                # Truncar mensajes largos del historial a 120 chars para evitar que el modelo los copie
                texto_hist = m["texto"][:120] + "..." if len(m["texto"]) > 120 else m["texto"]
                mensajes_previos.append(f"<user>{texto_hist}</user>")
            else:
                texto_hist = m["texto"][:200] + "..." if len(m["texto"]) > 200 else m["texto"]
                mensajes_previos.append(f"<assistant>{texto_hist}</assistant>")
        contexto_charla = "\n".join(mensajes_previos) if mensajes_previos else "<sin_historial/>"

        with st.spinner("Jefe, estoy analizando la memoria..."):
            try:
                cadena    = st.session_state.cadena
                retriever = st.session_state.retriever

                # 1. Fast-Path Inteligente: Solo consultar Chroma si la orden pregunta por documentos subidos
                orden_l = orden.lower()
                necesita_rag = any(w in orden_l for w in [
                    "documento", "archivo", "pdf", "apunte", "en la clase", "en el video", 
                    "grabaci", "libro", "segun el", "según el", "que subí", "que subi", 
                    "pagina", "página", "manual", "datasheet", "video"
                ])
                if necesita_rag:
                    try:
                        fuentes = retriever.invoke(orden)
                    except Exception:
                        fuentes = []
                else:
                    fuentes = []

                # 2. Evaluar si se requiere Radar Web en tiempo real
                forzar_web = st.session_state.get("forzar_web", False)
                usar_web = forzar_web or necesita_busqueda_web(orden, fuentes)

                contexto_extra = ""
                fuentes_web = []

                if usar_web:
                    # ── Construir query enriquecida con contexto del historial ──
                    # Si el mensaje es corto o usa referencias vagas, agregar contexto previo
                    query_busqueda = orden
                    historial_reciente = st.session_state.historial[:-1][-3:]
                    if len(orden.split()) <= 8 and historial_reciente:
                        # Extraer palabras clave de los últimos mensajes del usuario
                        palabras_clave = []
                        for m in reversed(historial_reciente):
                            if m["rol"] == "usuario":
                                texto_previo = m["texto"]
                                # Tomar máximo 6 palabras del último mensaje del usuario
                                palabras_clave = texto_previo.split()[:6]
                                break
                        if palabras_clave:
                            contexto_query = " ".join(palabras_clave)
                            # Combinar: contexto previo + pregunta actual
                            query_busqueda = f"{contexto_query} {orden}".strip()

                    with st.spinner("🛰️ Radar web activo — escaneando fuentes en tiempo real..."):
                        try:
                            resultados_web = buscar_en_web(query_busqueda, max_resultados=4)
                        except Exception:
                            resultados_web = []

                        if resultados_web:
                            contexto_web_str, fuentes_web = formatear_contexto_web(resultados_web)
                            contexto_local_str = "\n\n".join(doc.page_content for doc in fuentes) if fuentes else ""
                            contexto_extra = f"{contexto_local_str}\n\n{contexto_web_str}".strip()
                        else:
                            # Sin resultados web: usar solo contexto local si existe
                            if fuentes:
                                contexto_extra = "\n\n".join(doc.page_content for doc in fuentes)

                # 3. Invocar a la red neuronal local con memoria y datos web
                cerebro_actual = config_global.get("cerebro_activo", "auto")

                # Si está en modo Automático, triage de acuerdo a la especialidad
                modelo_a_usar = cerebro_actual
                if cerebro_actual == "auto":
                    orden_lower = orden.lower()
                    disparadores_codigo = [
                        "código", "codigo", "sketch", "c++", "cpp", "arduino", "esp32", "stm32",
                        "firmware", "programar", "programa", "función", "funcion", "librería", "libreria",
                        "servidor web", "html", "javascript", "python", "clase c++", "rust", "sql",
                        "plc", "ladder", "css", "script", "compilar", "bug", "depurar", "refactorizar",
                        "microcontrolador", "gpio", "i2c", "spi", "uart", "json", "endpoint",
                        "diagrama", "conexion", "conexión", "cableado", "wiring", "esquema",
                        "esquemático", "circuito", "pinout", "conectar", "sensor", "haz un diagrama"
                    ]
                    disparadores_razonamiento = [
                        "calcula", "calcular", "cálculo", "matemática", "ecuación", "fórmula",
                        "torque", "potencia", "pid", "cinemática", "matriz", "optimiza",
                        "deriva", "integral", "resistencia equivalente", "ley de kirchhoff",
                        "pwm frecuencia", "interrupción", "timer", "precisión", "demuestra",
                        "física", "termodinámica", "estática", "dinámica"
                    ]
                    # Fast-Triage Jarvis: Priorizar LLaMA 3.2 3B para respuestas instantáneas
                    quiere_codigo_completo = any(w in orden_lower for w in [
                        "escribe el código", "escribe el codigo", "dame el sketch", "genera el firmware", 
                        "código c++", "codigo c++", "sketch completo", "programa en c++", "escribe el script"
                    ])
                    quiere_razonamiento_pesado = any(w in orden_lower for w in [
                        "demuestra paso a paso", "deducción matemática", "calcula paso a paso la integral", 
                        "deriva analíticamente", "razona a fondo con deepseek"
                    ])
                    if quiere_codigo_completo:
                        modelo_a_usar = "qwen2.5-coder:7b"
                    elif quiere_razonamiento_pesado:
                        modelo_a_usar = "deepseek-r1:7b"
                    else:
                        modelo_a_usar = "llama3.2:latest"

                # Si el modelo a usar no coincide con la cadena actual, ajustar al vuelo
                cadena_a_usar = cadena
                if modelo_a_usar != LLM_MODEL:
                    try:
                        cadena_a_usar, _ = configurar_red_neuronal(st.session_state.vectorstore, modelo_llm=modelo_a_usar)
                    except Exception:
                        cadena_a_usar = cadena  # Fallback a LLaMA si DeepSeek no está descargado

                # Detectar si el usuario está haciendo una pregunta o consulta técnica
                orden_l = orden.lower()
                es_pregunta_o_consulta = any(q in orden_l for q in [
                    "?", "¿", "dime", "por que", "por qué", "como ", "cómo ", "cual", "cuál", 
                    "que ", "qué ", "cuanto", "cuánto", "calcula", "tolerancia", "ajuste", 
                    "recomiend", "explica", "analiza", "duda", "revis", "porqué", "cuántos", "cuantos",
                    "para que", "para qué", "sirve", "falla", "avería", "averia"
                ])

                # ── DETECCIÓN EXPLÍCITA DE IMÁGENES O FICHAS DE SENSORES ──
                es_peticion_imagenes_sensores = any(w in orden_l for w in [
                    "imagen", "imágenes", "imagenes", "foto", "fotos", "fichas", "ficha visual",
                    "ver los sensores", "ver esos", "enséñame", "enseñame", "muestra las fotos",
                    "muestra las imagenes", "muestra los sensores", "dame las imagenes", "dame las imágenes"
                ]) and any(w in orden_l for w in ["sensor", "sensores", "componente", "componentes", "modulo", "módulo", "dispositivo", "esos dos", "estos dos", "esos", "estos", "agua"])

                sensores_objetivo = []
                if es_peticion_imagenes_sensores:
                    sensores_objetivo = buscar_sensores_en_texto(orden)
                    if len(sensores_objetivo) < 2 and st.session_state.historial:
                        for m in reversed(st.session_state.historial):
                            if m.get("rol") in ["ia", "asistente"]:
                                s_hist = buscar_sensores_en_texto(m["texto"])
                                for sh in s_hist:
                                    if not any(so["nombre"] == sh["nombre"] for so in sensores_objetivo):
                                        sensores_objetivo.append(sh)
                                if sensores_objetivo:
                                    break

                # Detectar petición explícita de desplegar o abrir un diagrama / 3D
                es_peticion_diagrama = (es_peticion_imagenes_sensores and bool(sensores_objetivo)) or ((not es_pregunta_o_consulta) and any(k in orden_l for k in [
                    "diagrama", "conexion", "conexión", "cableado", "wiring", "esquema",
                    "esquemático", "circuito", "pinout", "conectar", "haz un diagrama",
                    "haz el diagrama", "muestra el diagrama", "visualiza", "anatomy",
                    "despiece", "isometric", "isométric", "mecanismo", "máquina", "maquina", "rig",
                    "holograma", "3d", "desarmar", "desensambl", "ensambl", "hiro", "stark",
                    "big hero", "pelicula", "película", "despliega", "desplegar", "gemelo digital", "twin", "vista 3d", "rayos x", "wireframe", "pon eso", "pon pieza",
                    "laboratorio", "desarme"
                ]))
                es_peticion_codigo = any(k in orden.lower() for k in [
                    "código", "codigo", "sketch", "c++", "cpp", "arduino", "firmware",
                    "programar", "programa", "script", "función", "funcion"
                ]) and not es_peticion_diagrama

                orden_efectiva = orden
                # Inyección táctica de telemetría si pregunta por componentes del actuador robótico 3D
                if any(p in orden_l for p in ["rodamiento", "608zz", "rotor", "estator", "engranaje", "planetario", "tolerancia", "holograma", "eje", "bobina"]):
                    orden_efectiva += """

(DIRECTIVA DE TELEMETRÍA TÉCNICA - ACTUADOR ROBÓTICO 3D:
Tienes en pantalla el Actuador Robótico Servo-Industrial con 8 piezas:
1. Rodamiento de Bolas Radial 608ZZ:
   - Medidas: Diámetro interior d=8 mm, exterior D=22 mm, espesor B=7 mm.
   - Material: Acero cromo 100Cr6, tolerancia de precisión ABEC-7, Carga máx 3,300 N.
   - TOLERANCIA DE AJUSTE DEL EJE RECOMENDADA: k5 (+1 µm a +7 µm). Es un ajuste con apriete o interferencia ligera para eje giratorio bajo carga dinámica, lo que evita por completo el deslizamiento y desgaste por frotamiento (fretting corrosion).
   - ¿Por qué NO g6?: g6 (-5 a -14 µm) es un ajuste con juego que patinaría inmediatamente bajo torque.
   - ¿Por qué NO h6?: h6 (0 a -9 µm) es deslizante/transición; si no se usa adhesivo anaeróbico Loctite 641, terminará aflojándose con las vibraciones.
   - Alojamiento exterior en la carcasa: H7 (0 a +15 µm).
2. Engranajes planetarios: Relación 1:4.8, acero 42CrMo4, módulo 0.8.
3. Rotor magnético Neodimio N52 con 14 polos permanentes.
4. Estator con 8 devanados de cobre clase H 180°C.
5. Tornillería M3 DIN 912 clase 12.9, torque 1.5 N·m.
Responde de forma técnica, empática, profesional y directa dirigiéndote siempre al usuario como 'Jefe'.)"""
                if es_peticion_diagrama and "```" not in orden:
                    orden_efectiva += """

(DIRECTIVA TÉCNICA - DIAGRAMA SVG OBLIGATORIO:
Debes generar EXCLUSIVAMENTE un bloque ```html ... ``` con un HTML completo autocontenido que dibuje el diagrama de conexión.
El HTML DEBE contener un SVG de 800x400 con:
- Componente IZQUIERDO (ej: ESP32) como rectángulo en x=30 a x=220, y=80 a y=320, fondo #1e3a5f, texto blanco
- Componente DERECHO (ej: sensor) como rectángulo en x=560 a x=750, y=120 a y=280, fondo #2d4a1e, texto blanco
- Pines del componente izquierdo como círculos en el BORDE DERECHO del bloque izquierdo (x=220)
- Pines del componente derecho como círculos en el BORDE IZQUIERDO del bloque derecho (x=560)
- Cables como líneas <line> que van de x=220 (pin izquierdo) hasta x=560 (pin derecho), con colores:
  rojo=VCC/3.3V/5V, negro=GND, verde=señal digital/TRIG, azul=datos/ECHO
- Etiquetas de texto para cada pin y cable
- Tabla de conexiones debajo del SVG
- Fondo oscuro #0f172a, estilo futurista
NUNCA respondas con texto plano o tabla sin SVG. SIEMPRE genera el bloque ```html completo.)"""

                elif es_peticion_codigo and "```" not in orden:
                    orden_efectiva += "\n\n(DIRECTIVA TÉCNICA: Debes escribir OBLIGATORIAMENTE el bloque de código C++ completo y funcional ```cpp ... ``` con todas sus librerías <WiFi.h>, <WebServer.h>, funciones setup() y loop(). No te limites solo a dar explicaciones o pasos)."

                payload = {"question": orden_efectiva, "chat_history": contexto_charla}
                if contexto_extra:
                    payload["context"] = contexto_extra

                try:
                    # En peticiones de diagramas o 3D, evaluamos directamente
                    if es_peticion_diagrama:
                        respuesta = ""
                    else:
                        # ── STREAMING EN TIEMPO REAL ESTILO J.A.R.V.I.S. ──
                        with st.chat_message("assistant"):
                            _nombre_asist = "🌸 ISABELLA" if config_global.get("personalidad_activa", "isabella") == "isabella" else "🛠️ AUREX"
                            st.markdown(f'<div class="chat-aurex"><b>{_nombre_asist}:</b></div>', unsafe_allow_html=True)
                            placeholder_stream = st.empty()
                            acumulado = []
                            for chunk in cadena_a_usar.stream(payload):
                                acumulado.append(chunk)
                                placeholder_stream.markdown("".join(acumulado) + " ▌")
                            
                            respuesta_bruta = "".join(acumulado)
                            # Limpiar trazas de DeepSeek y caracteres orientales
                            if "<think>" in respuesta_bruta:
                                respuesta_bruta = re.sub(r'<think>[\s\S]*?</think>', '', respuesta_bruta).strip()
                            respuesta = re.sub(r'[\u4e00-\u9fff]+', '', respuesta_bruta)
                            # Limpiar si el modelo envolvió toda la respuesta en un bloque de código
                            respuesta = re.sub(r'^```[\w]*\n', '', respuesta.strip())
                            respuesta = re.sub(r'\n```$', '', respuesta.strip())
                            placeholder_stream.markdown(normalizar_latex(respuesta))
                            renderizar_artifacts_interactivos(respuesta, element_key_prefix="stream_live")
                    
                    # ── DIAGRAMA ULTRA-REALISTA, ANATOMY O LABORATORIO HOLOGRÁFICO 3D ──
                    if es_peticion_diagrama:
                        orden_l = orden.lower()
                        es_holograma_3d = any(h in orden_l for h in ["holograma", "3d", "desarmar", "desensambl", "ensambl", "hiro", "stark", "big hero", "pelicula", "película", "rayos x", "wireframe", "pon eso", "pon pieza", "laboratorio", "desarme", "despliega", "desplegar", "muestra en 3", "mostrar en 3", "vista 3d", "gemelo digital", "twin"])
                        es_anatomy = any(a in orden_l for a in ["anatomy", "isometric", "isométric", "mecanismo", "rig", "calibraci", "banco", "máquina", "maquina"])
                        es_ultrasonico = any(u in orden_l for u in ["ultrason", "hc-sr04", "hcsr04", "distancia"]) or ("sensor" in orden_l and ("esp32" in orden_l or "esp-32" in orden_l))
                        
                        if es_holograma_3d:
                            import importlib
                            import plantillas.holograma_3d
                            importlib.reload(plantillas.holograma_3d)
                            from plantillas.holograma_3d import generar_laboratorio_holografico_3d
                            pers_act = config_global.get("personalidad_activa", "isabella")
                            nombre_ia = "Isabella" if pers_act == "isabella" else "AUREX"
                            es_modelo_brazo = any(b in orden_l for b in ["brazo", "arm", "articulad", "robotico", "robótico", "pinza", "gripper"])
                            modelo_ini = "brazo" if es_modelo_brazo else "actuador"
                            nombre_mecanismo = "Brazo Robótico Articulado 6-DOF con Pinza (Gripper)" if es_modelo_brazo else "Actuador Robótico Servo-Industrial"
                            respuesta = f"""¡Protocolo holográfico en línea, Jefe! He desplegado el **Laboratorio 3D Interactivo** del **{nombre_mecanismo}** estilo Hiro Hamada / Tony Stark:

{generar_laboratorio_holografico_3d(modelo_inicial=modelo_ini)}

### 🦾 Guía del Gemelo Digital (Objeto Físico Real ↔ Modelo 3D):
- **◫ Vista Dividida (Split Screen):** En la pantalla izquierda tienes el **Objeto Físico Real** montado en el banco de taller con materiales industriales PBR. En la derecha tienes el **Gemelo Digital 3D** desarmable.
- **🔄 Rotación Sincronizada 360°:** Arrastra con el ratón en cualquiera de los dos lados para rotar ambos objetos a la vez y comparar cada detalle físico con el diseño digital.
- **🎛️ Modos de Pantalla:** Puedes alternar con los botones superiores entre **◫ Físico + 3D**, **📷 Objeto Físico** a pantalla completa o **🌐 Modelo 3D**.
- **🔓 Desarmar / Explosión 3D:** Pulsa **Desarmar 3D** o mueve el slider para ver cómo el gemelo digital se separa en el aire mientras el objeto físico permanece armado como referencia visual.
- **🔍 Inspección Táctica:** Haz clic en cualquier pieza del 3D para ver su material, tolerancia y procedimiento de montaje en el HUD lateral.
- **🦾 Selector de Mecanismo:** Alterna entre el **Brazo Robótico 6-DOF** y el **Actuador Servo** con los botones superiores."""

                        elif es_anatomy:
                            from plantillas.anatomy_demos import generar_anatomy_test_rig
                            pers_act = config_global.get("personalidad_activa", "isabella")
                            nombre_ia = "Isabella" if pers_act == "isabella" else "AUREX"
                            respuesta = f"""Jefe, he construido e integrado la primera máquina mecatrónica isométrica interactiva bajo la norma **ANATOMY**:

{generar_anatomy_test_rig()}

### 📐 Ficha Técnica de la Máquina (Norma Anatomy):
- **Estructura y Base:** Bloque de aluminio mecanizado con ranuras en T métricas y 4 pies de apoyo antivibratorios.
- **Accionamiento:** Motor paso a paso NEMA 17 con acoplador elástico helicoidal de bronce/aluminio.
- **Transmisión Mecánica:** Husillo roscado trapezoidal con paso rectificado acoplado a carro de eje X.
- **Metrología en Tiempo Real:** Reloj comparador analógico de 0.01 mm con palpador de carburo de contacto directo y aguja giratoria 360°.
- **Interacción en Vivo:** Puedes arrastrar el deslizador de posición, pulsar **Homing** para volver al cero de máquina o activar el **Barrido Automático** para verla en movimiento."""

                        elif es_peticion_imagenes_sensores and sensores_objetivo:
                            pers_act = config_global.get("personalidad_activa", "isabella")
                            nombre_ia = "Isabella" if pers_act == "isabella" else "AUREX"
                            nombres_txt = " y del ".join([f"**{s['nombre']}**" for s in sensores_objetivo])
                            respuesta = f"""¡A sus órdenes, Jefe! Aquí tiene las **fichas tácticas, esquemas vectoriales de pines (pinouts) y especificaciones técnicas completas** del {nombres_txt}:

Puede consultar abajo los diagramas de cableado y directivas de taller para cada uno."""

                        elif es_ultrasonico:
                            from plantillas.diagramas import generar_diagrama_esp32_hcsr04
                            respuesta = f"""Aquí tienes el diagrama de conexión del **ESP32** con el **sensor ultrasónico HC-SR04**, Jefe:

{generar_diagrama_esp32_hcsr04()}

### Conexiones:
| ESP32 | HC-SR04 |
| :--- | :--- |
| **3V3** | **VCC** |
| **GPIO 5** | **TRIG** |
| **GPIO 18** | **ECHO** |
| **GND** | **GND** |

> ⚠️ **Importante:** El pin ECHO del HC-SR04 entrega 5 V y el ESP32 opera con lógica de 3.3 V. Utiliza un divisor de voltaje (1kΩ y 2kΩ) entre ECHO y GPIO 18 para proteger el microcontrolador.

También puedo prepararte el código Arduino IDE para medir distancias con este circuito."""

                    # Si el modelo rechazó otra petición de diagrama, generar diagrama hardcodeado de alta calidad
                    frases_rechazo = ["lo siento, pero no puedo", "no puedo ayudar", "i cannot", "i can't", "lo siento, no puedo"]
                    if es_peticion_diagrama and any(f in respuesta.lower() for f in frases_rechazo):
                        # Parsear componentes de la orden
                        orden_l = orden.lower()
                        comp_a = "ESP32"
                        comp_b = "HC-SR04"
                        if "dht11" in orden_l or "dht22" in orden_l:
                            comp_b = "DHT11/22"
                        elif "l298n" in orden_l or "motor dc" in orden_l:
                            comp_b = "L298N"
                        elif "neopixel" in orden_l or "ws2812" in orden_l:
                            comp_b = "NeoPixel"
                        elif "oled" in orden_l or "ssd1306" in orden_l:
                            comp_b = "OLED SSD1306"
                        elif "bmp280" in orden_l or "bme280" in orden_l:
                            comp_b = "BMP/BME280"
                        respuesta = f"""Jefe, aquí está el diagrama de conexión del **{comp_a}** con el **{comp_b}**:

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Diagrama {comp_a} ↔ {comp_b}</title>
<style>
  body {{ margin: 0; background: #0f172a; font-family: 'Courier New', monospace; color: #e2e8f0; display: flex; flex-direction: column; align-items: center; padding: 24px; }}
  h1 {{ color: #38bdf8; font-size: 1.3rem; margin-bottom: 16px; letter-spacing: 2px; text-transform: uppercase; }}
  .diagram-container {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px; }}
  table {{ border-collapse: collapse; margin-top: 20px; width: 100%; max-width: 760px; }}
  th {{ background: #1e3a5f; color: #38bdf8; padding: 8px 16px; text-align: left; border: 1px solid #334155; }}
  td {{ padding: 8px 16px; border: 1px solid #334155; font-size: 0.9rem; }}
  .wire-red {{ background: rgba(239,68,68,0.15); color: #ef4444; }}
  .wire-gray {{ background: rgba(107,114,128,0.15); color: #9ca3af; }}
  .wire-green {{ background: rgba(34,197,94,0.15); color: #22c55e; }}
  .wire-blue {{ background: rgba(59,130,246,0.15); color: #3b82f6; }}
  .warning {{ background: rgba(239,68,68,0.1); border: 1px solid #ef4444; border-radius: 8px; padding: 12px; margin-top: 16px; color: #fca5a5; font-size: 0.85rem; }}
</style>
</head>
<body>
<h1>⚡ Diagrama: {comp_a} ↔ {comp_b}</h1>
<div class="diagram-container">
<svg width="760" height="400" viewBox="0 0 760 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Fondo SVG -->
  <rect width="760" height="400" fill="#0f172a" rx="8"/>
  <!-- Título -->
  <text x="380" y="30" text-anchor="middle" fill="#94a3b8" font-size="13" font-family="Courier New">WIRING DIAGRAM — AUREX TACTICAL ENGINEER</text>

  <!-- COMPONENTE A: ESP32 (IZQUIERDA) -->
  <rect x="30" y="70" width="190" height="280" rx="12" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
  <text x="125" y="95" text-anchor="middle" fill="#38bdf8" font-size="14" font-weight="bold" font-family="Courier New">{comp_a}</text>
  <text x="125" y="112" text-anchor="middle" fill="#64748b" font-size="10" font-family="Courier New">ESP-WROOM-32</text>
  <!-- Pines ESP32 (borde derecho x=220) -->
  <circle cx="220" cy="150" r="6" fill="#ef4444"/>
  <text x="210" y="145" text-anchor="end" fill="#e2e8f0" font-size="11" font-family="Courier New">3V3</text>
  <circle cx="220" cy="200" r="6" fill="#22c55e"/>
  <text x="210" y="195" text-anchor="end" fill="#e2e8f0" font-size="11" font-family="Courier New">GPIO5</text>
  <circle cx="220" cy="250" r="6" fill="#3b82f6"/>
  <text x="210" y="245" text-anchor="end" fill="#e2e8f0" font-size="11" font-family="Courier New">GPIO18</text>
  <circle cx="220" cy="300" r="6" fill="#6b7280"/>
  <text x="210" y="295" text-anchor="end" fill="#e2e8f0" font-size="11" font-family="Courier New">GND</text>

  <!-- COMPONENTE B: HC-SR04 (DERECHA) -->
  <rect x="540" y="110" width="190" height="210" rx="12" fill="#14532d" stroke="#22c55e" stroke-width="2"/>
  <text x="635" y="135" text-anchor="middle" fill="#86efac" font-size="14" font-weight="bold" font-family="Courier New">{comp_b}</text>
  <text x="635" y="152" text-anchor="middle" fill="#4ade80" font-size="10" font-family="Courier New">ULTRASÓNICO</text>
  <!-- Pines HC-SR04 (borde izquierdo x=540) -->
  <circle cx="540" cy="175" r="6" fill="#ef4444"/>
  <text x="550" y="170" fill="#e2e8f0" font-size="11" font-family="Courier New">VCC</text>
  <circle cx="540" cy="215" r="6" fill="#22c55e"/>
  <text x="550" y="210" fill="#e2e8f0" font-size="11" font-family="Courier New">TRIG</text>
  <circle cx="540" cy="255" r="6" fill="#3b82f6"/>
  <text x="550" y="250" fill="#e2e8f0" font-size="11" font-family="Courier New">ECHO</text>
  <circle cx="540" cy="295" r="6" fill="#6b7280"/>
  <text x="550" y="290" fill="#e2e8f0" font-size="11" font-family="Courier New">GND</text>

  <!-- CABLES de conexión -->
  <!-- Cable VCC (rojo): ESP32 3V3 → HC-SR04 VCC -->
  <polyline points="220,150 380,150 380,175 540,175" fill="none" stroke="#ef4444" stroke-width="3" stroke-linecap="round"/>
  <!-- Cable TRIG (verde): ESP32 GPIO5 → HC-SR04 TRIG -->
  <polyline points="220,200 380,200 380,215 540,215" fill="none" stroke="#22c55e" stroke-width="3" stroke-linecap="round"/>
  <!-- Cable ECHO (azul): ESP32 GPIO18 → HC-SR04 ECHO -->
  <polyline points="220,250 380,250 380,255 540,255" fill="none" stroke="#3b82f6" stroke-width="3" stroke-linecap="round"/>
  <!-- Cable GND (gris): ESP32 GND → HC-SR04 GND -->
  <polyline points="220,300 380,300 380,295 540,295" fill="none" stroke="#6b7280" stroke-width="3" stroke-linecap="round"/>

  <!-- Etiquetas de cables en el centro -->
  <text x="380" y="142" text-anchor="middle" fill="#ef4444" font-size="10" font-family="Courier New">VCC 3.3V</text>
  <text x="380" y="192" text-anchor="middle" fill="#22c55e" font-size="10" font-family="Courier New">TRIG</text>
  <text x="380" y="242" text-anchor="middle" fill="#3b82f6" font-size="10" font-family="Courier New">ECHO</text>
  <text x="380" y="292" text-anchor="middle" fill="#6b7280" font-size="10" font-family="Courier New">GND</text>
</svg>
</div>

<!-- Tabla de conexiones -->
<table>
  <tr><th>{comp_a}</th><th>PIN</th><th>→</th><th>{comp_b}</th><th>PIN</th><th>Color</th></tr>
  <tr class="wire-red"><td>3.3V</td><td>3V3</td><td>→</td><td>Alimentación</td><td>VCC</td><td>🔴 Rojo</td></tr>
  <tr class="wire-green"><td>GPIO 5</td><td>D5</td><td>→</td><td>Trigger</td><td>TRIG</td><td>🟢 Verde</td></tr>
  <tr class="wire-blue"><td>GPIO 18</td><td>D18</td><td>→</td><td>Echo</td><td>ECHO</td><td>🔵 Azul</td></tr>
  <tr class="wire-gray"><td>GND</td><td>GND</td><td>→</td><td>Tierra</td><td>GND</td><td>⚫ Negro</td></tr>
</table>
<div class="warning">
  ⚠️ <strong>ADVERTENCIA:</strong> El pin ECHO del HC-SR04 puede entregar hasta <strong>5V</strong> y el ESP32 tolera únicamente <strong>3.3V</strong> en sus GPIOs.
  Usa un divisor de voltaje (R1=10kΩ, R2=20kΩ) entre ECHO y GPIO18 para proteger el microcontrolador.
</div>
</body>
</html>
```"""
                except Exception as e_inner:
                    err_str = str(e_inner).lower()
                    # DeepSeek entró en bucle de repetición → reintentar con LLaMA
                    if "repeat" in err_str or "status code: -1" in err_str or "aborted" in err_str:
                        try:
                            cadena_fallback, _ = configurar_red_neuronal(
                                st.session_state.vectorstore, modelo_llm="llama3.2:latest"
                            )
                            respuesta = cadena_fallback.invoke(payload)
                            respuesta = "*(AUREX: DeepSeek entró en bucle, respondiendo con LLaMA)*\n\n" + respuesta
                        except Exception as e_fb:
                            respuesta = f"Jefe, anomalía temporal en la red: {e_fb}"
                    else:
                        raise

            except Exception as e:
                respuesta = f"Jefe, anomalía temporal en la red: {e}"
                fuentes   = []
                fuentes_web = []

        # Verificacion numerica con Python (AUREX Calc)
        try:
            verificacion = verificar_con_python(orden, respuesta)
            if not verificacion:
                verificacion = extraer_y_ejecutar_codigo_llm(respuesta)
            if verificacion:
                respuesta = respuesta + verificacion
        except Exception:
            pass

        st.session_state.historial.append({
            "rol": "ia",
            "texto": respuesta,
            "fuentes": fuentes,
            "fuentes_web": fuentes_web
        })

        st.session_state.ultimo_streaming = respuesta
        st.rerun()

# ═════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════
#  PESTAÑA 2: GENERADOR & GALERÍA DE IMÁGENES DE SENSORES
# ═════════════════════════════════════════════════════════════

# ═════════════════════════════════════════════════════════════
#  PESTAÑA 2: AGENTE AUTÓNOMO AUREX (MODO ANTIGRAVITY)
# ═════════════════════════════════════════════════════════════
with tab_autonomo:
    st.subheader("⚡ Taller de Agente Autónomo AUREX · Modo Antigravity")
    st.caption("Bucle cerrado agéntico en tiempo real: Generación → Compilación/Ejecución Local → Detección de Errores → Auto-Corrección Autónoma.")
    
    from agente_autonomo import ejecutar_ciclo_agente_autonomo, WORKSPACE_DIR
    
    # Pruebas rápidas mecatrónicas con 1 clic
    st.markdown("**Misiones Mecatrónicas Rápidas:**")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        if st.button("📊 ADC & Calibración (Py)", use_container_width=True):
            st.session_state["orden_agente_autonomo"] = "Crea un script en Python que simule la lectura analógica de un sensor TDS en el ESP32 (VCC 3.3V, ADC 12 bits), calcule el voltaje, convierta a ppm y muestre una tabla calibrada con 5 muestras."
    with col_m2:
        if st.button("🦾 Cinemática y Torque (Py)", use_container_width=True):
            st.session_state["orden_agente_autonomo"] = "Crea un script en Python que calcule el torque estático y dinámico de un brazo robótico de 3 DOF levantando 1.5 kg y muestre los torques calculados en cada articulación."
    with col_m3:
        if st.button("⚡ Firmware ESP32 Web (C++)", use_container_width=True):
            st.session_state["orden_agente_autonomo"] = "Crea un sketch completo para ESP32 con WebServer en el puerto 80, lectura analógica en GPIO 34, control de relé en GPIO 2 y JSON en endpoint /status."
    with col_m4:
        if st.button("📡 Monitor Serial COM (Py)", use_container_width=True):
            st.session_state["orden_agente_autonomo"] = "Crea un script en Python con manejo de excepciones para listar y verificar puertos COM disponibles para enlace de microcontrolador."

    orden_autonoma = st.text_area(
        "🎯 Ingrese la meta u orden para el Agente Autónomo:",
        value=st.session_state.get("orden_agente_autonomo", "Crea un script en Python que calcule el torque necesario para levantar 2.5 kg con un brazo de 35 cm y muestre el resultado en N*m y kg*cm"),
        height=90,
        key="input_mision_autonoma"
    )
    
    c_btn_exec, c_btn_dir = st.columns([3, 1])
    with c_btn_exec:
        btn_ejecutar_agente = st.button("🚀 Iniciar Ciclo Agéntico Autónomo (Ejecutar & Auto-Reparar)", type="primary", use_container_width=True)
    with c_btn_dir:
        if st.button("📁 Abrir Workspace Local", use_container_width=True):
            try:
                os.startfile(WORKSPACE_DIR)
            except Exception as e:
                st.info(f"Ruta: {WORKSPACE_DIR}")

    if btn_ejecutar_agente and orden_autonoma.strip():
        status_box = st.status("🤖 Agente AUREX en ejecución autónoma...", expanded=True)
        
        logs_en_vivo = []
        def callback_ui(etapa, msg, estado):
            icono = "🔹" if estado == "INFO" else ("⚠️" if estado == "WARNING" else "✅")
            logs_en_vivo.append(f"{icono} [{etapa}] {msg}")
            status_box.write(f"{icono} **[{etapa}]** {msg}")
            
        with st.spinner("Procesando ciclo agéntico con Qwen 2.5 Coder 7B..."):
            res_agente = ejecutar_ciclo_agente_autonomo(orden_autonoma, max_intentos=3, progreso_callback=callback_ui)
            
        if res_agente["exito"]:
            status_box.update(label=f"✅ Misión Autónoma Completada con Éxito (Ciclo {res_agente['intentos']})", state="complete", expanded=False)
            st.success(f"🎯 Misión cumplida en {res_agente['intentos']} ciclo(s). Archivo generado en workspace: `{res_agente['nombre_archivo']}`")
        else:
            status_box.update(label="❌ Anomalía no resuelta tras agotar ciclos", state="error", expanded=True)
            st.error("El agente detectó un error persistente en el entorno local.")

        # HUD de Telemetría Agéntica
        c_code, c_out = st.columns([1, 1])
        with c_code:
            st.markdown(f"**💻 Código Final Verificado ({res_agente['lenguaje'].upper()}):**")
            st.code(res_agente["codigo_final"], language="python" if res_agente["lenguaje"]=="python" else "cpp")
            st.download_button(
                label=f"💾 Descargar {res_agente['nombre_archivo']}",
                data=res_agente["codigo_final"],
                file_name=res_agente["nombre_archivo"],
                key="dl_codigo_autonomo"
            )
        with c_out:
            st.markdown("**🖥️ Terminal de Salida Real (Hardware / OS):**")
            if res_agente["salida_consola"]:
                st.code(res_agente["salida_consola"], language="text")
            if res_agente["error_consola"]:
                st.markdown("**⚠️ Diagnóstico del Compilador / Errores:**")
                st.code(res_agente["error_consola"], language="text")


with tab_imagenes:
    st.subheader("📸 Generador & Galería Visual de Componentes Mecatrónicos")
    st.caption("Escriba cualquier sensor, actuador o módulo para generar instantáneamente su ficha táctica, foto de referencia y plano vectorial de pines (Pinout).")

    # ── BARRA DE PROMPT INTERACTIVA PARA PEDIR IMÁGENES ──
    with st.form("form_prompt_imagenes", clear_on_submit=False):
        c_input, c_btn = st.columns([5, 1])
        with c_input:
            orden_img_escrita = st.text_input(
                "💬 Escriba su orden visual a Isabella:",
                placeholder="Ejemplo: 'dame las imágenes del sensor de flotador y calidad de agua', 'muestra el servo sg90 y el esp32'...",
                key="input_orden_img_directa"
            )
        with c_btn:
            submit_img = st.form_submit_button("🚀 Generar", use_container_width=True)

    # ── BANCO DE PRUEBAS RÁPIDAS PARA EL JEFE (1 CLICK) ──
    with st.expander("🧪 Pruebas Rápidas de Imágenes (Haga clic para probar de inmediato)", expanded=True):
        st.markdown("**Copie o pulse sobre cualquier prueba para ver sus imágenes y diagramas de pines:**")
        cp1, cp2, cp3 = st.columns(3)
        with cp1:
            if st.button("💧 Sensores de Agua: Flotador + TDS", use_container_width=True, key="p_agua"):
                st.session_state["filtro_sensor_manual"] = "agua"
        with cp2:
            if st.button("🦇 Distancia & Servos: HC-SR04 + SG90", use_container_width=True, key="p_dist"):
                st.session_state["filtro_sensor_manual"] = "distancia"
        with cp3:
            if st.button("⚡ Cerebros & Drivers: ESP32 + L298N", use_container_width=True, key="p_power"):
                st.session_state["filtro_sensor_manual"] = "driver"

    # Procesar orden escrita si el usuario pulsó Generar
    sensores_resultado = []
    texto_a_buscar = ""
    if submit_img and orden_img_escrita.strip():
        texto_a_buscar = orden_img_escrita.strip().lower()
        sensores_resultado = buscar_sensores_en_texto(texto_a_buscar, permitir_fallback=True)
        if sensores_resultado:
            st.success(f"✅ Isabella: Generando fichas visuales para {len(sensores_resultado)} componente(s) detectado(s).")
        else:
            st.warning("⚠️ No se detectó un nombre exacto. Buscando coincidencias generales en el catálogo...")
    
    # Si no hubo submit de form, usar filtro o pruebas rápidas
    if not sensores_resultado:
        filtro_rapido = st.session_state.get("filtro_sensor_manual", "")
        if filtro_rapido == "agua":
            sensores_resultado = [CATALOGO_SENSORES.get("sensor-nivel-flotador"), CATALOGO_SENSORES.get("sensor-calidad-agua")]
        elif filtro_rapido == "distancia":
            sensores_resultado = [CATALOGO_SENSORES.get("hc-sr04"), CATALOGO_SENSORES.get("sg90"), CATALOGO_SENSORES.get("mg996r")]
        elif filtro_rapido == "driver":
            sensores_resultado = [CATALOGO_SENSORES.get("esp32"), CATALOGO_SENSORES.get("l298n"), CATALOGO_SENSORES.get("rele-5v")]
        elif texto_a_buscar:
            for k, v in CATALOGO_SENSORES.items():
                if (texto_a_buscar in k) or (texto_a_buscar in v["nombre"].lower()) or (texto_a_buscar in v.get("descripcion", "").lower()):
                    sensores_resultado.append(v)

    # Catálogo y filtro por categorías
    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        categorias = ["Todos", "Sensores de Nivel y Líquidos", "Sensores Químicos y Calidad de Líquidos", "Sensores de Distancia", "Sensores Ambientales", "Actuadores y Motores", "Controladores de Potencia", "Microcontroladores y SoCs", "Interfaces y Pantallas"]
        cat_sel = st.selectbox("Filtrar por subsistema:", categorias, key="cat_sel_imagenes")
    with col_f2:
        termino_box = st.text_input("🔍 Filtro manual por texto:", value="", placeholder="Escriba para filtrar catálogo...", key="txt_box_filtro").strip().lower()

    if not sensores_resultado:
        for k, v in CATALOGO_SENSORES.items():
            if cat_sel != "Todos" and v.get("categoria") != cat_sel:
                continue
            if termino_box:
                if (termino_box not in k) and (termino_box not in v["nombre"].lower()) and (termino_box not in v.get("descripcion", "").lower()):
                    continue
            sensores_resultado.append(v)

    # Limpiar None si hubiese
    sensores_resultado = [s for s in sensores_resultado if s]

    st.markdown(f"**Fichas Visuales y Planos Técnicos ({len(sensores_resultado)}):**")
    if sensores_resultado:
        for s in sensores_resultado:
            renderizar_tarjeta_sensor(s)
    else:
        st.info("No se encontraron sensores. Pruebe con 'flotador', 'calidad del agua', 'hc-sr04', 'esp32' o 'servo'.")

# ═════════════════════════════════════════════════════════════
#  PESTAÑA 3: GEMELO DIGITAL (OBJETO FÍSICO REAL ↔ MODELO 3D)
# ═════════════════════════════════════════════════════════════
with tab_gemelo_3d:
    st.subheader("🦾 Gemelo Digital: Objeto Físico Real ↔ Modelo 3D Holográfico")
    st.caption("Laboratorio táctico interactivo permanente. Inspección de tolerancias ISO, despiece 3D sincronizado y comparación directa con el prototipo de taller.")

    # ── BARRA DE PROMPT INTERACTIVA PARA EL GEMELO DIGITAL UNIVERSAL ──
    with st.form("form_prompt_3d", clear_on_submit=False):
        c_in_3d, c_btn_3d = st.columns([5, 1])
        with c_in_3d:
            orden_3d_escrita = st.text_input(
                "💬 Comandar al Gemelo Digital en lenguaje natural:",
                placeholder="Escriba CUALQUIER objeto: 'ESP32', 'NEMA 17', 'Arduino', 'Brazo', 'Servo SG90', 'lo que sea'...",
                key="input_orden_3d_directa"
            )
        with c_btn_3d:
            submit_3d = st.form_submit_button("⚡ Ejecutar 3D", use_container_width=True)

    # ── BOTONES DE ACCESO RÁPIDO A MODELOS CLAVE ──
    with st.expander("🧪 Selector Directo de Mecanismos y Componentes 3D", expanded=True):
        st.markdown("**Haga clic para sintetizar de inmediato cualquier dispositivo en 3D:**")
        c_p1, c_p2, c_p3, c_p4, c_p5, c_p6, c_p7 = st.columns(7)
        with c_p1:
            if st.button("⚡ ESP32 (3D)", use_container_width=True, key="btn_p_esp32"):
                st.session_state["objeto_3d_actual"] = "esp32"
                st.rerun()
        with c_p2:
            if st.button("💧 Flujo YF-S201", use_container_width=True, key="btn_p_flujo"):
                st.session_state["objeto_3d_actual"] = "sensor de flujo de agua"
                st.rerun()
        with c_p3:
            if st.button("🟦 Arduino Uno (3D)", use_container_width=True, key="btn_p_arduino"):
                st.session_state["objeto_3d_actual"] = "arduino"
                st.rerun()
        with c_p4:
            if st.button("📐 NEMA 17 (3D)", use_container_width=True, key="btn_p_nema"):
                st.session_state["objeto_3d_actual"] = "nema17"
                st.rerun()
        with c_p5:
            if st.button("🦾 Brazo 6-DOF", use_container_width=True, key="btn_p_brazo"):
                st.session_state["objeto_3d_actual"] = "brazo"
                st.rerun()
        with c_p6:
            if st.button("⚙️ Actuador 608ZZ", use_container_width=True, key="btn_p_actuador"):
                st.session_state["objeto_3d_actual"] = "actuador"
                st.rerun()
        with c_p7:
            if st.button("🧪 Sensores TDS", use_container_width=True, key="btn_p_sensores"):
                st.session_state["objeto_3d_actual"] = "sensores"
                st.rerun()

    # Procesar orden escrita si el Jefe usó la barra
    if submit_3d and orden_3d_escrita.strip():
        txt_ped = orden_3d_escrita.strip()
        st.session_state["objeto_3d_actual"] = txt_ped
        st.success(f"⚡ Protocolo AUREX: Sintetizando gemelo digital 3D para '{txt_ped.upper()}'. Banco táctico sincronizado.")

    objeto_3d_activo = st.session_state.get("objeto_3d_actual", "esp32")

    # Banner táctico de telemetría y objeto activo
    st.markdown(f"""
    <div style="background:#0f172a; border:1px solid #00f0ff; border-radius:8px; padding:10px 16px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
        <div>
            <span style="color:#00f0ff; font-weight:700; font-size:0.95rem;">🛰️ OBJETO 3D ACTIVO:</span>
            <span style="color:#f8fafc; font-weight:800; font-size:1.05rem; margin-left:8px;">{objeto_3d_activo.upper()}</span>
        </div>
        <div style="font-size:0.82rem; color:#38bdf8;">
            <b>Telemetría:</b> EN LÍNEA · 60 FPS · Gemelo Físico ↔ Holograma Digital
        </div>
    </div>
    """, unsafe_allow_html=True)

    import importlib
    import plantillas.holograma_3d
    importlib.reload(plantillas.holograma_3d)
    from plantillas.holograma_3d import generar_laboratorio_holografico_3d
    raw_lab_html = generar_laboratorio_holografico_3d(modelo_inicial=objeto_3d_activo, objeto_personalizado=objeto_3d_activo)
    clean_lab_html = raw_lab_html.replace("```html", "").replace("```", "").strip()
    st.components.v1.html(clean_lab_html, height=760, scrolling=False)

# ═════════════════════════════════════════════════════════════
#  PESTAÑA 3: ÓPTICA TÁCTICA Y ANÁLISIS DE VIDEO (QWEN + GEMINI)
# ═════════════════════════════════════════════════════════════
with tab_vision:
    st.subheader("👁️ Escáner Óptico, Reconocimiento de Diagramas y Análisis de Video")
    st.caption("Suba capturas de planos, circuitos, fotos de componentes o **VIDEOS** de mecanismos en funcionamiento para un diagnóstico táctico.")

    col_media, col_analisis = st.columns([1, 1])

    with col_media:
        archivo_multimedia = st.file_uploader(
            "Cargue una Imagen o Video (PNG, JPG, MP4, MOV, WEBM)",
            type=["png", "jpg", "jpeg", "webp", "mp4", "mov", "avi", "webm"],
            key="visor_tactico_multimedia"
        )
        es_video = False
        mime_archivo = "image/jpeg"
        if archivo_multimedia:
            ext = Path(archivo_multimedia.name).suffix.lower()
            if ext in [".mp4", ".mov", ".avi", ".webm"]:
                es_video = True
                mime_archivo = f"video/{ext.replace('.', '')}" if ext != ".mov" else "video/quicktime"
                st.video(archivo_multimedia)
            else:
                mime_archivo = f"image/{ext.replace('.', '')}" if ext != ".jpg" else "image/jpeg"
                st.image(archivo_multimedia, caption="Transmisión óptica recibida", use_container_width=True)

    with col_analisis:
        if archivo_multimedia:
            if es_video:
                st.markdown("### 🎬 Protocolo Táctico de Video")
                col_vb1, col_vb2 = st.columns(2)
                with col_vb1:
                    analizar_video_btn = st.button("🎬 Analizar y Explicar Video", type="primary", use_container_width=True)
                with col_vb2:
                    asimilar_video_btn = st.button("🧠 Asimilar en Memoria RAG", use_container_width=True)

                modo_video = st.radio(
                    "⚡ Velocidad y Enfoque:",
                    [
                        "🚀 Rápido (Audio Whisper Base + 4 Fotos Clave)",
                        "🎙️ Solo Audio/Clase (Ultrarrápido, ~2 min)",
                        "👁️ Solo Visual (Mecanismos/Circuitos mudos)"
                    ],
                    horizontal=True
                )

                pregunta_vid = st.text_area(
                    "Pregunta o directiva sobre el video (opcional):",
                    placeholder="Ej: AUREX, explica el funcionamiento del mecanismo y en qué minuto ocurre la conmutación",
                    height=70,
                    key="pregunta_tactica_video"
                )
                
                st.caption(f"Motor: `PyAV` + `Whisper Base (int8 · 6 hilos CPU)` + `{VISION_MODEL}` | 100% Offline")

                if analizar_video_btn or asimilar_video_btn:
                    hablar_espera_inmediata()
                    nombre_vid = archivo_multimedia.name
                    
                    desea_audio = "Solo Visual" not in modo_video
                    desea_fotos = "Solo Audio" not in modo_video
                    
                    # Guardar video temporalmente para decodificar con PyAV
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(nombre_vid).suffix) as tmp_f:
                        tmp_f.write(archivo_multimedia.getvalue())
                        tmp_vid_path = tmp_f.name

                    try:
                        with st.spinner("Jefe, abriendo video y analizando pistas con PyAV..."):
                            ruta_wav, fotogramas, duracion = extraer_audio_y_fotogramas(
                                tmp_vid_path,
                                extraer_visual=desea_fotos,
                                intervalo_segundos=30.0,
                                max_fotogramas=4
                            )
                        
                        transcripcion = ""
                        if desea_audio and ruta_wav and os.path.exists(ruta_wav):
                            barra_audio = st.progress(0.0, text=f"🎙️ Transcribiendo audio ({formatear_segundos_a_tiempo(duracion)}) con Whisper Base...")
                            def cb_audio(pct, seg_act, seg_tot):
                                barra_audio.progress(
                                    pct,
                                    text=f"🎙️ Transcribiendo clase: {formatear_segundos_a_tiempo(seg_act)} de {formatear_segundos_a_tiempo(seg_tot)} ({int(pct*100)}%)"
                                )
                            
                            whisper_mod = cargar_whisper_base()
                            transcripcion, _ = transcribir_audio_video(ruta_wav, whisper_mod, callback_progreso=cb_audio)
                            barra_audio.progress(1.0, text="✅ Transcripción de audio completada")
                            try:
                                os.remove(ruta_wav)
                            except Exception:
                                pass
                        
                        resumen_visual = ""
                        if desea_fotos and fotogramas:
                            barra_vis = st.progress(0.0, text=f"👁️ Analizando {len(fotogramas)} fotogramas clave con Qwen...")
                            def cb_vis(act, tot):
                                barra_vis.progress(act / tot, text=f"👁️ Escaneando fotograma {act} de {tot}...")
                            
                            resumen_visual = analizar_fotogramas_con_qwen(fotogramas, modelo_vision=VISION_MODEL, callback_progreso=cb_vis)
                            barra_vis.progress(1.0, text="✅ Escaneo visual completado")
                        
                        directiva = pregunta_vid.strip() if pregunta_vid else "Explica detalladamente todo el contenido del video, sus etapas, componentes o conceptos técnicos y conclusiones."
                        
                        with st.spinner("Compilando informe de ingeniería con LLaMA 3.2..."):
                            informe_final = generar_sintesis_video_aurex(
                                nombre_vid,
                                transcripcion,
                                resumen_visual,
                                directiva,
                                modelo_llm=LLM_MODEL
                            )

                        if asimilar_video_btn:
                            with st.spinner("Asimilando protocolo de video en la memoria ChromaDB..."):
                                ruta_doc_txt = asimilar_video_en_memoria_aurex(nombre_vid, transcripcion, resumen_visual)
                                docs = cargar_documento(ruta_doc_txt)
                                if docs:
                                    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
                                    fragmentos = splitter.split_documents(docs)
                                    vs = st.session_state.get("vectorstore") or obtener_vectorstore()
                                    vs.add_documents(fragmentos)
                                    reg = cargar_registro()
                                    reg.append({
                                        "nombre": Path(ruta_doc_txt).name,
                                        "fragmentos": len(fragmentos)
                                    })
                                    guardar_registro(reg)
                                    st.session_state.vectorstore = vs
                                    cadena, retriever = configurar_red_neuronal(vs)
                                    st.session_state.cadena = cadena
                                    st.session_state.retriever = retriever
                                    st.success(f"🛡️ Video asimilado en la memoria permanente como '{Path(ruta_doc_txt).name}'. Ahora puede hacerle preguntas sobre este video en cualquier momento desde el chat principal, Jefe.")

                        # Guardar permanentemente en session_state para que NUNCA desaparezca al interactuar
                        st.session_state["video_analizado"] = {
                            "nombre": nombre_vid,
                            "informe": informe_final,
                            "fotogramas": fotogramas,
                            "transcripcion": transcripcion
                        }
                        st.session_state["preguntas_video_historial"] = []
                        st.rerun()

                    finally:
                        if os.path.exists(tmp_vid_path):
                            try:
                                os.remove(tmp_vid_path)
                            except Exception:
                                pass

                # ── RENDERIZADO PERSISTENTE DEL ANÁLISIS DE VIDEO (NUNCA DESAPARECE) ──
                if "video_analizado" in st.session_state and st.session_state["video_analizado"]:
                    v_datos = st.session_state["video_analizado"]
                    st.divider()
                    st.markdown(f"### 📋 Informe Táctico: {v_datos.get('nombre', 'Video')}")
                    st.markdown(v_datos["informe"])

                    if v_datos.get("fotogramas"):
                        with st.expander(f"🎞️ Ver {len(v_datos['fotogramas'])} Fotogramas Clave Analizados", expanded=True):
                            cols_fot = st.columns(min(4, len(v_datos["fotogramas"])))
                            for idx_f, f_item in enumerate(v_datos["fotogramas"]):
                                with cols_fot[idx_f % len(cols_fot)]:
                                    st.image(f_item["bytes"], caption=f"⏱️ {f_item['tiempo_str']}", use_container_width=True)

                    if v_datos.get("transcripcion"):
                        with st.expander("📝 Transcripción Completa del Audio (Marcas de Tiempo)", expanded=False):
                            st.text_area("Transcripción Whisper", v_datos["transcripcion"], height=200)

                    # ── PANEL DE PREGUNTAS DIRECTAS SOBRE ESTE VIDEO ──
                    st.markdown("---")
                    st.markdown("#### 💬 Consultar o Preguntar sobre esta Grabación")
                    
                    if "preguntas_video_historial" not in st.session_state:
                        st.session_state["preguntas_video_historial"] = []
                    
                    for pv in st.session_state["preguntas_video_historial"]:
                        st.markdown(f"**Usted:** {pv['pregunta']}")
                        st.markdown(f"**AUREX:** {pv['respuesta']}")
                        st.write("")

                    col_qp_in, col_qp_btn = st.columns([4, 1])
                    with col_qp_in:
                        pregunta_vid_interactiva = st.text_input(
                            "Escriba su pregunta sobre la clase o video:",
                            placeholder="Ej: ¿Qué explicó el profesor sobre la ley de Schmid y qué fórmula usó?",
                            key="input_q_video_persistente"
                        )
                    with col_qp_btn:
                        st.write("")
                        enviar_q_vid = st.button("Consultar ⚡", key="btn_enviar_q_vid_persistente", use_container_width=True)

                    if enviar_q_vid and pregunta_vid_interactiva:
                        hablar_espera_inmediata()
                        with st.spinner("AUREX revisando la clase y fotogramas..."):
                            prompt_q_vid = f"""Eres AUREX, Ingeniero Mecatrónico Senior.
El Jefe te está preguntando sobre la grabación: {v_datos.get('nombre', 'Video')}.

CRÓNICA Y FOTOGRAMAS:
{v_datos.get('informe', '')}

TRANSCRIPCIÓN COMPLETA:
{v_datos.get('transcripcion', '')[:10000]}

PREGUNTA DEL JEFE: {pregunta_vid_interactiva}

Responde de forma clara, directa, citando minutos y fórmulas exactas si las hay, dirigiéndote a él como 'Jefe'."""
                            try:
                                resp_q = ollama.chat(
                                    model=LLM_MODEL,
                                    messages=[{"role": "user", "content": prompt_q_vid}],
                                    options={"temperature": 0.2, "num_predict": 1800}
                                )
                                txt_resp = resp_q["message"]["content"].strip()
                            except Exception as e_q:
                                txt_resp = f"Jefe, anomalía al procesar la consulta: {e_q}"
                            
                            st.session_state["preguntas_video_historial"].append({
                                "pregunta": pregunta_vid_interactiva,
                                "respuesta": txt_resp
                            })
                            st.rerun()

            else:
                st.markdown("### 🎯 Directiva Visual (Imagen)")
                col_b1, col_b2, col_b3 = st.columns(3)
                with col_b1:
                    analizar_rapido = st.button("🔍 Explicar", use_container_width=True)
                with col_b2:
                    analizar_fallas = st.button("⚠️ Detectar Fallas", use_container_width=True)
                with col_b3:
                    asimilar_img_btn = st.button("🧠 Asimilar en Memoria RAG", use_container_width=True)
                
                pregunta_img = st.text_area(
                    "O haga una pregunta específica sobre el archivo:",
                    placeholder="Ej: AUREX, ¿qué componente está fallando o qué diagrama representa?",
                    height=90
                )
                
                st.caption(f"Sensor Óptico activo: `{VISION_MODEL}` (100% Offline · Procesamiento GPU Local)")
                ejecutar_analisis = st.button("⚡ Iniciar Análisis Táctico", type="primary", use_container_width=True)

                prompt_final = None
                if asimilar_img_btn:
                    prompt_final = "Genera un protocolo técnico exhaustivo y completo de este diagrama o plano para archivarlo en la memoria permanente del taller: lista todos los componentes visibles, numeración de pines, conexiones, voltajes, valores de resistencias/capacitores y directiva de funcionamiento detallada."
                elif analizar_rapido:
                    prompt_final = "Explica detalladamente qué representa este diagrama o imagen, cuáles son sus componentes principales y cómo funciona el sistema."
                elif analizar_fallas:
                    prompt_final = "Identifica todos los componentes electrónicos o mecánicos visibles, sus valores y evalúa si hay alguna falla, riesgo o desconexión en el circuito."
                elif ejecutar_analisis and pregunta_img:
                    prompt_final = pregunta_img

                if prompt_final:
                    hablar_espera_inmediata()
                    media_bytes = archivo_multimedia.getvalue()
                    with st.spinner("Jefe, procesando sensores ópticos locales (Qwen 2.5 VL)..."):
                        diagnostico = analizar_imagen_aurex(media_bytes, prompt_final)
                        
                        # Si se presionó asimilar en memoria, indexar en ChromaDB
                        if asimilar_img_btn:
                            nombre_base = Path(archivo_multimedia.name).stem
                            nombre_txt = f"Diagrama_{nombre_base}_protocolo.txt"
                            ruta_txt = os.path.join(DOCS_DIR, nombre_txt)
                            contenido_img_doc = f"REGISTRO DE PLANO / DIAGRAMA ASIMILADO POR AUREX\n==============================================\nArchivo: {archivo_multimedia.name}\n\nINFORME TÉCNICO Y COMPONENTES:\n{diagnostico}\n"
                            with open(ruta_txt, "w", encoding="utf-8") as f_img:
                                f_img.write(contenido_img_doc)
                            
                            docs = cargar_documento(ruta_txt)
                            if docs:
                                splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
                                fragmentos = splitter.split_documents(docs)
                                vs = st.session_state.get("vectorstore") or obtener_vectorstore()
                                vs.add_documents(fragmentos)
                                reg = cargar_registro()
                                reg.append({
                                    "nombre": nombre_txt,
                                    "fragmentos": len(fragmentos)
                                })
                                guardar_registro(reg)
                                st.session_state.vectorstore = vs
                                cadena, retriever = configurar_red_neuronal(vs)
                                st.session_state.cadena = cadena
                                st.session_state.retriever = retriever
                                st.success(f"🛡️ Diagrama asimilado en la memoria permanente como '{nombre_txt}'. Ahora puede consultarlo en el chat principal en cualquier momento, Jefe.")
                        
                        renderizar_streaming_con_voz(diagnostico, element_id="aurex-vision-teleprompter")

        else:
            st.info("👈 Arrastre o suba una imagen o video en el panel izquierdo (circuito, mecanismo en movimiento, plano) para que AUREX lo examine.")
