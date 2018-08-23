Link to the Grove 433Mhz Simple RF Link Kit product  : https://www.seeedstudio.com/Grove-433MHz-Simple-RF-link-kit-p-1062.html
Link to the Grove 433Mhz Simple RF Link Kit datasheet :
* http://wiki.seeedstudio.com/images/9/95/ADI%3BACTR433A.pdf
* http://wiki.seeedstudio.com/images/1/1a/1110010P1.pdf

Library written for **Python 3**!

---

You'll need 2 Raspberry's in order to test the given example programs.
When using it with the GrovePi board, please pay attention that the transmitter must pe connected with jumpers to the RPi board, because TX / RX pins were switched (a design flaw).
On the other hand, the receiver's pins are aligned corectly.

---

Available functions for the Grove 433Mhz Simple RF Link Kit (`RFLinker` class):
* `RFLinker(port = '/dev/ttyS0', chunk_size = 32, max_bad_readings = 32, retries = 20)` : class constructor
    * *port* is the UART port to which the RF module is connected
    * *chunk_size* specifies the maximum length of a message. If the length is > *chunk_size*, then the message is fragmented in multiple transmissions - **If you lower *chunk_size*, then be sure to increase *retries* variable when reading**
    * *max_bad_readings* specifies the maximum number of bad bytes read from the RF receiver before the operation is aborded
* `writeMessage(message)` : member function for sending messages
    * you can send up to 256 bytes per transmission
* `readMessage(message)` : member function reading messages
    * returns a string with the received message : if it fails, it returns an empty string
* `setDisplayVerbose(choice = True)` : enable/disable feedback printing - by default it's deactivated
* `setChunkSize(chunk_size)` : set the chunk size in bytes
* `setMaxRetries(retries)` : set the number of times it starts reading a transmission before giving up - higher level stuff
* `setMaxBadReadings(max_bad_readings)` : set the number of times it's allowed to read a bad byte from the stream before quitting - lower level stuff

Attention:
* `chunk_size` is closely related to `retries`. The bigger the `chunk_size` the lower `retries` it has to be in order to detect a transmission. It's also a valid statement vice-versa.
