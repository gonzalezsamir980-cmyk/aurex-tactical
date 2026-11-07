import urllib.request, urllib.parse, json, re

def buscar_imagenes_ddg(query, max_results=3):
    vqd_url = 'https://duckduckgo.com/?q=' + urllib.parse.quote(query)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    req = urllib.request.Request(vqd_url, headers=headers)
    with urllib.request.urlopen(req, timeout=8) as r:
        html = r.read().decode('utf-8', errors='ignore')
    
    m = re.search(r'vqd=([0-9_\-]+)', html) or re.search(r'vqd="([0-9_\-]+)"', html)
    if not m:
        # Check alternative token
        m2 = re.search(r'vqd\s*=\s*[\'"]([0-9_\-]+)[\'"]', html)
        if m2:
            vqd = m2.group(1)
        else:
            return f"no vqd found in html (len={len(html)})"
    else:
        vqd = m.group(1)
        
    img_url = f'https://duckduckgo.com/i.js?l=es-es&o=json&q={urllib.parse.quote(query)}&vqd={vqd}&f=,,,&p=1'
    req2 = urllib.request.Request(img_url, headers=headers)
    with urllib.request.urlopen(req2, timeout=8) as r2:
        data = json.loads(r2.read().decode('utf-8'))
        return [{'title': x.get('title'), 'image': x.get('image'), 'thumbnail': x.get('thumbnail'), 'url': x.get('url')} for x in data.get('results', [])[:max_results]]

if __name__ == '__main__':
    try:
        res = buscar_imagenes_ddg('sensor de nivel flotador')
        print('Result:', res)
    except Exception as e:
        print('Error:', e)
