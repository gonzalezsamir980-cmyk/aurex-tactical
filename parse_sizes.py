import urllib.request, re

url = "https://www.mediawiki.org/wiki/Common_thumbnail_sizes"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=5) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Find sizes
for m in re.finditer(r'([0-9]+px)', html):
    print(m.group(1))
