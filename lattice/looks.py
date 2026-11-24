"""Lattice: glass with a modular grid and accent hairline.

Drawn on Umbra's Tile glyph layout; only the tile changes.
"""
from umbra.looks import _px, svg, tile
from umbra.palette import mix

SQUIRCLE = 'x="8" y="8" width="112" height="112" rx="28"'


def _small(size):
    return _px(size) <= 22


def _faces(p):
    """Near-black (or light frost) panel colours — no satin."""
    bg, text = p["bg"], p["text"]
    if p["light"]:
        return {
            "top": mix(bg, "#ffffff", 0.55),
            "bottom": mix(bg, text, 0.04),
            "rim": mix(text, bg, 0.55),
        }
    return {
        "top": mix(bg, text, 0.07),
        "bottom": mix(bg, "#000000", 0.35),
        "rim": mix(text, bg, 0.55),
    }


def _pair(p):
    """Accent → violet ends so Omarchy themes still recolour the brand rim."""
    return p["accent"], p["swatches"]["violet"]


def _linear(id_, top, bottom):
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient>')

LOOKS = ["lattice"]


def _base(palette, accent, inner, size):
    """Glass panel with a faint modular grid and an accent hairline rim."""
    f = _faces(palette)
    col = accent
    grid_op = 0.07 if palette["light"] else 0.11
    grid_col = mix(col, palette["text"] if palette["light"] else "#ffffff", 0.25)
    defs = _linear("t", f["top"], f["bottom"])
    rim_op = 0.55 if not palette["light"] else 0.45
    grid = ""
    if not _small(size):
        lines = []
        for i in range(1, 6):
            o = 8 + i * (112 / 6)
            lines.append(f'<line x1="{o:.2f}" y1="8" x2="{o:.2f}" y2="120" stroke="{grid_col}" '
                         f'stroke-opacity="{grid_op}" stroke-width="1"/>')
            lines.append(f'<line x1="8" y1="{o:.2f}" x2="120" y2="{o:.2f}" stroke="{grid_col}" '
                         f'stroke-opacity="{grid_op}" stroke-width="1"/>')
        defs += f'<clipPath id="c"><rect {SQUIRCLE}/></clipPath>'
        grid = f'<g clip-path="url(#c)">{"".join(lines)}</g>'
    body = (f'<rect {SQUIRCLE} fill="url(#t)"/>{grid}'
            f'<rect x="8.5" y="8.5" width="111" height="111" rx="27.5" fill="none" stroke="{col}" '
            f'stroke-opacity="{rim_op}" stroke-width="1.25"/>')
    return svg(body + inner, defs)


def lattice(spec, palette, size):
    return tile(spec, palette, size, _base)


def render(look, spec, palette, size):
    return lattice(spec, palette, size)
