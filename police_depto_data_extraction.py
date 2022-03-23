# Importing modules
import bs4
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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

# Selecting occurences per year
WebDriverWait(driver, 20).until(EC.presence_of_element_located(
    (By.ID, 'conteudo_btnMensal'))).click()

# Wait for ddm to be visible [REGION]
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'conteudo_ddlRegioes')))

# Open the region drop down list
region_select = Select(driver.find_element(By.ID, 'conteudo_ddlRegioes'))

# Select the desired Region (In the case we want 'Capital')
i = 1
region_select.select_by_index(i)

# Wait for the ddm to be visible [POLICE DEPARTMENTS]
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'conteudo_ddlDelegacias')))

# Open the PD drop drown list
depto_select = Select(driver.find_element(By.ID, 'conteudo_ddlDelegacias'))

# Select the desired police department (We need to iterate over the +100 PDs in Sao Paulo)
e = 1
depto_select.select_by_index(e)

# Wait for the ddm to be visible [YEAR]
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'conteudo_ddlAnos')))

# Open the year drop down list
year_select = Select(driver.find_element(By.ID, 'conteudo_ddlAnos'))

# Select the desired year (We need to iterate over the 20+ years of available data for each PD)
j = 1
year_select.select_by_index(j)
time.sleep(2)

# Creating DataFrame from table
data = []
table = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'conteudo_repAnos_gridDados_0')))
for row in table.find_elements(By.XPATH, './/tr'):
    cols = row.find_elements(By.XPATH, './/td')
    temp_row = []
    for col in cols:
        temp_row.append(col.text)
    data.append(temp_row)

df = pd.DataFrame(data, columns=['Tipo', 'Jan', 'Fev', 'Mar', 'Abr',
                  'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Total'])

print(df)

print('Worked')

# Proximo passo: Remover 1 linha, adicionar coluna de ano, coluna de dp e depois pivotar meses com tipo

# # Quit driver
# driver.close()
