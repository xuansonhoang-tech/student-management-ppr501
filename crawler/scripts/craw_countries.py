from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#headless (craw not need to open browers)
from selenium.webdriver.chrome.options import Options
import csv
import os

#config
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DRIVER_PATH = os.path.join(BASE_DIR, "drivers", "chromedriver.exe")
OUTPUT_PATH = os.path.join(BASE_DIR, "output", "countries.csv")

# ====== INIT DRIVER ======
options = Options() #setup for headless
options.add_argument("--headless")
service = Service(DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)


# ====== OPEN WEBSITE ======
driver.get("https://www.scrapethissite.com/pages/simple/")

# ====== CRAW DATA ======
countries = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "country")))
data = []
count = 0

for count, country in enumerate(countries, start=1):
    country_name = country.find_element(By.CLASS_NAME, "country-name").text
    country_capital = country.find_element(By.CLASS_NAME, "country-capital").text
    country_population = float(country.find_element(By.CLASS_NAME, "country-population").text)
    country_area = float(country.find_element(By.CLASS_NAME, "country-area").text)
    print(f"append data country [{count}]: ", [country_name, country_capital, country_population, country_area])
    data.append([country_name, country_capital, country_population, country_area])

print(f"Apply {count} data countries")
# ====== SAVE CSV ======
with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["country_name", "country_capital", "country_population", "country_area"])
    writer.writerows(data)

driver.quit()
print("✅ Crawl done, data in crawler/output/")