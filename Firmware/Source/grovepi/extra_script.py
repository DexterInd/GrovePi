# Import('env')
#
# env.Replace(FUSESCMD="avrdude -c usbtiny -p m328p -U lfuse:w:0xFF:m -U hfuse:w:0xDA:m -U efuse:w:0xfd:m -B 3")

from os.path import join
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

env.Replace(
    MYUPLOADERFLAGS=[
        "-v",
        "-p", "$BOARD_MCU",
        "-c", "$UPLOAD_PROTOCOL",
        "-b", "115200",
        "-U", "lfuse:w:0xFF:m",
        "-U", "hfuse:w:0xDA:m",
        "-U", "efuse:w:0xFD:m"
     ],
    UPLOADHEXCMD='"$UPLOADER" $MYUPLOADERFLAGS -U flash:w:$SOURCES:i'
)
