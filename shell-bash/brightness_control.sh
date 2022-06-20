#!/bin/zsh

# getopts https://stackoverflow.com/questions/16483119/an-example-of-how-to-use-getopts-in-bash
# float number calculation https://www.shell-tips.com/bash/math-arithmetic-calculation/#gsc.tab=0
# output current screen brightness https://unix.stackexchange.com/questions/150816/how-can-i-lazily-read-output-from-xrandr

current_brightness () { xrandr --verbose | awk '/Brightness/ {print $2; exit}'  } 
up () { xrandr --output eDP-1 --brightness $(printf %.1f "$(current_brightness) + 0.1") }
down () { xrandr --output eDP-1 --brightness $(printf %.1f "$(current_brightness) - 0.1") }

while getopts "ud" option; do
	case "${option}" in
	  	u)
			up
			;;
		d)
			down
			;;
	esac
done
