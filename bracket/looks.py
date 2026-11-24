"""Bracket: glass with HUD corner brackets.

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

LOOKS = ["bracket"]


def _base(palette, accent, inner, size):
    """Glass with HUD corner brackets in accent / violet."""
    f = _faces(palette)
    a, b = _pair(palette)
    defs = _linear("t", f["top"], f["bottom"])
    corners = ""
    if not _small(size):
        w = 2.0
        corners = (
            f'<path d="M18 34 V22 A14 14 0 0 1 32 18 H44" fill="none" stroke="{a}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M110 34 V22 A14 14 0 0 0 96 18 H84" fill="none" stroke="{a}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M18 94 V106 A14 14 0 0 0 32 110 H44" fill="none" stroke="{b}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M110 94 V106 A14 14 0 0 1 96 110 H84" fill="none" stroke="{b}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    body = f'<rect {SQUIRCLE} fill="url(#t)"/>{corners}'
    return svg(body + inner, defs)


def bracket(spec, palette, size):
    return tile(spec, palette, size, _base)


def render(look, spec, palette, size):
    return bracket(spec, palette, size)
