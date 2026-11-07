import urllib.request, urllib.parse, json

def buscar_imagenes_wikimedia(query, max_results=3):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&gsrsearch={urllib.parse.quote(query)}&gsrlimit={max_results}&prop=imageinfo&iiprop=url|mime&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'AurexBot/1.0 (contact@local.ia)'})
    try:
        with urllib.request.urlopen(req, timeout=6) as r:
            data = json.loads(r.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            results = []
            for p in pages.values():
                info = p.get('imageinfo', [{}])[0]
                img_url = info.get('url')
                if img_url:
                    results.append({'title': p.get('title'), 'url': img_url})
            return results
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    print('Wikimedia:', buscar_imagenes_wikimedia('float level sensor'))
    print('Wikimedia es:', buscar_imagenes_wikimedia('sensor flotador'))
