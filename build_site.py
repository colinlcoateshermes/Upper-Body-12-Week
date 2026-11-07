#!/usr/bin/env python3
"""Generate the self-contained index.html for the Upper Body 12-Week site.

v2.0 — hard 45-minute session cap. Superset restructure (4 stations/day), new
periodisation, per-session time badges that follow the block selector, and a
per-card rest timer. See /home/hermes/upper-body-spec/SPEC_V2.md.
"""
import json, os

SPEC = "/home/hermes/upper-body-spec/exercises.json"
OUT = os.path.expanduser("~/Upper-Body-12-Week/index.html")

data = json.load(open(SPEC))
EX = {e["key"]: e for cat in data.values() for e in cat}
CATS = list(data.keys())  # chest, back, shoulders, biceps, triceps, forearms, core, cardio
CAT_LABEL = {
    "chest": "Chest", "back": "Back", "shoulders": "Shoulders", "biceps": "Biceps",
    "triceps": "Triceps", "forearms": "Forearms", "core": "Core", "cardio": "Cardio",
}

# ============================================================
# STRENGTH — 4 numbered stations per day, mostly antagonist supersets
# station = (label, kind, items); items = (key, role, note)
# kind: "solo" | "ss" | "tri"   role: main | other | core | finisher
# ============================================================
STRENGTH = {
    "A": {
        "title": "STRENGTH A — Push",
        "sub": "Chest · Front Delts · Triceps",
        "intro": "Antagonist supersets: do a and b back-to-back, rest only after the b exercise.",
        "stations": [
            ("A1", "solo", [("bb-bench-press", "main",
                "Main lift. Rest fully at 105s in block 3 — this is the one lift worth the long rest.")]),
            ("A2", "ss", [("bb-incline-bench-press", "other", "SS with A2b"),
                          ("db-fly", "other", "SS with A2a")]),
            ("A3", "ss", [("bb-military-press", "other", "Standing, brace hard, no leg drive."),
                          ("db-lateral-raise", "other", "SS with A3a")]),
            ("A4", "ss", [("cable-pushdown", "other", "SS with A4b"),
                          ("push-up", "finisher", "Finisher: 1 set, to near-failure.")]),
        ],
        "swaps": ["db-incline-bench-press", "db-incline-fly", "chest-dip", "bench-dip"],
    },
    "B": {
        "title": "STRENGTH B — Pull",
        "sub": "Back · Rear Delts · Traps · Biceps",
        "intro": "Antagonist supersets: pull, then the a/b pairs back-to-back with rest after b.",
        "stations": [
            ("B1", "solo", [("bb-bent-over-row", "main",
                "Main lift. Control the eccentric, no torso heave.")]),
            ("B2", "ss", [("pull-up", "other", "Use a band or the assisted machine if you cannot get 6 clean reps."),
                          ("cable-rear-delt-row", "other", "SS with B2a — rope attachment, pull to the face.")]),
            ("B3", "ss", [("db-bent-over-row", "other", "SS with B3b — single-arm, brace on a bench."),
                          ("bb-shrug", "other", "SS with B3a")]),
            ("B4", "ss", [("bb-curl", "other", "SS with B4b — no swing, strict tempo."),
                          ("db-hammer-curl", "other", "SS with B4a — neutral grip, elbows fixed.")]),
        ],
        "swaps": ["chin-up", "lat-pulldown", "close-grip-pulldown", "seated-row", "db-shrug"],
    },
    "C": {
        "title": "STRENGTH C — Shoulders &amp; Arms",
        "sub": "Delts · Triceps · Biceps · (optional forearms)",
        "intro": "Pressing and raises for all three delt heads, then arm isolation — superset as usual.",
        "stations": [
            ("C1", "solo", [("db-shoulder-press", "main", "Seated, back supported.")]),
            ("C2", "ss", [("bb-upright-row", "other", "SS with C2b — wide grip to spare the shoulders."),
                          ("db-lateral-raise", "other", "SS with C2a — strict, light, lead with the elbows.")]),
            ("C3", "ss", [("close-grip-bench-press", "other", "SS with C3b — shoulder-width grip, elbows tucked."),
                          ("db-rear-lateral-raise", "other", "SS with C3a — chest supported, tiny weights.")]),
            ("C4", "ss", [("skull-crusher", "other", "SS with C4b — control the bar to the forehead."),
                          ("db-concentration-curl", "other", "SS with C4a — brace the elbow on the thigh.")]),
        ],
        "optional": ["bb-preacher-curl", "db-arnold-press", "db-front-raise",
                     "bb-wrist-curl", "bb-reverse-wrist-curl", "bb-reverse-curl",
                     "db-triceps-extension", "db-kickback"],
    },
    "D": {
        "title": "STRENGTH D — Upper-body Hypertrophy + Core",
        "sub": "Bodyweight pushes/pulls · Core",
        "intro": "Higher-rep bodyweight and cable supersets, finishing with a core triset.",
        "stations": [
            ("D1", "ss", [("chest-dip", "other", "SS with D1b — lean forward for the chest."),
                          ("inverted-row", "other", "SS with D1a — bodyweight horizontal pull.")]),
            ("D2", "ss", [("push-up", "other", "SS with D2b — elevate feet or add a vest to progress."),
                          ("cable-lying-fly", "other", "SS with D2a — constant tension on the pecs.")]),
            ("D3", "ss", [("db-kickback", "other", "SS with D3b — elbow high and fixed."),
                          ("db-curl", "other", "SS with D3a — alternating dumbbell curl.")]),
            ("D4", "tri", [("crunch", "core", "Controlled, no neck pulling."),
                           ("hanging-leg-hip-raise", "core", "Ab strap or bar."),
                           ("superman", "core", "Lower-back / spinal erectors.")]),
        ],
        "core_options": ["crunch-arms-crossed", "sit-up", "weighted-incline-sit-up",
                         "cable-kneeling-crunch", "cable-seated-crunch", "twisting-crunch",
                         "db-side-bend", "bird-dog"],
    },
}

CARDIO = {
    "1": {
        "title": "CARDIO 1 — Easy Zone 1–2 steady state",
        "day": "Tuesday",
        "prescription": [
            "5 min easy warm-up",
            "25–35 min continuous at a conversational pace (Zone 1–2) — never exceed 35 min of main work",
            "5 min cool-down (total 35–45 min)",
        ],
        "note": "Keep it low-impact and truly easy — it must not compromise Wednesday's pull session. Pick any modality below.",
        "mods": ["treadmill-walk", "cycle-ergometer", "elliptical-trainer", "row-ergometer"],
        "presets": [60, 120, 180],
    },
    "2": {
        "title": "CARDIO 2 — Intervals / conditioning",
        "day": "Thursday",
        "prescription": [
            "8 min warm-up, then by block:",
            "Block 1: 6 × (30s hard / 90s easy) · Block 2: 8 × (30s / 90s)",
            "Block 3: 8 × (30s / 60s) · Block 4: 10 × (20s hard / 40s easy)",
            "Block 5: 15 min easy only",
            "5 min cool-down — max total 30 min",
        ],
        "note": "Hard means genuinely hard but repeatable — never all-out on a no-rest-day week.",
        "mods": ["treadmill-run", "row-ergometer", "cycle-ergometer",
                 "ski-ergometer", "stair-climber", "stepmill"],
        "presets": [20, 30, 40, 60, 90],
    },
    "3": {
        "title": "CARDIO 3 — Bodyweight / mixed-modal circuit",
        "day": "Saturday",
        "prescription": [
            "5 min warm-up, then 40s work / 20s rest through the 8-move circuit:",
            "Block 1–2: 3 rounds · Block 3–4: 4 rounds (hard cap — never 5) · Block 5: 2 easy rounds",
            "One round = 8 min · 5 min cool-down — max total 42 min",
        ],
        "note": "Hard cap of 4 rounds on blocks 3–4 — adding a 5th round breaks the 45-minute cap, and Sunday is Strength D.",
        "mods": ["jumping-jack", "high-knee-run", "burpee", "mountain-climber",
                 "jump-rope", "bear-crawl", "lateral-shuffle", "arm-ergometer"],
        "presets": [20, 40],
    },
}

# ---- periodisation (new, SPEC_V2 §2) ----
BLOCKS = [
    ("1 — Foundation", "1–3", "3 / 3", "10–12", "main 75s · other 45–60s", "7"),
    ("2 — Volume", "4–6", "3 / 3", "8–10", "main 90s · other 60–75s", "8"),
    ("3 — Strength", "7–9", "4 / 3", "6–8", "main 105s · other 60–75s", "8–9"),
    ("4 — Peak Overload", "10–11", "main 3 (top set + 2 back-off @ −10%) / other 4", "5–8",
     "main 105s · other 60–75s", "9"),
    ("5 — Deload &amp; Retest", "12", "2 / 2", "8–10 @ ~60% of week-11 load", "45–60s", "5–6"),
]

# per-block sets / reps / rest by role
BLKSCHEME = {
    1: {"main": ("3", "10–12", "75s"), "other": ("3", "10–12", "45–60s"),
        "core": ("3", "12–20", "45s"), "finisher": ("1", "to near-failure", "—")},
    2: {"main": ("3", "8–10", "90s"), "other": ("3", "8–10", "60–75s"),
        "core": ("3", "15–20", "45s"), "finisher": ("1", "to near-failure", "—")},
    3: {"main": ("4", "6–8", "105s"), "other": ("3", "6–8", "60–75s"),
        "core": ("3", "12–15", "45s"), "finisher": ("1", "to near-failure", "—")},
    4: {"main": ("3 (top + 2 back-off @ −10%)", "5–8", "105s"), "other": ("4", "5–8", "60–75s"),
        "core": ("4", "15–20", "45s"), "finisher": ("1", "to near-failure", "—")},
    5: {"main": ("2", "8–10 @ 60%", "45–60s"), "other": ("2", "8–10 @ 60%", "45–60s"),
        "core": ("2", "15 easy", "45s"), "finisher": ("1", "easy set", "—")},
}
RPE = {1: "7", 2: "8", 3: "8–9", 4: "9", 5: "5–6"}

# per-block session times (SPEC_V2 §4)
TIME = {
    "A": ["35 min", "36 min", "41 min", "39 min", "24 min"],
    "B": ["35 min", "36 min", "41 min", "39 min", "24 min"],
    "C": ["35 min", "35 min", "39 min", "41 min", "24 min"],
    "D": ["38 min", "39 min", "41 min", "41 min", "27 min"],
}
CARDIO_TIME = {
    "1": ["35-45 min", "35-45 min", "35-45 min", "35-45 min", "25-30 min"],
    "2": ["25 min", "29 min", "29 min", "23 min", "15 min"],
    "3": ["34 min", "34 min", "42 min", "42 min", "26 min"],
}

WEEK = [
    ("Monday", "STRENGTH A", "strength"), ("Tuesday", "CARDIO 1", "cardio"),
    ("Wednesday", "STRENGTH B", "strength"), ("Thursday", "CARDIO 2", "cardio"),
    ("Friday", "STRENGTH C", "strength"), ("Saturday", "CARDIO 3", "cardio"),
    ("Sunday", "STRENGTH D", "strength"),
]

STRENGTH_PRESETS = [45, 60, 75, 90, 105]


def scheme_str(role, b, lead=False):
    sets, reps, rest = BLKSCHEME[b].get(role, BLKSCHEME[b]["other"])
    s = f"{sets} × {reps}"
    s += " · straight into b" if lead else f" · rest {rest}"
    return f"{s} · RPE {RPE[b]}"


def time_badge(times):
    spans = "".join(
        f'<span class="scheme" data-block="{b}">{times[b-1]}</span>' for b in range(1, 6)
    )
    return f'<span class="time-badge" title="Session length by block">⏱ {spans}</span>'


def rest_timer(tid, presets):
    btns = "".join(
        f'<button class="rt-preset" data-sec="{p}">{p}s</button>' for p in presets
    )
    return (
        f'<div class="rest-timer" data-timer="{tid}">'
        f'<span class="rt-label">Rest timer</span>'
        f'<span class="rt-display">0:00</span>'
        f'{btns}'
        f'<button class="rt-start">Start</button>'
        f'<button class="rt-reset">Reset</button>'
        f'</div>'
    )


# ---- exercise row ----
def ex_row(key, role, note, label, lead):
    e = EX[key]
    spans = "".join(
        f'<span class="scheme" data-block="{b}">{scheme_str(role, b, lead)}</span>' for b in range(1, 6)
    )
    note_html = f'<div class="ex-note">{note}</div>' if note else ""
    return (
        f'<div class="ex-item" data-role="{role}">'
        f'<a class="thumb" href="images/{e["file"]}" onclick="return lightbox(event,this)">'
        f'<img src="images/{e["file"]}" alt="{e["name"]}" loading="lazy"></a>'
        f'<div class="ex-body">'
        f'<span class="station-badge">{label}</span> '
        f'<a class="ex-name" href="{e["exrx"]}" target="_blank" rel="noopener">{e["name"]}</a>'
        f'<div class="ex-scheme">{spans}<span class="role-tag">{role if role != "other" else "accessory"}</span></div>'
        f'{note_html}'
        f'</div></div>'
    )


def station_html(label, kind, items):
    tag = {"ss": '<span class="ss-tag">SUPERSET</span>',
           "tri": '<span class="tri-tag">TRISET</span>',
           "solo": ""}[kind]
    rows = []
    for i, (key, role, note) in enumerate(items):
        sub = label if kind == "solo" else label + ("abc"[i])
        lead = (kind in ("ss", "tri")) and i < len(items) - 1
        rows.append(ex_row(key, role, note, sub, lead))
    return (
        f'<div class="station">'
        f'<div class="station-head"><span class="station-label">{label}</span>{tag}</div>'
        f'<div class="ex-list">{"".join(rows)}</div>'
        f'</div>'
    )


def cardio_mod(key):
    e = EX[key]
    return (
        f'<a class="lib-card" href="{e["exrx"]}" target="_blank" rel="noopener">'
        f'<img src="images/{e["file"]}" alt="{e["name"]}" loading="lazy">'
        f'<div class="lib-name">{e["name"]}</div></a>'
    )


# ---------- build strength cards ----------
strength_html = []
for day in "ABCD":
    d = STRENGTH[day]
    stations = "".join(station_html(lbl, kind, items) for lbl, kind, items in d["stations"])
    extra = ""
    if "optional" in d:
        opt_rows = "".join(ex_row(k, "other", "", "opt", False) for k in d["optional"])
        extra = (
            '<div class="section-title" style="margin-top:14px">Optional — only if the clock allows</div>'
            f'<div class="ex-list">{opt_rows}</div>'
        )
    if "core_options" in d:
        opt_rows = "".join(ex_row(k, "core", "", "core", False) for k in d["core_options"])
        extra = (
            '<div class="section-title" style="margin-top:14px">Rotate the core triset each week with</div>'
            f'<div class="ex-list">{opt_rows}</div>'
        )
    strength_html.append(f'''
    <div class="day-card" id="card-{day}" data-card="{day}">
      <div class="day-header" onclick="toggleCard('{day}')">
        <div>
          <h2>{d["title"]}</h2>
          <div class="day-sub">{d["sub"]}</div>
        </div>
        <div class="day-right">
          {time_badge(TIME[day])}
          <span class="collapse-icon">▾</span>
        </div>
      </div>
      <div class="day-body">
        <div class="intro">{d["intro"]}</div>
        {stations}
        {extra}
        {rest_timer("card-" + day, STRENGTH_PRESETS)}
      </div>
    </div>''')

# ---------- build cardio cards ----------
cardio_html = []
for num in "123":
    c = CARDIO[num]
    mods = "".join(cardio_mod(k) for k in c["mods"])
    presc = "".join(f"<li>{p}</li>" for p in c["prescription"])
    cardio_html.append(f'''
    <div class="day-card cardio-card" id="card-C{num}">
      <div class="day-header static">
        <div>
          <h2>{c["title"]}</h2>
          <div class="day-sub">{c["day"]}</div>
        </div>
        <div class="day-right">
          {time_badge(CARDIO_TIME[num])}
        </div>
      </div>
      <div class="day-body">
        <ul class="presc">{presc}</ul>
        <div class="intro">{c["note"]}</div>
        <div class="lib-grid small">{mods}</div>
        {rest_timer("card-C" + num, c["presets"])}
      </div>
    </div>''')

# ---------- library ----------
lib_html = []
for cat in CATS:
    cards = "".join(
        f'<a class="lib-card" href="{e["exrx"]}" target="_blank" rel="noopener">'
        f'<img src="images/{e["file"]}" alt="{e["name"]}" loading="lazy">'
        f'<div class="lib-name">{e["name"]}</div></a>'
        for e in data[cat]
    )
    lib_html.append(
        f'<div class="section-title">{CAT_LABEL[cat]} ({len(data[cat])})</div>'
        f'<div class="lib-grid">{cards}</div>'
    )

# ---------- tracker ----------
tracker_rows = []
for w in range(1, 13):
    deload = (w == 12)
    cells = []
    for di, (dow, sess, kind) in enumerate(WEEK):
        key = f"w{w}d{di+1}"
        cells.append(
            f'<div class="tcell {kind}" data-key="{key}" data-kind="{kind}" onclick="toggleDay(\'{key}\',this)">'
            f'<span class="tday">D{di+1}</span><span class="tsess">{sess}</span></div>'
        )
    tracker_rows.append(
        f'<div class="trow{" deload" if deload else ""}">'
        f'<div class="tweek">Wk {w}{" <em>(deload)</em>" if deload else ""}</div>'
        + "".join(cells) + "</div>"
    )

# ---------- periodisation rows ----------
block_rows = "".join(
    f'<tr><td class="bname">{b[0]}</td><td>{b[1]}</td><td>{b[2]}</td><td>{b[3]}</td><td>{b[4]}</td><td>{b[5]}</td></tr>'
    for b in BLOCKS
)

week_strip = "".join(
    f'<div class="wcell {kind}"><div class="wdow">{dow}</div><div class="wsess">{sess}</div></div>'
    for dow, sess, kind in WEEK
)

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Upper Body 12-Week — Strength + Cardio, No Rest Days</title>
<style>
  :root {{
    --bg:#0d1117; --card:#161b22; --border:#30363d; --text:#c9d1d9;
    --text-dim:#8b949e; --accent:#58a6ff; --green:#3fb950; --orange:#d29922;
    --red:#f85149; --purple:#bc8cff;
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{
    font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
    background:var(--bg); color:var(--text); line-height:1.6;
    -webkit-tap-highlight-color:transparent;
  }}
  .container {{ max-width:1100px; margin:0 auto; padding:12px; }}
  a {{ color:var(--accent); text-decoration:none; }}
  a:hover {{ text-decoration:underline; }}

  /* Header */
  .header {{
    background:linear-gradient(135deg,#161b22,#131a2a);
    border:1px solid var(--border); border-radius:12px; padding:22px; margin-bottom:16px;
  }}
  .header h1 {{ font-size:1.7em; color:#fff; margin-bottom:4px; }}
  .header .subtitle {{ color:var(--text-dim); font-size:0.9em; }}
  .stats-bar {{ display:flex; gap:10px; margin-top:16px; flex-wrap:wrap; align-items:stretch; }}
  .stat {{
    background:var(--bg); border:1px solid var(--border); border-radius:8px;
    padding:10px 14px; text-align:center; flex:1; min-width:76px;
  }}
  .stat .num {{ font-size:1.35em; font-weight:700; color:var(--green); }}
  .stat .label {{ font-size:0.72em; color:var(--text-dim); text-transform:uppercase; letter-spacing:.4px; }}
  .chip-cap {{
    display:flex; align-items:center; gap:6px; background:#1f6feb1a; border:1px solid #1f6feb;
    color:var(--accent); border-radius:8px; padding:10px 16px; font-weight:700; font-size:1em;
    white-space:nowrap;
  }}

  .card {{
    background:var(--card); border:1px solid var(--border); border-radius:12px;
    padding:18px; margin-bottom:16px;
  }}
  h2.sec {{ font-size:1.15em; color:#fff; margin-bottom:10px; }}
  .section-title {{
    font-size:0.85em; font-weight:700; text-transform:uppercase; color:var(--accent);
    margin-bottom:8px; letter-spacing:.5px;
  }}
  .notes p {{ margin-bottom:8px; font-size:0.9em; }}
  .notes .warn {{ color:var(--orange); }}
  .rule {{
    background:var(--bg); border-left:3px solid var(--accent); border-radius:6px;
    padding:10px 14px; margin:10px 0; font-size:0.9em; color:#fff;
  }}

  /* Periodisation table */
  table {{ width:100%; border-collapse:collapse; font-size:0.82em; }}
  th, td {{ border:1px solid var(--border); padding:8px 10px; text-align:left; vertical-align:top; }}
  th {{ background:var(--bg); color:var(--accent); font-size:0.8em; text-transform:uppercase; }}
  td.bname {{ color:#fff; font-weight:600; white-space:nowrap; }}
  .table-wrap {{ overflow-x:auto; }}

  /* Weekly strip */
  .week-strip {{ display:grid; grid-template-columns:repeat(7,1fr); gap:6px; }}
  .wcell {{ border:1px solid var(--border); border-radius:8px; padding:8px 6px; text-align:center; }}
  .wcell.strength {{ border-color:#1f6feb; background:#1f6feb1a; }}
  .wcell.cardio {{ border-color:#238636; background:#2386361a; }}
  .wcell .wdow {{ font-size:0.7em; color:var(--text-dim); text-transform:uppercase; }}
  .wcell .wsess {{ font-size:0.75em; font-weight:600; color:#fff; margin-top:3px; }}

  /* Day cards */
  .day-card {{ background:var(--card); border:1px solid var(--border); border-radius:12px; margin-bottom:14px; overflow:hidden; }}
  .day-card.cardio-card {{ border-left:3px solid var(--green); }}
  .day-header {{
    display:flex; justify-content:space-between; align-items:center; gap:8px;
    padding:14px 16px; cursor:pointer;
  }}
  .day-header.static {{ cursor:default; }}
  .day-card[data-card] .day-header:hover {{ background:#1c2333; }}
  .day-header h2 {{ font-size:1.05em; color:#fff; }}
  .day-sub {{ font-size:0.78em; color:var(--text-dim); }}
  .day-right {{ display:flex; align-items:center; gap:10px; flex-shrink:0; }}
  .collapse-icon {{ font-size:0.8em; color:var(--text-dim); transition:transform .2s; }}
  .day-card.collapsed .collapse-icon {{ transform:rotate(-90deg); }}
  .day-card.collapsed .day-body {{ display:none; }}
  .day-body {{ padding:0 16px 16px; }}
  .intro {{ font-size:0.85em; color:var(--text-dim); margin-bottom:10px; }}
  .presc {{ margin:0 0 10px 18px; font-size:0.87em; }}
  .presc li {{ margin-bottom:3px; }}

  /* Time badge */
  .time-badge {{
    display:inline-flex; align-items:center; gap:4px; background:#2386361a; border:1px solid #238636;
    color:var(--green); border-radius:20px; padding:3px 10px; font-size:0.72em; font-weight:700;
    white-space:nowrap;
  }}

  /* Station / superset */
  .station {{ margin-bottom:12px; }}
  .station-head {{ display:flex; align-items:center; gap:8px; margin:4px 0 6px; }}
  .station-label {{
    font-size:0.78em; font-weight:700; color:#fff; background:var(--bg);
    border:1px solid var(--border); border-radius:6px; padding:2px 9px;
  }}
  .ss-tag {{
    font-size:0.6em; font-weight:700; letter-spacing:.6px; color:var(--purple);
    border:1px solid var(--purple); border-radius:10px; padding:1px 8px;
  }}
  .tri-tag {{
    font-size:0.6em; font-weight:700; letter-spacing:.6px; color:var(--green);
    border:1px solid var(--green); border-radius:10px; padding:1px 8px;
  }}
  .station-badge {{
    display:inline-block; font-size:0.7em; font-weight:700; color:var(--accent);
    background:#1f6feb22; border:1px solid #1f6feb; border-radius:6px; padding:1px 7px;
    margin-right:6px; vertical-align:middle;
  }}

  /* Exercise list */
  .ex-list {{ display:flex; flex-direction:column; gap:8px; }}
  .ex-item {{
    display:flex; gap:12px; align-items:flex-start; background:var(--bg);
    border:1px solid var(--border); border-radius:8px; padding:10px;
  }}
  .ex-item .thumb {{ flex-shrink:0; display:block; }}
  .ex-item .thumb img {{
    width:150px; height:150px; object-fit:contain; background:#000;
    border:1px solid var(--border); border-radius:6px; display:block;
  }}
  .ex-body {{ min-width:0; flex:1; }}
  .ex-name {{ font-weight:600; color:#fff; font-size:0.95em; }}
  .ex-scheme {{ font-size:0.85em; color:var(--green); margin-top:4px; font-weight:600; }}
  .ex-note {{ font-size:0.8em; color:var(--text-dim); margin-top:4px; }}
  .role-tag {{
    display:inline-block; margin-left:8px; font-size:0.65em; text-transform:uppercase;
    color:var(--text-dim); border:1px solid var(--border); border-radius:10px; padding:1px 8px;
    vertical-align:middle; letter-spacing:.4px;
  }}
  .scheme {{ display:none; }}
  .scheme.active {{ display:inline; }}

  /* Rest timer */
  .rest-timer {{
    display:flex; align-items:center; gap:6px; flex-wrap:wrap; background:var(--bg);
    border:1px solid var(--border); border-radius:8px; padding:10px 12px; margin-top:14px;
  }}
  .rt-label {{ font-size:0.7em; text-transform:uppercase; color:var(--text-dim); letter-spacing:.5px; }}
  .rt-display {{
    font-size:1.3em; font-weight:700; color:#fff; min-width:58px; text-align:center;
    font-variant-numeric:tabular-nums;
  }}
  .rt-preset, .rt-start, .rt-reset {{
    padding:6px 11px; border:1px solid var(--border); border-radius:8px; background:var(--card);
    color:var(--text); cursor:pointer; font-size:0.8em;
  }}
  .rt-preset:hover, .rt-start:hover, .rt-reset:hover {{ background:#1c2333; }}
  .rt-preset.sel {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
  .rt-start {{ border-color:var(--green); color:var(--green); }}
  .rt-reset {{ border-color:var(--red); color:var(--red); }}
  .rest-timer.rt-done .rt-display {{ color:var(--green); }}

  /* Block selector */
  .block-bar {{ display:flex; gap:6px; flex-wrap:wrap; align-items:center; margin-bottom:14px; }}
  .block-bar .lbl {{ font-size:0.8em; color:var(--text-dim); margin-right:4px; }}
  .blk {{
    padding:7px 13px; border:1px solid var(--border); border-radius:8px; background:var(--card);
    color:var(--text); cursor:pointer; font-size:0.82em; transition:all .2s;
  }}
  .blk.active {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
  .blk:hover:not(.active) {{ background:#1c2333; }}

  /* Library grid */
  .lib-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:10px; margin-bottom:18px; }}
  .lib-grid.small {{ grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); }}
  .lib-card {{
    display:flex; flex-direction:column; background:var(--bg); border:1px solid var(--border);
    border-radius:8px; padding:8px; text-align:center;
  }}
  .lib-card:hover {{ border-color:var(--accent); text-decoration:none; }}
  .lib-card img {{
    width:100%; height:120px; object-fit:contain; background:#000;
    border-radius:6px; margin-bottom:6px;
  }}
  .lib-name {{ font-size:0.78em; color:var(--text); line-height:1.3; }}

  /* Tracker */
  .tprog {{ font-size:0.95em; font-weight:600; color:var(--green); margin-bottom:12px; }}
  .tracker {{ overflow-x:auto; }}
  .trow {{ display:grid; grid-template-columns:80px repeat(7,1fr); gap:5px; margin-bottom:5px; min-width:640px; }}
  .trow.deload .tweek {{ color:var(--orange); }}
  .tweek {{ font-size:0.75em; color:var(--text-dim); display:flex; align-items:center; font-weight:600; }}
  .tweek em {{ font-style:normal; }}
  .tcell {{
    border:1px solid var(--border); border-radius:6px; padding:6px 4px; text-align:center;
    cursor:pointer; user-select:none; transition:all .15s;
  }}
  .tcell.strength {{ border-color:#1f6feb66; }}
  .tcell.cardio {{ border-color:#23863666; }}
  .tcell:hover {{ background:#1c2333; }}
  .tcell .tday {{ display:block; font-size:0.62em; color:var(--text-dim); }}
  .tcell .tsess {{ display:block; font-size:0.68em; color:var(--text); font-weight:600; }}
  .tcell.done {{ background:var(--green); border-color:var(--green); }}
  .tcell.done .tday, .tcell.done .tsess {{ color:#04140a; }}

  .io-bar {{ display:flex; gap:8px; flex-wrap:wrap; margin-bottom:16px; }}
  .io-btn {{
    padding:8px 14px; border:1px solid var(--border); border-radius:8px; background:var(--card);
    color:var(--accent); cursor:pointer; font-size:0.82em;
  }}
  .io-btn:hover {{ background:#1c2333; }}
  .reset-btn {{
    display:block; width:100%; padding:12px; background:var(--card); border:1px solid var(--red);
    border-radius:8px; color:var(--red); cursor:pointer; font-size:0.9em; margin-top:8px;
  }}

  .footer {{ font-size:0.8em; color:var(--text-dim); text-align:center; padding:20px 12px 40px; }}
  .footer a {{ color:var(--text-dim); }}

  /* Lightbox */
  #lb {{
    display:none; position:fixed; inset:0; background:rgba(0,0,0,.9); z-index:500;
    align-items:center; justify-content:center; cursor:pointer; padding:16px;
  }}
  #lb.show {{ display:flex; }}
  #lb img {{ max-width:95%; max-height:95%; border-radius:8px; background:#000; }}

  @media (max-width:600px) {{
    .container {{ padding:8px; }}
    .header h1 {{ font-size:1.3em; }}
    .ex-item .thumb img {{ width:110px; height:110px; }}
    .lib-grid {{ grid-template-columns:repeat(auto-fill,minmax(110px,1fr)); }}
    .lib-card img {{ height:96px; }}
    .week-strip {{ grid-template-columns:repeat(2,1fr); }}
    table {{ font-size:0.75em; }}
  }}

  @media print {{
    * {{ background:#fff !important; color:#000 !important; }}
    .io-bar, .reset-btn, .block-bar, .tracker, .rest-timer {{ display:none; }}
    .day-body {{ display:block !important; }}
    .ex-item, .card, .day-card {{ break-inside:avoid; }}
  }}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>Upper Body 12-Week</h1>
    <div class="subtitle">Alternating strength + cardio · no rest days · legs excluded</div>
    <div class="stats-bar">
      <div class="stat"><div class="num">12</div><div class="label">Weeks</div></div>
      <div class="stat"><div class="num">84</div><div class="label">Days</div></div>
      <div class="stat"><div class="num">48</div><div class="label">Strength</div></div>
      <div class="stat"><div class="num">36</div><div class="label">Cardio</div></div>
      <div class="stat"><div class="num">0</div><div class="label">Rest days</div></div>
      <div class="chip-cap">≤ 45 min</div>
    </div>
  </div>

  <div class="io-bar">
    <button class="io-btn" onclick="exportData()">Download Save</button>
    <button class="io-btn" onclick="document.getElementById('importInput').click()">Restore Save</button>
    <input type="file" id="importInput" accept=".json" onchange="importData(event)" style="display:none">
  </div>

  <div class="card notes">
    <h2 class="sec">How this program works</h2>
    <p>The week is a fixed alternation of <strong>1 strength day + 1 cardio day</strong>, repeated every week for all 12 weeks — <strong>7 training days per week, zero rest days</strong>. Total: 48 strength sessions + 36 cardio sessions.</p>
    <p><strong>Weekly pattern:</strong> Mon Strength A (Push) · Tue Cardio 1 · Wed Strength B (Pull) · Thu Cardio 2 · Fri Strength C (Shoulders &amp; Arms) · Sat Cardio 3 · Sun Strength D (Hypertrophy + Core).</p>
    <div class="rule">Every session is capped at 45 minutes. Supersets (a/b pairs) and tighter rest are what make that possible — do the pairs back-to-back, rest only after the b exercise.</div>
    <div class="rule">Load progression: add <strong>2.5–5%</strong> to upper-body lifts (or +1–2 reps) once every set hits the top of its rep range at or below the block's target RPE. <strong>Never grind to failure</strong> on the no-rest-day schedule.</div>
    <p class="warn">No-rest-day autoregulation: if resting heart rate is elevated, sleep is poor, or joints ache, drop the cardio to Zone&nbsp;1 and skip the finishers for that day. <strong>The deload week (week 12) is not optional.</strong></p>
    <p>Cardio in this program is <strong>cardiovascular work, not leg strength training</strong> — legs are deliberately excluded.</p>
  </div>

  <div class="card">
    <h2 class="sec">Periodisation — 5 blocks</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Block</th><th>Weeks</th><th>Sets (main / other)</th><th>Reps</th><th>Rest between sets</th><th>RPE</th></tr></thead>
        <tbody>{block_rows}</tbody>
      </table>
    </div>
    <p class="intro" style="margin-top:10px">Core work uses <strong>45s rest in every block</strong>. Rest is taken <strong>after the second exercise of a superset pair</strong>, not between the pair.</p>
  </div>

  <div class="card">
    <h2 class="sec">Weekly template</h2>
    <div class="week-strip">{week_strip}</div>
  </div>

  <div class="card">
    <h2 class="sec">Strength days</h2>
    <div class="block-bar" id="blockBar">
      <span class="lbl">Show sets/reps for block:</span>
      <button class="blk" data-block="1" onclick="setBlock(1)">1 · Foundation</button>
      <button class="blk" data-block="2" onclick="setBlock(2)">2 · Volume</button>
      <button class="blk" data-block="3" onclick="setBlock(3)">3 · Strength</button>
      <button class="blk" data-block="4" onclick="setBlock(4)">4 · Peak</button>
      <button class="blk" data-block="5" onclick="setBlock(5)">5 · Deload</button>
    </div>
    {"".join(strength_html)}
  </div>

  <div class="card">
    <h2 class="sec">Cardio days</h2>
    {"".join(cardio_html)}
  </div>

  <div class="card">
    <h2 class="sec">Exercise library — all 68 movements</h2>
    <p class="intro">Every exercise in the program, with its animated technique GIF. Click any image to enlarge; click a name to open its ExRx.net reference page.</p>
    {"".join(lib_html)}
  </div>

  <div class="card">
    <h2 class="sec">12-week tick-off tracker</h2>
    <div class="tprog" id="tprog">0 / 48 strength · 0 / 36 cardio</div>
    <div class="tracker" id="tracker">
      {"".join(tracker_rows)}
    </div>
    <button class="reset-btn" onclick="if(confirm('Reset ALL tracker progress?')){{localStorage.removeItem('ub12_tracker');renderTracker();}}">Reset tracker</button>
  </div>

  <div class="footer">
    Exercise animations and technique reference: <a href="https://exrx.net" target="_blank" rel="noopener">ExRx.net</a>.<br>
    This program is for general information only and is not medical advice. Consult a qualified professional before starting any new training program. Stop if you feel pain or dizziness.<br>
    <strong>No leg exercises included by request.</strong>
  </div>

</div>

<div id="lb" onclick="this.classList.remove('show')"><img id="lbimg" alt=""></div>

<script>
const LS_OPEN = "ub12_open", LS_TRACK = "ub12_tracker", LS_BLOCK = "ub12_block";

/* ---------- collapsible strength cards ---------- */
function loadJSON(k, def) {{
  try {{ const r = localStorage.getItem(k); return r ? JSON.parse(r) : def; }} catch(e) {{ return def; }}
}}
function toggleCard(day) {{
  const card = document.getElementById("card-" + day);
  card.classList.toggle("collapsed");
  const open = loadJSON(LS_OPEN, {{}});
  open[day] = !card.classList.contains("collapsed");
  localStorage.setItem(LS_OPEN, JSON.stringify(open));
}}
(function initCards() {{
  const open = loadJSON(LS_OPEN, {{ A:true, B:true, C:true, D:true }});
  ["A","B","C","D"].forEach(d => {{
    const card = document.getElementById("card-" + d);
    if (card && open[d] === false) card.classList.add("collapsed");
  }});
}})();

/* ---------- block selector (drives prescriptions AND time badges) ---------- */
function setBlock(b) {{
  localStorage.setItem(LS_BLOCK, b);
  document.querySelectorAll(".scheme").forEach(s => s.classList.toggle("active", s.dataset.block == b));
  document.querySelectorAll(".blk").forEach(x => x.classList.toggle("active", x.dataset.block == b));
}}
(function initBlock() {{
  let b = parseInt(localStorage.getItem(LS_BLOCK) || "1", 10);
  if (b < 1 || b > 5) b = 1;
  setBlock(b);
}})();

/* ---------- rest timers ---------- */
function fmtTime(s) {{
  s = Math.max(0, Math.round(s));
  return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0");
}}
function initTimer(t) {{
  const disp = t.querySelector(".rt-display");
  const startBtn = t.querySelector(".rt-start");
  const presets = t.querySelectorAll(".rt-preset");
  let total = 0, remaining = 0, iv = null;
  function render() {{ disp.textContent = fmtTime(remaining); }}
  function stop() {{ if (iv) {{ clearInterval(iv); iv = null; }} startBtn.textContent = "Start"; }}
  function tick() {{
    remaining--;
    if (remaining <= 0) {{ remaining = 0; render(); stop(); t.classList.add("rt-done"); }}
    else render();
  }}
  presets.forEach(b => b.addEventListener("click", () => {{
    total = parseInt(b.dataset.sec, 10);
    remaining = total;
    t.classList.remove("rt-done");
    presets.forEach(x => x.classList.remove("sel"));
    b.classList.add("sel");
    stop();
    render();
  }}));
  startBtn.addEventListener("click", () => {{
    if (iv) {{ stop(); return; }}
    if (remaining <= 0) {{ remaining = total || (presets.length ? parseInt(presets[0].dataset.sec, 10) : 60); }}
    t.classList.remove("rt-done");
    startBtn.textContent = "Pause";
    iv = setInterval(tick, 1000);
  }});
  t.querySelector(".rt-reset").addEventListener("click", () => {{
    stop();
    remaining = total;
    t.classList.remove("rt-done");
    render();
  }});
  render();
}}
document.querySelectorAll(".rest-timer").forEach(initTimer);

/* ---------- tracker ---------- */
function renderTracker() {{
  const st = loadJSON(LS_TRACK, {{}});
  let s = 0, c = 0;
  document.querySelectorAll(".tcell").forEach(el => {{
    const done = !!st[el.dataset.key];
    el.classList.toggle("done", done);
    if (done) {{ el.dataset.kind === "strength" ? s++ : c++; }}
  }});
  document.getElementById("tprog").textContent = s + " / 48 strength · " + c + " / 36 cardio";
}}
function toggleDay(key, el) {{
  const st = loadJSON(LS_TRACK, {{}});
  st[key] = !st[key];
  if (!st[key]) delete st[key];
  localStorage.setItem(LS_TRACK, JSON.stringify(st));
  renderTracker();
}}
renderTracker();

/* ---------- lightbox ---------- */
function lightbox(ev, a) {{
  ev.preventDefault();
  document.getElementById("lbimg").src = a.href;
  document.getElementById("lb").classList.add("show");
  return false;
}}

/* ---------- import / export ---------- */
function exportData() {{
  const payload = {{
    tracker: loadJSON(LS_TRACK, {{}}),
    open: loadJSON(LS_OPEN, {{}}),
    block: localStorage.getItem(LS_BLOCK) || "1"
  }};
  const blob = new Blob([JSON.stringify(payload, null, 2)], {{ type: "application/json" }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "upper-body-12-week-" + new Date().toISOString().slice(0,10) + ".json";
  a.click();
  URL.revokeObjectURL(url);
}}
function importData(ev) {{
  const f = ev.target.files[0];
  if (!f) return;
  const r = new FileReader();
  r.onload = e => {{
    try {{
      const d = JSON.parse(e.target.result);
      if (d.tracker) localStorage.setItem(LS_TRACK, JSON.stringify(d.tracker));
      if (d.open) localStorage.setItem(LS_OPEN, JSON.stringify(d.open));
      if (d.block) localStorage.setItem(LS_BLOCK, d.block);
      location.reload();
    }} catch(err) {{ alert("Could not load file: " + err.message); }}
  }};
  r.readAsText(f);
  ev.target.value = "";
}}
</script>
</body>
</html>
'''

open(OUT, "w").write(HTML)
print("wrote", OUT, len(HTML), "bytes")
print("images/*.gif references (unique):", len(set(
    part.split('"')[0] for part in HTML.split("images/")[1:]
)))
print("total images/ occurrences:", HTML.count("images/"))
print("tracker cells:", HTML.count("data-key="))
