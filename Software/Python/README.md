## Installing the GrovePi for Python

This is how the GrovePi python library has to be installed:
```bash
curl -kL dexterindustries.com/update_grovepi | bash
```

You can also install it by running the `setup.py` installer, but beware of the other requirements for it too: specifically about the `di_i2c` module from https://github.com/DexterInd/RFR_Tools that has to be installed and the enabling of the I2C in `raspi-config` menu. 
```
pip install -r requirements.txt
```
```
python3 setup.py install
```

You can also run `python setup.py test` to test import the modules of the GrovePi package that are listed in the [package_modules.txt](package_modules.txt) file. The `python setup.py test` commands should be run after pip installing the dependencies.

## Library Breakdown

There are 2 kind of example scripts:

1. Example programs that only require the `grovepi` module - these example scripts are found in this directory (or root directory of the Python package).

1. Example programs that are based on other sublibraries other than the `grovepi` module - these example scripts are found in the subdirectories of this directory.

The libraries installed with the GrovePi package are listed in [here](package_modules.txt).

## Python Consideration

Even though you can install the GrovePi package for both versions of it (2.x and 3.x), some libraries other than the main one (`grovepi.py`) can only be used with Python3. Therefore, it's just better to use Python 3 by-default, instead of relying on an older version of Python which will anyway get retired in the very near future.
