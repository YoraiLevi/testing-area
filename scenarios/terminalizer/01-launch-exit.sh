#!/usr/bin/env sh
# S1 launch-exit (minimal, REQUIRED): show a prompt, run `omp --version`, pause so the
# version line is legible, then exit cleanly. Terminalizer records this via the record
# step's `-d 'bash <this>'`; the script exiting ends the recording.
set -u
printf '%s\n' '$ omp --version'
omp --version
sleep 2
printf '%s\n' '$ exit'
sleep 1
