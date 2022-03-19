#!/usr/bin/python3
import socket
import mopp

m = mopp.mopp(wpm=23)
f=m.str2mopp("hi")

msgFromClient       = f
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 7373)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
mm = msgFromServer[0].decode("utf-8", errors='ignore')
#msg = "Message from Server {}".format(msgFromServer[0])
#print(msg)

print (mm)
m1 = m.decodePacket(mm)
print (m1)
print (m.rx_wpm)

m1 = m.mopp2str(mm)
print (m1)


