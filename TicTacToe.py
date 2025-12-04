import os
import random

# Initialisation des variables
current_player = ""
round = 0
end_game = False # Une variable pour savoir si on doit arrêter
gamemode = 0
signe_ia = ""
difficulte = 0
# Un tableau 3x3 vide
board = [
    [" ", " ", " "], # Ligne 0
    [" ", " ", " "], # Ligne 1
    [" ", " ", " "]  # Ligne 2
]

# Fonction pour afficher la grille de jeu
def afficher_grille(p):
    print("-------------")
    for line in p:
        # On prend chaque élément de la ligne et on met une barre " | " entre eux
        print("| " + " | ".join(line) + " |")
        print("-------------")

# Fonction pour vérifier la victoire
def verifier_victoire(board, symbole):
    # Lignes
    for line in board:
        if line[0] == line[1] == line[2] == symbole: return True
    # Colonnes
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == symbole: return True
    # Diagonales
    if board[0][0] == board[1][1] == board[2][2] == symbole: return True
    if board[0][2] == board[1][1] == board[2][0] == symbole: return True
    return False

# Fonction IA pour choisir une case aléatoire
def ordinateur(board, signe):
    free_box = []
    for i in range(9):
        line = i // 3
        column = i % 3
        if board[line][column] == " ":
            free_box.append(i)
    
    if not free_box:
        return False
        
    if difficulte == 1: # FACILE : coup aléatoire
        return random.choice(free_box)
    elif difficulte == 2: # NORMAL : 50% aléatoire, 50% bon coup
        if random.random() < 0.5:
            return random.choice(free_box)
        else:
            # Essayer de gagner
            for coup in free_box:
                line = coup // 3
                column = coup % 3
                board[line][column] = signe
                if verifier_victoire(board, signe):
                    board[line][column] = " "
                    return coup
                board[line][column] = " "
            # Sinon coup aléatoire
            return random.choice(free_box)
    elif difficulte == 3: # DIFFICILE : toujours le bon coup
        # Essayer de gagner
        for coup in free_box:
            line = coup // 3
            column = coup % 3
            board[line][column] = signe
            if verifier_victoire(board, signe):
                board[line][column] = " "
                return coup
            board[line][column] = " "
        # Bloquer l'adversaire
        adversaire = "O" if signe == "X" else "X"
        for coup in free_box:
            line = coup // 3
            column = coup % 3
            board[line][column] = adversaire
            if verifier_victoire(board, adversaire):
                board[line][column] = " "
                return coup
            board[line][column] = " "
        # Sinon coup aléatoire
        return random.choice(free_box)

# Fonction pour nettoyer l'écran
def nettoyer_ecran():
    #Efface le contenu de la console
    if os.name == 'nt':
        os.system('cls') # Pour Windows
    else:
        os.system('clear') # Pour Linux et MacOS

# debut du jeu
print("Bienvenue dans le jeu du Morpion !")

# Choix du mode de jeu
while gamemode not in [1, 2]:
    try:
        gamemode = int(input("VS IA(1) ou vs J2(2): "))
        if gamemode not in [1, 2]:
            print("Erreur : Le chiffre doit être 1 ou 2.")
    except ValueError:
        print("veuiller choisir un mode de jeu valide. (1 ou 2)")
        continue

# Si mode IA, choix de la difficulté
if gamemode == 1:
    while difficulte not in [1, 2, 3]:
        try:
            difficulte = int(input("Difficulté IA : 1=Facile, 2=Normal, 3=Difficile : "))
            if difficulte not in [1, 2, 3]:
                print("Erreur : Le chiffre doit être 1, 2 ou 3.")
        except ValueError:
            print("Veuillez choisir une difficulté valide. (1, 2 ou 3)")
            continue

# Choix du symbole du joueur
while current_player not in ["X", "O"]:
    choice = input("Qui commence ? (Tapez X ou O) : ")
    current_player = choice.upper() # On convertit en majuscule
    
    if current_player not in ["X", "O"]:
        print("Symbole invalide, essayez encore.")

if gamemode == 1:
    if current_player == "X":
        signe_ia = "O"  # L'IA sera O
    else:
        signe_ia = "X"  # L'IA sera X

print(f"Parfait ! C'est le joueur {current_player} qui commence.")
while round < 9 and not end_game:
    nettoyer_ecran()
    afficher_grille(board)
    print(f"C'est au tour de : {current_player}")
    
    if gamemode == 1 and current_player == signe_ia:
        choice = ordinateur(board, current_player)
    
    # tour de l'utilisateur
    else:
        try:
            choice = int(input("Choisissez une case (0-8) : "))
        except ValueError:
            print("Erreur : Entrez un chiffre !")
            input("Appuyez sur Entrée pour continuer...")
            continue # On recommence la boucle
    # Vérification que le chiffre est bon
    if 0 <= choice <= 8:
        # Conversion
        line = choice // 3
        column = choice % 3

        # Est-ce que la case est libre ?
        if board[line][column] == " ":
            board[line][column] = current_player
            if verifier_victoire(board, current_player):
                    nettoyer_ecran()
                    afficher_grille(board)
                    if gamemode == 1 and current_player == signe_ia:
                        print(f"Dommage ! L'IA ({current_player}) a gagné !")
                    else:
                        print(f"BRAVO ! Le joueur {current_player} a gagné !")
                    end_game = True    # Cela va arrêter la boucle while
            else:
                # Changement de joueur pour le tour suivant
                if current_player == "X":
                    current_player = "O"
                else:
                    current_player = "X"
            round += 1 # On compte le tour validé
        else:
            print("Cette case est déjà prise. Réessayez une autre case.")
            input("Appuyez sur Entrée pour continuer...")
    else:
        print("Le chiffre doit être entre 0 et 8.Réessayez.")
        input("Appuyez sur Entrée pour continuer...")
if round == 9 and not end_game:
    nettoyer_ecran()
    afficher_grille(board)
    print("Fin de la partie (tableau plein) !")