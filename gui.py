#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter
from sercomm import Sercomm
import thread
import time

def uebergabe(befehl):
	if befehl.startswith("ag0") and len(befehl) > 4:
	    schieber.set(int(befehl[3:6]))
	antwort = rig.lesen(befehl)
	ausgabefenster["text"] = "Transceiver-Antwort:\n" + antwort
	return antwort
	
def slider(wert):
	if int(wert) < 10:
		wert = "ag000"+str(wert)+";"
	elif int(wert) < 100:
		wert = "ag00"+str(wert)+";"
	else:
		wert = "ag0"+str(wert)+";"
	uebergabe(wert)
	
def freqformat(wert):
	wert = wert[5:7]+"."+wert[7:10]+"."+wert[10:12]
	if wert[0] == "0":
		wert = wert[1:]
	return wert
	
def formfreq(wert):
	finstring = frequenz.get()
	finstring = finstring.replace(".", "")
	if len(finstring) < 5:
		finstring = "0" + finstring + "00"
	elif len(finstring) < 6:
		finstring = finstring + "00"
	elif len(finstring) < 7:
		finstring = "0" + finstring
	if wert == "fr0;":
		finstring = "FA000"+finstring+"0;"
	else:
		finstring = "FB000"+finstring+"0;"
	uebergabe(finstring)
	
def freqprint():
	if uebergabe("fr;") == "FR0;":
		vfoa.config(relief="sunken", bg="white", fg="red")
		vfob.config(relief="raised", bg="grey", fg="black")
		#frequenz.delete(0,"end")
		#frequenz.insert(0,freqformat(uebergabe("fa;")))
	elif uebergabe("fr;") == "FR1;":
		vfoa.config(relief="raised", bg="grey", fg="black")
		vfob.config(relief="sunken", bg="white", fg="red")
		#frequenz.delete(0,"end")
		#frequenz.insert(0,freqformat(uebergabe("fb;")))
		
def wechsel(richtung):
	formfreq(richtung)
	uebergabe(richtung)
	freqprint()

def befehlzeigen(befehl):
	befehlsantwort["text"] = "Befehls-Antwort:\n" + uebergabe(befehl)
	befehlsantwort["fg"] = "blue"

def smeteranzeige():
	while True:
		smeter["text"] = "S-Wert: " + uebergabe("sm0;")[4:7]
		time.sleep(0.2)

def vfoathread():
	while True:
		ausgabefreq = freqformat(uebergabe("fa;"))
		x = int(ausgabefreq[:ausgabefreq.index(".")])
		if x in band:
			vfoafreq["text"] = "VFO A: " + ausgabefreq + "\n" + band[x]
		else:
			vfoafreq["text"] = "VFO A: " + ausgabefreq + "\nKein Amateurband!"
		time.sleep(0.5)

def vfobthread():
	while True:
		ausgabefreq = freqformat(uebergabe("fb;"))
		y = int(ausgabefreq[:ausgabefreq.index(".")])
		if y in band:
			vfobfreq["text"] = "VFO B: " + ausgabefreq + "\n" + band[y]
		else:
			vfobfreq["text"] = "VFO B: " + ausgabefreq + "\nKein Amateurband!"
		time.sleep(0.6)
	
def rigzustand():
	while True:
		freqprint()
		schieber.set(int(uebergabe("ag0;")[3:6]))
		betriebsart = uebergabe("md;")
		for z in buttonliste:
			z.config(bg='grey',relief='raised', fg="black")
		buttonliste[int(betriebsart[2])-1].config(bg='white',fg="red", relief='sunken')
		time.sleep(0.3)


# Start Hauptprogramm		

# Liste für die Betriebsarten-Buttons erstellen für gemeinsame Änderungen
buttonliste = list()

# Zuordnung Frequenz - Band via dictionary
band = {1:"160m Band", 3:"80m Band", 7:"40m Band", 
        10:"30m Band", 14:"20m Band", 18:"17m Band", 
        21:"15m Band", 24:"12m Band", 
        28:"10m Band", 29:"10m Band"}

#Hauptfenster
main = Tkinter.Tk()
rig = Sercomm()

main.geometry("520x350+150+150")
main.title("Mini Rig Control by DL5PD")

# Erklärungs-Labels erzeugen
label1 = Tkinter.Label(main, text="Befehlseingabe:")
label1.grid(padx=5, pady=1, row=0, column=1)
label2 = Tkinter.Label(main, text="Frequenzeingabe:")
label2.grid(padx=5, pady=1, row=0, column=3)

# einzeiliges Eingabefeld für Befehlseingabe
e = Tkinter.Entry(main)
e.grid(padx=5,pady=2, row=1, column=1)

# Ausführen Knopf
knopfbefehl = Tkinter.Button(main, text="Befehl senden", command = lambda: befehlzeigen(e.get()))
knopfbefehl.grid(padx=5, pady=2, row=1, column=2)

#Info-Fenster zur Ausgabe der ser. Schnittstellenaktivität und die explizite Befehlsantwort
ausgabefenster = Tkinter.Label(main, text="Transceiver-Antwort:\n")
ausgabefenster.grid(padx=5, pady=5, row=2, column=1)

befehlsantwort = Tkinter.Label(main, text="Befehls-Antwort:\n")
befehlsantwort.grid(padx=5, pady=5, row=2, column=2)

#Band-Umschaltungs-Frame
#frame = Tkinter.Frame(main)
#frame.pack()
bandup = Tkinter.Button(main, text="Band Up", fg="brown", command = lambda: wechsel("bu;"))
bandup.grid(row=3, column=1)
banddown = Tkinter.Button(main, text="Band Down", fg="brown", command = lambda: wechsel("bd;"))
banddown.grid(row=3, column=2)

#Lautstärke-Regler
schieber = Tkinter.Scale(main, orient="horizontal", from_=0, to=255, resolution=5, 
    command = slider)
schieber.set(int(uebergabe("ag0;")[3:6]))
schieber.grid(padx=10,pady=10, row=3, column=3)

# Frequenzanzeige / Eingabe für 2 VFOs
#framefreq = Tkinter.Frame(main)
#framefreq.pack()
frequenz = Tkinter.Entry(main)
frequenz.grid(row=1, column=3, padx=5, pady=2)
vfoa = Tkinter.Button(main, text="VFO A", fg="black", command = lambda: wechsel("fr0;"))
vfoa.grid(padx=5, pady=15, row=4, column=2)
vfob = Tkinter.Button(main, text="VFO B", fg="black", command = lambda: wechsel("fr1;"))
vfob.grid(padx=5, pady=15, row=4, column=3)
clear = Tkinter.Button(main, text="CLEAR", fg="black", command = lambda: frequenz.delete(0,"end"))
clear.grid(padx=5, pady=15, row=4, column=1)

# Betriebsarten - Schalter
#frame2 = Tkinter.Frame(main)
#frame2.pack()
lsb = Tkinter.Button(main, text="LSB", fg="red", command = lambda: uebergabe("md1;"))
lsb.grid(padx=5, pady=3, row=5, column=1)
buttonliste.append(lsb)
usb = Tkinter.Button(main, text="USB", fg="red", command = lambda: uebergabe("md2;"))
usb.grid(padx=5, pady=3, row=5, column=2)
buttonliste.append(usb)
cw = Tkinter.Button(main, text="CW", fg="red", command = lambda: uebergabe("md3;"))
cw.grid(padx=5, pady=3, row=5, column=3)
buttonliste.append(cw)
f3e = Tkinter.Button(main, text="FM", fg="red", command = lambda: uebergabe("md4;"))
f3e.grid(padx=5, pady=3, row=6, column=1)
buttonliste.append(f3e)
a3e = Tkinter.Button(main, text="AM", fg="red", command = lambda: uebergabe("md5;"))
a3e.grid(padx=5, pady=3, row=6, column=2)
buttonliste.append(a3e)
fsk = Tkinter.Button(main, text="FSK", fg="red", command = lambda: uebergabe("md6;"))
fsk.grid(padx=5, pady=3, row=6, column=3)
buttonliste.append(fsk)

# S-Meter-Anzeige, VFO A u. B mit aktueller Frequenz
smeter = Tkinter.Label(main, text="S-Wert: ", font=("Helvetica", 11))
smeter.grid(padx=5, pady=15, row=7, column=1)
vfoafreq = Tkinter.Label(main, text="VFO A: ", font=("Helvetica", 11))
vfoafreq.grid(padx=5, pady=15, sticky='W', row=7, column=2)
vfobfreq = Tkinter.Label(main, text="VFO B: ", font=("Helvetica", 11))
vfobfreq.grid(padx=5, pady=15, row=7, column=3)


thread.start_new_thread(rigzustand, ())
thread.start_new_thread(smeteranzeige, ())
thread.start_new_thread(vfoathread, ())
thread.start_new_thread(vfobthread, ())

#Endlosschleife 
main.mainloop()
