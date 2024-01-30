#!/bin/bash

set -e

xrandr --output DP-2 --auto --primary
xrandr -o right
xrandr --output HDMI-1 --auto --left-of DP-2
xrandr --output eDP-1 --off

i3-msg 'workspace 1'
i3-msg 'workspace 10; exec /usr/bin/google-chrome --new-window --profile-direcory="Profile 1" spotify.com pomofocus.io'
