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
RFR_TOOLS_PATH=$LIB_PATH/$DEXTER/RFR_Tools

# let's test for the presence of ~/Dexter/lib/Dexter as a sign that all tools are 
# pre-installed
if [ ! -d "$DEXTERLIB_PATH" ]
then
    echo "Installation issues. Please install GrovePi first."
    echo "curl -kL dexterindustries.com/update_grovepi | bash"
    exit 1
fi
if [ ! -d "$RFR_TOOLS_PATH" ]
then
    echo "Installation issues. Please install GrovePi first."
    echo "curl -kL dexterindustries.com/update_grovepi | bash"
    exit 2
fi
if [ ! -d "$PIHOME/$DEXTER/$ROBOT_FOLDER" ]
then
    echo "Installation issues. Please install GrovePi first."
    echo "curl -kL dexterindustries.com/update_grovepi | bash"
    exit 3
fi

source $DEXTERLIB_PATH/script_tools/functions_library.sh

# feedback  "Installing some libraries"
# sudo apt-get install python-smbus python3-smbus

setup_modules_and_config(){
    feedback "activating I2C"
    sudo sed -i "/i2c-dev/d" /etc/modules
    sudo echo "i2c-dev" >> /etc/modules
    sudo sed -i "/dtparam=i2c_arm=on/d" /boot/config.txt
    sudo echo "dtparam=i2c_arm=on" >> /boot/config.txt
}

install_scratchpy() {
    # installing scratch_controller
    pushd $LIB_PATH > /dev/null
    delete_folder scratchpy
    git clone --depth=1 https://github.com/DexterInd/scratchpy
    cd scratchpy
    sudo make install > /dev/null
    popd > /dev/null
}


# Copy shortcut to desktop.
install_desktop_icons() {
    feedback "Installing Scratch on the desktop"

    if [ -f "/usr/bin/scratch" ]
    then
        echo "Installing support for Scratch 1.4"
        echo $RFR_TOOLS_PATH/Scratch_GUI/Scratch_Start.desktop
        sudo cp $RFR_TOOLS_PATH/Scratch_GUI/Scratch_Start.desktop /home/pi/Desktop/Scratch_Start.desktop
    else 
        echo "scratch not found"
    fi

    if [ -f "/usr/bin/scratch2" ]
    then
        echo "Installing support for Scratch 2"
        pushd $PIHOME/$DEXTER/$ROBOT_FOLDER/Software/Scratch/s2pifiles > /dev/null
        sudo cp extensions.json /usr/lib/scratch2/scratch_extensions/extensions.json
        sudo cp piGrovePiExtension.js /usr/lib/scratch2/scratch_extensions/piGrovePiExtension.js
        sudo cp grovepi.html /usr/lib/scratch2/scratch_extensions/grovepi.html
        sudo cp -u grovepi.png /usr/lib/scratch2/medialibrarythumbnails/grovepi.png
        popd > /dev/null
        sudo cp $PIHOME/$DEXTER/$ROBOT_FOLDER/Software/Scratch/Local_Scratch2_Start.desktop /home/pi/Desktop/Local_Scratch2_Start.desktop
    fi

    # Desktop shortcut permissions.
    sudo chmod +x $PIHOME/Desktop/*.desktop
}

feedback "Installing Scratch Environment"
setup_modules_and_config
install_scratchpy

sudo rm -r $DEXTERLIB_PATH/$SCRATCH
mkdir -p $DEXTERLIB_PATH/$SCRATCH
cp -r $RFR_TOOLS_PATH/$SCRATCH $DEXTERLIB_PATH/

install_desktop_icons

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