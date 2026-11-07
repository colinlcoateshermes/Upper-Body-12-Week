#!/usr/bin/env python3
"""Generate the self-contained index.html for the Upper Body 12-Week site."""
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

# ---- Program definitions: (key, role, note) ----
STRENGTH = {
    "A": {
        "title": "STRENGTH A — Push",
        "sub": "Chest · Front Delts · Triceps",
        "intro": "Main lifts first, then accessories, finish with a push-up AMRAP.",
        "ex": [
            ("bb-bench-press", "main", "Main lift. Add 2.5–5% when all sets hit the top of the range."),
            ("bb-incline-bench-press", "main", "Main lift. Swap → Dumbbell Incline Bench Press."),
            ("db-fly", "accessory", "Swap → Dumbbell Incline Fly."),
            ("bb-military-press", "main", "Main lift (standing). Brace hard, no leg drive."),
            ("db-lateral-raise", "accessory", "Strict, light — lead with the elbows."),
            ("cable-pushdown", "accessory", "Elbows pinned to the sides."),
            ("bench-dip", "accessory", "Swap → Chest Dip (weighted when easy)."),
            ("push-up", "finisher", "Finisher: 1 set to AMRAP."),
        ],
    },
    "B": {
        "title": "STRENGTH B — Pull",
        "sub": "Back · Rear Delts · Traps · Biceps",
        "intro": "Horizontal + vertical pulling, rear delts and traps, then biceps.",
        "ex": [
            ("bb-bent-over-row", "main", "Main lift. Control the eccentric, no torso heave."),
            ("pull-up", "main", "Swap → Chin-up. Add load when >8 clean reps."),
            ("lat-pulldown", "main", "Swap → Close Grip Pulldown."),
            ("seated-row", "accessory", "Squeeze the shoulder blades together."),
            ("db-bent-over-row", "accessory", "Single-arm, brace on a bench."),
            ("cable-rear-delt-row", "accessory", "Rope attachment, pull to the face."),
            ("bb-shrug", "accessory", "Swap → Dumbbell Shrug."),
            ("bb-curl", "accessory", "No swing — strict tempo."),
            ("db-hammer-curl", "accessory", "Neutral grip, elbows fixed."),
        ],
    },
    "C": {
        "title": "STRENGTH C — Shoulders &amp; Arms",
        "sub": "Delts · Triceps · Biceps · (optional forearms)",
        "intro": "Pressing and raises for all three delt heads, then arm isolation.",
        "ex": [
            ("db-shoulder-press", "main", "Seated, back supported."),
            ("db-arnold-press", "main", "Rotate through the press."),
            ("bb-upright-row", "accessory", "Wide grip to spare the shoulders."),
            ("db-rear-lateral-raise", "accessory", "Chest supported, tiny weights."),
            ("db-front-raise", "accessory", "Alternate arms or together."),
            ("close-grip-bench-press", "accessory", "Shoulder-width grip, elbows tucked."),
            ("skull-crusher", "accessory", "Lying triceps extension — control the bar to the forehead."),
            ("bb-preacher-curl", "accessory", "Full stretch at the bottom."),
            ("db-concentration-curl", "accessory", "Brace the elbow on the thigh."),
        ],
        "optional": ["bb-wrist-curl", "bb-reverse-wrist-curl", "bb-reverse-curl",
                     "db-triceps-extension", "db-kickback"],
    },
    "D": {
        "title": "STRENGTH D — Upper-body Hypertrophy + Core",
        "sub": "Bodyweight pushes/pulls · Core",
        "intro": "Higher-rep bodyweight and cable work, finishing with core.",
        "ex": [
            ("push-up", "accessory", "Elevate feet or add a weight vest to progress."),
            ("chest-dip", "main", "Lean forward for the chest."),
            ("inverted-row", "accessory", "Bodyweight horizontal pull."),
            ("cable-lying-fly", "accessory", "Constant tension on the pecs."),
            ("db-kickback", "accessory", "Triceps, elbow high and fixed."),
            ("db-curl", "accessory", "Alternating Dumbbell Curl."),
            ("crunch", "core", "Controlled, no neck pulling."),
            ("hanging-leg-hip-raise", "core", "Ab strap or bar."),
            ("db-side-bend", "core", "Obliques — one arm at a time."),
            ("superman", "core", "Lower-back / spinal erectors."),
        ],
        "core_options": ["crunch-arms-crossed", "sit-up", "weighted-incline-sit-up",
                         "cable-kneeling-crunch", "cable-seated-crunch", "twisting-crunch",
                         "bird-dog"],
    },
}

CARDIO = {
    "1": {
        "title": "CARDIO 1 — Easy Zone 1–2 steady state",
        "day": "Tuesday",
        "prescription": [
            "5 min easy warm-up",
            "25–35 min continuous at a conversational pace (able to speak full sentences)",
            "5 min cool-down",
        ],
        "note": "Keep it low-impact and truly easy — it must not compromise Wednesday's pull session. Pick any modality below.",
        "mods": ["treadmill-walk", "cycle-ergometer", "elliptical-trainer", "row-ergometer"],
    },
    "2": {
        "title": "CARDIO 2 — Intervals / conditioning",
        "day": "Thursday",
        "prescription": [
            "5–8 min warm-up, then by block:",
            "Block 1: 6 × (30s hard / 90s easy) · Block 2: 8 × (30s / 90s)",
            "Block 3: 8 × (30s / 60s) · Block 4: 10 × (20s hard / 40s easy)",
            "Block 5: 15 min easy only",
            "5 min cool-down",
        ],
        "note": "Hard means genuinely hard but repeatable — never all-out on a no-rest-day week.",
        "mods": ["treadmill-run", "row-ergometer", "cycle-ergometer",
                 "ski-ergometer", "stair-climber", "stepmill"],
    },
    "3": {
        "title": "CARDIO 3 — Bodyweight / mixed-modal circuit",
        "day": "Saturday",
        "prescription": [
            "5 min warm-up, then 40s work / 20s rest through the circuit:",
            "Block 1–2: 3 rounds · Block 3–4: 4–5 rounds · Block 5: 2 easy rounds",
        ],
        "note": "Keep one round in reserve — Sunday is Strength D.",
        "mods": ["jumping-jack", "high-knee-run", "burpee", "mountain-climber",
                 "jump-rope", "bear-crawl", "lateral-shuffle", "arm-ergometer"],
    },
}

BLOCKS = [
    ("1 — Foundation", "1–3", "3 sets × 10–12 reps, rest 90s", "RPE 7 (3 reps in reserve)", "Zone 2, 30 min"),
    ("2 — Volume", "4–6", "4 sets × 8–10 reps, rest 90–120s", "RPE 8", "Zone 2, 35–40 min + 1 interval day"),
    ("3 — Strength", "7–9", "4 sets × 6–8 reps (accessories 3×10–12), rest 2–3 min", "RPE 8–9", "40 min + intervals 8×(30s hard / 90s easy)"),
    ("4 — Peak Overload", "10–11", "5 sets × 5–8: one top set, then back-off sets at −10% load, rest 2–3 min", "RPE 9", "45 min steady + HIIT 10×(20s / 40s)"),
    ("5 — Deload &amp; Retest", "12", "2 sets × 8–10 at ~60% of week-11 load, stop 3–4 reps short", "RPE 5–6", "Zone 1–2 only, 20–25 min"),
]

WEEK = [
    ("Monday", "STRENGTH A", "strength"), ("Tuesday", "CARDIO 1", "cardio"),
    ("Wednesday", "STRENGTH B", "strength"), ("Thursday", "CARDIO 2", "cardio"),
    ("Friday", "STRENGTH C", "strength"), ("Saturday", "CARDIO 3", "cardio"),
    ("Sunday", "STRENGTH D", "strength"),
]

# ---- scheme text per block/role ----
def scheme(role, b):
    i = b - 1
    return {
        "main":      ["3 × 10–12 · rest 90s", "4 × 8–10 · rest 90–120s", "4 × 6–8 · rest 2–3 min",
                      "5 × 5–8 (top set + back-off −10%) · rest 2–3 min", "2 × 8–10 @ 60% · rest 90s"][i],
        "accessory": ["3 × 10–12 · rest 90s", "4 × 8–10 · rest 90–120s", "3 × 10–12 · rest 90s",
                      "4 × 8–10 · rest 90–120s", "2 × 10–12 @ 60% · rest 90s"][i],
        "finisher":  ["1 × AMRAP", "1 × AMRAP", "1 × AMRAP", "1 × AMRAP", "1 × easy set"][i],
        "core":      ["3 × 12–20", "3 × 15–20", "3 × 12–15", "4 × 15–20", "2 × 15 easy"][i],
        "optional":  ["2–3 × 12–15", "3 × 12–15", "3 × 12–15", "3 × 12–15", "2 × 12 easy"][i],
    }[role]


def ex_row(key, role, note=""):
    e = EX[key]
    # per-block scheme spans
    spans = "".join(
        f'<span class="scheme" data-block="{b}">{scheme(role, b)}</span>' for b in range(1, 6)
    )
    note_html = f'<div class="ex-note">{note}</div>' if note else ""
    return (
        f'<div class="ex-item" data-role="{role}">'
        f'<a class="thumb" href="images/{e["file"]}" onclick="return lightbox(event,this)">'
        f'<img src="images/{e["file"]}" alt="{e["name"]}" loading="lazy"></a>'
        f'<div class="ex-body">'
        f'<a class="ex-name" href="{e["exrx"]}" target="_blank" rel="noopener">{e["name"]}</a>'
        f'<div class="ex-scheme">{spans}<span class="role-tag">{role}</span></div>'
        f'{note_html}'
        f'</div></div>'
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
    rows = "".join(ex_row(k, r, n) for k, r, n in d["ex"])
    optional = ""
    if "optional" in d:
        opt_rows = "".join(ex_row(k, "optional") for k in d["optional"])
        optional = (
            '<div class="section-title" style="margin-top:14px">Optional forearm finisher</div>'
            f'<div class="ex-list">{opt_rows}</div>'
        )
    if "core_options" in d:
        opt_rows = "".join(ex_row(k, "core") for k in d["core_options"])
        optional = (
            '<div class="section-title" style="margin-top:14px">Rotate core options each week</div>'
            f'<div class="ex-list">{opt_rows}</div>'
        )
    strength_html.append(f'''
    <div class="day-card" id="card-{day}" data-card="{day}">
      <div class="day-header" onclick="toggleCard('{day}')">
        <div>
          <h2>{d["title"]}</h2>
          <div class="day-sub">{d["sub"]}</div>
        </div>
        <span class="collapse-icon">▾</span>
      </div>
      <div class="day-body">
        <div class="intro">{d["intro"]}</div>
        <div class="ex-list">{rows}</div>
        {optional}
      </div>
    </div>''')

# ---------- build cardio cards ----------
cardio_html = []
for num in "123":
    c = CARDIO[num]
    mods = "".join(cardio_mod(k) for k in c["mods"])
    presc = "".join(f"<li>{p}</li>" for p in c["prescription"])
    cardio_html.append(f'''
    <div class="day-card cardio-card">
      <div class="day-header static">
        <div>
          <h2>{c["title"]}</h2>
          <div class="day-sub">{c["day"]}</div>
        </div>
      </div>
      <div class="day-body">
        <ul class="presc">{presc}</ul>
        <div class="intro">{c["note"]}</div>
        <div class="lib-grid small">{mods}</div>
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
    f'<tr><td class="bname">{b[0]}</td><td>{b[1]}</td><td>{b[2]}</td><td>{b[3]}</td><td>{b[4]}</td></tr>'
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
  .stats-bar {{ display:flex; gap:10px; margin-top:16px; flex-wrap:wrap; }}
  .stat {{
    background:var(--bg); border:1px solid var(--border); border-radius:8px;
    padding:10px 14px; text-align:center; flex:1; min-width:76px;
  }}
  .stat .num {{ font-size:1.35em; font-weight:700; color:var(--green); }}
  .stat .label {{ font-size:0.72em; color:var(--text-dim); text-transform:uppercase; letter-spacing:.4px; }}

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
  .collapse-icon {{ font-size:0.8em; color:var(--text-dim); transition:transform .2s; }}
  .day-card.collapsed .collapse-icon {{ transform:rotate(-90deg); }}
  .day-card.collapsed .day-body {{ display:none; }}
  .day-body {{ padding:0 16px 16px; }}
  .intro {{ font-size:0.85em; color:var(--text-dim); margin-bottom:10px; }}
  .presc {{ margin:0 0 10px 18px; font-size:0.87em; }}
  .presc li {{ margin-bottom:3px; }}

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
    .io-bar, .reset-btn, .block-bar, .tracker {{ display:none; }}
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
    <div class="rule">Load progression: add <strong>2.5–5%</strong> to upper-body lifts (or +1–2 reps) once every set hits the top of its rep range at or below the block's target RPE. <strong>Never grind to failure</strong> on the no-rest-day schedule.</div>
    <p class="warn">No-rest-day autoregulation: if resting heart rate is elevated, sleep is poor, or joints ache, drop the cardio to Zone&nbsp;1 and skip the finishers for that day. <strong>The deload week (week 12) is not optional.</strong></p>
    <p>Cardio in this program is <strong>cardiovascular work, not leg strength training</strong> — legs are deliberately excluded.</p>
  </div>

  <div class="card">
    <h2 class="sec">Periodisation — 5 blocks</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Block</th><th>Weeks</th><th>Strength</th><th>Load / intensity</th><th>Cardio</th></tr></thead>
        <tbody>{block_rows}</tbody>
      </table>
    </div>
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

/* ---------- block selector ---------- */
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
print("images/*.gif references:", HTML.count("images/"))
