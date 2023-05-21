#Permet un affichage sur l'écran du M5

from m5stack import lcd
import machine
from machine import ADC, Pin
from time import sleep

class Light:
     def __init__(self):
         self.adc = ADC(Pin(35,Pin.IN)) # Fil blanc
         self.adc.atten(ADC.ATTN_11DB)
     
     def lectAnalogique(self):
         donnees = 0
         for i in range(0, 10):
             lecture = 4095 - self.adc.read()
             donnees += lecture
         return round((100*(donnees / 8)/4096), 0)

lcd.clear()

lcd.setCursor(0, 0)

lcd.setColor(lcd.YELLOW) #YELLOW but en réalité c'est BLUE. BLUE is YELLOW and YELLOW is BLUE. Got it ? How about GREEN ?! hun.. GREEN IS PINK

lcd.print("\n\n\nje print le pourcentage de lumière\n dans la salle\n\n\n")



l=Light()
compteur = 9
while True:
     lcd.print(str(l.lectAnalogique()) + '%\n')
     sleep(1)

     compteur += 1
     if compteur >= 9:
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.setColor(lcd.YELLOW) #YELLOW but en réalité c'est BLUE. BLUE is YELLOW and YELLOW is BLUE. Got it ? How about GREEN ?! hun.. GREEN IS PINK
        lcd.print("\n\n\nje print le pourcentage de lumière\n dans la salle\n\n\n")
        compteur = 0
