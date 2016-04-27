#! /bin/bash

echo =============================
echo GrovePi Troubleshooting Script
echo ============================= 

echo ""
echo Adding permissions to the scripts
echo ================================= 
chmod +x software_status.sh
chmod +x avrdude_test.sh
chmod +x i2c_test1.sh
chmod +x firmware_version_test.sh

echo "Choose a test to run:"
echo =======================
echo 1. Software status test
echo 2. Atmega Test
echo 3. I2C test
echo 4. Firmware test
echo 5. Complete test
echo 6. Exit

read -n1 -p "Select and option:" doit 
case $doit in  
  1) sudo ./software_status.sh 2>&1| tee log.txt ;;
  2) sudo ./avrdude_test.sh 2>&1| tee log.txt ;;
  3) sudo ./i2c_test1.sh 2>&1| tee log.txt ;;
  4) sudo ./firmware_version_test.sh 2>&1| sudo tee log.txt ;;
  5) sudo ./software_status.sh 2>&1| tee log.txt ;
	 sudo ./avrdude_test.sh 2>&1| tee -a log.txt ;
	 sudo ./i2c_test1.sh 2>&1| tee -a log.txt  ;
	 sudo ./firmware_version_test.sh 2>&1| tee -a log.txt  ;;
  *) echo Exiting ;; 
esac

cp log.txt /home/pi/Desktop/log.txt
echo "Log has been saved to Desktop. Please copy it and send it by email or upload it on the forums"
