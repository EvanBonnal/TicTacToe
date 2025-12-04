import os
import random

# Initialisation des variables
joueur_actuel = ""
tours = 0
jeu_fini = False # Une variable pour savoir si on doit arrêter
mode_jeu = 0
signe_ia = ""
difficulte = 0
choix = 0 # Valeur par défaut invalide
# Un tableau 3x3 vide
plateau = [
    [" ", " ", " "], # Ligne 0
    [" ", " ", " "], # Ligne 1
    [" ", " ", " "]  # Ligne 2
]

# Fonction pour afficher la grille de jeu
def afficher_grille(p):
    print("-------------")
    for ligne in p:
        # On prend chaque élément de la ligne et on met une barre " | " entre eux
        print("| " + " | ".join(ligne) + " |")
        print("-------------")

# Fonction pour vérifier la victoire
def verifier_victoire(plateau, symbole):
    # Lignes
    for ligne in plateau:
        if ligne[0] == ligne[1] == ligne[2] == symbole: return True
    # Colonnes
    for col in range(3):
        if plateau[0][col] == plateau[1][col] == plateau[2][col] == symbole: return True
    # Diagonales
    if plateau[0][0] == plateau[1][1] == plateau[2][2] == symbole: return True
    if plateau[0][2] == plateau[1][1] == plateau[2][0] == symbole: return True
    return False

# Fonction IA pour choisir une case aléatoire
def ordinateur(board, signe):
    cases_libres = []
    for i in range(9):
        ligne = i // 3
        colonne = i % 3
        if board[ligne][colonne] == " ":
            cases_libres.append(i)
    
    if not cases_libres:
        return False
        
    if difficulte == 1: # FACILE : coup aléatoire
        return random.choice(cases_libres)
    elif difficulte == 2: # NORMAL : 50% aléatoire, 50% bon coup
        if random.random() < 0.5:
            return random.choice(cases_libres)
        else:
            # Essayer de gagner
            for coup in cases_libres:
                ligne = coup // 3
                colonne = coup % 3
                board[ligne][colonne] = signe
                if verifier_victoire(board, signe):
                    board[ligne][colonne] = " "
                    return coup
                board[ligne][colonne] = " "
            # Sinon coup aléatoire
            return random.choice(cases_libres)
    elif difficulte == 3: # DIFFICILE : toujours le bon coup
        # Essayer de gagner
        for coup in cases_libres:
            ligne = coup // 3
            colonne = coup % 3
            board[ligne][colonne] = signe
            if verifier_victoire(board, signe):
                board[ligne][colonne] = " "
                return coup
            board[ligne][colonne] = " "
        # Bloquer l'adversaire
        adversaire = "O" if signe == "X" else "X"
        for coup in cases_libres:
            ligne = coup // 3
            colonne = coup % 3
            board[ligne][colonne] = adversaire
            if verifier_victoire(board, adversaire):
                board[ligne][colonne] = " "
                return coup
            board[ligne][colonne] = " "
        # Sinon coup aléatoire
        return random.choice(cases_libres)

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
while mode_jeu not in [1, 2]:
    try:
        mode_jeu = int(input("VS IA(1) ou vs J2(2): "))
        if mode_jeu not in [1, 2]:
            print("Erreur : Le chiffre doit être 1 ou 2.")
    except ValueError:
        print("veuiller choisir un mode de jeu valide. (1 ou 2)")
        continue

# Si mode IA, choix de la difficulté
if mode_jeu == 1:
    while difficulte not in [1, 2, 3]:
        try:
            difficulte = int(input("Difficulté IA : 1=Facile, 2=Normal, 3=Difficile : "))
            if difficulte not in [1, 2, 3]:
                print("Erreur : Le chiffre doit être 1, 2 ou 3.")
        except ValueError:
            print("Veuillez choisir une difficulté valide. (1, 2 ou 3)")
            continue

# Choix du symbole du joueur
while joueur_actuel not in ["X", "O"]:
    choix = input("Qui commence ? (Tapez X ou O) : ")
    joueur_actuel = choix.upper() # On convertit en majuscule
    
    if joueur_actuel not in ["X", "O"]:
        print("Symbole invalide, essayez encore.")

if mode_jeu == 1:
    if joueur_actuel == "X":
        signe_ia = "O"  # L'IA sera O
    else:
        signe_ia = "X"  # L'IA sera X

print(f"Parfait ! C'est le joueur {joueur_actuel} qui commence.")
while tours < 9 and not jeu_fini:
    nettoyer_ecran()
    afficher_grille(plateau)
    print(f"C'est au tour de : {joueur_actuel}")
    
    if mode_jeu == 1 and joueur_actuel == signe_ia:
        choix = ordinateur(plateau, joueur_actuel)
    
    # tour de l'utilisateur
    else:
        try:
            choix = int(input("Choisissez une case (0-8) : "))
        except ValueError:
            print("Erreur : Entrez un chiffre !")
            input("Appuyez sur Entrée pour continuer...")
            continue # On recommence la boucle
    # Vérification que le chiffre est bon
    if 0 <= choix <= 8:
        # Conversion
        ligne = choix // 3
        colonne = choix % 3

        # Est-ce que la case est libre ?
        if plateau[ligne][colonne] == " ":
            plateau[ligne][colonne] = joueur_actuel
            if verifier_victoire(plateau, joueur_actuel):
                    nettoyer_ecran()
                    afficher_grille(plateau)
                    if mode_jeu == 1 and joueur_actuel == signe_ia:
                        print(f"Dommage ! L'IA ({joueur_actuel}) a gagné !")
                    else:
                        print(f"BRAVO ! Le joueur {joueur_actuel} a gagné !")
                    jeu_fini = True    # Cela va arrêter la boucle while
            else:
                # Changement de joueur pour le tour suivant
                if joueur_actuel == "X":
                    joueur_actuel = "O"
                else:
                    joueur_actuel = "X"
            tours += 1 # On compte le tour validé
        else:
            print("Cette case est déjà prise. Réessayez une autre case.")
            input("Appuyez sur Entrée pour continuer...")
    else:
        print("Le chiffre doit être entre 0 et 8.Réessayez.")
        input("Appuyez sur Entrée pour continuer...")
if tours == 9 and not jeu_fini:
    nettoyer_ecran()
    afficher_grille(plateau)
    print("Fin de la partie (tableau plein) !")