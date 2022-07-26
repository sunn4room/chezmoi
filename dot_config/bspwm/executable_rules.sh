#!/bin/sh

eval `xprop -id $1 | awk '{
	split($0, kv, " = ")
	if ("WM_NAME(STRING)" == kv[1]) print "name="kv[2]
	else if ("WM_NAME(UTF8_STRING)" == kv[1]) print "name="kv[2]
	else if ("WM_CLASS(STRING)" == kv[1]) {
		split(kv[2], arr, ", ")
		print "class0="arr[1]"; class1="arr[2]
	}
	else if ("WM_CLASS(UTF8_STRING)" == kv[1]) {
		split(kv[2], arr, ", ")
		print "class0="arr[1]"; class1="arr[2]
	}
	else if ("WM_WINDOW_ROLE(STRING)" == kv[1]) print "role="kv[2]
	else if ("WM_WINDOW_ROLE(UTF8_STRING)" == kv[1]) print "role="kv[2]
}'`

if [ -n "$name" ]; then
	case "$name" in
		floating)
			echo 'state=floating'
			;;
		"Task Manager - Vivaldi")
			echo 'state=floating'
			;;
	esac
fi

if [ -n "$class0" ]; then
	case "$class0" in
		dropdown)
			echo 'state=floating sticky=on'
			;;
	esac
fi

if [ -n "$class1" ]; then
	case "$class1" in
		Ulauncher|ulauncher)
			echo 'state=floating sticky=on border=off'
			;;
		copyq)
			echo 'state=floating sticky=on'
			;;
		Nitrogen)
			echo 'state=floating'
			;;
		Thunar)
			echo 'state=floating'
			;;
		Pcmanfm)
			echo 'state=floating'
			;;
		Lxappearance)
			echo 'state=floating'
			;;
		qt5ct)
			echo 'state=floating'
			;;
		"VirtualBox Manager")
			echo 'desktop=9 follow=on'
			;;
		"VirtualBox Machine")
			echo 'desktop=9 follow=on'
			;;
		"KeePassXC")
			echo 'desktop=0 follow=on'
			;;
	esac
fi

if [ -n "$role" ]; then
	case "$role" in
		browser)
			echo 'desktop=2'
			;;
	esac
fi

