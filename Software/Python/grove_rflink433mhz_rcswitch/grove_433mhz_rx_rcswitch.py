import grovepi


class Grove433mhzRxRCSwitch:
    """ Receives command codes from remotes sold with radio controlled switches or devices.

    This library receives on / off commands sent from the radio remotes of 4 different types of RC devices. 
    Each of these types can be identified by the way the device address is configured:
    - Type A devices addresses are set by 5 DIP switches
    - Type B devices addresses are set by 2 rotary or sliding switches, each with 4 positions
    - Type C 'Intertechno' devices addresses are set with 3 elements: family (a to f), group (1 to 4) and device
      (1 to 4)
    - Type D 'REV' devices addresses are set with 2 elements: group (A to D) and device (1 to 3)

    Using this library requires 2 steps:
    1. Subscribe to the on/off commands normally sent to a device. The GrovePi will from that point listen 
    to these commands, and store the last one.
    
    2. Periodically read the last received command, and act accordingly.

    This library makes use of the RCSwitch library: https://github.com/sui77/rc-switch/
    Please have a look at it for more details on the supported devices.

    """

    # Remote-controlled switch types
    TYPE_A = 0
    TYPE_B = 1
    TYPE_C = 2
    TYPE_D = 3

    # Last received command
    STATE_ON = 1
    STATE_OFF = 0
    STATE_UNKNOWN = 255

    def __init__(self, rx_pin):
        """Sets the Digital pin on which the RX component is wired.
        
        :param rx_pin: For D2, set to 2. Only pins D2 and D3 are compatible with this grove component.
        """
        self.rx_pin = rx_pin

    def subscribe_type_a(self, subscription_number, group, device, initial_state):
        """Subscribe to commands normally sent to a type A device.
        
        Type A devices addresses are typically set by 5 DIP switches.
        
        :param subscription_number: subscription slot to use. Can be any value from 0 to 7.
        
        :param group: group DIP switch setting, as a string of five 0s/1s. Set to the '00101' string for a DIP switch
                      set to OFF OFF ON OFF ON.
        :param device: device DIP switch setting, as a string of five 0s/1s. Set to the '00101' string for a DIP switch
                      set to OFF OFF ON OFF ON.   
        
        :param initial_state: set the value to be returned by the first call to read_subscription. Can be STATE_ON or 
        STATE_OFF.
        """

        # +-------------------------------------------------------------------------------+
        # | Type A switch                                                                 |
        # +---------+---------+-----------------------------------------------------------+
        # | Byte    | Bits    | Description                                               |
        # +---------+---------+-----------------------------------------------------------+
        # |      1  | 0 - 7   | Command byte: subscribe to RC switch commands.            |
        # |         |         | Decimal value: 111                                        |
        # +---------+---------+-----------------------------------------------------------+
        # |      2  | 0       | Pin on which the 433 MHz receiver module is connected.    |
        # |         |         | 0 -> D2 / 1 -> D3                                         |
        # |         +---------+-----------------------------------------------------------+
        # |         | 1 - 3   | Subscription number                                       |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 4       | Unused                                                    |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 5       | Initial state.                                            |
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
                                grovepi.rcswitch_sub_cmd +
                                [self.TYPE_A * 64 + initial_state * 32 + subscription_number * 2 + self.rx_pin - 2,
                                 int(group, 2),
                                 int(device, 2)])

    def subscribe_type_b(self, subscription_number, group, device, initial_state):
        """Subscribe to commands normally sent to a type B device.
        
        Type B devices addresses are typically set by two rotary or sliding switches, numbered from 1 to 4.
        
        :param subscription_number: subscription slot to use. Can be any value from 0 to 7.
        
        :param group: group switch setting (1 to 4).
        
        :param device: device switch setting (1 to 4). 
        
        :param initial_state: set the value to be returned by the first call to read_subscription. Can be STATE_ON or 
        STATE_OFF.
        """

        # Send command to the firmware, using the following scheme:
        #
        # +-------------------------------------------------------------------------------+
        # | Type B switch                                                                 |
        # +---------+---------+-----------------------------------------------------------+
        # | Byte    | Bits    | Description                                               |
        # +---------+---------+-----------------------------------------------------------+
        # |      1  | 0 - 7   | Command byte: subscribe to RC switch commands.            |
        # |         |         | Decimal value: 111                                        |
        # +---------+---------+-----------------------------------------------------------+
        # |      2  | 0       | Pin on which the 433 MHz receiver module is connected.    |
        # |         |         | 0 -> D2 / 1 -> D3                                         |
        # |         +---------+-----------------------------------------------------------+
        # |         | 1 - 3   | Subscription number                                       |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 4       | Unused                                                    |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 5       | Initial state.                                            |
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
                                grovepi.rcswitch_sub_cmd +
                                [self.TYPE_B * 64 + initial_state * 32 + subscription_number * 2 + self.rx_pin - 2,
                                 group,
                                 device])

    def subscribe_type_c(self, subscription_number, family, group, device, initial_state):
        """Subscribe to commands normally sent to a type C device.
        
        :param subscription_number: subscription slot to use. Can be any value from 0 to 7.
        
        :param family: device family setting ('a' to 'f')
        
        :param group: device group (1 to 4).
        
        :param device: device id (1 to 4). 
        
        :param initial_state: set the value to be returned by the first call to read_subscription. Can be STATE_ON or 
        STATE_OFF.
        """
        
        # Send command to the firmware, using the following scheme:
        #
        # +-------------------------------------------------------------------------------+
        # | Type C switch                                                                 |
        # +---------+---------+-----------------------------------------------------------+
        # | Byte    | Bits    | Description                                               |
        # +---------+---------+-----------------------------------------------------------+
        # |      1  | 0 - 7   | Command byte: subscribe to RC switch commands.            |
        # |         |         | Decimal value: 111                                        |
        # +---------+---------+-----------------------------------------------------------+
        # |      2  | 0       | Pin on which the 433 MHz receiver module is connected.    |
        # |         |         | 0 -> D2 / 1 -> D3                                         |
        # |         +---------+-----------------------------------------------------------+
        # |         | 1 - 3   | Subscription number                                       |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 4       | Unused                                                    |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 5       | Initial state.                                            |
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
        # |         +---------+-----------------------------------------------------------+
        # |         | 4 - 7   | Unused                                                    |
        # |         |         |                                                           |
        # +---------+---------+-----------------------------------------------------------+
        
        grovepi.write_i2c_block(grovepi.address,
                                grovepi.rcswitch_sub_cmd +
                                [self.TYPE_C * 64 + initial_state * 32 + subscription_number * 2 + self.rx_pin - 2,
                                 ord(family),
                                 (group - 1) * 4 + (device - 1)])

    def subscribe_type_d(self, subscription_number, group, device, initial_state):
        """Subscribe to commands normally sent to a type D device.
                
        :param subscription_number: subscription slot to use. Can be any value from 0 to 7.
        
        :param family: device family setting ('A' to 'D')
        
        :param device: device id (1 to 4). 
        
        :param initial_state: set the value to be returned by the first call to read_subscription. Can be STATE_ON or 
        STATE_OFF.
        """

        # Send command to the firmware, using the following scheme:
        #
        # +-------------------------------------------------------------------------------+
        # | Type D switch                                                                 |
        # +---------+---------+-----------------------------------------------------------+
        # | Byte    | Bits    | Description                                               |
        # +---------+---------+-----------------------------------------------------------+
        # |      1  | 0 - 7   | Command byte: subscribe to RC switch commands.            |
        # |         |         | Decimal value: 111                                        |
        # +---------+---------+-----------------------------------------------------------+
        # |      2  | 0       | Pin on which the 433 MHz receiver module is connected.    |
        # |         |         | 0 -> D2 / 1 -> D3                                         |
        # |         +---------+-----------------------------------------------------------+
        # |         | 1 - 3   | Subscription number                                       |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 4       | Unused                                                    |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 5       | Initial state.                                            |
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
                                grovepi.rcswitch_sub_cmd +
                                [self.TYPE_D * 64 + initial_state * 32 + subscription_number * 2 + self.rx_pin - 2,
                                 ord(group),
                                 device])

    def read_subscription(self, subscription_number):
        """Read last command received for a given subscription number
        
        :param subscription_number: 
        :return: STATE_ON, STATE_OFF or STATE_UNKNOWN
        """

        # +---------+---------+-----------------------------------------------------------+
        # | Byte    | Bits    | Description                                               |
        # +---------+---------+-----------------------------------------------------------+
        # |      1  | 0 - 7   | Command byte: subscribe to RC switch commands.            |
        # |         |         | Decimal value: 112                                        |
        # +---------+---------+-----------------------------------------------------------+
        # |      2  | 0       | Unused                                                    |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 1 - 3   | Subscription number                                       |
        # |         |         |                                                           |
        # |         +---------+-----------------------------------------------------------+
        # |         | 4 - 7   | Unused                                                    |
        # |         |         |                                                           |
        # +---------+---------+-----------------------------------------------------------+
        # |       3 | 0 - 7   | Unused                                                    |
        # |         |         |                                                           |
        # +---------+---------+-----------------------------------------------------------+
        # |       4 | 0 - 7   | Unused                                                    |
        # |         |         |                                                           |
        # +---------+---------+-----------------------------------------------------------+
        grovepi.write_i2c_block(grovepi.address,
                                grovepi.rcswitch_read_cmd +  # Byte 1
                                [subscription_number * 2,  # Byte 2
                                 0,  # Byte 3
                                 0])  # Byte 4

        return grovepi.read_i2c_byte(grovepi.address)