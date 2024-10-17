
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
        
    def perdrecoeur(self):
        self.coeur -= 1
        
    def ratio(self):
        if self.nb_tirs == 0:
            return 0
        return self.nb_kills / self.nb_tirs



class Balle:
    def __init__(self, tireur):
        self.tireur = tireur
        self.depart = tireur.position + 16  # Position initiale de la balle
        self.hauteur = 492  # Position y de la balle
        self.image = pygame.image.load("balle.png")
        self.etat = "chargee"
        self.vitesse = 100  # Vitesse de déplacement de la balle
        self.nb_kills = 0

    def bouger(self):
        # Met à jour la position de la balle
        if self.etat == "chargee":
            self.depart = self.tireur.position + 16
            self.hauteur = 492
        elif self.etat == "tiree":
            self.hauteur -= self.vitesse
        
        if self.hauteur < 0:
            self.etat = "chargee"

    def toucher(self, boss):
        # Vérifie si la balle touche le boss
        if (self.depart < boss.position + boss.image.get_width() and
            self.depart + self.image.get_width() > boss.position and
            self.hauteur < boss.hauteur + boss.image.get_height() and
            self.hauteur + self.image.get_height() > boss.hauteur):
            boss.toucher()  # Appelle la méthode pour réduire les PV du boss
            return True
        return False



    
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


class Boss:
    def __init__(self):
        image_originale = pygame.image.load('boss.png')
        self.image = pygame.transform.scale(image_originale, (100, 100))  
        self.position = 300  
        self.hauteur = 50    
        self.vitesse = 1     
        self.coins = 10      # Points de vie du boss

    def avancer(self):
        if self.position <= 0 or self.position >= 700:
            self.vitesse = -self.vitesse
        self.position += self.vitesse

    def est_vaincu(self):
        return self.coins <= 0

    def toucher(self):
        self.coins -= 1  # Réduit les points de vie du boss
        if self.coins < 0:  # Ne pas permettre des PV négatifs
            self.coins = 0
