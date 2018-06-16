#!/bin/sh

echo "Generating lines of code summary…"

SCRIPT_FILE="/Users/Rainland/Programming/Python/locc/locc.py"
OUTPUT_FILE="/Users/Rainland/Desktop/locc_output.txt"

if [ -f $SCRIPT_FILE ]; then
	echo "Found $SCRIPT_FILE"
	/usr/bin/python $SCRIPT_FILE -files=h,m .
else
	echo "Could not find script file."
fi
