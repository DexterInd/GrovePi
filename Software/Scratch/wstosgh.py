import array
import itertools
import socket
import struct
import sys
import threading
import time
from websocket_server import WebsocketServer


def rcv_from_sgh():
    global s,c,server
    dataPrevious = ""
    while True:
        print "listening for data from sgh"
        # time.sleep(1)
        data = dataPrevious + c.recv(8192)
        print "data length" , len(data)
        if data != "":
            print "Data received from sgh", data
            #print ("datalen: %s", len(data))

            if len(data) > 0:  # Connection still valid so process the data received

                dataIn = data

                datawithCAPS = data
                # dataOut = ""
                dataList = []  # used to hold series of broadcasts or sensor updates
                dataPrefix = ""  # data to be re-added onto front of incoming data
                while len(dataIn) > 0:  # loop thru data
                    if len(dataIn) < 4:  # If whole length not received then break out of loop
                        # print "<4 chrs received"
                        dataPrevious = dataIn  # store data and tag it onto next data read
                        break
                    sizeInfo = dataIn[0:4]
                    size = struct.unpack(">L", sizeInfo)[0]  # get size of Scratch msg
                    # print "size:", size
                    if size > 0:
                        # print dataIn[4:size + 4]
                        dataMsg = dataIn[4:size + 4].lower()  # turn msg into lower case

                        if len(dataMsg) < size:  # if msg recieved is too small
                            # print "half msg found"
                            # print size, len(dataMsg)
                            dataPrevious = dataIn  # store data and tag it onto next data read
                            break
                        #print "msg:",dataMsg
                        dataList.append(dataMsg)
                        dataIn = dataIn[size + 4:]  # cut data down that's been processed

                        # print "previous:", dataPrevious
            print "datalist:",dataList
            for msg in dataList:
                #print "msg:",msg[0:13]
                if msg[0:13] == 'sensor-update':
                    msgsplit = msg[14:].replace('"','').split(' ')
                    print "split",msgsplit
                    #for loop in range(int(len(msgsplit) / 2)):
                    #    server.send_message_to_all(msgsplit[loop * 2] + ':' + msgsplit[(loop * 2) + 1])
                    server.send_message_to_all(msgsplit[0] + ':' + msgsplit[1])
        else:
            time.sleep(0.1)




# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    #server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))
    dataOut = message

    n = len(dataOut)
    b = (chr((n >> 24) & 0xFF)) + (chr((n >> 16) & 0xFF)) + (chr((n >> 8) & 0xFF)) + (
        chr(n & 0xFF))
    c.send(b + dataOut)
    print "Data sent to sgh", dataOut


       

# For Scratch 3 handle long as int 
if sys.version > '3':
    long = int



      
        
s = socket.socket() #Create a socket object
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#host = socket.gethostname() #Get the local machine name
port = 42001 # Reserve a port for your service
s.bind(('127.0.0.1',port)) #Bind to the port

s.listen(5) #Wait for the client connection
print "wstosgh listening to scratchGPIO_handler"
c,addr = s.accept() #Establish a connection with the client
print "Got connection from ScratchGPIOHandler", addr


PORT=8000
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
d = threading.Thread(name='rcv_from_sgh', target=rcv_from_sgh)
d.setDaemon(True)
d.start()
server.run_forever()