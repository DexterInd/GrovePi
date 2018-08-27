## Installing the GrovePi for Python

Run the following 2 commands in the following order to get the GrovePi installed:
```
pip install -r requirements.txt
```
```
python setup.py install
```

You can also run `python setup.py test` to test import the modules of the GrovePi package that reside in [src](src/). The `python setup.py test` commands should be run after pip installing the dependencies.

## Library Breakdown

There are 2 directories in this directory that contain example scripts:

1. [connectables_examples](connectables_examples/) - containing example programs that rely on other libraries other than the `grovepi.py` module.

1. [grovepi_examples](grovepi_examples/) - containing example programs that only need the main module of the GrovePi, `grovepi.py`.
