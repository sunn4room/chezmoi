#!/bin/sh

function notify() {
	percentage=`expr $(brightnessctl g)00 / $(brightnessctl m)`"\%"
	notify-send -t 5000 -r 2 "backlight" "$percentage"
}

case "$1" in
	up)
		brightnessctl s 2%+
		notify
		;;
	down)
		brightnessctl s 2%-
		notify
		;;
esac

