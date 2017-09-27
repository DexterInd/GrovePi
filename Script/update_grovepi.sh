# This script updates the the code repos on Raspbian for Robots.

# definitions needed for standalone call
PIHOME=/home/pi
DEXTER=Dexter
DEXTER_PATH=$PIHOME/$DEXTER
RASPBIAN=$PIHOME/di_update/Raspbian_For_Robots
curl --silent https://raw.githubusercontent.com/DexterInd/script_tools/master/install_script_tools.sh | bash

# needs to be sourced from here when we call this as a standalone
source /home/pi/$DEXTER/lib/$DEXTER/script_tools/functions_library.sh

GROVEPI_DIR=$DEXTER_PATH/GrovePi

# Check for a GrovePi directory under "Dexter" folder.  If it doesn't exist, create it.

if [ -d "$GROVEPI_DIR" ]; then
    echo "GrovePi Directory Exists"
    cd $GROVEPI_DIR             # Go to directory
    sudo git fetch origin       # Hard reset the git files
    sudo git reset --hard  
    sudo git merge origin/master
else
	echo "Cloning"
    cd $PIHOME/$DEXTER/
    git clone https://github.com/DexterInd/GrovePi
    cd GrovePi
fi

change_branch $BRANCH   # Change to a branch we're working on in the GrovePi Directory. 
                        # Variable $BRANCH comes from /upd_script/fetch.sh

feedback "--> Start GrovePi update install."
feedback "---------------------------------"
pushd $PIHOME/$DEXTER/GrovePi/Script > /dev/null
sudo chmod +x install.sh
sudo bash ./install.sh
popd > /dev/null
