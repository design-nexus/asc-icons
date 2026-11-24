"""Lens: an icon theme drawn from Umbra's catalog and glyphs in the colours
of the current theme.
"""
from umbra.build import Family
from umbra.cli import IconSet

from . import looks

THEMES = {
    "lens": ("Lens", "Lens"),
}
COMMENT = "Frosted glass panel with a neutral rim; colour lives in the Umbra glyphs. Drawn for AscendantOS and Omarchy, in the colours of the current theme."
FAMILY = Family("lens", THEMES, looks.render, COMMENT, "lens")
SET = IconSet("lens-icons", "Lens", FAMILY, "lens", "50-lens-icons", "lens")
