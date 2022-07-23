#!/bin/sh

function notify() {
	percentage=`pactl get-sink-volume @DEFAULT_SINK@ | sed -n '1p' | awk '{print $5}'`
	notify-send -t 5000 -r 1 "audio" "$percentage"
}

case "$1" in
	up)
		pactl set-sink-volume @DEFAULT_SINK@ +2%
		notify
		;;
	down)
		pactl set-sink-volume @DEFAULT_SINK@ -2%
		notify
		;;
esac

