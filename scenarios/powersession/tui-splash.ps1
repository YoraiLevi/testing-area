# S3 tui-splash: launch the omp TUI splash/onboarding screen. omp never exits on
# its own headlessly, so drive.py runs a watchdog that tree-kills PowerSession
# after the splash has rendered (PowerSession cannot send an interactive quit to
# the TUI headlessly). Recording the onboarding screen without keys is honest.
omp --no-session
