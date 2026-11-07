#!/usr/bin/env python3
"""Independent verification for the v3.0 Upper Body 12-Week page.
Parses the BUILT page (index.html) itself and asserts SPEC_V3 §5 requirements.
"""
import json, re, os, sys

PAGE = os.path.expanduser("~/Upper-Body-12-Week/index.html")
html = open(PAGE, encoding="utf-8").read()
fails = []

def check(cond, msg):
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        fails.append(msg)

# 1. Parse the page's OWN station data blob and assert no ss pair has 2 equipments.
m = re.search(r'<script id="station-data" type="application/json">(.*?)</script>', html, re.S)
check(bool(m), "page contains embedded #station-data JSON")
station_meta = json.loads(m.group(1)) if m else []
pairs = [s for s in station_meta if s["kind"] == "ss"]
bad = [s["station"] for s in pairs if len({i["equipment"] for i in s["items"]}) > 1]
print(f"      superset pairs parsed from built page: {len(pairs)}")
check(not bad, f"AUTOMATED ASSERTION: no superset pair contains two different equipment labels (bad={bad})")

# 2. Every §3 equipment label appears verbatim.
EQUIP = ["Barbell + flat bench", "Dumbbells + flat bench", "Dumbbells",
         "Cable stack — high pulley", "Floor", "Barbell — standing, one bar",
         "Pull-up bar", "Dumbbells + bench", "Dip station", "Floor / mat",
         "Barbell rack — low bar"]
for lab in EQUIP:
    check(lab in html, f"equipment label present: {lab!r}")

# 3. New superset sentence + loads note.
check("Supersets are paired on the same equipment — set up once and stay put. "
      "Do a then b back-to-back and rest after b; move to the next station during your rest." in html,
      "same-equipment superset sentence present")
check("If the two exercises in a pair need different loads, put both sets of weights "
      "at the station before you start the pair." in html, "put both loads at the station note present")

# 4. Every §4 time value.
TIMES = ["37 min", "38 min", "41 min", "39 min", "25 min",
         "34 min", "35 min", "40 min", "35 min", "24 min",
         "36 min", "36 min", "38 min", "36 min", "25 min",
         "33 min", "35 min", "38 min", "35 min", "23 min",
         "35-45 min", "25-30 min", "29 min", "23 min", "15 min", "42 min", "26 min"]
missing = [t for t in TIMES if t not in html]
check(not missing, f"all §4 time values present (missing={missing})")

# 5. Still 68 unique gifs and 84 tracker cells.
uniq = set(re.findall(r'images/([A-Za-z0-9_\-]+\.gif)', html))
check(len(uniq) == 68, f"68 unique images/*.gif references (found {len(uniq)})")
check(html.count("data-key=") == 84, f"84 tracker cells (found {html.count('data-key=')})")

# 6. Retained markers.
for mk in ["≤ 45 min", "ExRx.net", "No leg exercises included by request.",
           "rest-timer", "STRENGTH A", "STRENGTH B", "STRENGTH C", "STRENGTH D",
           "CARDIO 1", "CARDIO 2", "CARDIO 3", "data-block"]:
    check(mk in html, f"retained marker present: {mk!r}")

# 7. Every station label from §3 present.
LABELS = ["A1","A2a","A2b","A3a","A3b","A4","A5",
          "B1a","B1b","B2a","B2b","B3","B4a","B4b",
          "C1a","C1b","C2a","C2b","C3a","C3b","C4a","C4b",
          "D1","D2a","D2b","D3a","D3b","D4"]
miss_lab = [l for l in LABELS if f'>{l}<' not in html]
check(not miss_lab, f"all §3 station labels present (missing={miss_lab})")

print()
if fails:
    print(f"{len(fails)} CHECK(S) FAILED")
    sys.exit(1)
print("ALL CHECKS PASSED")
