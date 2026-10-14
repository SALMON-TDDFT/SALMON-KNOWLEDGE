#!/bin/sh
set -eu

workdir="${1:-.local/003-si-hhg-from-cif-upf}"
downloads="$workdir/downloads"
mkdir -p "$downloads"

curl -fL -o "$downloads/Si.cif" \
  https://www.crystallography.net/cod/9013102.cif
curl -fL -o "$downloads/Si.upf.gz" \
  http://www.pseudo-dojo.org/pseudos/nc-sr_pw_standard/Si.upf.gz
gzip -dkf "$downloads/Si.upf.gz"

expected_cif="99fb6c6c297f8407aa779de46bf7eaa663ac079f7f12b582c042313f9c82f77e"
expected_upf="56df10485adc6e95f3063bd24baa1822dbd5ffab88838261a3db2dc5ba112b44"
actual_cif=$(shasum -a 256 "$downloads/Si.cif" | awk '{print $1}')
actual_upf=$(shasum -a 256 "$downloads/Si.upf" | awk '{print $1}')

test "$actual_cif" = "$expected_cif"
test "$actual_upf" = "$expected_upf"
