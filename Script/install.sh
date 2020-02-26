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

check_root_user() {
    if [[ $EUID -ne 0 ]]; then
        feedback "FAIL!  This script must be run as such: sudo ./install.sh"
        exit 1
    fi
}
compatible_with_pi4() {
	BOARDVERSION=$(cat /proc/device-tree/model | awk '{ print $3 }')
	BOOT_CONFIG="/boot/config.txt"
	if [ "${BOARDVERSION}" -eq '4' ]; then
		if grep -q "gpio=8=op,dh" ${BOOT_CONFIG}; then
			echo "Pi4 already configured"
		else
			echo "gpio=8=op,dh" >> /boot/config.txt
		fi
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
compatible_with_pi4
install_spi_i2c
install_avr
