#!/usr/bin/env bash
# Install one (or every) icon family from asc-icons and use it.
#
#   curl -fsSL https://raw.githubusercontent.com/design-nexus/asc-icons/main/install.sh | bash
#   … | bash -s -- signal
#   ./install.sh umbra|vellum|signal|lattice|lens|bracket|duo|all
#
# Always installs Umbra's library (catalog, glyphs, symbolic). Building a family
# switches to that family's default look and follows Omarchy theme changes.
set -euo pipefail

REPO="design-nexus/asc-icons"
say() { printf '\033[1m==>\033[0m %s\n' "$*"; }
die() { printf '\033[31m==>\033[0m %s\n' "$*" >&2; exit 1; }

command -v python3 >/dev/null || die "Python 3 is needed."
python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))' || die "Python 3.11 or newer is needed."

family=${1:-umbra}
shift || true
case $family in
  umbra|vellum|signal|lattice|lens|bracket|duo|all) ;;
  -h|--help) echo "Usage: install.sh [umbra|vellum|signal|lattice|lens|bracket|duo|all] [family-install-args…]"; exit 0 ;;
  *) die "Unknown family '$family'. Use umbra, vellum, signal, lattice, lens, bracket, duo or all." ;;
esac

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
fetch() {
  if command -v git >/dev/null; then
    git clone -q --depth 1 "https://github.com/$1.git" "$2"
  else
    mkdir -p "$2"
    curl -fsSL "https://github.com/$1/archive/refs/heads/main.tar.gz" | tar -xz -C "$2" --strip-components=1
  fi
}

here=""
[[ -n ${BASH_SOURCE[0]:-} && -f ${BASH_SOURCE[0]} ]] && here=$(cd "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ -n $here && -d $here/umbra && -f $here/bin/umbra-icons ]]; then
  src=$here
else
  say "Fetching asc-icons"
  fetch "$REPO" "$work/src"
  src="$work/src"
fi

data=${XDG_DATA_HOME:-$HOME/.local/share}
dest=$data/asc-icons

place() {
  local d=$1; shift
  rm -rf "$d.new"
  mkdir -p "$d.new"
  cp -a "$@" "$d.new/"
  find "$d.new" -name __pycache__ -type d -prune -exec rm -rf {} +
  rm -rf "$d"
  mv "$d.new" "$d"
}

# Library + every family package + all bins (bins are tiny; keeps look-switching easy).
say "Installing to $dest"
place "$dest" \
  "$src/umbra" "$src/symbolic" "$src/vellum" \
  "$src/signal_icons" "$src/lattice" "$src/lens" "$src/bracket" "$src/duo" \
  "$src/bin" "$src/LICENSE"

mkdir -p "$HOME/.local/bin"
link_bin() { ln -sf "$dest/bin/$1" "$HOME/.local/bin/$1"; }

install_one() {
  local f=$1; shift
  local cmd
  case $f in
    umbra) cmd=umbra-icons ;;
    vellum) cmd=vellum-icons ;;
    signal) cmd=signal-icons ;;
    lattice) cmd=lattice-icons ;;
    lens) cmd=lens-icons ;;
    bracket) cmd=bracket-icons ;;
    duo) cmd=duo-icons ;;
  esac
  link_bin "$cmd"
  say "Building $f"
  UMBRA_ICONS_LIB="$dest" "$dest/bin/$cmd" install "$@"
}

if [[ $family == all ]]; then
  for f in umbra vellum signal lattice lens bracket duo; do
    install_one "$f" "$@"
  done
else
  install_one "$family" "$@"
fi

case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) say "Add ~/.local/bin to your PATH." ;; esac
