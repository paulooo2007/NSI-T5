import pygame  # necessaire pour charger les images et les sons
import random
import math

class Joueur() : # classe pour créer le vaisseau du joueur
    def __init__(self) :
        self.position = 400
        self.image = pygame.image.load("vaisseau.png")
        self.sens = "O"
        self.vitesse = 12
        self.score = 0
        self.nb_tirs = 0 
        self.coeur = 5      
    
    def deplacer(self) :
        if (self.sens == "droite") and (self.position < 740):
            self.position = self.position + self.vitesse
        elif (self.sens == "gauche") and (self.position > 0):
           self.position = self.position - self.vitesse
           
    def tirer(self):
        self.sens = "O"
        self.nb_tirs += 1
        
    def marquer(self, score):
        self.score = self.score + score
        
    def perdrecoeur():
        self.coeur -= 1
        
    def ratio(self):
        if self.nb_tirs == 0:
            return 0
        return self.nb_kills / self.nb_tirs

class Balle() :
    def __init__(self, tireur):
        self.tireur = tireur
        self.depart = tireur.position + 16
        self.hauteur = 492
        self.image = pygame.image.load("balle.png")
        self.etat = "chargee"
        self.vitesse = 100
        self.nb_kills = 0
    
    def bouger(self):
        if self.etat == "chargee":
            self.depart = self.tireur.position + 16
            self.hauteur = 492
        elif self.etat == "tiree" :
            self.hauteur = self.hauteur - self.vitesse
        
        if self.hauteur < 0:
            self.etat = "chargee"
                
    def toucher(self, vaisseau):
        if (math.fabs(self.hauteur - vaisseau.hauteur) < 40) and (math.fabs(self.depart - vaisseau.depart) < 40):
            self.etat = "chargee"
            self.nb_kills += 1
            return True
  
class Ennemi():
    NbEnnemis = 6
    
    def __init__(self):
        self.depart = random.randint(1,700)
        self.hauteur = 10
        self.type = random.randint(1,2)
        if  (self.type == 1):
            self.image = pygame.image.load("invader1.png")
            self.vitesse = 2
        elif (self.type ==2):
            self.image = pygame.image.load("invader2.png")
            self.vitesse = 2
            
    def avancer(self):
        self.hauteur = self.hauteur + self.vitesse
    
    def disparaitre(self):
        self.depart = random.randint(1,700)
        self.hauteur = 10
        self.type = random.randint(1,2)
        if  (self.type == 1):
            self.image = pygame.image.load("invader1.png") 
        elif (self.type ==2):
            self.image = pygame.image.load("invader2.png")
            
            
    
class Niveau:
    def __init__(self):
        self.ennemis = [Ennemi(15) for _ in range(10)]  

    def mettre_a_jour(self):
        for ennemi in self.ennemis:
            ennemi.avancer(5)

    def dessiner(self, surface):
        for ennemi in self.ennemis:
            surface.blit(ennemi.image, (ennemi.depart, ennemi.hauteur))

                        

        
            
