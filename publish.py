#!/usr/bin/env python3
"""Create repo, push, enable Pages, poll until built. Never prints the token."""
import json, os, re, subprocess, time, urllib.request, urllib.error

REPO = "Upper-Body-12-Week"
OWNER = "colinlcoateshermes"
DIR = os.path.expanduser("~/Upper-Body-12-Week")
API = "https://api.github.com"

# parse token
tok = None
for line in open(os.path.expanduser("~/.git-credentials")):
    line = line.strip()
    m = re.match(r"https://([^:]+):([^@]+)@github\.com", line)
    if m and m.group(1) == OWNER:
        tok = m.group(2)
assert tok, "token not found"

def api(method, path, body=None, ok=(200, 201, 204, 422)):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Authorization", "token " + tok)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "ub12-publisher")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        r = urllib.request.urlopen(req)
        return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")

# 1. create repo (ignore 422 = already exists)
st, body = api("POST", "/user/repos", {
    "name": REPO, "private": False, "has_issues": False,
    "has_wiki": False, "auto_init": False,
    "description": "12-week upper-body-only strength + cardio program, no rest days, with animated ExRx.net GIFs.",
})
print("create repo:", st, body.get("full_name") or body.get("message"))

# 2. git init / commit / push
def run(cmd, **kw):
    print("$", " ".join(cmd))
    return subprocess.run(cmd, cwd=DIR, capture_output=True, text=True, **kw)

if not os.path.isdir(os.path.join(DIR, ".git")):
    run(["git", "init", "-b", "main"])
    run(["git", "config", "user.name", "Colin Coates"])
    run(["git", "config", "user.email", "hermes@colincoates.co.uk"])
run(["git", "remote", "remove", "origin"])
run(["git", "remote", "add", "origin", f"https://github.com/{OWNER}/{REPO}.git"])
run(["git", "add", "-A"])
run(["git", "commit", "-m", "Add Upper Body 12-Week site: index.html, 68 ExRx GIFs, build scripts"])

r = run(["git", "push", "-u", "origin", "main", "--force"])
print(r.stdout[-800:], r.stderr[-800:])
sha = run(["git", "rev-parse", "HEAD"]).stdout.strip()
print("COMMIT SHA:", sha)

# 3. enable Pages
st, body = api("POST", f"/repos/{OWNER}/{REPO}/pages",
               {"source": {"branch": "main", "path": "/"}})
print("enable pages:", st, body.get("message") or body.get("html_url", ""))
st, body = api("PUT", f"/repos/{OWNER}/{REPO}/pages", {"build_type": "legacy"})
print("set legacy build_type:", st, body.get("message", "ok"))

# 4. poll
for i in range(60):
    st, body = api("GET", f"/repos/{OWNER}/{REPO}/pages")
    status = body.get("status")
    print(f"poll {i}: status={status} url={body.get('html_url')}")
    if status == "built":
        break
    time.sleep(10)

print("PAGES_FINAL_STATUS:", body.get("status"))
print("PAGES_URL:", body.get("html_url"))
