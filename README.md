
# kingMod

**kingMod** est un projet Python conçu pour automatiser la récupération et l'exportation d'un résumé des mods publiés la veille, sous forme de fichier Excel. Le projet inclut un dossier dédié à Raspberry Pi, qui permet de gérer l'extraction et l'envoi des informations par email. Il est également possible de filtrer les mods non encore vus par l'utilisateur.

## Structure du projet

```
kingMod/
│
├── raspberry_pi/
│   ├── kingMod.py        # Script pour automatiser la récupération des mods et l'envoi de résumés par email
│   ├── requirements.txt     # Liste des dépendances pour Raspberry Pi
│   ├── config.py            # Fichier de configuration contenant les informations d'email (à créer)
│
├── webinterface # Ajout d'un script Flask pour gérer les mods sur une interface minimaliste
│
├── main.py                  # Fichier principal avec les fonctions
│
└── requirements.txt         # Liste des dépendances pour l'ensemble du projet
```

## Fonctionnalités

1. **Raspberry Pi :**
   - Récupère les mods publiés la veille.
   - Envoie un résumé par email au format Excel avec les titres des mods et leurs liens.

2. **Fonctions dans `main.py` :**
   - `LastDayModResume()`: Extrait les mods publiés la veille.
   - `ModResumeWithLastModSave()`: Filtre et extrait les mods qui n'ont pas encore été vus par l'utilisateur.

## Installation Raspberry Pi

### Prérequis

- Python 3.7 ou supérieur
- Pip (gestionnaire de packages Python)

### Fichier `config.py`

Le fichier `config.py` est nécessaire pour stocker vos informations d'email :

```python
sender_email = "votre_email@example.com"
receiver_email = "destinataire@example.com"
password = "votre_mot_de_passe"
```

### Dépendances 

Assurez-vous d'installer les dépendances nécessaires avec :

```bash
pip install -r raspberry_pi/requirements.txt
```

## Usage

### Exécuter l'automatisation des mods

1. Lancez le script d'automatisation pour récupérer les mods et envoyer le résumé par email.

```bash
python PC/extractDataKingMod.py
```

## Installation 

### Prérequis

- Python 3.7 ou supérieur
- Pip (gestionnaire de packages Python)

### Dépendances 

Assurez-vous d'installer les dépendances nécessaires avec :

```bash
pip install -r requirements.txt
```

### Utilisation des fonctions dans `main.py`

Dans `main.py`, vous pouvez appeler les fonctions suivantes :

```python
from main import LastDayModResume, ModResumeWithLastModSave

# Récupère tous les mods de la veille
LastDayModResume()

# Récupère les mods qui n'ont pas encore été vus
ModResumeWithLastModSave()
```

## Contribution

Les contributions sont les bienvenues ! Si vous avez des suggestions ou des améliorations, n'hésitez pas à ouvrir une **issue**.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
