"""Lens: frosted glass; colour in the Umbra glyphs.

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

LOOKS = ["lens"]


def _base(palette, accent, inner, size):
    """Frosted panel, subtle top highlight, thin neutral rim."""
    f = _faces(palette)
    hi = mix(f["top"], "#ffffff", 0.35 if palette["light"] else 0.18)
    defs = (_linear("t", f["top"], f["bottom"])
            + f'<linearGradient id="hl" x1="0" y1="0" x2="0" y2="1">'
              f'<stop offset="0" stop-color="{hi}" stop-opacity=".55"/>'
              f'<stop offset=".45" stop-color="{hi}" stop-opacity="0"/></linearGradient>')
    rim, rim_op = f["rim"], (0.28 if palette["light"] else 0.22)
    body = (f'<rect {SQUIRCLE} fill="url(#t)"/><rect {SQUIRCLE} fill="url(#hl)"/>'
            f'<rect x="8.5" y="8.5" width="111" height="111" rx="27.5" fill="none" stroke="{rim}" '
            f'stroke-opacity="{rim_op}"/>')
    return svg(body + inner, defs)


def lens(spec, palette, size):
    return tile(spec, palette, size, _base)


def render(look, spec, palette, size):
    return lens(spec, palette, size)
