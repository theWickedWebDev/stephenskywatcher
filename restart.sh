#! /usr/bin/sh
clear
pkill -9 -f "python3 -m src.main"
pkill -9 -f "/usr/libexec/gvfs-gphoto2-volume-monitor"
pkill -9 -f "/home/stephen/skywatcher/.venv/bin/python -m src.main"
/home/stephen/skywatcher/.venv/bin/python -m src.main

# $(basename $0)
# x-terminal-emulator -e ./run.sh