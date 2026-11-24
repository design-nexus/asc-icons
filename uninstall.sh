#!/usr/bin/env bash
# Remove one family (or every family) installed from asc-icons.
#
#   ./uninstall.sh signal
#   ./uninstall.sh all
set -euo pipefail
data=${XDG_DATA_HOME:-$HOME/.local/share}
dest=$data/asc-icons

family=${1:-}
[[ -n $family ]] || { echo "Usage: uninstall.sh umbra|vellum|signal|lattice|lens|bracket|duo|all"; exit 1; }

remove_one() {
  local f=$1 cmd
  case $f in
    umbra) cmd=umbra-icons ;;
    vellum) cmd=vellum-icons ;;
    signal) cmd=signal-icons ;;
    lattice) cmd=lattice-icons ;;
    lens) cmd=lens-icons ;;
    bracket) cmd=bracket-icons ;;
    duo) cmd=duo-icons ;;
    *) echo "Unknown family '$f'"; exit 1 ;;
  esac
  if [[ -x $dest/bin/$cmd ]]; then
    "$dest/bin/$cmd" remove || true
  fi
  rm -f "$HOME/.local/bin/$cmd"
}

if [[ $family == all ]]; then
  for f in umbra vellum signal lattice lens bracket duo; do remove_one "$f"; done
  rm -rf "$dest"
else
  remove_one "$family"
  # Drop the shared tree only when no family bins remain.
  left=0
  for c in umbra-icons vellum-icons signal-icons lattice-icons lens-icons bracket-icons duo-icons; do
    [[ -L $HOME/.local/bin/$c || -e $HOME/.local/bin/$c ]] && left=1
  done
  if [[ $left -eq 0 ]]; then
    rm -rf "$dest"
  fi
fi
