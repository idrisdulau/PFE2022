# AnaPost
Projet d'analyse de la posture par Apprentissage profond

Ce projet, via un réseau de neurones, avec l’utilisation de données sur la posture issues de vidéos de patients en rééducation lors de l’exécution d’exercices, et par l’extraction des caractéristiques posturales telles que les positions des articulations dans l’espace ou les orientations de ces articulations dans l’espace, devra permettre de déterminer la bonne ou la mauvaise exécution d’un mouvement.

## Table des matières
* [Execution avec UI-PRMD](#utilisation-avec-ui-prmd-sur-environnement-linux-personnel)
* [Execution avec Kinetics](#utilisation-avec-kinetics-sur-environnement-linux-personnel)

## Utilisation avec UI-PRMD sur environnement Linux personnel

**Prérequis : Python version >= 3.9**

#### Installation
*Installe les bibliothèques nécessaires au bon fonctionnement du projet :*

```
/Anapost$ python3 install.py
```

#### Création
*Crée les dossiers nécessaires au bon fonctionnement du projet :*

```
/Anapost$ mkdir DB
/Anapost/code$ mkdir checkpoints
/Anapost/code$ mkdir checkpoints/prova20
/Anapost/code$ mkdir checkpoints/cm
/Anapost/code$ mkdir checkpoints/plots
```

#### Positionnement
*Positionne les données UI-PRMD au bon endroit :*

* Accéder au site : https://webpages.uidaho.edu/ui-prmd/
* Télécharger les bases de données nommées : Movements (258 MB) et Incorrect Movements (265 MB)
    * Dans *Movements/Kinect/* renommer le dossier *Positions/* en *correctPositions/*
        * Placer ce dossier dans *AnaPost/DB*
    * Dans *Incorrect_Movements/Kinect/* renommer le dossier *Positions/* en *incorrectPositions/*
        * Placer ce dossier dans *AnaPost/DB*

#### Formatage
*Formate les données UI-PRMD :*
```
/AnaPost/toolsDB$ python3 uiprmdFormatAndSplit.py [split_rate]
```
**Exemple,** vous souhaiter obtenir une répartition des données de 85% d'entraînement et donc 15% de validation :
```
/AnaPost/toolsDB$ python3 uiprmdFormatAndSplit.py 85
```

#### Génération
*Génère les données d'entrée du réseau via les données précédemment formatées :*

```
/AnaPost/toolsDB$ python3 uiprmdGendata.py
```

#### Execution
*Execute le programme en utilisant les données précedemment générées :*

```
/AnaPost/code$ python3 main.py
```

## Utilisation avec Kinetics sur environnement Linux personnel

**Prérequis : Python version >= 3.9**

#### Installation
*Installe les bibliothèques nécessaires au bon fonctionnement du projet :*

```
/Kin$ python3 install.py
```

#### Création
*Crée les dossiers nécessaires au bon fonctionnement du projet :*

```
/Kin/code$ mkdir kinetics
/Kin/code$ mkdir checkpoints
/Kin/code$ mkdir checkpoints/prova20
/Kin/code$ mkdir checkpoints/cm
```

#### Positionnement
*Positionne les données Kinetics au bon endroit :*

* Télécharger la base de données depuis : https://drive.google.com/file/d/1PvIM_FjDRVSKh_kRDiWBpKkNNp3fUH3o/view?usp=sharing
    * Extraire l'archive *kinetics-skeleton.zip*
    * Placer le dossier *kinetics-skeleton/* dans *Kin/code/kinetics/*

#### Génération
*Génère les données d'entrée du réseau :*

```
/Kin/code$ python3 kinetics_gendata.py
```

#### Execution
*Execute le programme en utilisant les données précedemment générées :*

```
/Kin/code$ python3 main.py
```
