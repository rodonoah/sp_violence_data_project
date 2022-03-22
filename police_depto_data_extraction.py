# Importing modules
import bs4
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
# from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import random

# Pre-scrapping work to avoid reCaptcha detection
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1100,1000")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)


# Initialize chrome-driver
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

# Get URL
driver.get('https://www.ssp.sp.gov.br/Estatistica/Pesquisa.aspx')
driver.delete_all_cookies()

# Delay
time.sleep(random.randint(1, 5))

# Selecting occurences per year
driver.find_element(By.ID, 'conteudo_btnMensal').click()

# Delay
time.sleep(3)

# Open the region selector toggle
# region_toggle = driver.find_element(By.ID, 'conteudo_ddlRegioes').click()
# region_select = WebDriverWait(driver, 20).until(
# EC.visibility_of_element_located((By.ID, "conteudo_ddlRegioes"))).click()

region_select = Select(driver.find_element(By.ID, 'conteudo_ddlRegioes'))

# Delay
time.sleep(random.randint(1, 5))

# Selecting the desired Region (In the case we want 'Capital')
i = 1
region_select.select_by_value(f"{i}")

# Delay
time.sleep(5)
# time.sleep(random.randint(1, 5))

print('Working')
