import serial
import binascii
import struct

class RFLinker:

    def __init__(self, port = '/dev/ttyS0', chunk_size = 32, max_bad_readings = 30, read_timeout = 3.0):
        self.serial = serial.Serial(port, baudrate = 1200)
        self.max_bad_readings = max_bad_readings
        self.display_verbose = False

        self.delimiter = chr(2)
        self.start_condition = chr(1) + chr(27)
        self.set_as_onefragment = chr(50)
        self.chunk_size = chunk_size
        self.crc_offset = 256

        self.end_condition = '\r\n'

    def __print(self, *strings):
        if not self.display_verbose:
            return

        message_string = ""
        for string in strings:
            message_string += "[" + str(string) + "]"

        print(message_string)

    def __getListOfLengths(self, message):
        length_list = []
        chunks = int(len(message) / self.chunk_size)
        last_chunk = int(len(message) % self.chunk_size)

        length_list = chunks * [self.chunk_size] + [last_chunk]
        length_list = [size for size in length_list if size != 0]
        return length_list

    def __writeFragment(self, message, count, no_transmissions):

        self.__print("message to packetize", message)

        outgoing_message = self.delimiter
        outgoing_message += self.start_condition
        outgoing_message += count
        outgoing_message += no_transmissions
        outgoing_message += chr(len(message))

        outgoing_message += message

        crc32_checker = binascii.crc32(outgoing_message.encode('utf-8'))
        crc32_checker &= 0xffffffff
        crc_to_bytes = struct.pack('!I', crc32_checker)
        crc_to_str = ""
        for each_byte in crc_to_bytes:
            crc_to_str += chr(each_byte + self.crc_offset)

        outgoing_message += crc_to_str
        outgoing_message += self.end_condition

        outgoing_message = outgoing_message.encode('utf-8')

        self.__print('final message', outgoing_message)
        self.serial.write(outgoing_message)

    def setDisplayVerbose(self, choice = True):
        self.display_verbose = choice

    def setChunkSize(self, chunk_size):
        if chunk_size > 0:
            self.chunk_size = chunk_size

    def writeMessage(self, message):
        chunked_message_lengths = self.__getListOfLengths(message)

        if len(chunked_message_lengths) == 1:
            self.__writeFragment(message, count, count)

        elif len(chunked_message_lengths) > 0:
            no_transmissions = len(chunked_message_lengths)
            count = no_transmissions

            while len(chunked_message_lengths) > 0:
                self.__writeFragment(message[0:chunked_message_lengths[0]], chr(count), chr(no_transmissions))
                message = message[chunked_message_lengths.pop(0):]
                count -= 1

    def __readFraments(self, first_time, met_first_trans, last_counter = 1):
        current_bad_readings = 0
        while current_bad_readings < self.max_bad_readings:
            try:
                if self.serial.read().decode('utf-8') == self.delimiter:
                    break
                current_bad_readings += 1

            except UnicodeDecodeError:
                continue

        if current_bad_readings == self.max_bad_readings:
            raise serial.SerialTimeoutException("[rflink : too much time]")

        start_condition = self.serial.read(2).decode('utf-8')
        if start_condition != self.start_condition:
            raise IOError('[transmission error - bad start condition]')

        current_count = self.serial.read(1).decode('utf-8')
        no_transmissions = self.serial.read(1).decode('utf-8')
        message_length = self.serial.read(1).decode('utf-8')

        message = self.serial.read(ord(message_length)).decode('utf-8')
        incoming_message = self.delimiter + self.start_condition + current_count + no_transmissions + message_length + message
        crc32 = self.serial.read(8).decode('utf-8')

        crc_to_bytes = []
        for each_char in crc32:
            crc_to_bytes.append(ord(each_char) - self.crc_offset)
        try:
            unpacked_crc = struct.unpack('!I', bytes(crc_to_bytes))[0]
        except ValueError:
            raise IOError('[transmission error - cannot unpack CRC32]')

        if unpacked_crc != binascii.crc32(incoming_message.encode('utf-8')):
            raise IOError('[transmission error - CRC32 does not match]')

        current_count = ord(current_count)
        no_transmissions = ord(no_transmissions)
        #print(message, first_time, current_count, no_transmissions, unpacked_crc, binascii.crc32(incoming_message.encode('utf-8')))

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


    def readMessage(self, retries = 20):
        current_count = 0
        message = ""
        self.serial.flushInput()

        while True:
            try:
                message = self.__readFraments(True, True)
                return message
            except serial.SerialTimeoutException:
                return message
            except IOError:
                if current_count == retries:
                    return message
            except UnicodeDecodeError:
                continue
            finally:
                current_count += 1

        return message
