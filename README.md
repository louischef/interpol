# Scraping d'Interpol

## Description
Ce projet vise à collecter et analyser des données sur les criminels recherchés dans le but d'en tirer des conclusions pertinentes. En s'appuyant sur le scraping et des outils de traduction, le script récupère les informations disponibles sur Interpol et les enregistre dans des fichiers JSON structurés pour une analyse approfondie.

## Technologies utilisées
- **Multithreading** : pour optimiser la vitesse de scraping en traitant plusieurs requêtes simultanément.
- **pycountry** : pour gérer les codes de pays et fournir des noms de pays en différentes langues.
- **API DeepL** : pour traduire certaines informations textuelles en français.
- **API Interpol** : pour accéder aux données de personnes recherchées.
- **JSON** : pour le stockage des données de manière structurée.
- **Proxy** : pour éviter les blocages en alternant les adresses IP lors des requêtes.

## Fonctionnalités principales
- **Scraping des données** : collecte des informations sur les individus recherchés, incluant nom, prénom, date de naissance, pays, nationalité, etc.
- **Stockage en JSON** : enregistre les données collectées dans un fichier JSON pour faciliter leur analyse et manipulation.
- **Utilisation de proxy** : permet de contourner les restrictions en changeant périodiquement d'adresse IP.

## Prérequis
Avant de pouvoir exécuter le projet, il est nécessaire d'installer les modules suivants :

- `requests`
- `pycountry`
- `json`

Vous pouvez installer ces modules avec la commande suivante :

```bash
pip install requests pycountry
```

## Installation

- **Clonez le dépôt sur votre machine**
```bash
git clone https://github.com/votre_nom_utilisateur/scraping-interpol.git
cd scraping-interpol
```

##  Utilisation

1. Lancez le script principal
```bash
python main.py
```
- Le script effacera automatiquement les fichiers links.txt et clean_links.txt au démarrage.
- Ensuite, il collectera les informations pour chaque pays en parallèle grâce au multithreading.
2. Les données des criminels recherchés seront enregistrées dans un fichier JSON dans le répertoire du projet.


## Exemple de sortie
Les données collectées incluent les informations suivantes :
- Nom
- Prénom
- Date de naissance (formatée en français)
- taille
- poids
- sexe
- motif de recherche
- Pays d'origine
- couleur de cheveux
- couleur des yeux
- Nationalités
- Langues parlées
- Description des signes distinctifs (si disponibles)


Ces informations sont structurées en JSON, ce qui permet une intégration facile avec des outils d'analyse comme PowerBI ou des bibliothèques Python de data science.

## Contribution
Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, corriger des bugs, ou ajouter de nouvelles fonctionnalités :
1. Forkez ce dépôt.
2. Créez une branche pour vos modifications: 
```bash
git checkout -b ma-nouvelle-fonctionnalite
```
3. Effectuez vos changements et commitez-les.
4. Poussez la branche et créez une Pull Request.

##Licence
Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, de le modifier et de le distribuer, tant que vous incluez la licence originale.
