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

    url = "https://www.kingmods.net/fr/fs22/nouveaux-mods?page=" + str(nbPage)

    browser.get(url)

    titre = browser.find_elements(By.TAG_NAME, "a")

    linked = browser.find_elements(By.TAG_NAME, "a")

    dates = browser.find_elements(By.TAG_NAME, "time")

    for iteration in range(len(dates)):
        date = dates[iteration]
        links = linked[58 + iteration]

        dateStr = date.get_attribute("datetime")
        link = links.get_attribute("href")
        titreMod = links.get_attribute("title")

        dateDatetime = datetime.datetime.strptime(dateStr, "%Y-%m-%dT%H:%M:%SZ")
        nowDateTime = datetime.date.today()
        if dateDatetime.date() == nowDateTime:
            dataToAdd = titreMod + ";" + link + ";\n"
            tableauToPrint += dataToAdd
        else:
            newDay = 1

    nbPage += 1

browser.quit()

print(tableauToPrint)
