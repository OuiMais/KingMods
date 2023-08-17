"""
    Projet : KingMods
    Date Creation : 07/08/2023
    Date Revision : 16/08/2023
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Obtenir un document comportant tous les liens et noms des derniers mods ajoutés sur KingMods dans le but de générer un bot
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import datetime
import time
# import csv

# Option for website (no screen open)
options = Options()
options.add_argument('--headless')

# Initiate the browser
browser = webdriver.Chrome(options=options)

""" 
    Cette partie permet de savoir si un nouveau mod vient de sortir
"""
import keyboard

previousTitle = ""
timeBetweenRefresh = 10.0
programmRun = 1

while programmRun:
    url = "https://www.kingmods.net/fr/fs22/nouveaux-mod"

    browser.get(url)

    # on recupere toutes les donnees a partir des lignes html
    linked = browser.find_elements(By.TAG_NAME, "a")

    links = linked[58] # beaucoup de lignes permettant de naviguer sont presentes avant les mods

    link = links.get_attribute("href") # lien du mod
    titreMod = links.get_attribute("title") # titre

    if titreMod != previousTitle:
        print("We have a new mod on KingsMod : %s at the link %s" % (titreMod, link))
        previousTitle = titreMod

    browser.quit()
    time.sleep(timeBetweenRefresh)

    if keyboard.is_pressed("esc") or time.time() % 86400 != 0:
        # si on interrompt le programme avec la touche échap, on arrête tout, sinon c'est qu'il est minuit donc on
        # fait un bilan de la journée
        programmRun = 0

        """ 
            Cette partie permet de connaître le nombre de nouveaux mod de la veille et d'obtenir un fichier avec le nom 
            et le lien de chaque mod
        """

        if time.time() % 86400 == 0:
            time.sleep(1.0)
            tableauToPrint = ""
            nbPage = 1
            newDay = 0
            numberOfModsYesterday = 0

            while not newDay:
                print(nbPage)
                # on charge la page souhaitee
                url = "https://www.kingmods.net/fr/fs22/nouveaux-mods?page=" + str(nbPage)

                browser.get(url)

                # on recupere toutes les donnees a partir des lignes html
                linked = browser.find_elements(By.TAG_NAME, "a")

                dates = browser.find_elements(By.TAG_NAME, "time")

                # Une page contient 12 mods
                for iteration in range(len(dates)):
                    date = dates[iteration]
                    links = linked[
                        58 + iteration]  # beaucoup de lignes permettant de naviguer sont presentes avant les mods

                    dateStr = date.get_attribute("datetime")  # date
                    link = links.get_attribute("href")  # lien du mod
                    titreMod = links.get_attribute("title")  # titre

                    dateDatetime = datetime.datetime.strptime(dateStr,
                                                              "%Y-%m-%dT%H:%M:%SZ")  # utilisation de datetime pour
                    # comparer des dates
                    nowDateTime = datetime.date.today()
                    yesterdayDateTime = nowDateTime - datetime.timedelta(days=1)

                    if dateDatetime.date() == nowDateTime:
                        pass
                    elif dateDatetime.date() == yesterdayDateTime:
                        # preparation pour csv
                        dataToAdd = titreMod + ";" + link + ";\n"
                        tableauToPrint += dataToAdd
                        numberOfModsYesterday += 1
                    else:
                        newDay = 1

                nbPage += 1

            browser.quit()

            print(tableauToPrint)
            print("%s Mods add yesterday!!" % numberOfModsYesterday)
            programmRun = 1

"""
    To add: 
        - Faire un bot qui envoie les messages de nouveau mods et le récapitulatif
        - Mettre les mods dans un fichier csv pour faciliter la lecture
        - 
"""
