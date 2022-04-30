# Importing modules
import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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

# Get list of PDs (Filtered to only retrieve the '103 Distritos policiais da capital')
pds_list = []
options = depto_select.options
for index in range(1, len(options)):
    pds_list.append(options[index].text)
pds_list = [dp for dp in pds_list if 'DP -' in dp]

# Converting the pds coordinates text file into a list
with open('pds_coordinates00:01:25.txt', 'r') as f:
    pds_coordinates = json.loads(f.read())

# Merging PDs names with their coordinates into a dict
pds_info = dict(zip(pds_list, pds_coordinates))

# Wait for the ddm to be visible [YEAR]
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, 'conteudo_ddlAnos')))

# Open the year drop down list
year_select = Select(driver.find_element(By.ID, 'conteudo_ddlAnos'))

# Get list of years
years_list = []
options = year_select.options
for index in range(1, len(options)):
    years_list.append(options[index].text)

# Looping through the years for each PD
small_dfs = []

p = 1
# for e in pds_list:
for key in pds_info:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'conteudo_ddlDelegacias')))
    depto_select = Select(driver.find_element(By.ID, 'conteudo_ddlDelegacias'))
    depto_select.select_by_visible_text(key)
    # counter
    for i in years_list:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'conteudo_ddlAnos')))
        year_select = Select(driver.find_element(By.ID, 'conteudo_ddlAnos'))
        year_select.select_by_visible_text(i)

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

        child = pd.DataFrame(data, columns=[
            'Tipo', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Total'])

        # Transposing and dropping the first column (None values) and last column (year total)
        child = child.transpose().iloc[:-1, 1:]
        child = child.reset_index()

        # Setting the first row as the header
        new_header = child.iloc[0]  # grab the first row for the header
        child = child[1:]  # retrieve the data besides the header
        child.columns = new_header  # set the header row as the df header

        # Adding the year, coordinates and PD name columns and renaming column name 'Tipo' to 'Mes'
        child.insert(0, 'Ano', i)
        child.insert(0, 'Coordenadas', str(pds_info[key]))
        child.insert(0, 'DP', key)
        child = child.rename(columns={'Tipo': 'Mes'})
        # Appending the small df to the list of dfs
        small_dfs.append(child)
        print(f'Year {i} done')
    print(f'PD {key} done')
large_df = pd.concat(small_dfs, ignore_index=True)

# Save to csv
t = time.localtime()
current_time = time.strftime("%b%d%Y%H:%M:%S", t)
large_df.to_csv(f'large_df_{current_time}.csv',
                encoding='utf-8', index=False, header=True)

print('Large PDs csv exported!')
# Quit driver
driver.quit()
