import urllib.request

test_sizes = ["320px", "500px", "800px", "1024px"]
base = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Arduino_Uno_-_R3.jpg/"

for s in test_sizes:
    u = base + s + "-Arduino_Uno_-_R3.jpg"
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as r:
            print(f"Size {s}: OK {r.status}")
    except Exception as e:
        print(f"Size {s}: FAILED {e}")

# Also test original (no /thumb/)
u_orig = "https://upload.wikimedia.org/wikipedia/commons/8/87/Arduino_Uno_-_R3.jpg"
try:
    req = urllib.request.Request(u_orig, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=4) as r:
        print(f"Original: OK {r.status}")
except Exception as e:
    print(f"Original: FAILED {e}")
