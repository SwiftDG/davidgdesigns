"""Generates index.html for davidgdesigns from brands.json.
World coordinates for the draggable floor are computed here, so the page needs
no layout JavaScript and still renders as a plain list when JS is off."""
import json, html, sys

brands = json.load(open(sys.argv[1]))
OUT = sys.argv[2]

CLUSTER_W = 2600
GAP = 96
PAD_X, PAD_Y = 32, 68          # paper border around each image
COL_GAP, ROW_GAP = 820, 940
COLS = 3
HEAD = 340                      # space above a cluster for its giant name


def piece_width(r):
    if r >= 2.2: return 880
    if r >= 1.55: return 780
    if r >= 0.95: return 440
    if r >= 0.75: return 540
    if r >= 0.65: return 520
    return 450


def seeded(text, mod):
    h = 2166136261
    for ch in text:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h % mod


# ---- pack each brand's pieces into shelves -------------------------------
for b in brands:
    x = y = row_h = 0
    for p in b["pieces"]:
        r = p["w"] / p["h"]
        w = piece_width(r)
        h = round(w / r)
        fw, fh = w + PAD_X, h + PAD_Y
        if x and x + fw > CLUSTER_W:
            x, y, row_h = 0, y + row_h + GAP, 0
        jitter = (seeded(p["src"], 7) - 3) * 10
        p.update(w=w, h=h, x=x, y=y + jitter,
                 rot=round((seeded(p["cap"] + b["id"], 9) - 4) * 0.55, 2))
        x += fw + GAP
        row_h = max(row_h, fh + abs(jitter))
    b["h"] = y + row_h


# ---- place clusters on the floor -----------------------------------------
rows = [brands[i:i + COLS] for i in range(0, len(brands), COLS)]
top = HEAD
for row in rows:
    tallest = max(b["h"] for b in row)
    for i, b in enumerate(row):
        b["x"] = i * (CLUSTER_W + COL_GAP)
        b["y"] = top
    top += tallest + ROW_GAP + HEAD

MARGIN = 700
WORLD_W = COLS * CLUSTER_W + (COLS - 1) * COL_GAP + MARGIN * 2
WORLD_H = top - ROW_GAP + MARGIN * 2
for b in brands:
    b["x"] += MARGIN
    b["y"] += MARGIN

e = html.escape

clusters = []
for n, b in enumerate(brands):
    figs = []
    for i, p in enumerate(b["pieces"]):
        figs.append(
            f'<figure class="piece" style="--x:{p["x"]}px;--y:{p["y"]}px;--w:{p["w"]}px;'
            f'--h:{p["h"]}px;--rot:{p["rot"]}deg">'
            f'<button type="button" class="paper" data-brand="{b["id"]}" data-i="{i}" '
            f'aria-label="Open {e(p["cap"])}, {e(b["title"])}">'
            f'<img src="{p["src"]}" width="{p["w"]}" height="{p["h"]}" loading="lazy" '
            f'decoding="async" alt="{e(p["alt"])}">'
            f'<figcaption>{e(p["cap"])}</figcaption></button></figure>')
    clusters.append(
        f'<section class="cluster" id="{b["id"]}" aria-labelledby="{b["id"]}-h" '
        f'style="--x:{b["x"]}px;--y:{b["y"]}px;--w:{CLUSTER_W}px;--h:{b["h"]}px">'
        f'<header class="chead"><p class="ckind">{n + 1:02d} &nbsp; {e(b["kind"])}</p>'
        f'<h2 id="{b["id"]}-h" class="cname">{e(b["title"])}</h2>'
        f'<p class="cdesc">{e(b["desc"])}</p></header>'
        f'<div class="pieces">{"".join(figs)}</div></section>')

nav = "".join(
    f'<li><button type="button" class="jump" data-to="{b["id"]}">'
    f'<span class="jn">{i + 1:02d}</span><span class="jt">{e(b["title"])}</span>'
    f'<span class="jc">{len(b["pieces"])}</span></button></li>'
    for i, b in enumerate(brands))

dots = "".join(
    f'<i style="left:{b["x"] / WORLD_W * 100:.2f}%;top:{b["y"] / WORLD_H * 100:.2f}%;'
    f'width:{CLUSTER_W / WORLD_W * 100:.2f}%;height:{b["h"] / WORLD_H * 100:.2f}%" '
    f'data-to="{b["id"]}"></i>'
    for b in brands)

meta = json.dumps({b["id"]: {"t": b["title"], "k": b["kind"], "d": b["desc"]} for b in brands},
                  separators=(",", ":"))

tpl = open(sys.argv[3]).read()
for key, val in [("__CLUSTERS__", "\n".join(clusters)), ("__NAV__", nav), ("__DOTS__", dots),
                 ("__META__", meta), ("__WORLDW__", str(WORLD_W)), ("__WORLDH__", str(WORLD_H)),
                 ("__TOTAL__", str(sum(len(b["pieces"]) for b in brands))),
                 ("__BRANDS__", str(len(brands)))]:
    tpl = tpl.replace(key, val)
open(OUT, "w").write(tpl)
print(f"world {WORLD_W}x{WORLD_H}")
