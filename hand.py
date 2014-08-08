__author__ = 'ansi'

import os
import time
import serial
import datetime
import threading

class Receiver(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self._active = False
        self._buttonstart = 0
        self.setDaemon(True)

    def setSer(self,ser, hand):
        self._ser = ser
        self._active = True
        self._hand = hand

    def run(self):
        while self._active:
            c = self._ser.read()
            if datetime.datetime.now().microsecond
            if c in ('0','1','2'):
                if c == '0':
                    hand.nextGesture()
                if c == '1':
                    hand.previousGesture()
                if c == '2':
                    hand.endButton()
            print c

    def stop(self):
        self._active = False

class Hand:

    """
        000000
        |||||+ Sign
        ||||+- Thump
        |||+--Index
        ||+---Middle
        |+----Ring
        +-----Little
    """

    def __init__(self, port='/dev/ttyACM0', speed = 9600):
        self._port      = port
        self._speed     = speed
        self._array     = (0,0,0,0,0,0)
        self._ser       = None
        self._receiver  = Receiver()
        self._gesture   = 0
        self._endbutton = 0

    def _getTimeArray(self):
        now      = datetime.datetime.now()
        intval   = now.hour * 100 + now.minute
        intarray = []
        while intval:
            intarray.append(intval%5)
            intval=intval/5
        return intarray

    def _update(self):
        if self._ser is not None and self._ser.isOpen():
            self._ser.write(''.join(str(x) for x in self._array))
            self._ser.write('\n')
            print ''.join(str(x) for x in self._array)

    def connect(self):
        try:
            self._ser = serial.Serial(self._port, self._speed)
            if self._ser == None:
                print "No serial port"
                os.exit(1)
            if not self._ser.isOpen():
                self._ser.open()
            self._receiver.setSer(self._ser,self)
            self._receiver.start()
        except Exception, e:
            print e

    def disconnect(self):
        if self._ser is not None and self._ser.isOpen():
            self._receiver.stop()
            self._ser.close()

    def setTime(self):
        sign = self._array[5]
        self._array = self._getTimeArray()
        self._array.append(sign)
        self._update()

    def signHide(self):
        self._array[5] = 0
        self._update()

    def signShow(self):
        self._array[5] = 4
        self._update()

    def setGesture(self, index):
        sign = self._array[5]
        if index == 0:
            self._array = [0,0,4,0,0] #Stinkefinger
        if index == 1:
            self._array = [0,4,4,0,0] #Victory
        if index == 2:
            self._array = [0,4,0,0,4] #devil
        if index == 3:
            self._array = [0,0,0,0,4] #dr evil
        if index == 4:
            self._array = [4,4,4,4,4] #high five
        if index == 5:
            self._array = [4,4,0,4,4] #superman
        self._array.append(sign)
        self._update()

    def nextGesture(self):
        self._gesture += 1
        if self._gesture > 5:
            self._gesture = 0
        self.setGesture(self._gesture)

    def previousGesture(self):
        self._gesture -= 1
        if self._gesture < 0:
            self._gesture = 5
        self.setGesture(self._gesture)

    def endButton(self):
        if self._endbutton == 0:
            self._array[5] = 4
            self._update()
            self._endbutton += 1
        elif self._endbutton == 1:
            self._array[5] = 0
            self.setGesture(0)
            self._update()
            self._endbutton += 1
        elif self._endbutton == 2:
            self._endbutton == 0

if __name__ == '__main__':
    hand = Hand()
    hand.connect()
    hand.setTime()
    time.sleep(100)
    hand.disconnect()

