
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
boss = None  # Le boss sera créé lorsque le joueur atteint un certain niveau
# chargement de l'image de fond
fond = pygame.image.load('background.png')
def persocoeur():
    texte_score = f.render(f'coeur: {player.coeur}', True, (255, 255, 255))
    screen.blit(texte_score, (10,550))
    
def afficher_points_de_vie_boss():
    if boss:
        texte_pv_boss = f.render(f'Boss: {boss.coins} PV', True, (255, 0, 0))
        screen.blit(texte_pv_boss, (650, 550))  # Position du texte sur l'écran
    

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
while running:  # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond, (0, 0))
    text = f.render(f'Score: {player.score}', True, (255, 0, 0))
    screen.blit(text, (10, 10))

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.sens = "gauche"
            if event.key == pygame.K_RIGHT:
                player.sens = "droite"
            if event.key == pygame.K_SPACE:
                player.tirer()
                tir.etat = "tiree"

    if boss:  # Si le boss existe
        boss.avancer()  # Déplace le boss
        screen.blit(boss.image, [boss.position, boss.hauteur])  # Dessine le boss

        # Vérifie si le tir touche le boss
        if tir.toucher(boss):
            print("Le boss a été touché ! PV restants :", boss.coins)  # Affiche les PV restants
            boss.toucher()  # Appelle la méthode pour réduire les PV du boss
            
            # Vérifie si le boss est vaincu
            if boss.est_vaincu():
                print("Le boss est vaincu !")
                boss = None  # Supprime le boss après avoir été vaincu
                player.score += 5  # Bonus de score

    persocoeur()
    afficher_points_de_vie_boss()

    # Gestions des collisions
    for ennemi in listeEnnemis:
        if tir.toucher(ennemi):
            ennemi.disparaitre()
            player.marquer(ennemi.type)

    # placement des objets
    player.deplacer()
    screen.blit(player.image, [player.position, 500])  # Vaisseau du joueur
    tir.bouger()
    screen.blit(tir.image, [tir.depart, tir.hauteur])  # Balle du joueur
    for ennemi in listeEnnemis:
        ennemi.avancer()
        screen.blit(ennemi.image, [ennemi.depart, ennemi.hauteur])  # Ennemis

    clock.tick(20)

    if player.score > 4 and niveau == 1:
        niveau = 2
        print("Niveau 2")
        for ennemi in listeEnnemis:
            ennemi.vitesse *= 1.5
    
    if player.score > 8 and niveau == 2:
        niveau = 3
        print("Niveau 3")
        for ennemi in listeEnnemis:
            ennemi.vitesse *= 1.8
            
    if player.score > 12 and boss is None:  # Le boss apparaît quand le score dépasse 12
        boss = space.Boss()
        print("Boss apparaît !")

    Niveau(niveau)
    pygame.display.update()  # Pour ajouter tout changement à l'écran

