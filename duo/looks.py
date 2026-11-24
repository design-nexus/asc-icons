"""Duo: glass with a split accent / violet rim.

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

LOOKS = ["duo"]


def _base(palette, accent, inner, size):
    """Glass with a split rim: accent on top, violet on the bottom."""
    f = _faces(palette)
    a, b = _pair(palette)
    defs = _linear("t", f["top"], f["bottom"])
    rim = ""
    if not _small(size):
        rim = (f'<path d="M22 11 H98 A27 27 0 0 1 117 30 V70" fill="none" stroke="{a}" '
               f'stroke-width="1.6" stroke-linecap="round" opacity=".85"/>'
               f'<path d="M106 117 H30 A27 27 0 0 1 11 98 V58" fill="none" stroke="{b}" '
               f'stroke-width="1.6" stroke-linecap="round" opacity=".85"/>')
    body = f'<rect {SQUIRCLE} fill="url(#t)"/>{rim}'
    return svg(body + inner, defs)


def duo(spec, palette, size):
    return tile(spec, palette, size, _base)


def render(look, spec, palette, size):
    return duo(spec, palette, size)
