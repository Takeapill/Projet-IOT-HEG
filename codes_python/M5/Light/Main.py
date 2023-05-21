from m5stack import lcd  # Importe le module 'lcd' de la bibliothèque 'm5stack'
import machine  # Importe le module 'machine' de la bibliothèque standard
from machine import ADC, Pin  # Importe les classes ADC et Pin du module 'machine'
from time import sleep  # Importe la fonction sleep du module 'time'
import ubinascii  # Importe le module 'ubinascii' pour manipuler les données binaires
import machine  # Importe le module 'machine' de la bibliothèque standard
import network  # Importe le module 'network' de la bibliothèque standard
from classMQTTClient import MQTTClient  # Importe la classe 'MQTTClient' du module 'classMQTTClient'

def connect():
  global client_id, mqtt_broker  # Déclare les variables 'client_id' et 'mqtt_broker' en tant que globales
  client = MQTTClient(client_id, mqtt_broker)  # Crée une instance de la classe MQTTClient avec les arguments 'client_id' et 'mqtt_broker'
  client.connect()  # Établit une connexion MQTT
  return client  # Retourne l'instance du client MQTT

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')  # Affiche un message indiquant l'échec de la connexion au courtier MQTT
  time.sleep(10)  # Pause de 10 secondes
  machine.reset()  # Redémarre la machine

class Light:
     def __init__(self):
         self.adc = ADC(Pin(35,Pin.IN))  # Crée une instance de la classe ADC avec la broche 35 en entrée
         self.adc.atten(ADC.ATTN_11DB)  # Définit l'atténuation du signal analogique

     def lectAnalogique(self):
         donnees = 0
         for i in range(0, 10):
             lecture = 4095 - self.adc.read()  # Lit la valeur analogique et l'inverse
             donnees += lecture
         return round((100*(donnees / 8)/4096), 0)  # Calcule et retourne le pourcentage de lumière

ssid = 'iPhone'  # Définit le nom du réseau Wi-Fi (SSID)
password = 'Rohsamer'  # Définit le mot de passe du réseau Wi-Fi
mqtt_broker = '172.20.10.4'  # Définit l'adresse IP du courtier MQTT

client_id = ubinascii.hexlify(machine.unique_id())  # Génère un ID client unique à partir de l'ID matériel de la machine
topic_pub = b'SallePrincipale/Lumiere'  # Définit le sujet (topic) de publication MQTT

last_message = 0  # Initialise la variable 'last_message' à 0
message_interval = 5  # Définit l'intervalle de temps entre les messages MQTT
counter = 0  # Initialise le compteur à 0

station = network.WLAN(network.STA_IF)  # Crée une instance de la classe WLAN pour gérer la connexion Wi-Fi

station.active(True)  # Active la station Wi-Fi
station.connect(ssid, password)  # Connecte la station Wi-Fi au réseau spécifié

lcd.clear()  # Efface l'affichage LCD
lcd.setCursor(0, 0)  # Déplace le curseur de l'affichage LCD à la position (0, 0)

lcd.setColor(lcd.YELLOW)  # Définit la couleur de l'affichage LCD sur JAUNE

lcd.print("\n\n\nje print le pourcentage de lumière\n dans la salle\n\n\n")  # Affiche un message sur l'affichage LCD

l = Light()  # Crée une instance de la classe Light
compteur = 9  # Initialise le compteur à 9

while True:
    lcd.print(str(l.lectAnalogique()) + '%\n')  # Affiche le pourcentage de lumière sur l'affichage LCD
    print(str(l.lectAnalogique()))  # Affiche le pourcentage de lumière sur la console
    compteur += 1  # Incrémente le compteur

    if compteur >= 9:
        lcd.clear()  # Efface l'affichage LCD
        lcd.setCursor(0, 0)  # Déplace le curseur de l'affichage LCD à la position (0, 0)
        lcd.setColor(lcd.YELLOW)  # Définit la couleur de l'affichage LCD sur JAUNE
        lcd.print("\n\n\nje print le pourcentage de lumière\n dans la salle\n\n\n")  # Affiche un message sur l'affichage LCD
        compteur = 0  # Réinitialise le compteur

    while station.isconnected() == False:  # Boucle tant que la station n'est pas connectée au réseau Wi-Fi
      pass

    print('Connection successful')  # Affiche un message indiquant que la connexion est réussie
    print(station.ifconfig())  # Affiche la configuration IP de la station

    try:
      client = connect()  # Établit une connexion MQTT
    except OSError as e:
      print("erreur connect MQTT")  # Affiche un message d'erreur indiquant une erreur lors de la connexion MQTT
      #restart_and_reconnect()  # Redémarre et tente de se reconnecter

    try:
        client.check_msg()  # Vérifie les messages MQTT entrants
        msg = b'Le pourcentage de lumière est de #%d' % l.lectAnalogique()  # Crée un message MQTT avec le pourcentage de lumière
        client.publish(topic_pub, msg)  # Publie le message sur le sujet (topic) spécifié
        last_message = time.time()  # Met à jour le timestamp du dernier message publié
        sleep(60)  # Pause de 60 secondes
    except OSError as e:
        print("erreur sub")  # Affiche un message d'erreur indiquant une erreur lors de la réception des messages MQTT
        #restart_and_reconnect()  # Redémarre et tente de se reconnecter
