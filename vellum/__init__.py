"""Vellum: an icon theme in two looks, Paper and Mono, drawn from Umbra's catalog and
glyphs in the colours of the current theme."""
from umbra.build import Family
from umbra.cli import IconSet

from . import looks

THEMES = {
    "paper": ("Vellum", "Vellum"),
    "mono": ("Vellum-Mono", "Vellum Mono"),
}
COMMENT = "Paper and mono icons for Nyx and Omarchy, in the colours of the current theme"
FAMILY = Family("vellum", THEMES, looks.render, COMMENT, "paper")
SET = IconSet("vellum-icons", "Vellum", FAMILY, "vellum", "50-vellum-icons", "paper")
