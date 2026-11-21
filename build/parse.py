import re, json, sys
src = open('/home/claude/davidgdesigns/index.html').read()
secs = re.findall(r'<section class="project" id="([^"]+)">(.*?)</section>', src, re.S)
out = []
for sid, body in secs:
    kind = re.search(r'<div class="kind">(.*?)</div>', body, re.S).group(1).strip()
    title = re.search(r'<h2>(.*?)</h2>', body, re.S).group(1).strip()
    desc = re.search(r'</div><p>(.*?)</p>', body, re.S).group(1).strip()
    figs = re.findall(r'<img src="([^"]+)" width="(\d+)" height="(\d+)"[^>]*alt="([^"]*)"><figcaption>(.*?)</figcaption>', body, re.S)
    pieces = [{"src": s, "w": int(w), "h": int(h), "alt": a, "cap": c.strip()} for s, w, h, a, c in figs]
    out.append({"id": sid, "kind": kind, "title": title, "desc": desc, "pieces": pieces})
json.dump(out, open('/home/claude/gen/brands.json', 'w'), indent=1)
print(len(out), "brands,", sum(len(b["pieces"]) for b in out), "pieces")
print(" ".join(b["id"] for b in out))
