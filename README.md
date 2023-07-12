# genetic_car

## Description

Ce projet a été réalisé dans le cadre d’un stage au sein du laboratoire IETR à l’INSA de Rennes, dans l’équipe Vaader. Il a pour but de réaliser une application pouvant être utilisée pour expliquer le fonctionnement d’un algorithme génétique à un public allant des enfants aux adultes.

Dans l’application, on peut simuler des voitures qui tentent d’aller le plus loin possible sur un circuit en un temps donné. Au fil des générations, les voitures vont de plus en plus loin et de plus en plus vite. La simulation est complètement déterministe.

Il y a aussi la possibilité d’utiliser une caméra afin de capturer les valeurs de plusieurs dés colorés, qui permettent alors de générer une voiture avec des propriétés aléatoires. On peut alors comparer les performances d’une voiture choisie au hasard (ou non si on veut tricher) avec les performances des meilleures voitures obtenues grâce à l’algorithme génétique.


## Guide d’utilisation

Pour utiliser l’application, il est nécessaire d’installer plusieurs librairies. Vous pouvez les installer directement à l’aide de ces commandes :
```bash
pip install pygame
pip install opencv-python
pip install matplotlib
```
Assurez- vous d’avoir Python 3.8 installé sur votre machine. 
Si ce n’est pas le cas, vous pouvez l’installer ic : “https://www.python.org/downloads/release/python-380/”.
Vous pouvez ensuite lancer le programme avec la commande :

```bash
python3.8 main.py
```
