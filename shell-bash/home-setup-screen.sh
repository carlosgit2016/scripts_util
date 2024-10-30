#!/bin/bash

set -e

xrandr --output HDMI-1 --auto --left-of eDP-1
xrandr --output eDP-1 --off
