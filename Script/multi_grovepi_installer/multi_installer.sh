#!/usr/bin/env sh
echo "What address would you like to use the GrovePi on?"
read ADDRESS

# Check if the neccessary files for the address exist.
if [ -e "grove_pi_v1_2_2_addr$ADDRESS.cpp.hex" ] && [ -e "setup$ADDRESS.py" ] && [ -e "grovepi$ADDRESS.py" ]; then
  echo "Setting up GrovePi with Address $ADDRESS"
  echo "BURNING FIRMWARE"
  echo "..."
  sudo avrdude -c gpio -p m328p -U flash:w:grove_pi_v1_2_2_addr"$ADDRESS".cpp.hex
  echo "INSTALLING PYTHON LIBRARY"
  sudo python setup"$ADDRESS".py install
  echo "I2C DEVICES AVAILABLE"
  sleep 1
  sudo i2cdetect -y 1
  exit 0
else
  echo "The neccessary files for this address do not exist."
  exit 0
fi
