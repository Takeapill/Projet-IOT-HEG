import sys
from time import sleep
from machine import Pin, I2C
import machine
import network
from classTCS import *
from classMQTTClient import MQTTClient
import ubinascii


ssid = ''
password = ''
mqtt_broker = '192.168.1.142'

client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = b'SallePrincipale/Couleur'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

def connect():
  global client_id, mqtt_broker
  client = MQTTClient(client_id, mqtt_broker)
  client.connect()
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def main():
    while station.isconnected() == False:
      pass

    print('Connection successful')
    print(station.ifconfig())

    try:
      client = connect()
    except OSError as e:
      print("erreur connect MQTT")
      #restart_and_reconnect()
    
    print("Starting tcs34725_test program")
    tcs = TCS34725(scl=Pin(22), sda=Pin(21))      
    if not tcs.isconnected:                         
        print("Terminating...")
        sys.exit()
    tcs.gain = TCSGAIN_LOW
    tcs.integ = TCSINTEG_HIGH
    tcs.autogain = True                               
    color_names = ("Clear", "Red", "Green", "Blue")
    print(" Clear   Red Green  Blue    gain  >")
    try:
        while True:                                   
            """ show color counts """
            counts_tuple = tcs.colors                  
            counts = list(counts_tuple)        
            for count in counts_tuple:
                if count >= tcs.overflow_count:      
                    count = -1                   
                print(" {:5d}".format(count // tcs.gain_factor), end="")
            largest = max(counts[1:])                   
            avg = sum(counts[1:]) // 3       
            if largest > avg * 3 // 2:       
                color = color_names[counts.index(largest)]
                try:
                    client.check_msg()
                    msg = b'Couleur: %s' % counter
                    client.publish(topic_pub, msg)
                except OSError as e:
                    print("erreur sub")
                #restart_and_reconnect() 
            else:
                color = "-"
            print("    ({:2d})  {:s}" .format(tcs.gain_factor, color))
            sleep(5)                             
    except KeyboardInterrupt:
        print("Closing down!")
    except Exception as err:
        print("Exception:", err)
    tcs.close()

main()
