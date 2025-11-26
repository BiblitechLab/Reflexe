🎮 Reflexe

Un jeu ultra-nerveux en Python/Pygame, pensé pour tester tes réflexes et exploser tes limites.
Écrit en un seul fichier monstrueux de 3192 lignes, full fait-maison.

✨ Features principales

Gameplay rapide et punitif : t’es dedans ou t’es mort.

Skins personnalisés (couleurs, formes, effets).

Mode Comfort pour réduire les flashes / secousses.

SFX dynamiques proches/distance + death effect.

Musique intégrée avec gestion du fade et des fallback.

IA expérimentale qui joue à ta place (test de comportements).

Système de difficulté dynamique basé sur ta performance.

Trail system ultra fluide.

Obstacles générés intelligemment avec variation pseudo-aléatoire.

Score, best score, runs…

Mode custom (spécifiez la longueur du monde, etc.)

Tout ça en Pygame 2 dans un seul fichier brut.

🔥 Pour les devs

Code 100 % Python (3k+ lignes, split naturellement en blocs logiques).

Aucune dépendance externe en dehors de Pygame.

Gestion audio robuste (fallback .mp3 → .wav).

Architecture basée sur une game-loop propre avec update & draw séparés.

Système d’effets (trail, spark, invulnerability, dash) optimisé.

AI-mode plug’n’play via self.ai_enabled.

🚀 Installation

Assure-toi d’avoir Python 3.9+ et Pygame :

pip install pygame


Clone le repo :

git clone https://github.com/BiblitechLab/Reflexe
cd Reflexe


Lance le jeu :

python Reflexe.py
