"""Every icon renders in both looks, the themes are complete, marks stay their own."""
import os
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from umbra import build, catalog, palette  # noqa: E402
from umbra.glyphs import BRAND, LANG  # noqa: E402
from vellum import FAMILY, SET, looks  # noqa: E402

PALETTES = [palette.NYX_DARK, palette.NYX_LIGHT]


class Render(unittest.TestCase):
    def test_every_icon_in_every_look_is_valid_svg(self):
        for p in PALETTES:
            for look in looks.LOOKS:
                for _, names, spec in catalog.full_colour():
                    for size in build.FIXED + ["scalable"]:
                        svg = looks.render(look, spec, p, size)
                        root = ET.fromstring(svg)
                        self.assertEqual(root.get("viewBox"), "0 0 128 128", names[0])
                        ids = {el.get("id") for el in root.iter() if el.get("id")}
                        self.assertLessEqual(set(re.findall(r"url\(#([\w-]+)\)", svg)), ids, names[0])

    def test_brand_and_language_marks_are_their_own(self):
        for look in looks.LOOKS:
            for _, names, spec in catalog.full_colour():
                m = spec.get("mark") or ""
                svg = looks.render(look, spec, palette.NYX_DARK, "scalable")
                if m.startswith("brand:"):
                    self.assertIn(BRAND[m[6:]], svg, names[0])
                elif m.startswith("lang:"):
                    self.assertIn(LANG[m[5:]][0](), svg, names[0])

    def test_mono_keeps_colour_for_status_only(self):
        laptop = {"kind": "device", "mark": "laptop", "colour": "blue"}
        warning = {"kind": "device", "mark": "warning", "colour": "amber"}
        self.assertNotIn(palette.NYX_DARK["swatches"]["blue"], looks.render("mono", laptop, palette.NYX_DARK, 48))
        self.assertIn(palette.NYX_DARK["swatches"]["amber"], looks.render("mono", warning, palette.NYX_DARK, 48))

    def test_paper_drops_its_shadow_when_small(self):
        spec = {"kind": "folder", "mark": "documents", "colour": "blue"}
        self.assertIn("filter", looks.render("paper", spec, palette.NYX_LIGHT, 48))
        self.assertNotIn("filter", looks.render("paper", spec, palette.NYX_LIGHT, 16))


class Theme(unittest.TestCase):
    def test_build_writes_both_themes(self):
        with tempfile.TemporaryDirectory() as out:
            counts = build.build(palette.NYX_DARK, out, family=FAMILY)
            self.assertEqual(list(counts), ["paper", "mono"])
            self.assertIn("Name=Vellum\n", (Path(out) / "Vellum/index.theme").read_text())
            self.assertIn("Inherits=Vellum,Adwaita", (Path(out) / "Vellum-Mono/index.theme").read_text())
            self.assertTrue((Path(out) / "Vellum/symbolic/actions/edit-copy-symbolic.svg").is_file())
            self.assertTrue((Path(out) / "Vellum-Mono/scalable/mimetypes/text-rust.svg").is_file())
            self.assertTrue((Path(out) / "Vellum/vellum.json").is_file())

    def test_the_command_is_its_own(self):
        self.assertEqual(SET.settings_file.parent.name, "vellum")
        self.assertTrue(SET.owns("Vellum") and SET.owns("Vellum-Mono"))
        self.assertFalse(SET.owns("Umbra"))


if __name__ == "__main__":
    unittest.main()
