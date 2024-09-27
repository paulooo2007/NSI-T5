import pygame  # necessaire pour charger les images et les sons


class Joueur() : # classe pour créer le vaisseau du joueur
    def __init__(self) :
        self.position = 368
        self.sens = "centre"
        self.image = pygame.image.load('vaisseau.png')
        self.vitesse = 0.5
        pass
    
    def deplacer(self) :
        if self.sens == "gauche" :
            self.position -=0.5
            if self.position < 0 :
                self.position = 0 
           
        elif self.sens == "droite" :
            self.position +=0.5
            if self.position > 800-64: 
                self.position = 800-64
class Balle () :
    def __init__(self) :
        self.tireur = Joueur
        self.depart = int
        self.hauteur = int
        self.image = pygame.image.load()
        self.etat = 