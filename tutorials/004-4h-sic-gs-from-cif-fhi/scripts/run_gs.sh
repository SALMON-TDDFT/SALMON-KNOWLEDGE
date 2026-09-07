#!/bin/sh
set -eu

: "${SALMON:?Set SALMON to the MPI-enabled SALMON executable.}"

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
card_dir=$(dirname "$script_dir")
workdir="${1:-.local/004-4h-sic-gs-from-cif-fhi}"
nprocs="${NPROCS:-4}"

if [ "$nprocs" != 4 ]; then
  echo "This input fixes nproc_k=4; set NPROCS=4." >&2
  exit 2
fi

mkdir -p "$workdir/gs"
cp "$card_dir/inputs/4h-sic-gs.inp" "$workdir/gs/input.inp"
cd "$workdir/gs"
mpirun -n "$nprocs" "$SALMON" < input.inp > stdout.log 2> stderr.log
