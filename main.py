
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime
# import csv
# import time

# Option for website (no screen open)
options = Options()
# options.add_argument('--headless')

# Initiate the browser
browser = webdriver.Chrome(options=options)

# Open the Website
browser.get('https://www.kingmods.net/fr/fs22/nouveaux-mods')

titre = browser.find_elements(by=By.XPATH, value="//h2[@class='font-bold text-white truncate smd:text-16 _2xs:text-16 "
                                                "my-5 text-20']")

linked = browser.find_elements(By.TAG_NAME, "a")

for links in linked:
    link = links.get_attribute("href")

date = browser.find_elements(By.TAG_NAME, "time")

for data in date:
    dt = data.get_attribute("datetime")

browser.quit()
