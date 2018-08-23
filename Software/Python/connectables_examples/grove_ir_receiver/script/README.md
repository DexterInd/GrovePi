##IR remote control

### This folder contains the files to setup and use the Keyes IR remote with the GrovePi

**_Files:_**
- **ir_recv_example.py** : Used to test button press on the IR remote
- **/script/ir_install.sh** : Installation file for IR remote control
- **/script/setup_older_version.sh** : Installation file for older IR receiver

**Connection:_**
Connect the IR receiver to the RPi serial port on the GrovePi. This will act as a pass through to the IR signals to the Serial pins. 
IR receiver Hardware v1.0 and back have the IR receiver connected to white wire and v1.1 and v1.2 have it connected to the Yellow wire, so the GPIO changes

**Installation:_**
- Make the ir_install.sh executable: sudo chmod +x ir_install.sh
- Run the install script: sudo ./ir_install.sh
- If you have an IR receiver which is v1.0 or back, then run the setup_older_version script too: sudo chmod +x ir_install.sh and sudo ./ir_install.sh
**Usage:_**
Run the **ir_recv_example.py** to check if the remote is working properly