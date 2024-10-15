import pygame # importation de la librairie pygame
import space
import sys # pour fermer correctement l'application

# lancement des modules inclus dans pygame
pygame.init() 
clock = pygame.time.Clock()
f = pygame.font.Font(None, 36)
# création d'une fenêtre de 800 par 600
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders") 
# chargement de l'image de fond
fond = pygame.image.load('background.png')
def persocoeur():
    texte_score = f.render(f'coeur: {player.coeur}', True, (255, 255, 255))
    screen.blit(texte_score, (10,550))
# creation du joueur
player = space.Joueur()
# creation de la balle
tir = space.Balle(player)
tir.etat = "chargee"
# creation des ennemis
listeEnnemis = []
for indice in range(space.Ennemi.NbEnnemis):
    vaisseau = space.Ennemi()
    listeEnnemis.append(vaisseau)
    
victoire = False
f_victoire = pygame.font.Font(None,50)
def Niveau(n):
    message_victoire = f_victoire.render('Niveau '+str(n), True, (0, 255, 0))
    screen.blit(message_victoire, (650, 5))
    

    
### BOUCLE DE JEU  ###

running = True # variable pour laisser la fenêtre ouverte
niveau = 1
while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond,(0,0))
    text = f.render(f'Score: {player.score}', True, (255, 0, 0))
    screen.blit(text, (10, 10))
    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # running est sur False
            sys.exit() # pour fermer correctement
       
       # gestion du clavier
        if event.type == pygame.KEYDOWN : # si une touche a été tapée KEYUP quand on relache la touche
            if event.key == pygame.K_LEFT : # si la touche est la fleche gauche
                player.sens = "gauche" # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_RIGHT : # si la touche est la fleche droite
                player.sens = "droite" # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_SPACE : # espace pour tirer
                player.tirer()
                tir.etat = "tiree"

                
    persocoeur()
    ### Actualisation de la scene ###
    # Gestions des collisions
    
    for ennemi in listeEnnemis:
        if tir.toucher(ennemi):
            ennemi.disparaitre()
            player.marquer(ennemi.type)
                
    #print(f"Score = {player.score} points")
    # placement des objets
    # le joueur
    player.deplacer()
    screen.blit(player.image,[player.position,500]) # appel de la fonction qui dessine le vaisseau du joueur
    # la balle
    tir.bouger()
    screen.blit(tir.image,[tir.depart,tir.hauteur]) # appel de la fonction qui dessine la balle du joueur        
    # les ennemis
    for ennemi in listeEnnemis:
        ennemi.avancer()
        screen.blit(ennemi.image,[ennemi.depart, ennemi.hauteur]) # appel de la fonction qui dessine le vaisseau du joueur
    clock.tick(20)
    if player.score > 4:
        if niveau == 1:
            niveau = 2
            print("Niveau 2")
            for ennemi in listeEnnemis:
                ennemi.vitesse *= 1.5
                
    if player.score > 8:
        if niveau == 2:
            niveau = 3
            print("Niveau 3")
            for ennemi in listeEnnemis:
                ennemi.vitesse *= 1.8
                

    Niveau(niveau)

    pygame.display.update() # pour ajouter tout changement à l'écran
