"""Signal: an icon theme drawn from Umbra's catalog and glyphs in the colours
of the current theme.
"""
from umbra.build import Family
from umbra.cli import IconSet

from . import looks

THEMES = {
    "signal": ("Signal", "Signal"),
}
COMMENT = "Dark glass tile with an accent→violet rim and soft bloom; Umbra line glyphs. Drawn for AscendantOS and Omarchy, in the colours of the current theme."
FAMILY = Family("signal", THEMES, looks.render, COMMENT, "signal")
SET = IconSet("signal-icons", "Signal", FAMILY, "signal", "50-signal-icons", "signal")
