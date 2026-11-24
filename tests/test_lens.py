"""Every icon renders, the theme is complete, marks stay their own."""
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
from lens import FAMILY, SET, looks  # noqa: E402

PALETTES = [palette.NYX_DARK, palette.NYX_LIGHT]


class Render(unittest.TestCase):
    def test_every_icon_is_valid_svg(self):
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
                if m.startswith("brand:") and m != "brand:github":
                    self.assertIn(BRAND[m[6:]], svg, names[0])
                elif m.startswith("lang:"):
                    self.assertIn(LANG[m[5:]][0](), svg, names[0])


class Theme(unittest.TestCase):
    def test_build_writes_the_theme(self):
        with tempfile.TemporaryDirectory() as out:
            counts = build.build(palette.NYX_DARK, out, family=FAMILY)
            self.assertEqual(list(counts), ["lens"])
            self.assertIn("Name=Lens\n", (Path(out) / "Lens/index.theme").read_text())
            self.assertTrue((Path(out) / "Lens/symbolic/actions/edit-copy-symbolic.svg").is_file())
            self.assertTrue((Path(out) / "Lens/scalable/mimetypes/text-rust.svg").is_file())
            self.assertTrue((Path(out) / "Lens/lens.json").is_file())

    def test_the_command_is_its_own(self):
        self.assertEqual(SET.settings_file.parent.name, "lens")
        self.assertTrue(SET.owns("Lens"))
        self.assertFalse(SET.owns("Umbra"))


if __name__ == "__main__":
    unittest.main()
