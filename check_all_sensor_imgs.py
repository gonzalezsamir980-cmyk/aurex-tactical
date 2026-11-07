import sys
sys.path.append(r'C:\Users\samir\.gemini\antigravity\scratch\mi-ia-local')
from sensores_data import CATALOGO_SENSORES
import urllib.request

for k, v in CATALOGO_SENSORES.items():
    u = v.get('imagen_url', '')
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as r:
            print(f"{k}: OK {r.status}")
    except Exception as e:
        print(f"{k}: FAILED {e} ({u})")
