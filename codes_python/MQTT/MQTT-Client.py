import paho.mqtt.client as mqtt
import datetime
import socket

# Constantes
BROKER_ADDRESS = "192.168.1.142"
TCP_SERVER_ADDRESS = "192.168.1.142"
UDP_SERVER_ADDRESS = BROKER_ADDRESS
PORT = 1883

# Status des capteurs
passage = 0
visiteurs = round(passage / 2)
lumiere = ""
couleur = ""

# A chaque connexion au broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

# A chaque message recu
def on_message(client, userdata, msg):
    global passage
    visiteurs = round(passage / 2)
    global lumiere
    global couleur
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{now} {msg.topic} {msg.payload.decode()} {msg.retain}\n"
    with open('mqtt_logs.log', 'a') as f:
        f.write(log_message)
    print(log_message)
    send_tcp_message(log_message)
    
    
    # Stocke le status des capteurs
    if msg.topic == "SallePrincipale/Presence":
        passage += 1
        send_udp_message("passage:" + str(passage))
    elif msg.topic == "SallePrincipale/Lumiere":
        lumiere = msg.payload.decode()
        send_udp_message("lumiere:"+lumiere)
    elif msg.topic == "SallePrincipale/Couleur":
         couleur = msg.payload.decode()
         send_udp_message("couleur:"+couleur)
    
    
# Envoie un message en TCP
def send_tcp_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TCP_SERVER_ADDRESS , 65432))
        s.sendall(message.encode("UTF-8"))
        s.close()

def send_udp_message(message):
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
        s.connect((UDP_SERVER_ADDRESS, 12345))
        s.sendall(message.encode("UTF-8"))
        s.close()
      
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_ADDRESS, PORT, 60)

client.loop_forever()
