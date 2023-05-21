from realudp import *
from time import *
from gpio import *

socket = RealUDPSocket()

def onUDPReceive(ip, port, data):
	global socket
	print("received from "
		+ ip + ":" + str(port) + ":" + data);
	etatMusee = customRead(0)
	etatAlarm = digitalRead(1)
	if data == "toggle_light":
		print("light")
		if etatMusee == "1":
			customWrite(0, "0")
			etatMusee == "0"
			socket.send(ip, port, "Musee eteint")
		elif etatMusee == "0":
			customWrite(0, "1")
			etatMusee == "1"
			socket.send(ip, port, "Musee allume")
	elif data == "toggle_alarm":
		print("alarm")
		if etatAlarm == "1":
			customWrite(1, "0")
			etatAlarm == "0"
			socket.send(ip, port, "Alarme eteinte")
		elif etatAlarm == "0":
			customWrite(1, "1")
			etatAlarm == "1"
			socket.send(ip, port, "Alarme activee")
	        

def main():
    global socket
    socket.onReceive(onUDPReceive)
    print(socket.begin(12345))
    while True:
    	sleep(3600)
    

if __name__ == "__main__":
	main()
