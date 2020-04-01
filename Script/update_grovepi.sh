#! /bin/bash
# This script updates the the code repos on Raspbian for Robots.

################################################
######## Parsing Command Line Arguments ########
################################################

# definitions needed for standalone call
PIHOME=/home/pi
DEXTER=Dexter
DEXTER_PATH=$PIHOME/$DEXTER
RASPBIAN=$PIHOME/di_update/Raspbian_For_Robots
GROVEPI_DIR=$DEXTER_PATH/GrovePi
DEXTERSCRIPT=$DEXTER_PATH/lib/Dexter/script_tools

# the top-level module name of grovepi package
# used for detecting whether it's installed or not
REPO_PACKAGE=grovepi

# called way down bellow
check_if_run_with_pi() {
  ## if not running with the pi user then exit
  if [ $(id -ur) -ne $(id -ur pi) ]; then
    echo "GrovePi installer script must be run with \"pi\" user. Exiting."
    exit 6
  fi
}

# called way down below
parse_cmdline_arguments() {

  # whether to install the dependencies or not (avrdude, apt-get, wiringpi, and so on)
  installdependencies=true
  updaterepo=true
  install_rfrtools=true
  install_pkg_rfrtools=true
  install_rfrtools_gui=true

  # the following 3 options are mutually exclusive
  systemwide=true
  userlocal=false
  envlocal=false
  usepython3exec=true

  # the following option tells which branch has to be used
  selectedbranch="master"

  declare -ga rfrtools_options=("--system-wide")
  # iterate through bash arguments
  for i; do
    case "$i" in
      --no-dependencies)
        installdependencies=false
        ;;
      --no-update-aptget)
        updaterepo=false
        ;;
      --bypass-rfrtools)
        install_rfrtools=false
        ;;
      --bypass-python-rfrtools)
        install_pkg_rfrtools=false
        ;;
      --bypass-gui-installation)
        install_rfrtools_gui=false
        ;;
      --user-local)
        userlocal=true
        systemwide=false
        declare -ga rfrtools_options=("--user-local")
        ;;
      --env-local)
        envlocal=true
        systemwide=false
        declare -ga rfrtools_options=("--env-local")
        ;;
      --system-wide)
        ;;
      develop|feature/*|hotfix/*|fix/*|DexterOS*|v*)
        selectedbranch="$i"
        ;;
    esac
  done

  # show some feedback on the console
  if [ -f $DEXTERSCRIPT/functions_library.sh ]; then
    source $DEXTERSCRIPT/functions_library.sh
    # show some feedback for the GrovePi
    if [[ quiet_mode -eq 0 ]]; then
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
      echo "  _____                    _____ _ "
      echo " / ____|                  |  __ (_)  "
      echo "| |  __ _ __ _____   _____| |__) |   "
      echo "| | |_ | '__/ _ \ \ / / _ \  ___/ |  "
      echo "| |__| | | | (_) \ V /  __/ |   | |  "
      echo " \_____|_|  \___/ \_/ \___|_|   |_|  "
      echo " "
    fi

    feedback "Welcome to GrovePi Installer."
  else
    echo "Welcome to GrovePi Installer."
  fi

  echo "Updating GrovePi for $selectedbranch branch with the following options:"
  ([[ $installdependencies = "true" ]] && echo "  --no-dependencies=false") || echo "  --no-dependencies=true"
  ([[ $updaterepo = "true" ]] && echo "  --no-update-aptget=false") || echo "  --no-update-aptget=true"
  ([[ $install_rfrtools = "true" ]] && echo "  --bypass-rfrtools=false") || echo "  --bypass-rfrtools=true"
  ([[ $install_pkg_rfrtools = "true" ]] && echo "  --bypass-python-rfrtools=false") || echo "  --bypass-python-rfrtools=true"
  ([[ $install_rfrtools_gui = "true" ]] && echo "  --bypass-gui-installation=false") || echo "  --bypass-gui-installation=true"
  echo "  --user-local=$userlocal"
  echo "  --env-local=$envlocal"
  echo "  --system-wide=$systemwide"

  # create rest of list of arguments for rfrtools call
  rfrtools_options+=("$selectedbranch")
  [[ $usepython3exec = "true" ]] && rfrtools_options+=("--use-python3-exe-too")
  [[ $updaterepo = "true" ]] && rfrtools_options+=("--update-aptget")
  [[ $installdependencies = "true" ]] && rfrtools_options+=("--install-deb-deps")
  [[ $install_pkg_rfrtools = "true" ]] && rfrtools_options+=("--install-python-package")
  [[ $install_rfrtools_gui = "true" ]] && rfrtools_options+=("--install-gui")

  echo "Using \"$selectedbranch\" branch"
  echo "Options used for RFR_Tools script: \"${rfrtools_options[@]}\""
}

################################################
######## Cloning GrovePi & RFR_Tools  ##########
################################################

# called in <<install_rfrtools_repo>>
check_dependencies() {
  command -v git >/dev/null 2>&1 || { echo "This script requires \"git\" but it's not installed. Error occurred with RFR_Tools installation." >&2; exit 1; }
  command -v python >/dev/null 2>&1 || { echo "Executable \"python\" couldn't be found. Error occurred with RFR_Tools installation." >&2; exit 2; }
  command -v pip >/dev/null 2>&1 || { echo "Executable \"pip\" couldn't be found. Error occurred with RFR_Tools installation." >&2; exit 3; }
  if [[ $usepython3exec = "true" ]]; then
    command -v python3 >/dev/null 2>&1 || { echo "Executable \"python3\" couldn't be found. Error occurred with RFR_Tools installation." >&2; exit 4; }
    command -v pip3 >/dev/null 2>&1 || { echo "Executable \"pip3\" couldn't be found. Error occurred with RFR_Tools installation." >&2; exit 5; }
  fi

  if [[ ! -f $DEXTERSCRIPT/functions_library.sh ]]; then
    echo "script_tools didn\'t get installed. Enable the installation of dependencies with RFR_Tools.'"
    exit 8
  fi
}

# called way down below
install_rfrtools_repo() {

  # if rfrtools is not bypassed then install it
  if [[ $install_rfrtools = "true" ]]; then
    curl --silent -kL https://raw.githubusercontent.com/DexterInd/RFR_Tools/$selectedbranch/scripts/install_tools.sh > $PIHOME/.tmp_rfrtools.sh
    echo "Installing RFR_Tools. This might take a while.."
    bash $PIHOME/.tmp_rfrtools.sh ${rfrtools_options[@]} # > /dev/null
    ret_val=$?
    rm $PIHOME/.tmp_rfrtools.sh
    if [[ $ret_val -ne 0 ]]; then
      echo "RFR_Tools failed installing with exit code $ret_val. Exiting."
      exit 7
    fi
    echo "Done installing RFR_Tool"
  fi
  
  # check if all deb packages have been installed with RFR_Tools
  check_dependencies

  source $DEXTERSCRIPT/functions_library.sh
}

# called way down bellow
clone_grovepi() {
  # $DEXTER_PATH is still only available for the pi user
  # shortly after this, we'll make it work for any user
  sudo mkdir -p $DEXTER_PATH
  sudo chown pi:pi -R $DEXTER_PATH
  cd $DEXTER_PATH
  # it's simpler and more reliable (for now) to just delete the repo and clone a new one
  # otherwise, we'd have to deal with all the intricacies of git
  sudo rm -rf $GROVEPI_DIR
  git clone --quiet --depth=1 -b $selectedbranch https://github.com/DexterInd/GrovePi.git
  cd $GROVEPI_DIR
}

################################################
######## Install Python Packages & Deps ########
################################################

# called by <<install_python_pkgs_and_dependencies>>
install_python_packages() {
  [[ $systemwide = "true" ]] && sudo python setup.py install \
              && [[ $usepython3exec = "true" ]] && sudo python3 setup.py install
  [[ $userlocal = "true" ]] && python setup.py install --user \
              && [[ $usepython3exec = "true" ]] && python3 setup.py install --user
  [[ $envlocal = "true" ]] && python setup.py install \
              && [[ $usepython3exec = "true" ]] && python3 setup.py install
}

# called by <<install_python_pkgs_and_dependencies>>
remove_python_packages() {
  # the 1st and only argument
  # takes the name of the package that needs to removed
  rm -f $PIHOME/.pypaths

  # get absolute path to python package
  # saves output to file because we want to have the syntax highlight working
  # does this for both root and the current user because packages can be either system-wide or local
  # later on the strings used with the python command can be put in just one string that gets used repeatedly
  python -c "import pkgutil; import os; \
              eggs_loader = pkgutil.find_loader('$1'); found = eggs_loader is not None; \
              output = os.path.dirname(os.path.realpath(eggs_loader.get_filename('$1'))) if found else ''; print(output);" >> $PIHOME/.pypaths
  sudo python -c "import pkgutil; import os; \
              eggs_loader = pkgutil.find_loader('$1'); found = eggs_loader is not None; \
              output = os.path.dirname(os.path.realpath(eggs_loader.get_filename('$1'))) if found else ''; print(output);" >> $PIHOME/.pypaths
  if [[ $usepython3exec = "true" ]]; then
    python3 -c "import pkgutil; import os; \
                eggs_loader = pkgutil.find_loader('$1'); found = eggs_loader is not None; \
                output = os.path.dirname(os.path.realpath(eggs_loader.get_filename('$1'))) if found else ''; print(output);" >> $PIHOME/.pypaths
    sudo python3 -c "import pkgutil; import os; \
                eggs_loader = pkgutil.find_loader('$1'); found = eggs_loader is not None; \
                output = os.path.dirname(os.path.realpath(eggs_loader.get_filename('$1'))) if found else ''; print(output);" >> $PIHOME/.pypaths
  fi

  # removing eggs for $1 python package
  # ideally, easy-install.pth needs to be adjusted too
  # but pip seems to know how to handle missing packages, which is okay
  while read path;
  do
    if [ ! -z "${path}" -a "${path}" != " " ]; then
      echo "Removing ${path} egg"
      sudo rm -f "${path}"
    fi
  done < $PIHOME/.pypaths
}

# called by <<install_python_pkgs_and_dependencies>>
install_deb_dependencies() {
  feedback "Installing dependencies for the GrovePi"

  # in order for nodejs to be installed, the repo for it
  # needs to be in; this is all done in script_tools while doing an apt-get update
  sudo apt-get install --no-install-recommends -y nodejs\
    git libi2c-dev i2c-tools \
    python-setuptools python-pip python-smbus python-dev python-serial python-rpi.gpio python-numpy python-scipy \
    python3-setuptools python3-pip python3-smbus python3-dev python3-serial python3-rpi.gpio python3-numpy python3-scipy \
    libncurses5

  feedback "Dependencies for the GrovePi installed"
}

# called way down bellow
install_python_pkgs_and_dependencies() {
  # installing dependencies if required
  if [[ $installdependencies = "true" ]]; then
    feedback "Installing GrovePi dependencies. This might take a while.."
    install_deb_dependencies
    pushd $GROVEPI_DIR/Script > /dev/null
    sudo bash ./install.sh
    popd > /dev/null
  fi

  # feedback "Removing \"$REPO_PACKAGE\" and \"$DHT_PACKAGE\" to make space for new ones"
  feedback "Removing \"$REPO_PACKAGE\" to make space for the new one"
  remove_python_packages "$REPO_PACKAGE"
  # remove_python_packages "$DHT_PACKAGE"

  # installing the package itself
  pushd $GROVEPI_DIR/Software/Python > /dev/null
  install_python_packages
  popd > /dev/null
}

################################################
######## Aggregating all function calls ########
################################################

check_if_run_with_pi

parse_cmdline_arguments "$@"
install_rfrtools_repo

clone_grovepi
install_python_pkgs_and_dependencies

exit 0
