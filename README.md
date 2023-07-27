# Démonstrateur d'algorithme génétique

Ce projet a été réalisé dans le cadre d’un stage au sein du laboratoire IETR à l’INSA de Rennes, dans l’équipe Vaader.
Il a pour but de réaliser une application pouvant être utilisée pour expliquer le fonctionnement d’un algorithme 
génétique à un public allant des enfants aux adultes.

Dans l’application, on peut simuler des voitures qui tentent d’aller le plus loin possible sur un circuit en un temps 
donné. Au fil des générations, les voitures vont de plus en plus loin et de plus en plus vite. La simulation est complètement déterministe.

Il y a aussi la possibilité d’utiliser une caméra afin de capturer les valeurs de plusieurs dés colorés, qui permettent
alors de générer une voiture avec des propriétés aléatoires. On peut alors comparer les performances d’une voiture 
choisie au hasard (ou non si on veut tricher) avec les performances de voitures obtenues grâce à 
l’algorithme génétique.



## Guide d’utilisation

Pour utiliser l’application, il est nécessaire d’installer plusieurs librairies. Vous pouvez les installer directement à l’aide de ces commandes :
```bash
pip install pygame
pip install opencv-python
pip install matplotlib
```
Assurez-vous d’avoir Python 3.8 installé sur votre machine. 
Si ce n’est pas le cas, vous pouvez l’installer ic : “https://www.python.org/downloads/release/python-380/”.
Vous pouvez ensuite lancer le programme dans le dossier src avec la commande :

```bash
python3.8 src/main.py
```

## Fonctionnalités

<p align="center">
  <img src="/images/menu.png" alt="Capture d'écran de l'application">
</p>

Après avoir lancé le programme, vous arrivez directement dans l'application. Le bouton tout en haut à gauche permet
d'ouvrir un menu permettant de modifier les paramètres de la simulation. Ces paramètres sont expliquées plus bas dans 
ce document.

Le bouton 'Garage' permet de voir toutes les voitures des générations précédentes, ainsi que les voitures capturées 
avec les dés. Ces voitures se sauvegardent lorsque l'on ferme l'application. (⚠️ Pour que cela fonctionne, il faut 
fermer la simulation avec la croix en haut à droite et non en forçant la fermeture du programme) Dans ce menu, vous 
pouvez sélectionner les voitures pour les faire rouler, ou bien les modifier (modification du nom,
de la couleur, des paramètres ou suppression de la voiture)

Le bouton 'Capter les dés' permet d'utiliser la caméra pour reconnaître le score des différents dés. Une fenêtre 
s'affiche  et on peut y voir les dés ainsi que les scores de chaque dé.

<p align="center">
  <img src="/images/dice.png" alt="Capture d'écran de la reconnaissance des dés">
</p>

Il faut attendre un peu que le score se stabilise, et lorsque c'est bon, on peut cliquer n'importe où pour quitter
cette fenêtre. Il y a alors la possibilité de modifier la valeur des dés en cas d'erreurs. Les dés à utiliser doivent
avoir des points blancs. Ces dés sont les suivants:
- un dé **rouge**
- un dé **noir**
- un dé **vert**
- un dé **orange**
- un dé **jaune**
- un dé **jaune foncé** (avec des points noirs)

⚠️ Il est possible que la caméra ne soit pas reconnu. Dans ce cas, il faut modifier la valeur de la variable 
'NUM_CAMERA' dans le fichier 'src/other/camera.py', en mettant 1 ou 2 par exemple.

Ensuite, d'autres boutons sont présent en haut à droite de l'écran. Ils servent à changer le circuit, changer le nombre
de voitures, lancer la simulation, arrêter la simulation, mettre en pause, recommencer la dernière génération, ou 
passer à la génération suivante.

On peut aussi cliquer directement sur les voitures pour afficher leurs paramètres ainsi que leur champ de vision.

### Paramètres de la simulation

Les paramètres pouvant être modifiés sont les suivants :
- **Paramètres généraux** :
  - **FPS** : le nombre d'images par seconde, cela permet d'accélerer ou de ralentir la simulation (sans impact sur le
  résultat final)
  - **Seed** : la graine utilisée pour générer les voitures (si on utilise la même seed sur le même circuit, on obtiendra
  toujours le même résultat)
- **Paramètres d'affichage :**
  - **Champs de vision** : pour afficher les cônes de détections utilisés par les voitures
  - **Explosions** : pour afficher des explosions lorsqu'une voiture touche un mur
  - **Checkpoints** : pour afficher les checkpoints
- **Paramètres des voitures :**
  - **Vitesse maximale** : pour modifier la vitesse maximale des voitures
  - **Angle de rotation** : pour modifier l'angle de rotation des voitures
  - **Accélération** : pour modifier la puissance de l'accélération des voitures
  - **Freinage** : pour modifier la puissance de freinage des voitures
  - **Coef drift** : pour modifier le coefficient de drift des voitures (un coeficient plus élevé fait glisser les
  voitures)
- **Paramètres de l'algorithme génétique :**
  - **Proportion conservée** : pour modifier la proportion de voitures conservées à l'identique lors de la sélection
  naturelle
  - **Chance croisement** : pour modifier la chance de croiser des voitures (plus la valeur est élevée, plus les voitures
  ont de chance d'échanger leurs caractéristiques)
  - **Chance mutation** : pour modifier la chance de mutation des voitures (plus la valeur est élevée, plus les voitures
  ont de chance de muter)
  - **Temps / Génération** : pour modifier le temps de la simulation pour une génération (en secondes)
- **Paramètres des cônes de vision :**
  - **Largeur** : pour modifier la largeur du champ de vision des voitures
  - **Longueur** : pour modifier la longueur du champ de vision des voitures


## Explications des paramètres des voitures :

Le système de contrôle se base sur le champ de vision des voitures. Les différents véhicules ont tous les mêmes 
caractéristiques de base : taille, accélération, vitesse maximale, force du freinage… La seule différence est le 
champ de vision du pilote, représenté par un cône. Un cône peut être représenté avec deux dés : un dé pour la largeur
du cône, et un dé pour la longueur du cône. Les valeurs des dés indiquent la taille du cône.

<p align="center">
  <img src="/images/cones.png" alt="Exemple de cônes de détection">
</p>

Selon la vitesse à laquelle roule la voiture, le pilote n’a pas forcément le même champ de vision. C’est par 
exemple le cas dans la réalité, avec un champ de vision qui a tendance à se rétrécir au fur et à mesure que la 
vitesse augmente. Nous retrouvons cela avec les voitures de la simulation, qui possèdent 3 champs de vision différents 
en fonction de leur vitesse actuelle. Selon la vitesse, il faut donc utiliser le bon cône de vision. Nous pouvons 
par exemple imaginer 3 champs de visions différents pour 3 zones de vitesses différentes :
- Vitesse lente : Moins de 50 km/h
- Vitesse moyenne : Entre 50 et 100 km/h
- Vitesse rapide : Plus de 100 km/h

C’est le même principe pour les voitures de la simulation, avec bien sûr des unités de vitesse différentes. Chaque 
cône de vision étant représenté par deux dés, il faut 6 dés au total pour représenter nos voitures. Cela fait 
donc 46 656 possibilités de voitures différentes.

La voiture utilise ensuite son cône pour se déplacer. À chaque pas de simulation, la voiture détecte les murs et 
agit en conséquence. Tout d’abord, elle regarde si elle détecte un mur en face d’elle dans le cône de vision. Si
c’est le cas, elle freine, sinon, elle accélère. Elle regarde ensuite s’il y a un mur qui coupe le champ de vision. 
S’il y a un mur à gauche, elle tourne à droite et inversement. S’il y a un mur de chaque côté, la voiture regarde 
quel mur est le plus proche et tourne de telle sorte à s’en éloigner.


## Organisation des fichiers

- **data** : contient des données utiles lors de la simulation ainsi que les résultats de différents tests
    - **checkpoints** : contient les coordonnées des checkpoints pour chaque circuit
    - **tests** : contient les résultats des différents tests (des résultats concernant le nombre de voitures pouvant 
faire le tour de chaque circuit se trouvent dans le dossier 'data/tests/all_cars/analysis')
    - **cars** : contient les voitures sauvegardées
    - **parameters** : contient les paramètres de la simulation pour chaque circuit, modifiables facilement
  

- **images** : contient les images utilisées dans l'application


- **src** : contient le code source de l'application
    - **data**: contient les classes permettant de gérer les données
    - **game**: contient les classes permettant de gérer la simulation
    - **menus**: contient les classes permettant de gérer les menus
    - **render**: contient les classes permettant de gérer l'affichage
    - **other**: contient les classes permettant de gérer les autres fonctionnalités