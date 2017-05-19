import grovepi


TYPE_A = 0
TYPE_B = 1
TYPE_C = 2
TYPE_D = 3

COMMAND_ON = 1
COMMAND_OFF = 0
tx_pin = 5
rx_pin = 6

# Allumage lampe
grovepi.write_i2c_block(grovepi.address, 110 + [TYPE_B * 64 + COMMAND_ON * 32 + tx_pin, 2, 1])

