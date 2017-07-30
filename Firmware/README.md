GrovePi
=======

GrovePi is an open source platform for connecting Grove Sensors to the Raspberry Pi.  [See more about the GrovePi here.](http://www.dexterindustries.com/grovepi)

## Compiling
The best way to compile the firmware on the GrovePi is to use Ino.  You can see more about [ino](http://inotool.org).
Make a new file directory, preferably on the Desktop or in the ~ directory. 
Change directory into the new directory.
run **ino init -t grovepi**

Move the source code, including dependencies, into the /src directory that was automatically created.

The hex files are located in the **.build/uno directory**.  Specifically it should generate a file called firmware.hex

## Uploading

You can upload the firmware you've compiled using the following command:
**avrdude -c gpio -p m328p -U flash:w:.build/uno/firmware.hex**

## Updating the firmware on your GrovePi
If you don;t want to compile and upload, you can also run the firmware update script to update the firmware on your GrovePi to the latest version.

First make the firmware update script executable:

**sudo chmod +x firmware_update.sh**

then run it:

**sudo ./firmware_update.sh**

## Learn More

See more at the [GrovePi Site](http://www.GrovePi.com/)
[Dexter Industries](http://www.dexterindustries.com)


## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
