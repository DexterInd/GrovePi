#! /bin/bash

PIHOME=/home/pi
DEXTERSCRIPT=$PIHOME/Dexter/lib/Dexter/script_tools
USER_ID=$(/usr/bin/id -u)
USER_NAME=$(/usr/bin/who am i | awk '{ print $1 }')
SCRIPT_PATH=$(/usr/bin/realpath $0)
DIR_PATH=$(/usr/bin/dirname ${SCRIPT_PATH} | sed 's/\/Script$//')
REPO_PATH=$(readlink -f $(dirname $0) | grep -E -o "^(.*?\\GrovePi)")

source $DEXTERSCRIPT/functions_library.sh

display_welcome_msg() {
	echo "Special thanks to Joe Sanford at Tufts University. This script was derived from his work. Thank you Joe!"
}

install_dependencies() {
    # the sudo apt-get update is already
    # done by the script_tools installer in
    # update_grovepi.sh

  	feedback "Installing dependencies for the GrovePi"
    # in order for nodejs to be installed, the repo for it
    # needs to be in; this is all done in script_tools while doing an apt-get update
    sudo apt-get install nodejs -y

  	sudo apt-get install git libi2c-dev i2c-tools arduino minicom -y
    sudo apt-get install python-pip  python-smbus  python-dev  python-serial  python-rpi.gpio  python-scipy  python-numpy -y
    sudo apt-get install python3-pip python3-smbus python3-dev python3-serial python3-rpi.gpio python3-scipy python3-numpy -y

    feedback "Dependencies for the GrovePi installed"
}

check_root_user() {
    if [[ $EUID -ne 0 ]]; then
        feedback "FAIL!  This script must be run as such: sudo ./install.sh"
        exit 1
    fi
}

install_spi_i2c() {
	RASPI_BL="/etc/modprobe.d/raspi-blacklist.conf.bak"
	MODS="i2c spi"
	if [ -f ${RASPI_BL} ]; then
		feedback "Removing blacklist from ${RASPI_BL} . . ."
		for i in ${MODS}
		do
			MOD_NAME=$(echo $i | tr [a-z] [A-Z])
			sudo sed -i -e "s/blacklist ${i}-bcm2708/#blacklist ${i}-bcm2708/g" ${RASPI_BL}
			echo "${MOD_NAME} not present or removed from blacklist"
		done
	fi

	#Adding in /etc/modules
	feedback "Adding I2C-dev and SPI-dev in /etc/modules . . ."
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

	feedback "Making I2C changes in /boot/config.txt . . ."

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
	feedback "Installing avrdude for the GrovePi"
	source $DEXTERSCRIPT/install_avrdude.sh
	create_avrdude_folder
  install_avrdude
  cd $ROBOT_DIR
  echo "done with AVRDUDE for the GrovePi"
}

display_welcome_msg
check_root_user
install_dependencies
install_spi_i2c
install_avr
