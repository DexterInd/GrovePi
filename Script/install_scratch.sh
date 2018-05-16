echo "This script will install Scratch for GrovePi+ on a standard Stretch Raspbian"


PIHOME=/home/pi
RASPBIAN=$PIHOME/di_update/Raspbian_For_Robots
DEXTER=Dexter
ROBOT_FOLDER=GrovePi
LIB=lib
LIB_PATH=$PIHOME/$DEXTER/$LIB
DEXTERLIB_PATH=$LIB_PATH/$DEXTER
SCRATCH=Scratch_GUI
SCRATCH_PATH=$DEXTERLIB_PATH/$SCRATCH

if [ ! -d "$DEXTERLIB_PATH" ]
then
    echo "getting some helpers"
    # get the bash helper tools
    curl https://raw.githubusercontent.com/DexterInd/script_tools/master/install_script_tools.sh | bash
    pushd $DEXTERLIB_PATH/script_tools
    sudo python autodetect_setup.py install
    popd > /dev/null
fi
source $PIHOME/$DEXTER/lib/$DEXTER/script_tools/functions_library.sh

# feedback  "Installing some libraries"
# sudo apt-get install python-smbus python3-smbus

feedback "activating I2C"
sudo sed -i "/i2c-dev/d" /etc/modules
sudo echo "i2c-dev" >> /etc/modules
sudo sed -i "/dtparam=i2c_arm=on/d" /boot/config.txt
sudo echo "dtparam=i2c_arm=on" >> /boot/config.txt

feedback "Installing Scratch Environment"

create_folder $PIHOME/$DEXTER
create_folder $PIHOME/$DEXTER/$LIB
create_folder $PIHOME/$DEXTER/$LIB/$DEXTER
create_folder $PIHOME/$DEXTER/$LIB/$DEXTER/$SCRATCH

# installing scratch
pushd $LIB_PATH > /dev/null
delete_folder scratchpy
git clone https://github.com/DexterInd/scratchpy
cd scratchpy
sudo make install > /dev/null
popd > /dev/null



# Copy shortcut to desktop.
feedback "Installing Scratch on the desktop"

if [ -f "/usr/bin/scratch" ]
then
    echo "Installing support for Scratch"
    sudo cp $PIHOME/$DEXTER/$ROBOT_FOLDER/Software/Scratch/Local_Scratch_Start.desktop /home/pi/Desktop/Local_Scratch_Start.desktop
fi

if [ -f "/usr/bin/scratch2" ]
then
    echo "Installing support for Scratch 2"
    pushd $PIHOME/$DEXTER/GrovePi/Software/Scratch/s2pifiles > /dev/null
    sudo cp extensions.json /usr/lib/scratch2/scratch_extensions/extensions.json
    sudo cp piGrovePiExtension.js /usr/lib/scratch2/scratch_extensions/piGrovePiExtension.js
    sudo cp grovepi.html /usr/lib/scratch2/scratch_extensions/grovepi.html
    sudo cp -u grovepi.png /usr/lib/scratch2/medialibrarythumbnails/grovepi.png
    popd > /dev/null
    sudo cp $PIHOME/$DEXTER/$ROBOT_FOLDER/Software/Scratch/Local_Scratch2_Start.desktop /home/pi/Desktop/Local_Scratch2_Start.desktop
fi

# Desktop shortcut permissions.
sudo chmod +x $PIHOME/Desktop/Local_Scratch_Start.desktop

# Make select_state, error_log, nohup.out readable and writable
sudo echo "GrovePi" >> $SCRATCH_PATH/selected_state
sudo touch $SCRATCH_PATH/error_log
sudo chmod 666 $SCRATCH_PATH/selected_state
sudo chmod 666 $SCRATCH_PATH/error_log

sudo cp  $PIHOME/$DEXTER/$ROBOT_FOLDER/Software/Scratch/new.sb $PIHOME/$DEXTER/$LIB/$DEXTER/$SCRATCH/new.sb

# transferring Scratch examples into proper Scratch folder
sudo rm  /usr/share/scratch/Projects/$ROBOT_FOLDER 2> /dev/null
sudo ln -s $PIHOME/$DEXTER/$ROBOT_FOLDER/Software/Scratch/Examples /usr/share/scratch/Projects/$ROBOT_FOLDER  2> /dev/null

feedback "You now have a Scratch icon on your desktop. Double clicking it will start Scratch with all the necessary configuration to control your GrovePi+"
feedback "Please note that you cannot use Scratch from the menu or double click on a Scratch file to control your robot."