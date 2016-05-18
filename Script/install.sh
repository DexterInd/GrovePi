#! /bin/bash
echo -e "\E[32m"
echo "  _____            _                                ";
echo " |  __ \          | |                               ";
echo " | |  | | _____  _| |_ ___ _ __                     ";
echo " | |  | |/ _ \ \/ / __/ _ \ '__|                    ";
echo " | |__| |  __/>  <| ||  __/ |                       ";
echo " |_____/ \___/_/\_\\__\___|_| _        _            ";
echo " |_   _|         | |         | |      (_)           ";
echo "   | |  _ __   __| |_   _ ___| |_ _ __ _  ___  ___  ";
echo "   | | | '_ \ / _\` | | | / __| __| '__| |/ _ \/ __|";
echo "  _| |_| | | | (_| | |_| \__ \ |_| |  | |  __/\__ \ ";
echo " |_____|_| |_|\__,_|\__,_|___/\__|_|  |_|\___||___/ ";
echo -e "\E[0m"
echo "Welcome to GrovePi Installer."
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
sleep 5

echo " "
echo "Check for internet connectivity..."
echo "=================================="
wget -q --tries=2 --timeout=100 http://google.com -O /dev/null
if [ $? -eq 0 ];then
	echo "Connected"
else
	echo "Unable to Connect, try again !!!"
	exit 0
fi

USER_ID=$(/usr/bin/id -u)
USER_NAME=$(/usr/bin/who am i | awk '{ print $1 }')
SCRIPT_PATH=$(/usr/bin/realpath $0)
DIR_PATH=$(/usr/bin/dirname ${SCRIPT_PATH} | sed 's/\/Script$//')

if [ ${USER_ID} -ne 0 ]; then
    echo "Please run this as root."
    exit 1
fi

echo " "
echo "Installing Dependencies"
echo "======================="
sudo apt-get install python-pip git libi2c-dev python-serial i2c-tools python-smbus python3-smbus arduino minicom python-dev -y
sudo apt-get purge python-rpi.gpio -y
sudo apt-get purge python3-rpi.gpio -y
sudo apt-get install python-rpi.gpio -y
sudo apt-get install python3-rpi.gpio -y
sudo pip install -U RPi.GPIO
echo "Dependencies installed"

if [ -d wiringPi ]; then
    cd wiringPi
    git pull
else
    git clone git://git.drogon.net/wiringPi
    cd wiringPi
fi

./build
RES=$?

if [ $RES -ne 0 ]; then
  echo "Something went wrong building/installing wiringPi, exiting."
  exit 1
fi

echo "wiringPi Installed"

echo " "
RASPI_BL="/etc/modprobe.d/raspi-blacklist.conf.bak"
MODS="i2c spi"
if [ -f ${RASPI_BL} ]; then
    echo "Removing blacklist from ${RASPI_BL} . . ."
    echo "=================================================================="
    echo " "
    for i in ${MODS}
    do
        MOD_NAME=$(echo $i | tr [a-z] [A-Z])
        sudo sed -i -e "s/blacklist ${i}-bcm2708/#blacklist ${i}-bcm2708/g" ${RASPI_BL}
        echo "${MOD_NAME} not present or removed from blacklist"
    done
fi

#Adding in /etc/modules
echo " "
echo "Adding I2C-dev and SPI-dev in /etc/modules . . ."
echo "================================================"
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
echo "Making I2C changes in /boot/config.txt . . ."
echo "================================================"

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

#Adding ARDUINO setup files
echo " "
echo "Making changes to Arduino . . ."
echo "==============================="

cd /tmp
wget http://project-downloads.drogon.net/gertboard/avrdude_5.10-4_armhf.deb
sudo dpkg -i avrdude_5.10-4_armhf.deb
sudo chmod 4755 /usr/bin/avrdude

cd /tmp
wget http://project-downloads.drogon.net/gertboard/setup.sh
chmod +x setup.sh
sudo ./setup.sh
echo " "
echo "If you see errors related to /etc/inittab, it's fine."
echo "/etc/inittab has been deprecated in favor of systemd,"
echo "cfr. https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=123081"

echo " "
echo "Install smbus for python"
sudo apt-get install python-smbus -y

echo " "
echo "Making libraries global . . ."
echo "============================="
if [ -d /usr/lib/python2.7/dist-packages ]; then
    sudo cp ${DIR_PATH}/Script/grove.pth /usr/lib/python2.7/dist-packages/grove.pth
else
    echo "/usr/lib/python2.7/dist-packages not found, exiting"
    exit 1
fi

echo " "
echo "Please restart to implement changes!"
echo "  _____  ______  _____ _______       _____ _______ "
echo " |  __ \|  ____|/ ____|__   __|/\   |  __ \__   __|"
echo " | |__) | |__  | (___    | |  /  \  | |__) | | |   "
echo " |  _  /|  __|  \___ \   | | / /\ \ |  _  /  | |   "
echo " | | \ \| |____ ____) |  | |/ ____ \| | \ \  | |   "
echo " |_|  \_\______|_____/   |_/_/    \_\_|  \_\ |_|   "
echo " "
echo "Please restart to implement changes!"
echo "To Restart type sudo reboot"

echo "To finish changes, we will reboot the Pi."
echo "Pi must reboot for changes and updates to take effect."
echo "If you need to abort the reboot, press Ctrl+C.  Otherwise, reboot!"
echo "Rebooting in 5 seconds!"
sleep 1
echo "Rebooting in 4 seconds!"
sleep 1
echo "Rebooting in 3 seconds!"
sleep 1
echo "Rebooting in 2 seconds!"
sleep 1
echo "Rebooting in 1 seconds!"
sleep 1
echo "Rebooting now!  Your Pi wake up with a freshly updated Raspberry Pi!"
sleep 1
sudo reboot
