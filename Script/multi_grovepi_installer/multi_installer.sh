#!/usr/bin/env sh
echo "Current setup"
sudo i2cdetect -y 1

echo "What address would you like to use the GrovePi on? [3-9 a-c]"
read ADDRESS

# Check if the necessary files for the address exist.
if [ -e "grove_pi_v1_4_0_addr$ADDRESS.hex" ] && [ -e "setup$ADDRESS.py" ] && [ -e "grovepi$ADDRESS.py" ]; then
  echo "Setting up GrovePi with Address $ADDRESS"
  echo "BURNING FIRMWARE"
  echo "..."
  sudo avrdude -c gpio -p m328p -U flash:w:grove_pi_v1_4_0_addr"$ADDRESS".hex
  echo "INSTALLING PYTHON LIBRARY"
  sudo python setup"$ADDRESS".py install
  sudo python3 setup"$ADDRESS".py install
  echo "I2C DEVICES AVAILABLE"
  sleep 1
  sudo i2cdetect -y 1
  exit 0
else
  echo "The necessary files for this address do not exist."
  exit 0
fi

# thanks to https://github.com/Mimry  for the rewrite of this script. Much appreciated!