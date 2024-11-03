import pygame  # necessaire pour charger les images et les sons
import random
import math

class Joueur():  # classe pour créer le vaisseau du joueur
    def __init__(self):
        self.position = 400
        self.image = pygame.image.load("vaisseau.png")
        self.sens = "O"
        self.vitesse = 12
        self.score = 0
        self.nb_tirs = 0 
        self.coeur = 100
        
    def deplacer(self):
        if (self.sens == "droite") and (self.position < 740):
            self.position = self.position + self.vitesse
        elif (self.sens == "gauche") and (self.position > 0):
            self.position = self.position - self.vitesse
            
    def tirer(self):
        self.sens = "O"
        self.nb_tirs += 1
        
    def marquer(self, score):
        self.score += score
        
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
        if self.etat == "chargee":
            self.depart = self.tireur.position + 16
            self.hauteur = 492
        elif self.etat == "tiree":
            self.hauteur -= self.vitesse
        
        if self.hauteur < 0:
            self.etat = "chargee"

    def toucher(self, boss):
        if (self.depart < boss.position + boss.image.get_width() and
            self.depart + self.image.get_width() > boss.position and
            self.hauteur < boss.hauteur + boss.image.get_height() and
            self.hauteur + self.image.get_height() > boss.hauteur):
            boss.toucher()
            return True
        return False

    def toucher(self, vaisseau):
        if (math.fabs(self.hauteur - vaisseau.hauteur) < 40) and (math.fabs(self.depart - vaisseau.depart) < 40):
            self.etat = "chargee"
            self.nb_kills += 1
            return True


class TirEnnemi:
    def __init__(self, ennemi):
        self.depart = ennemi.depart + 16
        self.hauteur = ennemi.hauteur + 40  # Position de départ
        # Charger et redimensionner l'image ici
        image_originale = pygame.image.load("bombe.png")
        self.image = pygame.transform.scale(image_originale, (50, 50)) # Ajuste la taille ici
        self.image = pygame.transform.rotate(self.image, 180)
        self.vitesse = 5  # Vitesse de tir

    def bouger(self):
        self.hauteur += self.vitesse  # Descend vers le joueur

    def toucher(self, joueur):
        if (math.fabs(self.hauteur - joueur.position) < 40) and (math.fabs(self.depart - joueur.position) < 40):
            joueur.perdrecoeur()
            return True
        return False


class Ennemi():
    NbEnnemis = 6
    
    def __init__(self):
        self.depart = random.randint(1, 700)
        self.hauteur = 10
        self.type = random.randint(1, 2)
        if (self.type == 1):
            self.image = pygame.image.load("invader1.png")
            self.vitesse = 2
        elif (self.type == 2):
            self.image = pygame.image.load("invader2.png")
            self.vitesse = 2
        self.tirs = []  # Liste pour les tirs de l'ennemi

    def avancer(self):
        self.hauteur += self.vitesse
    
    def disparaitre(self):
        self.depart = random.randint(1, 700)
        self.hauteur = 10
        self.type = random.randint(1, 2)
        if (self.type == 1):
            self.image = pygame.image.load("invader1.png") 
        elif (self.type == 2):
            self.image = pygame.image.load("invader2.png")

    def tirer(self):
        if random.randint(0, 1000) < 5:  # 5% de chance de tirer à chaque frame
            self.tirs.append(TirEnnemi(self))


class Boss:
    def __init__(self):
        image_originale = pygame.image.load('boss.png')
        self.image = pygame.transform.scale(image_originale, (100, 100))  
        self.position = 300  
        self.hauteur = 50    
        self.vitesse = 1     
        self.coins = 10  # Points de vie du boss

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

