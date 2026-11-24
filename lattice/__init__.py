"""Lattice: an icon theme drawn from Umbra's catalog and glyphs in the colours
of the current theme.
"""
from umbra.build import Family
from umbra.cli import IconSet

from . import looks

THEMES = {
    "lattice": ("Lattice", "Lattice"),
}
COMMENT = "Glass tile with a modular grid and accent hairline; Umbra line glyphs. Drawn for AscendantOS and Omarchy, in the colours of the current theme."
FAMILY = Family("lattice", THEMES, looks.render, COMMENT, "lattice")
SET = IconSet("lattice-icons", "Lattice", FAMILY, "lattice", "50-lattice-icons", "lattice")
