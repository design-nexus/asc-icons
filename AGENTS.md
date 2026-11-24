# asc-icons

Python 3.11+, standard library only at runtime. Monorepo for every Design Nexus icon
family. Umbra (`umbra/`) is the library: catalog, glyphs, palette, builder
(`umbra.build.Family`), command (`umbra.cli.IconSet`) and symbolic set. Other families
draw looks on top of that and expose their own `*-icons` bin.

Families: `umbra` (six looks), `vellum` (paper, mono), `signal_icons` / `lattice` /
`lens` / `bracket` / `duo` (one look each).

```
./install.sh [umbra|vellum|signal|lattice|lens|bracket|duo|all]
python3 -m unittest discover -s tests
```

- Theme folders match the display names (Umbra, Vellum, Signal, …). Each gets a
  `<family-id>.json` stamp with the palette it was built in.
- Brand and language marks keep their own colours; everything else takes the palette.
- `symbolic/` is generated: edit `umbra/symbolic_src.py`, then
  `uv run --with skia-pathops==0.9.2 tools/outline.py` and commit the result.
- Never add an alias that is a real app's icon name.
- Style rules: STYLE.md in design-nexus/nyx-design (section 9, Icons).
- The Signal Python package is `signal_icons` so it does not shadow the stdlib `signal`
  module; the theme and command are still Signal / `signal-icons`.
