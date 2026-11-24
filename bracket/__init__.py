"""Bracket: an icon theme drawn from Umbra's catalog and glyphs in the colours
of the current theme.
"""
from umbra.build import Family
from umbra.cli import IconSet

from . import looks

THEMES = {
    "bracket": ("Bracket", "Bracket"),
}
COMMENT = "Glass tile with accent/violet HUD corner brackets; Umbra line glyphs. Drawn for AscendantOS and Omarchy, in the colours of the current theme."
FAMILY = Family("bracket", THEMES, looks.render, COMMENT, "bracket")
SET = IconSet("bracket-icons", "Bracket", FAMILY, "bracket", "50-bracket-icons", "bracket")
