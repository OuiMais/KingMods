"""
    Projet : KingMods/configJson
    Date Creation : 28/01/2025
    Date Revision : 28/01/2025
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : fichier pour centraliser les données json
"""
import json
import os

# Fichiers pour stocker les données
DOWNLOADED_MODS_JSON_FILE = "download_mods.json"
NEW_MODS_JSON_FILE = "new_mods.json"

# Initialiser les fichiers si besoin
for file in [DOWNLOADED_MODS_JSON_FILE, NEW_MODS_JSON_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

def load_data(json_filepath):
    with open(json_filepath, "r") as jsonFile:
        return json.load(jsonFile)

def save_data(json_filepath, data):
    with open(json_filepath, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)