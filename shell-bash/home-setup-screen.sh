#!/bin/bash

set -e

xrandr --output HDMI-1 --auto --left-of DP-2
xrandr --output eDP-1 --off
