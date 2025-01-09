"""
    Projet : KingMods
    Date Creation : 07/08/2023
    Date Revision : /01/2025
    Entreprise : 3SC4P3
    Auteur: Florian HOFBAUER
    Contact :
    But : Obtenir un document comportant tous les liens et noms des derniers mods ajoutés sur KingMods dans le but de générer un bot
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import datetime
import time

from openpyxl import Workbook

# Option for website (no screen open)
options = Options()
options.add_argument('--headless')

previousTitle = "Pack d'outils pour pierres"
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

excelFile = Workbook()

newModSheet = excelFile.active
newModSheet.title = "New Mod"
updateModSheet = excelFile.create_sheet(title="Update Mod")

newModSheet.append(["Title", "Link"])
updateModSheet.append(["Title", "Link"])

for index, mod in enumerate(filteredMod, start=2):
    title = mod[0]
    link = mod[1]

    if mod[2]:
        updateModSheet[f"A{index}"] = title
        updateModSheet[f"B{index}"] = link
    else:
        newModSheet[f"A{index}"] = title
        newModSheet[f"B{index}"] = link

excelFile.save("KingsMod_Resume.xlsx")


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
        - Comment save le previous mod pour un raspberry pi 
        - 
"""
