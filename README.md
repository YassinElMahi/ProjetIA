# Projet 2025 – IA Kamisado – Python

## Description
Ce projet consiste à créer une IA qui peut jouer au jeu Kamisado via un serveur TCP. Le bot communique avec un serveur principal pour participer à des parties en réseau et joue automatiquement en choisissant intelligemment ses coups grâce à un algorithme Minimax avec élagage alpha-bêta.

## Le jeu Kamisado
Kamisado est un jeu de société stratégique sur un plateau 8x8 aux cases colorées. Chaque joueur dispose de 8 pièces de couleurs différentes. La particularité du jeu est que **la pièce à jouer est imposée** : elle correspond à la couleur de la case sur laquelle l'adversaire vient de poser sa pièce. Une pièce se déplace en ligne droite (tout droit, diagonale gauche ou droite) vers le camp adverse, sans pouvoir sauter par-dessus une autre pièce. Le premier joueur à atteindre la rangée adverse gagne la partie.

## Stratégie de l'IA

### Détection de l'équipe
Le bot détecte automatiquement s'il joue en `light` (rangée 0, va vers la rangée 7) ou en `dark` (rangée 7, va vers la rangée 0) en fonction de sa position dans la liste des joueurs reçue par le serveur.

### Directions de déplacement
Selon l'équipe, les directions possibles sont adaptées :
- `light` : tout droit vers le bas, diagonale bas-gauche, diagonale bas-droite
- `dark` : tout droit vers le haut, diagonale haut-gauche, diagonale haut-droite

### Minimax avec élagage alpha-bêta
Le bot utilise un algorithme Minimax à profondeur 3 pour choisir le meilleur coup. Il simule les coups à l'avance en alternant entre son tour (maximisation) et le tour adverse (minimisation), et utilise l'élagage alpha-bêta pour éviter d'explorer des branches inutiles et gagner en performance.

### Fonction d'évaluation
La fonction `evaluate` donne un score au plateau selon les critères suivants :
- **Avancement des pièces** : plus une pièce est avancée vers le camp adverse, plus le score est élevé (+10 par rangée)
- **Victoire instantanée** : si une pièce atteint la dernière rangée, le score est de +10000 (priorité absolue)
- **Avancement ennemi** : plus l'adversaire est avancé, plus le score est pénalisé (-10 par rangée)
- **Défaite instantanée** : si l'adversaire atteint la dernière rangée, le score est de -10000

## Fonctionnalités principales
- Connexion TCP au serveur du professeur et inscription automatique
- Réponse aux pings pour maintenir la connexion active
- Détection automatique de l'équipe (`light` ou `dark`)
- Calcul de tous les coups valides pour une pièce donnée
- Simulation d'état du plateau pour anticiper les coups futurs via `apply_move`
- Algorithme Minimax avec élagage alpha-bêta sur 3 niveaux de profondeur
- Communication JSON pour échanger les coups avec le serveur

## Bibliothèques utilisées
- `socket` : Pour la communication réseau TCP
- `json` : Pour sérialiser/désérialiser les messages échangés
- `struct` : Pour encoder la taille des messages en binaire
- `copy` : Pour simuler les coups sur des copies du plateau sans modifier l'état réel


## Auteur
[El Mahi Izikki, Yassin - 24115]
