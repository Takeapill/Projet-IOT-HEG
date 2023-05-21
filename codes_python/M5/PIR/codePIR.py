# Importation des bibliothèques nécessaires
from machine import Pin
from time import sleep

# Définition de la classe PIR
class PIR():
    # Initialisation de la classe avec la broche GPIO à utiliser et l'état initial du capteur de mouvement
    def __init__(self):
        self.pin = Pin(22,Pin.IN) # Broche 22 en entrée
        self.mvt = 0 # L'état initial du capteur de mouvement est zéro
        # Configuration d'un gestionnaire d'interruption sur la broche 22 qui appelle la méthode actionInterruption()
        self.pin.irq(trigger=(Pin.IRQ_RISING | Pin.IRQ_FALLING), handler=self.actionInterruption)
    
    # Méthode pour mettre à jour l'état du capteur de mouvement en fonction de l'état de la broche 22
    def actionInterruption(self, pin):
        if (pin.value()==1):
            if (self.mvt==0):
                self.mvt=1 # Si la broche 22 est à l'état haut et que l'état du capteur de mouvement est zéro, on met l'état du capteur de mouvement à 1 pour indiquer un mouvement
        else:
            if (self.mvt==1):
                self.mvt=0 # Si la broche 22 est à l'état bas et que l'état du capteur de mouvement est à 1, on met l'état du capteur de mouvement à 0 pour indiquer l'arrêt du mouvement
    
    # Méthode pour récupérer l'état actuel du capteur de mouvement
    def read(self):
        return self.mvt

# Création d'une instance de la classe PIR appelée "pir"
pir = PIR()

# Boucle infinie pour lire en continu l'état du capteur de mouvement et l'afficher toutes les 0,5 seconde
while True:
    print(pir.read())
    sleep(0.5) # Pause de 0,5 seconde avant la prochaine lecture
