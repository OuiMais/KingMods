"""
    Projet : KingMods
    Date Creation : 07/08/2023
    Date Revision : 10/08/2023
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Obtenir un document comportant tous les liens et noms des derniers mods ajoutés sur KingMods dans le but de générer un bot
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import datetime
# import csv
# import time

# Option for website (no screen open)
options = Options()
options.add_argument('--headless')

# Initiate the browser
browser = webdriver.Chrome(options=options)

tableauToPrint = ""
nbPage = 1
newDay = 0

while not newDay:
    print(nbPage)
    # on charge la page souhaitee
    url = "https://www.kingmods.net/fr/fs22/nouveaux-mods?page=" + str(nbPage)

    browser.get(url)

    # on recupere toutes les donnees a partir des lignes html
    linked = browser.find_elements(By.TAG_NAME, "a")

    dates = browser.find_elements(By.TAG_NAME, "time")

    # Une oage contient 12 mods
    for iteration in range(len(dates)):
        date = dates[iteration]
        links = linked[58 + iteration] # beaucoup de lignes permettant de naviguer sont presentes avant les mods

        dateStr = date.get_attribute("datetime") # date
        link = links.get_attribute("href") # lien du mod
        titreMod = links.get_attribute("title") # titre

        dateDatetime = datetime.datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%SZ") # utilisation de datetime pour
        # comparer des dates
        nowDateTime = datetime.date.today() # - timedelta(days=1)

        if dateDatetime.date() == nowDateTime:
            # preparation pour csv
            dataToAdd = titreMod + ";" + link + ";\n"
            tableauToPrint += dataToAdd
        else:
            newDay = 1

    nbPage += 1

browser.quit()

print(tableauToPrint)
