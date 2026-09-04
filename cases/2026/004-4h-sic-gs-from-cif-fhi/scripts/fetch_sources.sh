#!/bin/sh
set -eu

workdir="${1:-.local/004-4h-sic-gs-from-cif-fhi}"
downloads="$workdir/downloads"
mkdir -p "$downloads"

curl -fL -o "$downloads/4H-SiC-aflow.cif" \
  https://raw.githubusercontent.com/aflow-org/aflow_prototype_encyclopedia/97fa9596493465a4349736abcb8d862d11b8004d/data/AB_hP8_186_ab_ab-001/aflow.cif
curl -fL -o "$downloads/06-C.LDA.fhi" \
  https://www.abinit.org/atomic_data/psps/miscellaneous/ATOMICDATA/LDA_FHI/06-C.LDA.fhi
curl -fL -o "$downloads/14-Si.LDA.fhi" \
  https://www.abinit.org/atomic_data/psps/miscellaneous/ATOMICDATA/LDA_FHI/14-Si.LDA.fhi

expected_cif="8d5696467e6ffccb5fd9b45dcf62a616de36e8389a1912c292dcdb9a9771a89a"
expected_c="cccd183e2f42e0464326a26899c00165daa7ca0d08182e610ce9b09692e24f12"
expected_si="835f3f3affacd5bb64dcfbee39b4f68de82289eeeacaea97d6b726ea5ca96b84"

actual_cif=$(shasum -a 256 "$downloads/4H-SiC-aflow.cif" | awk '{print $1}')
actual_c=$(shasum -a 256 "$downloads/06-C.LDA.fhi" | awk '{print $1}')
actual_si=$(shasum -a 256 "$downloads/14-Si.LDA.fhi" | awk '{print $1}')

test "$actual_cif" = "$expected_cif"
test "$actual_c" = "$expected_c"
test "$actual_si" = "$expected_si"
