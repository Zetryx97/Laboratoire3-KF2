#Laboratoire 3 - KF2 Gabriel Lessard - Samy Tétrault - Guillaume Légaré

import gpiozero
from time import sleep

class Moteur:
    def __init__(self):
        self.moteur_avg = gpiozero.DigitalOutputDevice(6) #roue avant gauche
        self.moteur_arg = gpiozero.DigitalOutputDevice(5) #roue arrière gauche

        self.moteur_avd = gpiozero.DigitalOutputDevice(15) #roue avant droite
        self.moteur_ard = gpiozero.DigitalOutputDevice(14) #roue arrière droite

        self.control_moteur_g = gpiozero.PWMOutputDevice(13) #permet d'allumer ou d'éteindre les 2 moteurs de gauche
        self.control_moteur_d = gpiozero.PWMOutputDevice(18) #permet d'allumer ou d'éteindre les 2 moteur de droite
    
    def avancer(self,speed):
        self.moteur_avg.on()
        self.moteur_arg.off()
        self.control_moteur_g.on()
        self.moteur_avd.on()
        self.moteur_ard.off()
        self.control_moteur_d.on()

        self.control_moteur_g.value = speed
        self.control_moteur_d.value = speed

    def freiner(self):
        self.moteur_avg.on()
        self.moteur_arg.on()
        self.control_moteur_g.on()
        self.moteur_avd.on()
        self.moteur_ard.on()
        self.control_moteur_d.on()

    def arreter(self):
        self.moteur_avg.off()
        self.moteur_arg.off()
        self.control_moteur_g.off()
        self.moteur_avd.off()
        self.moteur_ard.off()
        self.control_moteur_d.off()
