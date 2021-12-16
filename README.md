# P10_DE-MATTEIS_Ludovic
Créez une API sécurisée RESTful en utilisant Django REST


## Installation du projet

### Téléchargement du projet depuis la source GitHub :

`
$ git clone https://github.com/Ldm3110/P10_DE-MATTEIS_Ludovic.git
`

### Rendez-vous dans le dossier du projet :

`
$ cd P10_DE-MATTEIS_ludovic
`

### Programmez l'environnement virtuel et activez-le :

`
$ python3 -m venv env
`

- puis

`
$ source env/bin/activate
`

### Installez les requirements :


- Tout d'abord accéder au dossier de l'API :

`
$ cd SoftDesk_API
`


- Puis :

`
$ pip install -r requirements.txt
`

## Connection de l'API

### Première connexion :

Avant de pouvoir utiliser l'API, vous devrez effectuer les migrations nécessaires afin de pouvoir activer celle-ci. Pour cela assurez-vous d'être dans le dossier SoftDesk_API et indiquez la commande suivante dans le terminal :

`
$ ./manage.py migrate

Une fois cette action effectuée vous pouvez démarrer l'API avec la commande suivante :

`
$ ./manage.py runserver

### Connexions suivantes :

A partir du moment où vous avez bien effectué les étapes du point précédent, vous n'avez rien d'autre à faire que démarrer l'API en tapant la commande suivante :

`
$ ./manage.py runserver


## Documentation POSTMAN de l'API

veuillez vous référer à la documentation à l'url suivante :

https://documenter.getpostman.com/view/18365116/UVR5s9xD
