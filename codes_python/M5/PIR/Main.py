from m5stack import lcd  # Importe le module 'lcd' de la bibliothèque 'm5stack'
from capteurPIR import *  # Importe tous les éléments du module 'capteurPIR'
from subMQTT import *  # Importe tous les éléments du module 'subMQTT'
from classMQTTClient import MQTTClient  # Importe la classe 'MQTTClient' du module 'classMQTTClient'
import machine  # Importe le module 'machine' de la bibliothèque standard
import network  # Importe le module 'network' de la bibliothèque standard

def connected():
  global client_id, mqtt_broker  # Déclare les variables 'client_id' et 'mqtt_broker' en tant que globales
  client = MQTTClient(client_id, mqtt_broker)  # Crée une instance de la classe MQTTClient avec les arguments 'client_id' et 'mqtt_broker'
  client.connect()  # Établit une connexion MQTT
  print("connect")  # Affiche un message "connect"
  return client  # Retourne l'instance du client MQTT

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')  # Affiche un message indiquant l'échec de la connexion au courtier MQTT
  time.sleep(10)  # Pause de 10 secondes
  machine.reset()  # Redémarre la machine

compteur = 0  # Initialise la variable 'compteur' à 0
pir = PIR()  # Crée une instance de la classe PIR
ssid = 'iPhone'  # Définit le nom du réseau Wi-Fi (SSID)
password = 'Rohsamer'  # Définit le mot de passe du réseau Wi-Fi
mqtt_broker = '172.20.10.4'  # Définit l'adresse IP du courtier MQTT

client_id = ubinascii.hexlify(machine.unique_id())  # Génère un ID client unique à partir de l'ID matériel de la machine
topic_pub = b'SallePrincipale/Presence'  # Définit le sujet (topic) de publication MQTT

last_message = 0  # Initialise la variable 'last_message' à 0
message_interval = 5  # Définit l'intervalle de temps entre les messages MQTT
counter = 0  # Initialise la variable 'counter' à 0

station = network.WLAN(network.STA_IF)  # Crée une instance de la classe WLAN pour gérer la connexion Wi-Fi

station.active(True)  # Active la station Wi-Fi
station.connect(ssid, password)  # Connecte la station Wi-Fi au réseau spécifié

lcd.clear()  # Efface l'affichage LCD
lcd.setCursor(0, 0)  # Définit la position du curseur de l'affichage LCD à la première ligne et première colonne
lcd.setColor(lcd.YELLOW)  # Définit la couleur de l'affichage LCD sur jaune
lcd.print("\n\n Je suis le capteur de mouvement\n\n")  # Affiche un message sur l'affichage LCD

# Boucle infinie pour lire en continu l'état du capteur de mouvement et l'afficher toutes les 0,5 seconde
while True:
    value = pir.read()  # Lit la valeur du capteur de mouvement
    lcd.print(str(value) + '\n')  # Affiche la valeur sur l'affichage LCD
    compteur += 1  # Incrémente le compteur

    sleep(0.5)  # Pause de 0,5 seconde avant la prochaine lecture

    if compteur >= 9:
        compteur = 0
        lcd.clear()  # Efface l'affichage LCD
        lcd.setCursor(0, 0)  # Définit la position du curseur de l'affichage LCD à la première ligne et première colonne
        lcd.setColor(lcd.YELLOW)  # Définit la couleur de l'affichage LCD sur jaune
        lcd.print("\n\n Je suis le capteur de mouvement\n\n")  # Affiche un message sur l'affichage LCD

    while station.isconnected() == False:  # Boucle tant que la station n'est pas connectée au réseau Wi-Fi
      pass

    print('Connection successful')  # Affiche un message indiquant que la connexion est réussie
    print(station.ifconfig())  # Affiche la configuration IP de la station

    try:
      client = connected()  # Établit une connexion MQTT
    except OSError as e:
      print("erreur connect MQTT")  # Affiche un message d'erreur indiquant une erreur lors de la connexion MQTT
      #restart_and_reconnect()  # Redémarre et tente de se reconnecter

    try:
        client.check_msg()  # Vérifie les messages MQTT entrants
        if value == 1:
          msg = b'Il y a eu un passage #%d' % counter  # Crée un message MQTT avec un compteur
          client.publish(topic_pub, msg)  # Publie le message sur le sujet (topic) spécifié
          last_message = time.time()  # Met à jour le timestamp du dernier message publié
          counter += 1  # Incrémente le compteur
    except OSError as e:
        print("erreur sub")  # Affiche un message d'erreur indiquant une erreur lors de la réception des messages MQTT
        #restart_and_reconnect()  # Redémarre et tente de se reconnecter
