#!/bin/sh
set -eu

: "${CIF2SALMON:?Set CIF2SALMON to the cif2salmon.py script.}"

workdir="${1:-.local/004-4h-sic-gs-from-cif-fhi}"
mkdir -p "$workdir/converted"

# AFLOW writes the otherwise equivalent H-M symbol as P6_{3}mc; Gemmi expects
# the standard CIF spelling used below.
sed 's/P6_{3}mc/P 63 m c/' "$workdir/downloads/4H-SiC-aflow.cif" \
  > "$workdir/converted/4H-SiC-normalized.cif"

python3 "$CIF2SALMON" \
  "$workdir/converted/4H-SiC-normalized.cif" \
  -o "$workdir/converted/structure.inp" \
  --coordinates reduced \
  --force
