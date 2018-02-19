import array
import itertools
import socket
import struct

class ScratchError(Exception): pass
class ScratchConnectionError(ScratchError): pass	

class Scratch(object):

    prefix_len = 4
    broadcast_prefix_len = prefix_len + len('broadcast ')
    sensorupdate_prefix_len = prefix_len + len('sensor-update ')

    msg_types = set(['broadcast', 'sensor-update'])

    def __init__(self, host='localhost', port=42001):
	self.host = host
	self.port = port
	self.socket = None
	self.connected = False
	self.connect()

    def __repr__(self):
	return "Scratch(host=%r, port=%r)" % (self.host, self.port)

    def _pack(self, msg):
	"""
	Packages msg according to Scratch message specification (encodes and 
	appends length prefix to msg). Credit to chalkmarrow from the 
	scratch.mit.edu forums for the prefix encoding code.
	"""
	n = len(msg) 
	a = array.array('c')
	a.append(chr((n >> 24) & 0xFF))
	a.append(chr((n >> 16) & 0xFF))
	a.append(chr((n >>  8) & 0xFF))
	a.append(chr(n & 0xFF))
	return a.tostring() + msg 

    def _extract_len(self, prefix):
	"""
	Extracts the length of a Scratch message from the given message prefix. 
	"""
	return struct.unpack(">L", prefix)[0]

    def _get_type(self, s):
	"""
	Converts a string from Scratch to its proper type in Python. Expects a
	string with its delimiting quotes in place. Returns either a string, 
	int or float. 
	"""
	# TODO: what if the number is bigger than an int or float?
	if s.startswith('"') and s.endswith('"'):
	    return s[1:-1]
	elif s.find('.') != -1: 
	    return float(s) 
	else: 
	    return int(s)

    def _escape(self, msg):
	"""
	Escapes double quotes by adding another double quote as per the Scratch
	protocol. Expects a string without its delimiting quotes. Returns a new
	escaped string. 
	"""
	escaped = ''	
	for c in msg: 
	    escaped += c
	    if c == '"':
		escaped += '"'
	return escaped

    def _unescape(self, msg):
	"""
	Removes double quotes that were used to escape double quotes. Expects
	a string without its delimiting quotes, or a number. Returns a new
	unescaped string.
	"""
	if isinstance(msg, (int, float, long)):
	    return msg

	unescaped = ''
	i = 0
	while i < len(msg):
	    unescaped += msg[i]
	    if msg[i] == '"':
		i+=1
	    i+=1
	return unescaped     

    def _is_msg(self, msg):
	"""
	Returns True if message is a proper Scratch message, else return False.
	"""
	if not msg or len(msg) < self.prefix_len:
	    return False
	length = self._extract_len(msg[:self.prefix_len])
	msg_type = msg[self.prefix_len:].split(' ', 1)[0]
	if length == len(msg[self.prefix_len:]) and msg_type in self.msg_types:
	    return True
	return False

    def _parse_broadcast(self, msg):
	"""
	Given a broacast message, returns the message that was broadcast.
	"""
	# get message, remove surrounding quotes, and unescape
	return self._unescape(self._get_type(msg[self.broadcast_prefix_len:]))

    def _parse_sensorupdate(self, msg):
	"""
	Given a sensor-update message, returns the sensors/variables that were
	updated as a dict that maps sensors/variables to their updated values.
	"""
	update = msg[self.sensorupdate_prefix_len:]
	parsed = [] # each element is either a sensor (key) or a sensor value
	curr_seg = '' # current segment (i.e. key or value) being formed
	numq = 0 # number of double quotes in current segment
	for seg in update.split(' ')[:-1]: # last char in update is a space
	    numq += seg.count('"')
	    curr_seg += seg
	    # even number of quotes means we've finished parsing a segment
	    if numq % 2 == 0: 
		parsed.append(curr_seg)
		curr_seg = ''
		numq = 0
	    else: # segment has a space inside, so add back it in
		curr_seg += ' '
	unescaped = [self._unescape(self._get_type(x)) for x in parsed]
	# combine into a dict using iterators (both elements in the list
	# inputted to izip have a reference to the same iterator). even 
	# elements are keys, odd are values
	return dict(itertools.izip(*[iter(unescaped)]*2)) 

    def _parse(self, msg):
	"""
	Parses a Scratch message and returns a tuple with the first element
	as the message type, and the second element as the message payload. The 
	payload for a 'broadcast' message is a string, and the payload for a 
	'sensor-update' message is a dict whose keys are variables, and values
	are updated variable values. Returns None if msg is not a message.
	"""
	if not self._is_msg(msg):
	    return None
	msg_type = msg[self.prefix_len:].split(' ')[0]
	if msg_type == 'broadcast':
	    return ('broadcast', self._parse_broadcast(msg))
	else:
	    return ('sensor-update', self._parse_sensorupdate(msg))

    def _write(self, data):
	"""
	Writes string data out to Scratch
	"""
	total_sent = 0
	length = len(data)
	while total_sent < length:
	    try:
		sent = self.socket.send(data[total_sent:])
	    except socket.error as (err, msg):
		self.connected = False
		raise ScratchError("[Errno %d] %s" % (err, msg))
	    if sent == 0:
		self.connected = False
		raise ScratchConnectionError("Connection broken")
	    total_sent += sent

    def _send(self, data):
	"""
	Sends a message to Scratch
	"""
	self._write(self._pack(data))

    def _read(self, size):
	"""
	Reads size number of bytes from Scratch and returns data as a string
	"""
	data = ''
	while len(data) < size:
	    try:
		chunk = self.socket.recv(size-len(data))
	    except socket.error as (err, msg):
		self.connected = False
		raise ScratchError("[Errno %d] %s" % (err, msg))
	    if chunk == '':
		self.connected = False
		raise ScratchConnectionError("Connection broken")
	    data += chunk
	return data

    def _recv(self):
	"""
	Receives and returns a message from Scratch
	"""
	prefix = self._read(self.prefix_len)
	msg = self._read(self._extract_len(prefix))
	return prefix + msg

    def connect(self):
	"""
	Connects to Scratch.
	"""
	self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
	    self.socket.connect((self.host, self.port))
	except socket.error as (err, msg):
	    self.connected = False
	    raise ScratchError("[Errno %d] %s" % (err, msg))
	self.connected = True

    def disconnect(self):
	"""
	Closes connection to Scratch
	"""
	try: # connection may already be disconnected, so catch exceptions
	    self.socket.shutdown(socket.SHUT_RDWR) # a proper disconnect
	except socket.error:
	    pass
	self.socket.close()
	self.connected = False

    def sensorupdate(self, data):
	"""
	Given a dict of sensors and values, updates those sensors with the 
	values in Scratch.
	"""
	if not isinstance(data, dict):
	    raise TypeError('Expected a dict')
	msg = 'sensor-update '
	for key in data.keys():
	    msg += '"%s" "%s" ' % (self._escape(str(key)), 
				   self._escape(str(data[key])))
	self._send(msg)

    def broadcast(self, msg):
	"""
	Broadcasts msg to Scratch. msg can be a single message or an iterable 
	(list, tuple, set, generator, etc.) of messages.
	"""
	if getattr(msg, '__iter__', False): # iterable
	    for m in msg:
		self._send('broadcast "%s"' % self._escape(str(m)))
	else: # probably a string or number
	    self._send('broadcast "%s"' % self._escape(str(msg)))

    def receive(self):
	"""
	Receives broadcasts and sensor updates from Scratch. Returns a tuple
	with the first element as the message type and the second element 
	as the message payload. broadcast messages have a string as payload, 
	and the sensor-update messages have a dict as payload. Returns None if 
	message received could not be parsed. Raises exceptions on connection
	errors.
	"""
	return self._parse(self._recv())

