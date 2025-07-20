#!/bin/bash
export DISPLAY=:0
export XAUTHORITY=$HOME/.Xauthority
cd "$(dirname "$0")"
gnome-screenshot -f "$1"
