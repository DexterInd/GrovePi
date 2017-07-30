import serial
import binascii
import struct

# Library written for Python 3!

class RFLinker:

    # port = '/dev/ttyS0' - it's the default and only UART port on the Raspberry
    #
    # chunk_size = 32 represents the number of data bytes a transmission can have at most
    # if the number of bytes exceed this threshold, then the data that's needed to be sent
    # is fragmented
    #
    # max_bad_readings = 32 represents how many times we wait for a valid byte data before giving up
    #
    # retries = 20 number of times it starts the process of reading a message before giving up
    def __init__(self, port = '/dev/ttyS0', chunk_size = 32, max_bad_readings = 32, retries = 20):
        self.serial = serial.Serial(port, baudrate = 1200)
        self.chunk_size = chunk_size
        self.max_bad_readings = max_bad_readings
        self.retries = retries
        self.display_verbose = False # whether we want or not feedback on the screen

        self.delimiter = chr(2) # new transmission delimiter -> the 1st thing we search when reading
        self.start_condition = chr(1) + chr(27) # new transmission start condition
        self.crc_offset = 256 # how much we offset crc32's bytes by adding this value so that we can send data over the air

        self.end_condition = '\r\n' # CR + LF for ending a transmssion

    # private function for displaying information
    def __print(self, *strings):
        if not self.display_verbose:
            return

        message_string = ""
        for string in strings:
            message_string += "[" + str(string) + "]"

        print(message_string)

    # private function for determining how many transmissions we need for a writeMessage call
    def __getListOfLengths(self, message):
        length_list = []
        chunks = int(len(message) / self.chunk_size)
        last_chunk = int(len(message) % self.chunk_size)

        length_list = chunks * [self.chunk_size] + [last_chunk]
        length_list = [size for size in length_list if size != 0]
        return length_list

    # private function for sending a fragment of the whole data we need to send
    def __writeFragment(self, message, count, no_transmissions):

        self.__print("message to packetize", message)

        outgoing_message = self.delimiter
        outgoing_message += self.start_condition
        outgoing_message += count
        outgoing_message += no_transmissions
        outgoing_message += chr(len(message)) # this is the length of the fragment message

        outgoing_message += message # we add the actual message

        # compute the CRC32
        crc32_checker = binascii.crc32(outgoing_message.encode('utf-8'))
        crc32_checker &= 0xffffffff
        crc_to_bytes = struct.pack('!I', crc32_checker)
        crc_to_str = ""
        for each_byte in crc_to_bytes:
            crc_to_str += chr(each_byte + self.crc_offset)

        # and add the UTF-8-converted CRC32 to the message
        outgoing_message += crc_to_str
        # and finalize by adding CR + LF
        outgoing_message += self.end_condition

        # encode it
        outgoing_message = outgoing_message.encode('utf-8')

        self.__print('final message', outgoing_message)
        # and broadcast it
        self.serial.write(outgoing_message)

    # function for enabling / disabling feedback
    def setDisplayVerbose(self, choice = True):
        self.display_verbose = choice

    # function for setting the chunk_size
    def setChunkSize(self, chunk_size):
        if chunk_size > 0:
            self.chunk_size = chunk_size

    # function for setting retries variable
    # it specifies how many times it tries to
    # start a transmission before giving up
    def setMaxRetries(self, max_retries):
        if max_retries > 0:
            self.retries = max_retries

    def setMaxBadReadings(self, max_bad_readings):
        if max_bad_readings > 0:
            self.max_bad_readings = max_bad_readings

    # function we call from the user-program to send messages
    def writeMessage(self, message):
        # determine how many fragments/transmssions are needed
        chunked_message_lengths = self.__getListOfLengths(message)

        # if it's only one transmission then it's simple
        if len(chunked_message_lengths) == 1:
            count = 1
            self.__writeFragment(message, chr(count), chr(count))

        elif len(chunked_message_lengths) > 0:
            no_transmissions = len(chunked_message_lengths)
            count = no_transmissions

            # otherwise send the data repeatedly
            # until everything is sent
            while len(chunked_message_lengths) > 0:
                self.__writeFragment(message[0:chunked_message_lengths[0]], chr(count), chr(no_transmissions))
                message = message[chunked_message_lengths.pop(0):]
                count -= 1

    # private function for reading data
    # it's a recursive function and works in tandem with readMessage function
    def __readFraments(self, first_time, met_first_trans, last_counter = 1):
        current_bad_readings = 0
        # read until threshold of bad read characters is reached
        # don't consider UnicodeDecodeError exceptions
        while current_bad_readings < self.max_bad_readings:
            try:
                if self.serial.read().decode('utf-8') == self.delimiter:
                    break
                current_bad_readings += 1

            except UnicodeDecodeError:
                continue

        # if threshold is reached raise exception and let readMessage deal with it
        if current_bad_readings == self.max_bad_readings:
            raise serial.SerialTimeoutException("[rflink : too much time]")

        # read the start_condition which is made out of 2 bytes
        start_condition = self.serial.read(2).decode('utf-8')
        if start_condition != self.start_condition:
            raise IOError('[transmission error - bad start condition]')

        # read the next portions of the header
        current_count = self.serial.read(1).decode('utf-8')
        no_transmissions = self.serial.read(1).decode('utf-8')
        message_length = self.serial.read(1).decode('utf-8')

        # read the actual message
        message = self.serial.read(ord(message_length)).decode('utf-8')
        incoming_message = self.delimiter + self.start_condition + current_count + no_transmissions + message_length + message
        # next, read the CRC32
        crc32 = self.serial.read(8).decode('utf-8')

        # compute the CRC32
        crc_to_bytes = []
        for each_char in crc32:
            crc_to_bytes.append(ord(each_char) - self.crc_offset)
        try:
            unpacked_crc = struct.unpack('!I', bytes(crc_to_bytes))[0]
        except ValueError:
            raise IOError('[transmission error - cannot unpack CRC32]')

        # and compare it with what we got
        if unpacked_crc != binascii.crc32(incoming_message.encode('utf-8')):
            raise IOError('[transmission error - CRC32 does not match]')

        current_count = ord(current_count)
        no_transmissions = ord(no_transmissions)
        #print(message, first_time, current_count, no_transmissions, unpacked_crc, binascii.crc32(incoming_message.encode('utf-8')))

        # the next following lines check whether the data fragments are out of order
        # and whether we still need to read fragments. If that's the case, then we append the
        # so far read string and re-call this function to read the remaining text
        if first_time:
            if current_count == no_transmissions:
                met_first_trans = True
                if current_count == 1:
                    return message
                else:
                    return message + self.__readFraments(False, met_first_trans, current_count)
            else:
                raise IOError('[chunks out of order - abording reading operation]')
        else:
            if current_count + 1 == last_counter:
                if current_count == 1:
                    return message
                else:
                    return message + self.__readFraments(False, met_first_trans, current_count)

            else:
                raise IOError('[chunks out of order - abording reading operation]')

    # function for reading incoming messages
    def readMessage(self):
        current_count = 0
        message = ""
        # we need to flush the input
        # There's so much pollution around us
        # that the program would get busy analysing the whole
        # input buffer, and that'd be crazy - we'd wait lots of time
        # before we get something the transmitter sent
        self.serial.flushInput()

        # do some unicorn magic here
        while True:
            try:
                message = self.__readFraments(True, True)
                return message
            except serial.SerialTimeoutException:
                return message
            except IOError:
                if current_count == self.retries:
                    return message
            except UnicodeDecodeError:
                continue
            finally:
                current_count += 1

        return message
