#!/usr/bin/python3
from math import ceil

class mopp():
    serial = 1
    protocol_version = '01'

    morse = {
        "0" : "-----", "1" : ".----", "2" : "..---", "3" : "...--", "4" : "....-", "5" : ".....",
        "6" : "-....", "7" : "--...", "8" : "---..", "9" : "----.",
        "a" : ".-", "b" : "-...", "c" : "-.-.", "d" : "-..", "e" : ".", "f" : "..-.", "g" : "--.",
        "h" : "....", "i" : "..", "j" : ".---", "k" : "-.-", "l" : ".-..", "m" : "--", "n" : "-.",
        "o" : "---", "p" : ".--.", "q" : "--.-", "r" : ".-.", "s" : "...", "t" : "-", "u" : "..-",
        "v" : "...-", "w" : ".--", "x" : "-..-", "y" : "-.--", "z" : "--..", "=" : "-...-",
        "/" : "-..-.", "+" : ".-.-.", "-" : "-....-", "." : ".-.-.-", "," : "--..--", "?" : "..--..",
        ":" : "---...", "!" : "-.-.--", "'" : ".----."
    }

    def __init__(self, wpm=20):
        self.wpm = wpm

    def str2mopp(self, str):
        """
        Variables: 
        m - data in 0/1 notation
        res - data in binary notation
        """

        # Header
        m = self.protocol_version               
        m += bin(self.serial)[2:].zfill(6)
        m += bin(self.wpm)[2:].zfill(6)

        # Payload
        for c in str:
            if c == " ":
                m += '11'			# spaces not supported by morserino - treat as word
                continue

            for b in self.morse[c.lower()]:
                if b == '.':
                    m += '01'       # .
                else:
                    m += '10'       # -

            m += '00'				# EOC

        m = m[0:-2] + '11'	        # final EOW
 
        m = m.ljust(int(8*ceil(len(m)/8.0)),'0') # fill rest with 0
        self.serial += 1
        #debug print (m)

        return self.bit2str(m)

    def bit2str (self, bit):
        # Encode data to binary notation
        m = bit
        res = ''
        for i in range (0, len(m), 8):
            #debug: print (m[i:i+8])
            res += chr(int(m[i:i+8],2))
        
        return res

    def decodePacket(self, packet):
        """
        //// byte 1: header; first two bits are the protocol version (curently 01), plus 6 bit packet serial number (starting from random)
        //// byte 2: first 6 bits are wpm (must be between 5 and 60; values 00 - 04 and 61 to 63 are invalid), the remaining 2 bits are already data payload!

        """
        bits = "".join("{:08b}".format(ord(c)) for c in packet)
        # debug print (bits)

        l = len(bits)

        # Extract Header
        protocol_version = bits[0:2]
        serial = bits[3:8]
        wpm = int(bits[9:14],2)

        # Extract payload
        msg = ""
        for i in range (14, l, 2):
            if bits[i:i+2] == "01": # .
                msg += "."
            elif bits[i:i+2] == "10": # -
                msg += "-"
            elif bits[i:i+2] == "00": # EOC
                msg += " "
            elif bits[i:i+2] == "11": # EOW
                msg += " <EOW>  "
            
        print (protocol_version, serial, wpm, msg)

    def str2hex(self,str):
        return ":".join("{:02x}".format(ord(c)) for c in str)
    
    def str2bit(self,str):
        return ":".join("{:08b}".format(ord(c)) for c in str)

m = mopp(wpm=23)
f=m.str2mopp("Gerolf ok")
#print(m.str2bit(f))
m.decodePacket(f)