"""
MÓDULO DE RADAR Y BÚSQUEDA WEB EN TIEMPO REAL - AUREX
Permite a AUREX escanear internet sin costo, sin registros y sin API keys.
Devuelve resúmenes técnicos con enlaces y fuentes verificadas.
"""

import urllib.request
import urllib.parse
import json
import re
from html import unescape

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}


def _limpiar_html(texto: str) -> str:
    """Elimina etiquetas HTML y decodifica entidades."""
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = unescape(texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def _extraer_url_ddg(href: str) -> str:
    """Limpia las URLs de redirección de DuckDuckGo."""
    href = href.strip()
    # Formato: //duckduckgo.com/l/?uddg=URL&rut=...
    m = re.search(r"uddg=([^&]+)", href)
    if m:
        return urllib.parse.unquote(m.group(1))
    if href.startswith("//"):
        return "https:" + href
    return href


def buscar_en_web(query: str, max_resultados: int = 4) -> list[dict]:
    """
    Realiza una búsqueda en internet usando DuckDuckGo HTML + API Instant Answer.
    Retorna lista de dicts con 'titulo', 'snippet' y 'url'.
    """
    query_limpia = query.strip()
    resultados = []

    # ── MÉTODO 1: DuckDuckGo HTML  ──────────────────────────────────────────────
    try:
        url_ddg = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query_limpia) + "&kl=es-es"
        req = urllib.request.Request(url_ddg, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # DDG HTML usa divs con clase "result" que contiene:
        #   <a class="result__a" href="//duckduckgo.com/l/?uddg=ENCODED_URL">Titulo</a>
        #   <a class="result__snippet">Descripcion...</a>
        #
        # Extraemos bloques de resultado completos primero
        bloques = re.findall(
            r'class="result__body">(.*?)</div>\s*</div>',
            html,
            re.DOTALL
        )

        for bloque in bloques[:max_resultados + 2]:
            # Título y URL
            m_titulo = re.search(
                r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
                bloque, re.DOTALL
            )
            # Snippet
            m_snippet = re.search(
                r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
                bloque, re.DOTALL
            )

            if not m_titulo:
                # Intento alternativo: buscar cualquier <a class="result__a"
                m_titulo = re.search(
                    r'href="([^"]+)"[^>]*class="result__a"[^>]*>(.*?)</a>',
                    bloque, re.DOTALL
                )

            if m_titulo and m_snippet:
                url_raw = m_titulo.group(1)
                titulo = _limpiar_html(m_titulo.group(2))
                snippet = _limpiar_html(m_snippet.group(1))
                url_real = _extraer_url_ddg(url_raw)

                if titulo and snippet and url_real.startswith("http"):
                    resultados.append({
                        "titulo": titulo[:120],
                        "snippet": snippet[:350],
                        "url": url_real
                    })

            if len(resultados) >= max_resultados:
                break

        # Si los bloques no funcionaron, intento alternativo más simple
        if not resultados:
            # Buscar todos los enlaces result__a con su texto
            enlaces = re.findall(
                r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
                html, re.DOTALL
            )
            snippets = re.findall(
                r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
                html, re.DOTALL
            )

            for i, (href, titulo_raw) in enumerate(enlaces[:max_resultados]):
                titulo = _limpiar_html(titulo_raw)
                snippet = _limpiar_html(snippets[i]) if i < len(snippets) else ""
                url_real = _extraer_url_ddg(href)

                if titulo and url_real.startswith("http"):
                    resultados.append({
                        "titulo": titulo[:120],
                        "snippet": snippet[:350] if snippet else titulo,
                        "url": url_real
                    })

    except Exception:
        pass

    # ── MÉTODO 2 (FALLBACK): DuckDuckGo Instant Answer API ─────────────────────
    if not resultados:
        try:
            url_api = (
                "https://api.duckduckgo.com/?q="
                + urllib.parse.quote(query_limpia)
                + "&format=json&no_html=1&skip_disambig=1"
            )
            req = urllib.request.Request(url_api, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            if data.get("AbstractText"):
                resultados.append({
                    "titulo": data.get("Heading", "Resumen DuckDuckGo"),
                    "snippet": data["AbstractText"][:400],
                    "url": data.get("AbstractURL", "https://duckduckgo.com")
                })

            for topic in data.get("RelatedTopics", [])[:max_resultados]:
                if isinstance(topic, dict) and topic.get("Text") and topic.get("FirstURL"):
                    resultados.append({
                        "titulo": topic["Text"][:80],
                        "snippet": topic["Text"][:350],
                        "url": topic["FirstURL"]
                    })
                    if len(resultados) >= max_resultados:
                        break

        except Exception:
            pass

    # ── MÉTODO 3: Wikipedia en español (fallback final) ─────────────────────────
    if not resultados:
        try:
            termino = urllib.parse.quote(query_limpia.replace(" ", "_"))
            url_wiki = f"https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query_limpia)}&format=json&utf8=1&srlimit=3"
            req = urllib.request.Request(url_wiki, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            for item in data.get("query", {}).get("search", [])[:max_resultados]:
                titulo = _limpiar_html(item.get("title", ""))
                snippet = _limpiar_html(item.get("snippet", ""))
                pagina = urllib.parse.quote(titulo.replace(" ", "_"))
                resultados.append({
                    "titulo": titulo,
                    "snippet": snippet[:350],
                    "url": f"https://es.wikipedia.org/wiki/{pagina}"
                })

        except Exception:
            pass

    return resultados[:max_resultados]


def formatear_contexto_web(resultados: list[dict]) -> tuple[str, list[dict]]:
    """
    Formatea los resultados web en un texto claro para el prompt de AUREX
    y devuelve la lista de fuentes limpias.
    """
    if not resultados:
        return "", []

    lineas = ["🛰️ INFORMACIÓN EN TIEMPO REAL DESDE EL RADAR WEB:"]
    for i, r in enumerate(resultados, 1):
        lineas.append(f"{i}. [{r['titulo']}]")
        lineas.append(f"   Fragmento: {r['snippet']}")
        lineas.append(f"   Fuente URL: {r['url']}\n")

    return "\n".join(lineas), resultados


def necesita_busqueda_web(pregunta: str, docs_encontrados: list) -> bool:
    """
    Determina si la consulta del Jefe requiere internet.
    Cubre: precios, estrenos, noticias, versiones, eventos actuales, personas,
    y cualquier pregunta factual cuando no hay documentos locales relevantes.
    """
    p = pregunta.lower().strip()

    # ── Disparadores EXPLÍCITOS de búsqueda ─────────────────────────────────────
    disparadores_explicitos = [
        "busca en internet", "busca en la web", "buscar en internet", "buscar en la web",
        "googlea", "rastrea", "investiga en la web", "en internet", "en la red",
        "busca online", "encuentra en internet",
    ]
    if any(d in p for d in disparadores_explicitos):
        return True

    # ── Precios y compras ────────────────────────────────────────────────────────
    disparadores_precio = [
        "precio", "precios", "cuanto cuesta", "cuánto cuesta",
        "donde comprar", "dónde comprar", "cotizacion", "cotización",
        "mercado actual", "costo", "valor de", "tarifa",
    ]
    if any(d in p for d in disparadores_precio):
        return True

    # ── Noticias y actualidad ────────────────────────────────────────────────────
    disparadores_actualidad = [
        "noticias", "actualidad", "hoy", "reciente", "últimas", "ultimas",
        "novedades", "última hora", "lo mas nuevo", "lo más nuevo",
    ]
    if any(d in p for d in disparadores_actualidad):
        return True

    # ── Estrenos, lanzamientos, fechas de eventos ────────────────────────────────
    disparadores_estreno = [
        "se estrena", "estreno", "cuando sale", "cuándo sale", "fecha de estreno",
        "fecha de lanzamiento", "cuando lanza", "cuándo lanza", "cuando llega",
        "cuándo llega", "lanzamiento", "sale el", "estrena el",
        "sale cuando", "nueva temporada", "temporada nueva", "capitulo",
        "capitulos", "pelicula", "película", "serie", "trailer", "tráiler",
    ]
    if any(d in p for d in disparadores_estreno):
        return True

    # ── Tecnología y versiones ───────────────────────────────────────────────────
    disparadores_tech = [
        "version actual", "versión actual", "ultima version", "última versión",
        "datasheet", "hoja de datos", "especificaciones de", "compatible con",
        "review de", "comparativa", "vs ", " vs",
    ]
    if any(d in p for d in disparadores_tech):
        return True

    # ── Clima ────────────────────────────────────────────────────────────────────
    if any(d in p for d in ["clima", "tiempo hoy", "temperatura hoy", "lluvia hoy"]):
        return True

    # ── Personas, lugares, eventos sin docs locales ──────────────────────────────
    if not docs_encontrados:
        disparadores_sin_docs = [
            "quién es", "quien es", "qué es", "que es",
            "qué pasó", "que paso", "cuándo fue", "cuando fue",
            "dónde está", "donde esta", "dónde queda", "donde queda",
            "cuántos", "cuantos", "cuándo nació", "cuando nacio",
            "cuándo murió", "cuando murio", "historia de",
        ]
        if any(w in p for w in disparadores_sin_docs):
            return True

        # Si no hay docs y la pregunta es larga (>4 palabras) y no es de ingeniería
        palabras_ingenieria = [
            "codigo", "código", "programa", "arduino", "esp32", "sensor",
            "resistencia", "voltaje", "corriente", "circuito", "motor",
            "servo", "pwm", "i2c", "spi", "uart", "robot", "pid",
        ]
        palabras_p = p.split()
        es_pregunta_larga = len(palabras_p) >= 4
        es_ingenieria = any(ing in p for ing in palabras_ingenieria)

        if es_pregunta_larga and not es_ingenieria:
            # Detectar si parece una pregunta sobre un hecho concreto
            indicadores_factual = [
                "cuando", "cuándo", "quien", "quién", "cual", "cuál",
                "donde", "dónde", "cuanto", "cuánto", "que dia", "qué día",
                "en que año", "en qué año", "como se llama",
            ]
            if any(ind in p for ind in indicadores_factual):
                return True

    return False
