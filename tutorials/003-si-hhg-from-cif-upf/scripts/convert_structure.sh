#!/bin/sh
set -eu

: "${SALMON2_ROOT:?Set SALMON2_ROOT to the SALMON2 checkout used for conversion.}"
workdir="${1:-.local/003-si-hhg-from-cif-upf}"
mkdir -p "$workdir/converted"

python3 "$SALMON2_ROOT/utility/cif2salmon/cif2salmon.py" \
  "$workdir/downloads/Si.cif" \
  -o "$workdir/converted/structure.inp"
