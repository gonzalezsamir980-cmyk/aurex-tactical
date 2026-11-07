import urllib.request, json

def test_wiki_direct(filename):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles=File:{filename}&prop=imageinfo&iiprop=url&iiurlwidth=400&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'AurexApp/1.0 (test@local)'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
            pages = data['query']['pages']
            for p in pages.values():
                info = p.get('imageinfo', [{}])[0]
                thumb = info.get('thumburl')
                print(f"{filename} -> thumb: {thumb}")
                # test fetching thumb
                req_img = urllib.request.Request(thumb, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_img, timeout=5) as r_img:
                    print(f"  Fetch status: {r_img.status}")
    except Exception as e:
        print(f"{filename} error: {e}")

if __name__ == '__main__':
    test_wiki_direct('Float_switch_off.jpg')
    test_wiki_direct('HC-SR04_Ultrasonic_Sensor.jpg')
