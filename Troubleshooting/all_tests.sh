#! /bin/bash
REPO_PATH=$(readlink -f $(dirname $0) | grep -E -o "^(.*?\\GrovePi)")
echo =============================
echo GrovePi Troubleshooting Script
echo =============================
cd $REPO_PATH/Troubleshooting
echo ""

sudo bash ./software_status.sh 2>&1 | sudo tee log.txt
# bash ./avrdude_test.sh 2>&1 | sudo tee -a log.txt
bash ./i2c_test1.sh 2>&1 | sudo tee -a log.txt
bash ./firmware_version_test.sh 2>&1 | sudo tee -a log.txt

sudo cp log.txt /home/pi/Desktop/log.txt
echo "Log has been saved to Desktop. Please copy it and send it by email or upload it on the forums"
