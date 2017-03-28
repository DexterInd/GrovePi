#! /bin/bash
REPO_PATH=$(readlink -f $(dirname $0) | grep -E -o "^(.*?\\GrovePi)")
echo ""
echo Checking for firmware version
echo =============================
sudo python $REPO_PATH/Software/Python/grove_firmware_version_check.py
