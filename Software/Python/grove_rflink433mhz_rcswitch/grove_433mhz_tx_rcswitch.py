import grovepi


class Grove433mhzTxRCSwitch:
    """ Sends command codes to radio remote controlled switches or devices.

    This library sends on / off commands to 4 different types of RC devices. Each of these types can be identified by
    the way the device address is configured:
    - Type A devices addresses are set by 5 DIP switches
    - Type B devices addresses are set by 2 rotary or sliding switches, each with 4 positions
    - Type C 'Intertechno' devices addresses are set with 3 elements: family (a to f), group (1 to 4) and device
      (1 to 4)
    - Type D 'REV' devices addresses are set with 2 elements: group (A to D) and device (1 to 3)

    This library makes use of the RCSwitch library: https://github.com/sui77/rc-switch/

    This method does not update existing subscriptions defined using grove_433mhz_rx_rcswitch

    """

    # Remote-controlled switch types
    TYPE_A = 0
    TYPE_B = 1
    TYPE_C = 2
    TYPE_D = 3

    # Remote-controlled switch state
    COMMAND_ON = 1
    COMMAND_OFF = 0

    def __init__(self, tx_pin):
        """Sets the Digital pin on which the TX component is wired.
        
        :param tx_pin: For D2, set to 2. Only pins D2 and D3 are compatible with this grove component.
        """
        self.tx_pin = tx_pin

    def send_type_a(self, command, group, device):
        """Sends an ON or OFF command to a type A device.
        
        Type A devices addresses are typically set by 5 DIP switches.
        
        :param command: set to COMMAND_ON or COMMAND_OFF.
        :param group: group DIP switch setting, as a string of five 0s/1s. Set to the '00101' string for a DIP switch
                      set to OFF OFF ON OFF ON.
        :param device: device DIP switch setting, as a string of five 0s/1s. Set to the '00101' string for a DIP switch
                      set to OFF OFF ON OFF ON.   
        """

        # Send command to the firmware, using the following scheme:
        # +-------------------------------------------------------------------------------+
        # | Type A switch                                                                 |
        # +---------+---------+-----------------------------------------------------------+
        # | Byte    | Bits    | Description                                               |
        # +---------+---------+-----------------------------------------------------------+
        # |      1  | 0 - 7   | Command byte: send command to RC switch.                  |
        # |         |         | Decimal value: 110                                        |
        # +---------+---------+-----------------------------------------------------------+
        # |      2  | 0       | Pin on which the 433 MHz transmitter module is connected. |
        # |         |         | 0 -> D2 / 1 -> D3                                         |
        # |         +---------+-----------------------------------------------------------+
        # |         | 1 - 4   | Unused                                                    |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 5       | Requested switch state.                                   |
        # |         |         | 0 = off / 1 = on                                          |
        # |         +---------+-----------------------------------------------------------+
        # |         | 6 - 7   | RC switch type.                                           |
        # |         |         | Type A: 00                                                |
        # +---------+---------+-----------------------------------------------------------+
        # |       3 | 0 - 4   | Group DIP switch.                                         |
        # |         |         | Ex: OFF-ON-ON-ON-OFF --> 01110                            |
        # |         +---------+-----------------------------------------------------------+
        # |         | 5 - 7   | Unused                                                    |
        # |         |         |                                                           |
        # +---------+---------+-----------------------------------------------------------+
        # |       4 | 0 - 4   | Device DIP switch.                                        |
        # |         |         | Ex: OFF-ON-ON-ON-OFF --> 01110                            |
        # |         +---------+-----------------------------------------------------------+
        # |         | 5 - 7   | Unused                                                    |
        # |         |         |                                                           |
        # +---------+---------+-----------------------------------------------------------+
        grovepi.write_i2c_block(grovepi.address,
                                grovepi.rcswitch_send_cmd +  # Byte 1
                                [self.TYPE_A * 64 + command * 32 + self.tx_pin - 2,  # Byte 2
                                int(group, 2),  # Byte 3
                                int(device, 2)])  # Byte 4

        
    def send_type_b(self, command, group, device):
        """Sends an ON or OFF command to a type B device.
        
        Type B devices addresses are typically set by two rotary or sliding switches, numbered from 1 to 4.
        
        :param command: set to COMMAND_ON or COMMAND_OFF.
        :param group: group switch setting (1 to 4).
        :param device: device switch setting (1 to 4). 
        """

        # Send command to the firmware, using the following scheme:
        # +-------------------------------------------------------------------------------+
        # | Type B switch                                                                 |
        # +---------+---------+-----------------------------------------------------------+
        # | Byte    | Bits    | Description                                               |
        # +---------+---------+-----------------------------------------------------------+
        # |      1  | 0 - 7   | Command byte: send command to RC switch.                  |
        # |         |         | Decimal value: 110                                        |
        # +---------+---------+-----------------------------------------------------------+
        # |      2  | 0       | Pin on which the 433 MHz transmitter module is connected. |
        # |         |         | 0 -> D2 / 1 -> D3                                         |
        # |         +---------+-----------------------------------------------------------+
        # |         | 1 - 4   | Unused                                                    |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 5       | Requested switch state.                                   |
        # |         |         | 0 = off / 1 = on                                          |
        # |         +---------+-----------------------------------------------------------+
        # |         | 6 - 7   | RC switch type.                                           |
        # |         |         | Type B: 01                                                |
        # +---------+---------+-----------------------------------------------------------+
        # |       3 | 0 - 7   | Group id (1 - 4).                                         |
        # |         |         | Ex: 3 --> 0000 0011                                       |
        # +---------+---------+-----------------------------------------------------------+
        # |       4 | 0 - 7   | Device id (1 - 4).                                        |
        # |         |         | Ex: 3 --> 0000 0011                                       |
        # +---------+---------+-----------------------------------------------------------+
        grovepi.write_i2c_block(grovepi.address,
                                grovepi.rcswitch_send_cmd +
                                [self.TYPE_B * 64 + command * 32 + self.tx_pin - 2,
                                group,
                                device])

    def send_type_c(self, command, family, group, device):
        """Sends an ON or OFF command to a type C (Intertechno) device.
                
        :param command: set to COMMAND_ON or COMMAND_OFF.
        :param family: device family setting ('a' to 'f')
        :param group: device group (1 to 4).
        :param device: device id (1 to 4). 
        """

        # +-------------------------------------------------------------------------------+
        # | Type C switch                                                                 |
        # +---------+---------+-----------------------------------------------------------+
        # | Byte    | Bits    | Description                                               |
        # +---------+---------+-----------------------------------------------------------+
        # |      1  | 0 - 7   | Command byte: send command to RC switch.                  |
        # |         |         | Decimal value: 110                                        |
        # +---------+---------+-----------------------------------------------------------+
        # |      2  | 0       | Pin on which the 433 MHz transmitter module is connected. |
        # |         |         | 0 -> D2 / 1 -> D3                                         |
        # |         +---------+-----------------------------------------------------------+
        # |         | 1 - 4   | Unused                                                    |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 5       | Requested switch state.                                   |
        # |         |         | 0 = off / 1 = on                                          |
        # |         +---------+-----------------------------------------------------------+
        # |         | 6 - 7   | RC switch type.                                           |
        # |         |         | Type C: 10                                                |
        # +---------+---------+-----------------------------------------------------------+
        # |       3 | 0 - 7   | Device family ('a' - 'f'), as the ASCII code of the       |
        # |         |         | desired letter.                                           |
        # |         |         | Ex: 'b' --> 0110 0001                                     |
        # +---------+---------+-----------------------------------------------------------+
        # |       4 | 0 - 1   | Device id (1 - 4), minus 1.                               |
        # |         |         | Ex: device #3 --> 10                                      |
        # |         +---------+-----------------------------------------------------------+
        # |         | 2 - 3   | Device group (1 - 4), minus 1.                            |
        # |         |         | Ex: group #1 --> 00                                       |
        # +         +---------+-----------------------------------------------------------+
        # |         | 4 - 7   | Unused                                                    |
        # |         |         |                                                           |
        # +---------+---------+-----------------------------------------------------------+
        grovepi.write_i2c_block(grovepi.address,
                                grovepi.rcswitch_send_cmd +
                                [self.TYPE_C * 64 + command * 32 + self.tx_pin - 2,
                                ord(family),
                                (group - 1) * 4 + (device - 1)])

    def send_type_d(self, command, family, device):
        """Sends an ON or OFF command to a type D device.
                
        :param command: set to COMMAND_ON or COMMAND_OFF.
        :param family: device family setting ('A' to 'D')
        :param device: device id (1 to 4). 
        """

        # +-------------------------------------------------------------------------------+
        # | Type D switch                                                                 |
        # +---------+---------+-----------------------------------------------------------+
        # | Byte    | Bits    | Description                                               |
        # +---------+---------+-----------------------------------------------------------+
        # |      1  | 0 - 7   | Command byte: send command to RC switch.                  |
        # |         |         | Decimal value: 110                                        |
        # +---------+---------+-----------------------------------------------------------+
        # |      2  | 0       | Pin on which the 433 MHz transmitter module is connected. |
        # |         |         | 0 -> D2 / 1 -> D3                                         |
        # |         +---------+-----------------------------------------------------------+
        # |         | 1 - 4   | Unused                                                    |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 5       | Requested switch state.                                   |
        # |         |         | 0 = off / 1 = on                                          |
        # |         +---------+-----------------------------------------------------------+
        # |         | 6 - 7   | RC switch type.                                           |
        # |         |         | Type D: 11                                                |
        # +---------+---------+-----------------------------------------------------------+
        # |       3 | 0 - 7   | Device family ('A' - 'D'), as the ASCII code of the       |
        # |         |         | desired letter.                                           |
        # |         |         | Ex: 'C' --> 0100 0011                                     |
        # +---------+---------+-----------------------------------------------------------+
        # |       4 | 0 - 7   | Device id (1 - 3).                                        |
        # |         |         | Ex: 3 --> 0000 0011                                       |
        # +---------+---------+-----------------------------------------------------------+
        grovepi.write_i2c_block(grovepi.address,
                                grovepi.rcswitch_send_cmd +
                                [self.TYPE_D * 64 + command * 32 + self.tx_pin - 2,
                                ord(family),
                                device])
