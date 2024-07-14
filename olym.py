from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

start = time.time()
web_open = './geckodriver.exe'

# A Service class that is responsible for the starting and stopping of geckodriver.
DRIVER_PATH = Service(web_open)

# Service – (Optional) service instance for managing the starting and stopping of the driver
driver = webdriver.Firefox(service=DRIVER_PATH)
driver.maximize_window()

url = "http://www.olympedia.org/statistics/medal/country"
driver.get(url)

table_header = ["奧林匹克種類", "年", "性別", "國家", "金", "銀", "銅", "總數"]
medal_data = []

# Iterate through the gender options (male and female)
for gender_value, gender_label in [("male", "male"), ("female", "female")]:
    driver.find_element(By.ID, "athlete_gender").send_keys(gender_value)
    time.sleep(2)

    # Iterate through the Olympic types and years
    for optgroup in driver.find_elements(By.TAG_NAME, "optgroup")[:6]:
        olym_type = optgroup.get_attribute("label")
        options = optgroup.find_elements(By.TAG_NAME, "option")

        for option in options:
            olym_year = option.get_attribute("text")
            option.click()
            time.sleep(2)

            try:
                table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "medals")))
                usa_rows = table.find_elements(By.XPATH, f".//tr[td/a[contains(@href, '/countries/USA')]]")
               
                if len(usa_rows) == 0:
                    medal_data.append([olym_type, olym_year, gender_label, "0", "0", "0", "0", "0"])

                for usa_row in usa_rows:
                    country = usa_row.find_element(By.XPATH, "./td[2]/a").text
                    gold = usa_row.find_element(By.XPATH, "./td[3]").text
                    silver = usa_row.find_element(By.XPATH, "./td[4]").text
                    bronze = usa_row.find_element(By.XPATH, "./td[5]").text
                    total = usa_row.find_element(By.XPATH, "./td[6]").text
                    medal_data.append([olym_type, olym_year, gender_label, country, gold, silver, bronze, total])

            except:
                medal_data.append([olym_type, olym_year, gender_label, "0", "0", "0", "0", "0"])

            # Go back to the main page
            driver.back()
            time.sleep(2)

# Create a DataFrame from the medal data
df = pd.DataFrame(medal_data, columns=table_header)

# Save the DataFrame to a CSV file
df.to_csv("olym_0612.csv", encoding="utf_8_sig", index=False)

driver.quit()

end = time.time()
print("花費",end-start,"秒")