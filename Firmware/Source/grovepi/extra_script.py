from os.path import join
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

env.Replace(
    # MYUPLOADERFLAGS=[
    #     "-v",
    #     "-p", "$BOARD_MCU",
    #     "-C", "/etc/avrdude.conf"
    #     # "-c", "$UPLOAD_PROTOCOL",
    #     "-c", "gpio",
    #     "-b", "$UPLOAD_SPEED",
    #     "-U", "lfuse:w:0xFF:m",
    #     "-U", "hfuse:w:0xDA:m",
    #     "-U", "efuse:w:0x05:m"
    #  ],
    # UPLOADHEXCMD='"$UPLOADER" $MYUPLOADERFLAGS -U flash:w:$SOURCES:i'
    UPLOADHEXCMD='avrdude -C /etc/avrdude.conf -c gpio -p m328p -U lfuse:w:0xFF:m -U hfuse:w:0xDA:m -U efuse:w:0x05:m flash:w:$SOURCES:i'
)
