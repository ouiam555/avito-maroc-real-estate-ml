from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Chrome options for Docker
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

data = []

base_url = "https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?rooms=1&bathrooms=1&has_price=true&price=100000-&size=30-&o="

for page in range(1, 20):
    url = base_url + str(page)
    print(f"Scraping page {page} ...")

    driver.get(url)

    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "a[href*='/fr/']")
        )
    )

    time.sleep(2)

    cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='/fr/']")

    for c in cards:

        try:
            titre = c.find_element(By.CSS_SELECTOR, 'p[title]').text
        except:
            titre = ""

        try:
            prix = c.find_element(By.CSS_SELECTOR, '.sc-3286ebc5-6').text
        except:
            prix = ""

        ville = ""

        try:
            p_tags = c.find_elements(By.CSS_SELECTOR, "p.layWaX")

            for p in p_tags:
                txt = p.text.strip()

                if "il y a" in txt:
                    continue

                if "," in txt or "Casablanca" in txt or "Marrakech" in txt or "Rabat" in txt:
                    ville = txt
                    break
        except:
            ville = ""

        try:
            surface = c.find_element(By.CSS_SELECTOR, 'span[title="Surface totale"]').text
        except:
            surface = ""

        try:
            chambres = c.find_element(By.CSS_SELECTOR, 'span[title="Chambres"]').text
        except:
            chambres = ""

        try:
            sdb = c.find_element(By.CSS_SELECTOR, 'span[title="Salle de bain"]').text
        except:
            sdb = ""

        try:
            lien = c.get_attribute("href")
        except:
            lien = ""

        if titre != "":
            data.append({
                "titre": titre,
                "prix": prix,
                "ville": ville,
                "surface": surface,
                "chambres": chambres,
                "salle_de_bain": sdb,
                "lien": lien
            })

driver.quit()

df = pd.DataFrame(data)
df.drop_duplicates(inplace=True)

# IMPORTANT: path compatible Docker
df.to_csv("data/bronze/raw.csv", index=False, encoding="utf-8-sig")

print("Done")