#! /bin/bash

echo =============================
echo GrovePi Troubleshooting Script
echo ============================= 

cd /home/pi/Desktop/GrovePi/Troubleshooting
echo ""
echo Adding permissions to the scripts
echo ================================= 
chmod +x software_status.sh
chmod +x avrdude_test.sh
chmod +x i2c_test1.sh
chmod +x firmware_version_test.sh

sudo ./software_status.sh | tee log.txt
sudo ./avrdude_test.sh 2>&1| tee -a log.txt
sudo ./i2c_test1.sh | tee -a log.txt
sudo ./firmware_version_test.sh | tee -a log.txt

cp log.txt /home/pi/Desktop/log.txt
echo "Log has been saved to Desktop. Please copy it and send it by email or upload it on the forums"