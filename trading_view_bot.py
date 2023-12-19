import os
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import pandas as pd
from io import StringIO

url = "https://www.tradingview.com/markets/cryptocurrencies/prices-all/"

driver_path = os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe")
chrome_service = Service(driver_path)
chrome_options = Options()

browser = Chrome(service=chrome_service, options=chrome_options)
browser.implicitly_wait(7)
browser.maximize_window()

browser.get(url)

# Step 1. Import Tables
xlwriter = pd.ExcelWriter("tradingview_crypto.xlsx", engine="xlsxwriter")

class_ = "square-tab-button-huvpscfz"

def get_categories():
    categories  = browser.find_elements(By.XPATH, '//button[starts-with(@class, "square-tab-button-huvpscfz")]')[:-1] # we don't need the last one
    for category in categories:
        print(category.text)
        try:
            browser.find_element(By.XPATH, f"//span[text()='{category.text}']").click()
        except ElementNotInteractableException as e:  # replace Exception with the specific exception you want to catch
            pass
        
        load_more = True
        while load_more:
            try:
                browser.find_element(By.XPATH, '//button[starts-with(@class, "button-SFwfC2e0")]').click()
                time.sleep(2)
            except NoSuchElementException as e:
                load_more = False
            except ElementNotInteractableException as e:
                load_more = False
            except TimeoutException as e:
                load_more = False
                
        df = pd.read_html(StringIO(browser.page_source))[1]
        # print(df[1])
        df.to_excel(xlwriter, sheet_name=category.text, index=False)
        
    xlwriter._save()
    browser.quit()
    
if __name__ == "__main__":
    get_categories()


