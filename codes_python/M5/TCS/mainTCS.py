"""
mainTCS using classTCS class library
"""
import sys
from time import sleep
from machine import Pin, I2C
from classTCS import *  

def main():
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
