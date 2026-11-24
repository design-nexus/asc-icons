"""Signal: dark glass with an accent→violet rim.

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

LOOKS = ["signal"]


def _base(palette, accent, inner, size):
    """Dark glass, accent→violet rim, soft outer bloom on the rim only."""
    f = _faces(palette)
    a, b = _pair(palette)
    defs = (_linear("t", f["top"], f["bottom"])
            + f'<linearGradient id="r" x1="0" y1="0" x2="1" y2="1">'
              f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
    bloom = not _small(size)
    if bloom:
        defs += ('<filter id="b" x="-25%" y="-25%" width="150%" height="150%">'
                 '<feGaussianBlur stdDeviation="2.4"/></filter>')
    glow = (f'<rect x="8" y="8" width="112" height="112" rx="28" fill="none" stroke="url(#r)" '
            f'stroke-width="4" filter="url(#b)" opacity=".55"/>' if bloom else "")
    body = (f'<rect {SQUIRCLE} fill="url(#t)"/>{glow}'
            '<rect x="8.75" y="8.75" width="110.5" height="110.5" rx="27.25" fill="none" '
            'stroke="url(#r)" stroke-width="1.5"/>')
    return svg(body + inner, defs)


def signal(spec, palette, size):
    return tile(spec, palette, size, _base)


def render(look, spec, palette, size):
    return signal(spec, palette, size)
