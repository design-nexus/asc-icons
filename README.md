# asc-icons

Icon themes for Linux desktops, drawn in the colours of your theme. One repo, separate
commands:

| Command | Themes |
| --- | --- |
| `umbra-icons` | Umbra, Umbra Solid, Umbra Line, Umbra Tinted, Umbra Frame, Umbra Colour |
| `vellum-icons` | Vellum (Paper), Vellum Mono |
| `signal-icons` | Signal — dark glass, accent→violet rim |
| `lattice-icons` | Lattice — glass with a modular grid |
| `lens-icons` | Lens — frosted glass, colour in the glyphs |
| `bracket-icons` | Bracket — HUD corner brackets |
| `duo-icons` | Duo — split accent / violet rim |

Umbra holds the catalog, glyphs, palette, builder and symbolic set. Everything else is a
look family on top of that.

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/design-nexus/asc-icons/main/install.sh | bash
```

Defaults to Umbra. Pass a family (and optional look) to start elsewhere:

```sh
curl -fsSL https://raw.githubusercontent.com/design-nexus/asc-icons/main/install.sh | bash -s -- signal
curl -fsSL https://raw.githubusercontent.com/design-nexus/asc-icons/main/install.sh | bash -s -- vellum --look mono
./install.sh all
```

Each family rebuilds when the Omarchy theme changes. `uninstall.sh <family>` (or `all`)
goes back to the icon theme you had before.

## Commands

Every `*-icons` binary supports the same verbs: `install`, `refresh`, `look`, `folders`,
`follow`, `build`, `status`, `remove`. Examples:

```
umbra-icons look tile|solid|line|tinted|frame|colour|off
vellum-icons look paper|mono|off
signal-icons look signal|off
```

Colours come from a palette file when given, else Omarchy's current `colors.toml`, else a
dark default.

## Developing

```sh
python3 -m unittest discover -s tests
./bin/signal-icons build --out /tmp/signal-out --palette nyx-dark
```

Looks live in each family's package (`umbra/looks.py`, `vellum/looks.py`,
`signal_icons/looks.py`, …). Shared pieces are under `umbra/`.

## License

MIT
