#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import Queue
import thread

class Sercomm(object):
    def __init__(self):
    	try:
    		self.ser = serial.Serial(
    		    port='/dev/ttyUSB0',
    		    baudrate=19200,
    		    parity=serial.PARITY_NONE,
    		    stopbits=serial.STOPBITS_ONE,
    		    bytesize=serial.EIGHTBITS)
    	except:
    		print "Fehler mit der Seriellen Schnittstelle!\nBitte Daten in Datei sercomm.py ueberpruefen!"
    		exit()
    	self.warteschlange = Queue.Queue()
    	self.lock = thread.allocate_lock()

    def schreiben(self,befehl):
    	self.ser.write(befehl)

    def lesen(self,befehl):
    		self.lock.acquire()
    		self.warteschlange.put(befehl, True)
    		if self.warteschlange.empty() == True:
    			print "Warteschlange leer, gehe zurück!"
    			return
    		self.ser.write(self.warteschlange.get(True))
    		out = ''
    		check = ''
    		time.sleep(0.1)
    		while self.ser.inWaiting() > 0:
    			check= self.ser.read(1)
    			out += check
    			if check == ";":
    				break
    		self.warteschlange.task_done()
    		self.lock.release()
    		if out == '':
    			out = 'Leere Antwort'
    		return out
    	
    def schliessen(self):
    	self.ser.close()

def main():
    doit = Sercomm()
#    print ("Schalte 1 Band hoch")
#    doit.schreiben("BU;")
#    time.sleep(3)
    seq = raw_input("Bitte Befehl eingeben zum Auslesen\n")
#    print ("Lese aktuelle Frequenz VFO A aus")
    print "Eingegebener Befehl: "+seq+"\n"
    print "Antwort des Transceivers: "+doit.lesen(seq)+"\n"
    doit.schliessen()

if __name__ == "__main__":
    main()
    
