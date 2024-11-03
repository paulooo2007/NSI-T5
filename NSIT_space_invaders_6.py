import pygame  # importation de la librairie pygame
import space
import sys  # pour fermer correctement l'application

# lancement des modules inclus dans pygame
pygame.init()
clock = pygame.time.Clock()
f = pygame.font.Font(None, 36)

# création d'une fenêtre de 800 par 600
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Chargement des images de fond pour chaque niveau et pour le menu
try:
    fonds = [
        pygame.transform.scale(pygame.image.load('background.png'), (800, 600)),
        pygame.transform.scale(pygame.image.load('niveau1.png'), (800, 600)),
        pygame.transform.scale(pygame.image.load('niveau2.png'), (800, 600)),
    ]
    menu_background = pygame.transform.scale(pygame.image.load('galaxy.png'), (800, 600))  # Image de fond pour le menu
except pygame.error as e:
    print(f"Erreur de chargement de l'image : {e}")

def afficher_menu():
    while True:
        screen.blit(menu_background, (0, 0))  # Dessiner le fond du menu
        title_text = f.render('Space Invaders', True, (255, 255, 255))
        start_text = f.render('Appuyer sur ENTER pour commencer', True, (255, 255, 255))
        quit_text = f.render('Appuyer sur ESC pour quitter', True, (255, 255, 255))
        
        screen.blit(title_text, (300, 200))
        screen.blit(start_text, (250, 300))
        screen.blit(quit_text, (250, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Démarre le jeu
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def persocoeur():
    texte_score = f.render(f'coeur: {player.coeur}', True, (255, 255, 255))
    screen.blit(texte_score, (10, 550))

def afficher_points_de_vie_boss():
    global boss  # Déclarer boss comme une variable globale
    if boss:
        texte_pv_boss = f.render(f'Boss: {boss.coins} PV', True, (255, 0, 0))
        screen.blit(texte_pv_boss, (650, 550))  # Position du texte sur l'écran

# Création du joueur
player = space.Joueur()
# Création de la balle
tir = space.Balle(player)
tir.etat = "chargee"
# Création des ennemis
listeEnnemis = [space.Ennemi() for _ in range(space.Ennemi.NbEnnemis)]

victoire = False
f_victoire = pygame.font.Font(None, 50)

def Niveau(n):
    message_victoire = f_victoire.render('Niveau ' + str(n), True, (0, 255, 0))
    screen.blit(message_victoire, (650, 5))

### BOUCLE DE JEU ###

def jouer():
    global boss
    running = True
    niveau = 1
    boss = None
    paused = False  # Variable to track if the game is paused

    while running:
        # Dessin du fond
        if niveau - 1 < len(fonds):
            screen.blit(fonds[niveau - 1], (0, 0))
        else:
            print("Niveau hors limites.")

        # Affichage du score
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
                if event.key == pygame.K_p:  # Toggle pause with 'P' key
                    paused = not paused

        if paused:
            # Afficher un message de pause
            pause_text = f.render('Jeu en pause. Appuyez sur P pour continuer.', True, (255, 255, 255))
            screen.blit(pause_text, (200, 300))
        else:
            # Si le boss existe
            if boss:
                boss.avancer()  # Déplace le boss
                screen.blit(boss.image, [boss.position, boss.hauteur])  # Dessine le boss

                # Vérifie si le tir touche le boss
                if tir.toucher(boss):
                    print("Le boss a été touché ! PV restants :", boss.coins)
                    boss.toucher()
                    # Vérifie si le boss est vaincu
                    if boss.est_vaincu():
                        print("Le boss est vaincu !")
                        boss = None
                        player.score += 5  # Bonus de score

            persocoeur()
            afficher_points_de_vie_boss()

            # Gestion des tirs ennemis
            for ennemi in listeEnnemis:
                ennemi.tirer()  # Les ennemis tirent
                for tir_ennemi in ennemi.tirs:
                    tir_ennemi.bouger()  # Met à jour la position des tirs ennemis
                    if tir_ennemi.toucher(player):  # Vérifie si un tir touche le joueur
                        player.perdrecoeur()
                        print(f"Le joueur a été touché ! Vies restantes : {player.coeur}")

            # Gestion des collisions avec les tirs ennemis
            for ennemi in listeEnnemis:
                if tir.toucher(ennemi):
                    ennemi.disparaitre()
                    player.marquer(ennemi.type)

            # Placement des objets
            player.deplacer()
            screen.blit(player.image, [player.position, 500])  # Vaisseau du joueur
            tir.bouger()
            screen.blit(tir.image, [tir.depart, tir.hauteur])  # Balle du joueur
            for ennemi in listeEnnemis:
                ennemi.avancer()
                screen.blit(ennemi.image, [ennemi.depart, ennemi.hauteur])  # Ennemis
                for tir_ennemi in ennemi.tirs:
                    screen.blit(tir_ennemi.image, (tir_ennemi.depart, tir_ennemi.hauteur))  # Tirs ennemis

            # Changement de niveau
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
        clock.tick(20)

# Affichage du menu
afficher_menu()
# Lancement du jeu
jouer()
