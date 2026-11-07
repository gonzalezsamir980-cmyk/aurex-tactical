import urllib.request
import urllib.parse
import re

q = "que dia se estrena doomsday avengers"
url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})

try:
    with urllib.request.urlopen(req, timeout=8) as r:
        html = r.read().decode("utf-8", errors="ignore")
        print("Longitud HTML:", len(html))
        # Extraer bloques de resultados completos
        snippets = re.findall(r'<a class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
        titulos = re.findall(r'<a class="result__url"[^>]*href="([^"]+)"', html)
        print(f"Snippets encontrados: {len(snippets)}")
        for s in snippets[:3]:
            limpio = re.sub(r'<[^>]+>', '', s).strip()
            print("->", limpio[:120])
except Exception as e:
    print("Error:", e)
