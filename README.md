# davidgdesigns

The graphic design work of David Gilbert, deployed on Vercel at
[davidgdesigns.vercel.app](https://davidgdesigns.vercel.app).

## The floor

The site is a single static page. By default it renders as **the floor**: one large
draggable canvas holding all 45 pieces, grouped into 12 brand clusters. Drag or
scroll to move, ctrl/⌘ + scroll or pinch to zoom, click a piece to open its case
view. The Index panel and the minimap fly you to a brand.

A **List view** toggle (remembered in `localStorage`) drops the canvas and renders
the same markup as an ordinary stacked page. That is also what you get with
JavaScript off, so the work is reachable either way. Keyboard: Tab walks the
pieces and brings each into view, arrow keys pan, `+`/`-` zoom, Escape closes.

## Editing

`index.html` is generated. Do not hand-edit it; edit the source and rebuild:

- `build/brands.json`: brand order, titles, kinds, descriptions and the pieces.
  Brand order in this file is the order on the page; MyLegacy and SignalDesk
  are first.
- `build/template.html`: the page shell, CSS and JavaScript.
- `build/build.py`: computes the floor coordinates and writes `index.html`.

```sh
python3 build/build.py build/brands.json index.html build/template.html
```

`build/parse.py` is kept only for reference: it is how `brands.json` was first
extracted from the previous version of the page.

## Honesty conventions

Keep these. Every brand here is self-initiated concept work, not a paid client
project. MyLegacy is an unofficial concept made for an application to MyLegacy
Management: its logo and colours are redrawn from their website and the tagline
is theirs. Photography is licensed from Pexels and is not David's own. These
statements live in the About panel, which is also the page footer in list view.
