## Java Library
### This repository contains the Java library for the GrovePi
#### Installation ####
Before to proceed you should install the Pi4J libraries. The easiest way to install it is using the following command:

```curl -s get.pi4j.com | sudo bash```

If you need more details you can visit the official website: http://pi4j.com/install.html

#### Compile and Execute the test program ####
Once your installation is complete and your local repository is ready then you can compile the GrovePi libraries and run the test program.
First, enter the Java directory:

```$ cd ./Java/```

The folder structure will be:

```$ config  doc  scripts  src  test```

* **bin** - it's the destination folder for the compiler and it will be created automatically, if not present, by the Bash script.
* **config** - contains the default configuration.
* **doc** - contains the GrovePi library documentation.
* **scripts** - contains some Bash scripts to compile the library and execute the basic test program.
* **src** - contains the sources of the GrovePi library.
* **test** - contains some example code/programs.

To compile the library and run the test program you can use the following command:

```$ ./scripts/compile.sh && ./scripts/Test.sh```

By default you will find some logs inside the /var/log/GrovePi folder.

In case of any trouble or if you need further information don't hesitate to leave a comment on the official forum: http://forum.dexterindustries.com/c/grovepi

## License
GrovePi for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.