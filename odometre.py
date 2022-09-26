#Laboratoire 3 - KF2
#Fait par: Gabriel Lessard - Samy Tétrault - Guillaume Légaréà
import threading
import gpiozero
import cv2
from time import sleep
from deplacement_robot import Moteur
import numpy as np

#Encodeur gauche pin = 27 droit pin = 22


class Odomètre:
    DISTANCE_PAR_TRANSITION = None #à modifier 

    def __init__(self, num_broche_gauche, num_broche_droite):
        self.DISTANCE_TRANSITION = 0.55
        self.NB_TRANSITION_FREINAGE = 40
        self.encodeur_gauche = gpiozero.DigitalInputDevice(num_broche_gauche)
        self.encodeur_droit = gpiozero.DigitalInputDevice(num_broche_droite)
        self.evenement = threading.Event()
        self.moteur = Moteur()
        self.nb_transition_gauche = 0
        self.nb_transition_droit = 0

    def augmenter_nb_transition_gauche(self):
        self.nb_transition_gauche += 1

    def augmenter_nb_transition_droit(self):
        self.nb_transition_droit += 1
        
    def calculer_nombre_transition(self,nb_transition_a_faire):
        self.encodeur_gauche.when_activated = self.augmenter_nb_transition_gauche
        self.encodeur_gauche.when_deactivated = self.augmenter_nb_transition_gauche
        self.encodeur_droit.when_activated = self.augmenter_nb_transition_droit
        self.encodeur_droit.when_deactivated = self.augmenter_nb_transition_droit
        nb_transition_a_faire = nb_transition_a_faire - self.NB_TRANSITION_FREINAGE
        while self.nb_transition_droit < nb_transition_a_faire and self.nb_transition_gauche < nb_transition_a_faire:
            sleep(0.01)
        self.evenement.set()
        
    def avancer_distance(self,distance_à_parcourir,vitesse):
        self.moteur.avancer(vitesse)
        #calcul du nombre de transition
        self.calculer_nombre_transition(distance_à_parcourir/self.DISTANCE_TRANSITION)
        
 
    def attendre(self):
        self.evenement.wait()
        self.moteur.freiner()
        self.encodeur_gauche.when_activated = None
        self.encodeur_gauche.when_deactivated = None
        self.encodeur_droit.when_activated = None
        self.encodeur_droit.when_deactivated = None
        print(self.nb_transition_droit)
        print(self.nb_transition_gauche)
        self.nb_transition_droit = 0
        self.nb_transition_gauche = 0

if __name__ == "__main__":
    distance_centimetre = 100
    odo = Odomètre(27,22) 
    img = np.zeros((512,512,3),np.uint8)
    cv2.imshow('Labo 3', img)
    quitter = True
    vitesse = 0.5
    while quitter:
        key = cv2.waitKey(100)
        if key == ord('w'):
            th_avancer = threading.Thread(target=odo.avancer_distance,args=(distance_centimetre,vitesse)) 
            th_avancer.start()
            odo.attendre()
            odo.moteur.arreter()
            quitter = False
    cv2.destroyAllWindows()