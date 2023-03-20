#!/bin/bash

if [ $# -eq 0 ]; then
	echo "Enter the country name"
else
	case "$1" in
	ko) echo "Seoul" ;;
	us) echo "Washington" ;;
	cn) echo "Beijing" ;;
	jp) echo "Tokyo" ;;
	*) echo "your entry => $1 is not on the list."
	esac
fi
