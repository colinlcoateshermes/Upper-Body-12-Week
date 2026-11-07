#!/usr/bin/env python3
"""Download all 68 ExRx GIFs per SPEC.md rules."""
import json, os, subprocess, time, sys

SPEC = "/home/hermes/upper-body-spec/exercises.json"
OUT = os.path.expanduser("~/Upper-Body-12-Week/images")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

os.makedirs(OUT, exist_ok=True)
data = json.load(open(SPEC))
ex = [e for cat in data.values() for e in cat]
print(f"total exercises: {len(ex)}")

def dl(e):
    dest = os.path.join(OUT, e["file"])
    return subprocess.run(
        ["curl", "-sS", "-A", UA, "-e", e["exrx"], "-o", dest,
         "-w", "%{http_code}", e["gif"]],
        capture_output=True, text=True)

results = []
for i, e in enumerate(ex, 1):
    dest = os.path.join(OUT, e["file"])
    ok = False
    for attempt in range(4):  # initial + 3 retries
        r = dl(e)
        code = r.stdout.strip()
        if code == "200":
            break
        if code == "429" and attempt < 3:
            backoff = [5, 15, 15][attempt]
            print(f"  429 on {e['file']} attempt {attempt+1}, sleeping {backoff}s")
            time.sleep(backoff)
            continue
        break
    # verify
    good = False
    size = os.path.getsize(dest) if os.path.exists(dest) else 0
    magic = ""
    if size:
        with open(dest, "rb") as f:
            magic = f.read(4).decode("latin-1")
    good = magic.startswith("GIF8") and size > 20 * 1024
    results.append((e["file"], code, size, magic, good))
    print(f"[{i:2d}/68] {e['file']:38s} http={code} size={size:7d} magic={magic!r} {'OK' if good else 'FAIL'}")
    time.sleep(1.5)

bad = [r for r in results if not r[4]]
print(f"\nVerified OK: {len(results)-len(bad)}/68")
if bad:
    print("FAILURES:")
    for b in bad:
        print("  ", b)
    sys.exit(1)
