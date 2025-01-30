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
DOWNLOADED_MODS_JSON_FILE = "/home/PyServer/Desktop/KingMod/download_mods.json"
NEW_MODS_JSON_FILE = "/home/PyServer/Desktop/KingMod/new_mods.json"

# Initialiser les fichiers si besoin
for file in [DOWNLOADED_MODS_JSON_FILE, NEW_MODS_JSON_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

def load_data(json_filepath):
    jsonFile = open(json_filepath, "r+")
    value = json.load(jsonFile)
    jsonFile.close()
    return value

def save_data(json_filepath, data):
    jsonFile = open(json_filepath, "w")
    json.dump(data, jsonFile, indent=4)
    jsonFile.close()