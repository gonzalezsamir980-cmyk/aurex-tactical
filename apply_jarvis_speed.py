# -*- coding: utf-8 -*-
import re

path = r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local\app.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. OPTIMIZAR RAG: Solo consultar Chroma si la orden pregunta por documentos/archivos/clases
old_rag = """                # 1. Consultar libros y bancos locales
                try:
                    fuentes = retriever.invoke(orden)
                except Exception:
                    fuentes = []"""

new_rag = """                # 1. Fast-Path Inteligente: Solo consultar Chroma si la orden pregunta por documentos subidos
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
                    fuentes = []"""

if old_rag in text:
    text = text.replace(old_rag, new_rag, 1)
    print("RAG Fast-Path applied successfully!")
else:
    print("old_rag not found!")

# 2. OPTIMIZAR TRIAGE DE MODELOS: Usar LLaMA 3.2 (3B) ultrarrápido salvo orden explícita de código/matemática pesada
old_triage = """                    if any(d in orden_lower for d in disparadores_codigo):
                        modelo_a_usar = "qwen2.5-coder:7b"
                    elif any(d in orden_lower for d in disparadores_razonamiento):
                        modelo_a_usar = "deepseek-r1:7b"
                    else:
                        modelo_a_usar = "llama3.2:latest\""""

new_triage = """                    # Fast-Triage Jarvis: Priorizar LLaMA 3.2 3B para respuestas instantáneas
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
                        modelo_a_usar = "llama3.2:latest\""""

if old_triage in text:
    text = text.replace(old_triage, new_triage, 1)
    print("Fast-Triage applied successfully!")
else:
    print("old_triage not found!")

# 3. STREAMING REAL EN VIVO CON CADENA.STREAM()
old_invoke = """                try:
                    respuesta = cadena_a_usar.invoke(payload)
                    # Limpiar trazas de razonamiento interno de DeepSeek R1 (<think>...</think>)
                    if "<think>" in respuesta:
                        respuesta = re.sub(r'<think>[\s\S]*?</think>', '', respuesta).strip()
                    # Limpiar posibles caracteres orientales residuales
                    respuesta = re.sub(r'[一-鿿]+', '', respuesta)"""

new_invoke = """                try:
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
                            respuesta = re.sub(r'[一-鿿]+', '', respuesta_bruta)
                            placeholder_stream.markdown(normalizar_latex(respuesta))
                            renderizar_artifacts_interactivos(respuesta, element_key_prefix="stream_live")"""

if old_invoke in text:
    text = text.replace(old_invoke, new_invoke, 1)
    print("Real-time streaming loop applied successfully!")
else:
    print("old_invoke not found!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Patching complete!")
