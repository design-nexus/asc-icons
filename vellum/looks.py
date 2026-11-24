"""Vellum's two looks, drawn from Umbra's catalog and glyphs.

Paper: pastel paper in tints of the icon's colour, with a crisp fold, a sheet peeking out
of each folder and a gentle shadow; on dark themes the paper is a raised surface.
Mono: neutral shapes in the theme's own greys, with colour only on the mark. Status
icons keep their meaning's colour.

Every icon is drawn on a 128 px canvas for a given size; 22 px and smaller drop the
sheet, shadows, labels and marks.
"""
from umbra.glyphs import LANG, label, text_width
from umbra.looks import FOLD, FOLDER_BACK, FOLDER_FRONT, FOLDER_FRONT_OPEN, PAGE, mark, placed, svg
from umbra.palette import colour, mix

LOOKS = ["paper", "mono"]
SCALABLE = 96
# Status glyphs keep their meaning's colour in Mono.
STATUS = {"info", "warning", "error", "question", "lock", "shield", "shield-warn", "shield-off", "missing"}
SQUIRCLE = 'x="8" y="8" width="112" height="112" rx="28"'


def _px(size):
    return SCALABLE if size == "scalable" else size


def _w(canvas_width, size, min_px):
    """A stroke `canvas_width` wide on the 128 canvas, but at least `min_px` on screen."""
    return max(canvas_width, min_px * 128 / _px(size))


def _small(size):
    return _px(size) <= 22


def _colour(spec, palette):
    m = spec.get("mark") or ""
    if m.startswith("lang:"):
        return LANG[m[5:]][1]
    if m.startswith("brand:"):
        return palette["accent"]
    return colour(palette, spec.get("colour"))


def _centred(m, palette, cx, cy, s, width, col):
    on_light = palette["light"]
    return mark(m, palette, cx - 12 * s, cy - 12 * s, s, width, col, on_light=on_light)


def _linear(id_, top, bottom):
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bottom}"/></linearGradient>')


def _labelled(text, size):
    return bool(text) and _px(size) >= 48 and text_width(text, 13) < 66


# ---------- Paper ----------

def _paper(p):
    bg, text = p["bg"], p["text"]
    if p["light"]:
        return {"top": "#ffffff", "bottom": mix(bg, text, 0.03), "sheet": "#ffffff", "edge": mix(bg, text, 0.14),
                "shadow": 0.18}
    return {"top": mix(bg, text, 0.24), "bottom": mix(bg, text, 0.17), "sheet": mix(bg, text, 0.62),
            "edge": mix(bg, text, 0.32), "shadow": 0.55}


def _ink(col, p):
    return mix(col, "#000000", 0.28) if p["light"] else mix(col, "#ffffff", 0.4)


def _shadowed(body, defs, p, size):
    if _small(size):
        return svg(body, defs)
    shadow = (f'<filter id="o" x="-20%" y="-20%" width="140%" height="150%">'
              f'<feGaussianBlur in="SourceAlpha" stdDeviation="3"/><feOffset dy="3" result="b"/>'
              f'<feFlood flood-color="#000000" flood-opacity="{_paper(p)["shadow"]}"/><feComposite in2="b" operator="in"/>'
              f'<feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    return svg(f'<g filter="url(#o)">{body}</g>', defs + shadow)


def paper(spec, p, size):
    pp = _paper(p)
    kind, m = spec["kind"], spec.get("mark")
    small = _small(size)
    col = _colour(spec, p)
    if kind == "folder":
        front = FOLDER_FRONT_OPEN if m == "open" else FOLDER_FRONT
        top, bottom = (0.62, 0.52) if p["light"] else (0.62, 0.7)
        body = f'<path d="{FOLDER_BACK}" fill="{mix(col, pp["top"], 0.42)}"/>'
        if not small:
            body += (f'<rect x="22" y="27" width="84" height="44" rx="4" fill="{pp["sheet"]}" stroke="{pp["edge"]}" '
                     f'stroke-width="1" transform="rotate(-3 64 50)"/>')
        body += f'<path d="{front}" fill="url(#f)"/>'
        if not small and m != "open":
            body += ('<path d="M17 37.5h94a8.5 8.5 0 0 1 8.5 8.5" fill="none" stroke="#ffffff" stroke-opacity=".5" '
                     'stroke-width="1.5"/>')
        if m and m != "open" and not small:
            if m.startswith("brand:"):
                body += f'<rect x="43" y="52" width="42" height="42" rx="12" fill="{pp["top"]}"/>'
                body += _centred(m, p, 64, 73, 1.45, 0, col)
            else:
                body += _centred(m, p, 64, 73, 1.7, _w(4, size, 1.15), _ink(col, p))
        return _shadowed(body, _linear("f", mix(col, pp["top"], top), mix(col, pp["top"], bottom)), p, size)
    if kind == "file":
        lang = m.startswith("lang:")
        if lang and small:
            return svg(placed(LANG[m[5:]][0](), 4, 4, 5))
        tinted = pp["top"] if lang else mix(col, pp["top"], 0.9)
        body = (f'<path d="{PAGE}" fill="url(#f)"/><path d="{PAGE}" fill="none" stroke="{pp["edge"]}" stroke-width="1"/>'
                f'<path d="{FOLD}" fill="{mix(col, pp["top"], 0.45)}"/>')
        text = spec.get("label") or ""
        if not small:
            if lang:
                body += _centred(m, p, 64, 70, 2.1, 0, col)
            else:
                labelled = _labelled(text, size)
                body += _centred(m, p, 64, 56 if labelled else 70, 1.9, _w(4.2, size, 1.15), _ink(col, p))
                if labelled:
                    body += label(text, 64, 97, 13, _ink(col, p), weight=_w(2.6, size, 0.9))
        return _shadowed(body, _linear("f", tinted, mix(col, pp["bottom"], 0.94)), p, size)
    body = (f'<rect x="12" y="12" width="104" height="104" rx="26" fill="url(#f)"/>'
            f'<rect x="12.5" y="12.5" width="103" height="103" rx="25.5" fill="none" stroke="{pp["edge"]}"/>'
            + _centred(m, p, 64, 64, 2.8, _w(5, size, 1.3), _ink(col, p)))
    return _shadowed(body, _linear("f", mix(col, pp["top"], 0.88), mix(col, pp["bottom"], 0.8)), p, size)


# ---------- Mono ----------

def _greys(p):
    bg, text = p["bg"], p["text"]
    if p["light"]:
        return {"top": mix(bg, "#ffffff", 0.9), "bottom": mix(bg, text, 0.06), "back": mix(bg, text, 0.2),
                "line": mix(bg, text, 0.28), "fold": mix(bg, text, 0.14), "ink": mix(text, bg, 0.12),
                "dim": mix(text, bg, 0.4)}
    return {"top": mix(bg, text, 0.4), "bottom": mix(bg, text, 0.27), "back": mix(bg, text, 0.22),
            "line": mix(bg, text, 0.5), "fold": mix(bg, text, 0.55), "ink": mix(text, bg, 0.05),
            "dim": mix(text, bg, 0.3)}


def mono(spec, p, size):
    g = _greys(p)
    kind, m = spec["kind"], spec.get("mark")
    small = _small(size)
    col = _colour(spec, p)
    defs = _linear("f", g["top"], g["bottom"])

    def face(d):
        return f'<path d="{d}" fill="url(#f)"/>' + ('' if small else f'<path d="{d}" fill="none" stroke="{g["line"]}" '
                                                                      'stroke-width="1.5"/>')
    if kind == "folder":
        front = FOLDER_FRONT_OPEN if m == "open" else FOLDER_FRONT
        body = f'<path d="{FOLDER_BACK}" fill="{g["back"]}"/>' + face(front)
        if m and m != "open" and not small:
            body += _centred(m, p, 64, 73, 1.75, _w(4.2, size, 1.15), col)
        return svg(body, defs)
    if kind == "file":
        lang = m.startswith("lang:")
        body = face(PAGE) + f'<path d="{FOLD}" fill="{g["fold"]}"/>'
        if small:
            if lang:
                body += _centred(m, p, 64, 74, 2.3, 0, col)
            return svg(body, defs)
        text = spec.get("label") or ""
        labelled = _labelled(text, size)
        if lang:
            body += _centred(m, p, 64, 66, 2.1, 0, col)
        else:
            body += _centred(m, p, 64, 56 if labelled else 70, 1.9, _w(4.2, size, 1.15), col)
        if labelled:
            body += label(text, 64, 97, 13, g["dim"], weight=_w(2.6, size, 0.9))
        return svg(body, defs)
    ink = col if m in STATUS else g["ink"]
    rim = '' if small else (f'<rect x="8.75" y="8.75" width="110.5" height="110.5" rx="27.25" fill="none" '
                            f'stroke="{g["line"]}" stroke-width="1.5"/>')
    return svg(f'<rect {SQUIRCLE} fill="url(#f)"/>{rim}' + _centred(m, p, 64, 64, 3.0, _w(4.8, size, 1.3), ink), defs)


RENDER = {"paper": paper, "mono": mono}


def render(look, spec, palette, size):
    return RENDER[look](spec, palette, size)
