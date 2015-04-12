#!/usr/bin/env sh
while true ; do
    echo "What address would you like to use the GrovePi on?"
	echo "Addr:"
    echo " 3"
    echo " 4 (Default)"
    echo " 5"
    echo " 6"
    echo " 7"
    echo "Any other key to exit"

    read INPUT
    if [ $INPUT -eq 3 ] ; then
        echo "Setting up GrovePi with Address 3"
        echo "..."
		echo "BURNING FIRMWARE"
		sudo avrdude -c gpio -p m328p -U flash:w:grove_pi_v1_2_2_addr3.cpp.hex
		echo "INSTALLING PYTHON LIBRARY"
		sudo python setup3.py install
		echo "I2C DEVICES AVAILABLE"
		sleep 1
		sudo i2cdetect -y 1
		exit 0
		
    elif [ $INPUT -eq 4 ] ; then
        echo "Setting up GrovePi with Address 4"
        echo "..."
		echo "BURNING FIRMWARE"
		sudo avrdude -c gpio -p m328p -U flash:w:grove_pi_v1_2_2_addr4.cpp.hex
		echo "INSTALLING PYTHON LIBRARY"
		sudo python setup4.py install
		echo "I2C DEVICES AVAILABLE"
		sleep 1
		sudo i2cdetect -y 1
		
		exit 0
		
    elif [ $INPUT -eq 5 ] ; then
        echo "Setting up GrovePi with Address 5"
        echo "..."
		echo "BURNING FIRMWARE"
		sudo avrdude -c gpio -p m328p -U flash:w:grove_pi_v1_2_2_addr5.cpp.hex
		echo "INSTALLING PYTHON LIBRARY"
		sudo python setup5.py install
		echo "I2C DEVICES AVAILABLE"
		sleep 1
		sudo i2cdetect -y 1
		exit 0
		
    elif [ $INPUT -eq 6 ] ; then
        echo "Setting up GrovePi with Address 6"
        echo "..."
		echo "BURNING FIRMWARE"
		sudo avrdude -c gpio -p m328p -U flash:w:grove_pi_v1_2_2_addr6.cpp.hex
		echo "INSTALLING PYTHON LIBRARY"
		sudo python setup6.py install
		echo "I2C DEVICES AVAILABLE"
		sleep 1
		sudo i2cdetect -y 1
		exit 0
		
    elif [ $INPUT -eq 7 ] ; then
        echo "Setting up GrovePi with Address 7"
        echo "..."
		echo "BURNING FIRMWARE"
		sudo avrdude -c gpio -p m328p -U flash:w:grove_pi_v1_2_2_addr7.cpp.hex
		echo "INSTALLING PYTHON LIBRARY"
		sudo python setup7.py install
		echo "I2C DEVICES AVAILABLE"
		sleep 1
		sudo i2cdetect -y 1
		exit 0
		
    else
        echo "invalid choice"
		exit 0
    fi
done