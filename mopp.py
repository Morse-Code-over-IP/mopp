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
        return

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
                continue				# spaces not supported by morserino!

            for b in self.morse[c.lower()]:
                if b == '.':
                    m += '01'       # .
                else:
                    m += '10'       # -

            m += '00'				# EOC

        m = m[0:-2] + '11'	        # final EOW
 
        m = m.ljust(int(8*ceil(len(m)/8.0)),'0') # fill rest with 0
        self.serial += 1

        # Encode data to binary notation
        res = ''
        for i in range (0, len(m), 8):
            res += chr(int(m[i:i+8],2))
        
        return res


m = mopp()
print (m.wpm)
print (m.str2mopp("test"))