import urllib.request

url = "https://w.wiki/GHai"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=5) as r:
        print("Redirected to:", r.geturl())
        content = r.read().decode('utf-8', errors='ignore')
        print("Content snippet:", content[:1000])
except Exception as e:
    print("Error:", e)
