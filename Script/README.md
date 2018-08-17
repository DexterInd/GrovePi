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

* `--no-update-aptget` - to skip using `sudo apt-get update` before installing dependencies. For this to be useful, `--no-dependencies` has to be not used. Applies to RFR_Tools and the GrovePi.
* `--bypass-rfrtools` - skips installing RFR_Tools completely.
    * `--bypass-python-rfrtools` - skips installing/updating the python package for  [RFR_Tools](https://github.com/DexterInd/RFR_Tools).
    * `--bypass-gui-installation` - skips installing the GUI packages/dependencies from [RFR_Tools](https://github.com/DexterInd/RFR_Tools).
* `--no-dependencies` - skip installing any dependencies for the GrovePi. It's supposed to be used on each consecutive update after the initial install has gone through.
* `--user-local` - install the python package for the GrovePi in the home directory of the user. This doesn't require any special read/write permissions: the actual command used is (`python setup.py install --force --user`).
* `--env-local` - install the python package for the GrovePi within the given environment without elevated privileges: the actual command used is (`python setup.py install --force`).
* `--system-wide` - install the python package for the GrovePi within the sytem-wide environment with `sudo`: the actual command used is (`sudo python setup.py install --force`).

Important to remember is that `--user-local`, `--env-local` and `--system-wide` options are all mutually-exclusive - they cannot be used together.
As a last thing, different versions of it can be pulled by appending a corresponding branch name or tag.

## Minimal Installation

Now, if you only want the absolute minimum in order to get going with the GrovePi, you can run this command:
```bash
curl -kL dexterindustries.com/update_grovepi | bash -s -- --bypass-gui-installation
```

This will only get you installed the GrovePi dependencies and nothing else. You still can use options such as `--user-local` or `--env-local` if you are working with a different kind of environment. Keep in mind that `--system-wide` is selected by default.

## Subsequent Updates

If the GrovePi has been installed either by using the full command or the one for the minimal installation, this means you have all the packages installed already and all dependencies put in. Therefore, on subsequent installation, you can skip installing any dependency and instead just reinstall the python package of the GrovePi. To do this, you can run this command:
```bash
curl -kL dexterindustries.com/update_grovepi | bash -s -- --bypass-rfrtools --no-dependencies
```

Or if this is too complex, you can always stick to the command meant for the full installation or the minimal one.
