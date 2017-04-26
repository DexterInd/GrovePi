#! /bin/bash
curl --silent https://raw.githubusercontent.com/DexterInd/script_tools/master/install_script_tools.sh | bash

PIHOME=/home/pi
DEXTERSCRIPT=$PIHOME/Dexter/lib/Dexter/script_tools
USER_ID=$(/usr/bin/id -u)
USER_NAME=$(/usr/bin/who am i | awk '{ print $1 }')
SCRIPT_PATH=$(/usr/bin/realpath $0)
DIR_PATH=$(/usr/bin/dirname ${SCRIPT_PATH} | sed 's/\/Script$//')
REPO_PATH=$(readlink -f $(dirname $0) | grep -E -o "^(.*?\\GrovePi)")

source $DEXTERSCRIPT/functions_library.sh

identify_cie() {
    if ! quiet_mode
    then
        echo "  _____            _                                ";
        echo " |  __ \          | |                               ";
        echo " | |  | | _____  _| |_ ___ _ __                     ";
        echo " | |  | |/ _ \ \/ / __/ _ \ '__|                    ";
        echo " | |__| |  __/>  <| ||  __/ |                       ";
        echo " |_____/ \___/_/\_\\\__\___|_|          _            ";
        echo " |_   _|         | |         | |      (_)           ";
        echo "   | |  _ __   __| |_   _ ___| |_ _ __ _  ___  ___  ";
        echo "   | | | '_ \ / _\ | | | / __| __| '__| |/ _ \/ __| ";
        echo "  _| |_| | | | (_| | |_| \__ \ |_| |  | |  __/\__ \ ";
        echo " |_____|_| |_|\__,_|\__,_|___/\__|_|  |_|\___||___/ ";
        echo "                                                    ";
        echo "                                                    ";
        echo " "
    fi
}

identify_robot() {
	echo "  _____                    _____ _ "
	echo " / ____|                  |  __ (_)  "
	echo "| |  __ _ __ _____   _____| |__) |   "
	echo "| | |_ | '__/ _ \ \ / / _ \  ___/ |  "
	echo "| |__| | | | (_) \ V /  __/ |   | |  "
	echo " \_____|_|  \___/ \_/ \___|_|   |_|  "

	feedback "Welcome to GrovePi Installer."
}

display_welcome_msg() {
	echo " "
	echo "Requirements:"
	echo "1) Must be connected to the internet"
	echo "2) This script must be run as root user"
	echo " "
	echo "Steps:"
	echo "1) Installs package dependencies:"
	echo "   - python-pip       alternative Python package installer"
	echo "   - git              fast, scalable, distributed revision control system"
	echo "   - libi2c-dev       userspace I2C programming library development files"
	echo "   - python-serial    pyserial - module encapsulating access for the serial port"
	echo "   - python-rpi.gpio  Python GPIO module for Raspberry Pi"
	echo "   - i2c-tools        This Python module allows SMBus access through the I2C /dev"
	echo "   - python-smbus     Python bindings for Linux SMBus access through i2c-dev"
	echo "   - python3-smbus    Python3 bindings for Linux SMBus access through i2c-dev"
	echo "   - arduino          AVR development board IDE and built-in libraries"
	echo "   - minicom          friendly menu driven serial communication program"
	echo "2) Clone, build wiringPi in GrovePi/Script and install it"
	echo "3) Removes I2C and SPI from modprobe blacklist /etc/modprobe.d/raspi-blacklist.conf"
	echo "4) Adds I2C-dev, i2c-bcm2708 and spi-dev to /etc/modules"
	echo "5) Installs gertboard avrdude_5.10-4_armhf.deb package"
	echo "6) Runs gertboard setup"
	echo "   - configures avrdude"
	echo "   - downloads gertboard known boards and programmers"
	echo "   - replaces avrsetup with gertboards version"
	echo "   - in /etc/inittab comments out lines containing AMA0"
	echo "   - in /boot/cmdline.txt removes: console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1"
	echo "   - in /usr/share/arduino/hardware/arduino creates backup of boards.txt"
	echo "   - in /usr/share/arduino/hardware/arduino creates backup of programmers.txt"
	echo " "
	echo "Special thanks to Joe Sanford at Tufts University. This script was derived from his work. Thank you Joe!"
	echo " "
	echo "Raspberry Pi wil reboot after completion."
	echo " "
	echo " "
}

check_root_user() {
    if [[ $EUID -ne 0 ]]; then
        feedback "FAIL!  This script must be run as such: sudo ./install.sh"
        exit 1
    fi
    echo " "
}

check_internet() {
    if ! quiet_mode ; then
        feedback "Check for internet connectivity..."
        feedback "=================================="
        wget -q --tries=2 --timeout=20 --output-document=/dev/null https://raspberrypi.org
        if [ $? -eq 0 ];then
            echo "Connected to the Internet"
        else
            echo "Unable to Connect, try again !!!"
            exit 0
        fi
    fi
}

install_dependencies() {
    if ! quiet_mode ; then
        sudo apt-get update
    fi
    echo " "
	feedback "Installing Dependencies"
	echo "======================="
	sudo apt-get install python-pip git libi2c-dev python-serial i2c-tools python-smbus python3-smbus arduino minicom python-dev -y
	sudo apt-get purge python-rpi.gpio -y
	sudo apt-get purge python3-rpi.gpio -y
	sudo apt-get install python-rpi.gpio -y
	sudo apt-get install python3-rpi.gpio -y
	sudo pip install -U RPi.GPIO

    feedback "Dependencies installed"
}

install_wiringpi() {
    # Check if WiringPi Installed

    # using curl piped to bash does not leave a file behind. no need to remove it
    # we can do either the curl - it works just fine
    # sudo curl https://raw.githubusercontent.com/DexterInd/script_tools/master/update_wiringpi.sh | bash
    # or call the version that's already on the SD card
    sudo bash $DEXTERSCRIPT/update_wiringpi.sh
    # done with WiringPi

    # remove wiringPi directory if present
    if [ -d wiringPi ]
    then
        sudo rm -r wiringPi
    fi
    # End check if WiringPi installed
    echo " "
}

install_spi_i2c() {
	echo " "
	RASPI_BL="/etc/modprobe.d/raspi-blacklist.conf.bak"
	MODS="i2c spi"
	if [ -f ${RASPI_BL} ]; then
		feedback "Removing blacklist from ${RASPI_BL} . . ."
		feedback "=================================================================="
		echo " "
		for i in ${MODS}
		do
			MOD_NAME=$(echo $i | tr [a-z] [A-Z])
			sudo sed -i -e "s/blacklist ${i}-bcm2708/#blacklist ${i}-bcm2708/g" ${RASPI_BL}
			echo "${MOD_NAME} not present or removed from blacklist"
		done
	fi

	#Adding in /etc/modules
	feedback " "
	feedback "Adding I2C-dev and SPI-dev in /etc/modules . . ."
	feedback "================================================"
	if grep -q "i2c-dev" /etc/modules; then
		echo "I2C-dev already present"
	else
		echo i2c-dev >> /etc/modules
		echo "I2C-dev added"
	fi
	if grep -q "i2c-bcm2708" /etc/modules; then
		echo "i2c-bcm2708 already present"
	else
		echo i2c-bcm2708 >> /etc/modules
		echo "i2c-bcm2708 added"
	fi
	if grep -q "spi-dev" /etc/modules; then
		echo "spi-dev already present"
	else
		echo spi-dev >> /etc/modules
		echo "spi-dev added"
	fi

	echo " "
	feedback "Making I2C changes in /boot/config.txt . . ."
	feedback "================================================"

	BOOT_CONFIG="/boot/config.txt"
	DTPARAMS="i2c1 i2c_arm"
	for i in ${DTPARAMS}
	do
		if grep -q "^dtparam=${i}=on$" ${BOOT_CONFIG}; then
			echo "${i} already present"
		else
			echo "dtparam=${i}=on" >> /boot/config.txt
		fi
	done

	sudo adduser ${USER_NAME} i2c
	sudo chmod +x ${DIR_PATH}/Software/Scratch/GrovePi_Scratch_Scripts/*.sh
}

install_avr() {
	feedback "Installing avrdude"
	feedback "=================="
	source /home/pi/Dexter/lib/Dexter/script_tools/install_avrdude.sh
	create_avrdude_folder
    install_avrdude
    cd $ROBOT_DIR
    echo "done with AVRDUDE "
}

install_python_libs(){
	feedback "Install python libraries"
	echo "If you see errors related to /etc/inittab, it's fine."
	echo "/etc/inittab has been deprecated in favor of systemd,"
	echo "cfr. https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=123081"

	echo " "

	sudo apt-get install python-smbus -y

	echo " "
	echo "Making libraries global . . ."
	echo "============================="
	if [ -d /usr/lib/python2.7/dist-packages ]; then
		# Usually "/" used as delimter in sed commands but since REPO_PATH variable contains many "/" and sed command gets
		# confused on expanding REPO_PATH as it finds "/" to be delimeters, hence here "@" is used as delimeter
		sudo sed -i "s@^/Software@$REPO_PATH&@" $REPO_PATH/Script/grove.pth
		sudo cp ${DIR_PATH}/Script/grove.pth /usr/lib/python2.7/dist-packages/grove.pth
	else
		echo "/usr/lib/python2.7/dist-packages not found, exiting"
		exit 1
	fi
	echo "Done"
}

call_for_reboot() {
    if ! quiet_mode ; then
        feedback " "
        feedback "Please restart the Raspberry Pi for the changes to take effect"
        feedback " "
        feedback "Please restart to implement changes!"
        feedback "  _____  ______  _____ _______       _____ _______ "
        feedback " |  __ \|  ____|/ ____|__   __|/\   |  __ \__   __|"
        feedback " | |__) | |__  | (___    | |  /  \  | |__) | | |   "
        feedback " |  _  /|  __|  \___ \   | | / /\ \ |  _  /  | |   "
        feedback " | | \ \| |____ ____) |  | |/ ____ \| | \ \  | |   "
        feedback " |_|  \_\______|_____/   |_/_/    \_\_|  \_\ |_|   "
        feedback " "
        feedback "Please restart to implement changes!"
        feedback "To Restart type sudo reboot"
    fi
}

identify_cie
identify_robot
display_welcome_msg
# sleep 5
check_internet
check_root_user
install_dependencies
install_wiringpi
install_spi_i2c
install_avr
install_python_libs
call_for_reboot
