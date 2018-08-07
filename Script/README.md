## Installing

You need internet access for the following step(s).

The quickest way for installing the GrovePi is to enter the following command:
```
curl -kL dexterindustries.com/update_grovepi | bash
```

By default, the GrovePi package is installed system-wide, [script_tools](https://github.com/DexterInd/script_tools) and [RFR_Tools](https://github.com/DexterInd/RFR_Tools) are updated each time the script is ran.

An example using options appended to the command can be:
```
curl -kL dexterindustries.com/update_grovepi | bash -s -- --user-local --no-update-aptget --no-dependencies
```

## Command Options

The options that can be appended to this command are:

* `--no-dependencies` - skip installing any dependencies for the GrovePi. It's supposed to be used on each consecutive update after the initial install has gone through.
* `--no-update-aptget` - to skip using `sudo apt-get update` before installing dependencies. For this to be useful, `--no-dependencies` has to be not used.
* `--no-grovepi-deb-packages` - skip installing debian packages with apt-get, but this doesn't mean it also skips installing whatever it's necessary to operate the GrovePi (avrdude, enabling I2C, etc). Lighter version of `--no-dependencies`.
* `--bypass-rfrtools` - skips installing RFR_Tools completely.
* `--bypass-python-rfrtools` - skips installing/updating the python package for  [RFR_Tools](https://github.com/DexterInd/RFR_Tools).
* `--bypass-gui-installation` - skips installing the GUI packages/dependencies from [RFR_Tools](https://github.com/DexterInd/RFR_Tools).
* `--user-local` - install the python package for the GrovePi in the home directory of the user. This doesn't require any special read/write permissions: the actual command used is (`python setup.py install --force --user`).
* `--env-local` - install the python package for the GrovePi within the given environment without elevated privileges: the actual command used is (`python setup.py install --force`).
* `--system-wide` - install the python package for the GrovePi within the sytem-wide environment with `sudo`: the actual command used is (`sudo python setup.py install --force`).

Important to remember is that `--user-local`, `--env-local` and `--system-wide` options are all mutually-exclusive - they cannot be used together.
As a last thing, different versions of it can be pulled by appending a corresponding branch name or tag.

## Minimal Installation

Now, if you only want the absolute minimum in order to get going with the GrovePi, you can run this commands in this order:
```bash
sudo apt-get update
```
```bash
sudo apt-get install git libi2c-dev i2c-tools minicom \
    python-setuptools python-pip python-smbus python-dev python-serial python-rpi.gpio python-numpy \
    python3-setuptools python3-pip python3-smbus python3-dev python3-serial python3-rpi.gpio python3-numpy
    --no-install-recommends -y
```
```bash
curl -kL dexterindustries.com/update_grovepi | sh -s -- --no-update-aptget --bypass-rfrtools
```

This will only get you installed the GrovePi dependencies and nothing else. You still can use options such as `--user-local` or `--env-local` if you are working with a different kind of environment. Keep in mind that `--system-wide` is selected by default.
