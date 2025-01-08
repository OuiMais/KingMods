"""
    Projet : KingMods
    Date Creation : 07/08/2023
    Date Revision : 08/01/2025
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Obtenir un document comportant tous les liens et noms des derniers mods ajoutés sur KingMods dans le but de générer un bot
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec

import datetime
import time
import csv

from selenium.webdriver.support.wait import WebDriverWait
import io
from PIL import Image

# Option for website (no screen open)
options = Options()
# options.add_argument('--headless')

previousTitle = "US Farmer"
url = "https://www.kingmods.net/fr/fs25/nouveaux-mods"

# Set time between data refresh
hoursRefresh = 0
minutesRefresh = 30
secondsRefresh = 0
timeBetweenRefresh = 3600 * hoursRefresh + 60 * minutesRefresh + secondsRefresh

modTitleAndLink = []
pageModArray = []

findPrevious = 0
page = 1

# Initiate the browser
browser = webdriver.Chrome(options=options)
browserImage = webdriver.Chrome(options=options)
# Open website
browser.get(url)

while not findPrevious:
    # Save ul data
    pageModList = browser.find_element(By.XPATH, "//ul[@class='w-full grid gap-20 grid-cols-2']")

    lastPageMod = pageModList.find_elements(By.TAG_NAME, 'a')

    for mod in lastPageMod:
        test = mod.find_element(By.TAG_NAME, 'img')
        img = test.get_attribute('src')
        browserImage.get(img)
        ima = browserImage.find_element(By.TAG_NAME, 'img').screenshot_as_png

        image = Image.open(io.BytesIO(ima))
        image.show()

        try:
            # Check if badge update is display
            badge = mod.find_element(By.XPATH, ".//div[contains(@class, 'bg-blue')]")
            updateMod = badge.is_displayed()
        except NoSuchElementException:
            updateMod = False

        title = mod.get_attribute("title")
        link = mod.get_attribute("href")

        if title != previousTitle:
            pageModArray.append([title, link, updateMod])
        else:
            modTitleAndLink += pageModArray
            previousTitle = title
            findPrevious = 1
            break

    page += 1
    url = "https://www.kingmods.net/fr/fs25/nouveaux-mods?page=" + str(page)

    browser.get(url)

browser.close()

filteredMod = []
seen = set()

for mod in modTitleAndLink:
    key = (mod[0], mod[1])
    if key not in seen:
        seen.add(key)
        filteredMod.append(mod)

newModCsv = open("NewModResume.csv", 'w', newline='', encoding='utf-8')
updateModCsv = open("NewModResume.csv", 'w', newline='', encoding='utf-8')

newWriter = csv.writer(newModCsv, delimiter=";")
updateWriter = csv.writer(updateModCsv, delimiter=";")

newWriter.writerow(['Title', 'Link'])
updateWriter.writerow(['Title', 'Link'])

for mod in filteredMod:
    data = [mod[0], mod[1]]
    if mod[2]:
        updateWriter.writerow(data)
    else:
        newWriter.writerow(data)

newModCsv.close()
updateModCsv.close()

"""
modification pour ajouter les images sur le excel

from openpyxl import Workbook
from openpyxl.drawing.image import Image
import os

# Exemple de données : liste des mods avec titre, lien et chemin de l'image
mods = [
    ["Mod 1", "https://example.com/mod1", "mod1.png"],
    ["Mod 2", "https://example.com/mod2", "mod2.png"],
    ["Mod 3", "https://example.com/mod3", "nonexistent_image.png"],  # Image inexistante
]

# Création du fichier Excel
wb = Workbook()
ws = wb.active

# Ajouter les en-têtes
ws.append(["Title", "Link", "Image"])

# Ajouter chaque mod au fichier Excel
for index, mod in enumerate(mods, start=2):  # Start=2 car la première ligne est pour les en-têtes
    title, link, image_path = mod

    # Ajouter le titre et le lien dans les colonnes A et B
    ws[f"A{index}"] = title
    ws[f"B{index}"] = link

    # Ajouter l'image si elle existe
    if os.path.exists(image_path):  # Vérifie si l'image existe
        img = Image(image_path)
        ws.add_image(img, f"C{index}")  # Place l'image dans la colonne C
    else:
        ws[f"C{index}"] = "Image not found"  # Indique que l'image est introuvable

# Sauvegarder le fichier Excel
wb.save("mods_with_images.xlsx")
print("Fichier Excel avec images créé.")


"""
    # timeEndDay = time.time() % 86400
    #
    # if keyboard.is_pressed("esc") or timeEndDay == 0:
    #     # si on interrompt le programme avec la touche échap, on arrête tout, sinon c'est qu'il est minuit donc on
    #     # fait un bilan de la journée
    #     programmRun = 0
    #
    #     """
    #         Cette partie permet de connaître le nombre de nouveaux mod de la veille et d'obtenir un fichier avec le nom
    #         et le lien de chaque mod
    #     """
    #
    #     if timeEndDay == 0:
    #         time.sleep(1.0)
    #         tableauToPrint = ""
    #         nbPage = 1
    #         newDay = 0
    #         numberOfModsYesterday = 0
    #
    #         while not newDay:
    #             print(nbPage)
    #             # on charge la page souhaitee
    #             url = "https://www.kingmods.net/fr/fs22/nouveaux-mods?page=" + str(nbPage)
    #
    #             browser.get(url)
    #
    #             # on recupere toutes les donnees a partir des lignes html
    #             linked = browser.find_elements(By.TAG_NAME, "a")
    #
    #             dates = browser.find_elements(By.TAG_NAME, "time")
    #
    #             # Une page contient 12 mods
    #             for iteration in range(len(dates)):
    #                 date = dates[iteration]
    #                 links = linked[
    #                     58 + iteration]  # beaucoup de lignes permettant de naviguer sont presentes avant les mods
    #
    #                 dateStr = date.get_attribute("datetime")  # date
    #                 link = links.get_attribute("href")  # lien du mod
    #                 titreMod = links.get_attribute("title")  # titre
    #
    #                 dateDatetime = datetime.datetime.strptime(dateStr,
    #                                                           "%Y-%m-%dT%H:%M:%SZ")  # utilisation de datetime pour
    #                 # comparer des dates
    #                 nowDateTime = datetime.date.today()
    #                 yesterdayDateTime = nowDateTime - datetime.timedelta(days=1)
    #
    #                 if dateDatetime.date() == nowDateTime:
    #                     pass
    #                 elif dateDatetime.date() == yesterdayDateTime:
    #                     # preparation pour csv
    #                     dataToAdd = titreMod + ";" + link + ";\n"
    #                     tableauToPrint += dataToAdd
    #                     numberOfModsYesterday += 1
    #                 else:
    #                     newDay = 1
    #
    #             nbPage += 1
    #
    #         browser.quit()
    #
    #         print(tableauToPrint)
    #         print("%s Mods add yesterday!!" % numberOfModsYesterday)
    #         programmRun = 1

"""
    To add: 
        - Faire un bot qui envoie les messages de nouveau mods et le récapitulatif
        - Mettre les mods dans un fichier csv pour faciliter la lecture
        - 
"""
