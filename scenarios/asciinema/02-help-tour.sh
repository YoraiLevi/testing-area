#!/usr/bin/env sh
# S2 help-tour (creative): run `omp --help` (long, colorized) and pause so the colored
# help renders, then exit. Exercises color + scrollback fidelity.
set -u
printf '%s\n' '$ omp --help'
omp --help
sleep 3
