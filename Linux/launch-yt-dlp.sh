#!/bin/bash
directory="$(cd "$(dirname "$0")" && pwd)"
/usr/bin/python3 "$directory/yt-dlp-gui.py"
