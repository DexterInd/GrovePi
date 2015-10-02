#! /bin/bash
echo ""
echo Checking for Atmega chip
echo ========================
echo ""
avrdude -c gpio -p m328p -v