"""Duo: an icon theme drawn from Umbra's catalog and glyphs in the colours
of the current theme.
"""
from umbra.build import Family
from umbra.cli import IconSet

from . import looks

THEMES = {
    "duo": ("Duo", "Duo"),
}
COMMENT = "Glass tile with a split accent / violet rim; Umbra line glyphs. Drawn for AscendantOS and Omarchy, in the colours of the current theme."
FAMILY = Family("duo", THEMES, looks.render, COMMENT, "duo")
SET = IconSet("duo-icons", "Duo", FAMILY, "duo", "50-duo-icons", "duo")
