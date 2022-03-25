# Importing modules
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

# Get list of PDs
pds_list = []
options = depto_select.options
for index in range(1, len(options)):
    pds_list.append(options[index].text)

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

for e in pds_list:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'conteudo_ddlDelegacias')))
    depto_select = Select(driver.find_element(By.ID, 'conteudo_ddlDelegacias'))
    depto_select.select_by_visible_text(e)

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
        child = child[1:]  # take the data less the header row
        child.columns = new_header  # set the header row as the df header

        # Adding the year and PD columns and renaming 'Tipo' to 'Mes'
        child.insert(0, 'Ano', i)
        child.insert(0, 'DP', e)
        child = child.rename(columns={'Tipo': 'Mes'})
        # Appending the small df to the list of dfs
        small_dfs.append(child)
        print(f'Year {i} done')
    break
large_df = pd.concat(small_dfs, ignore_index=True)
print(large_df)
large_df.to_csv('se_dp_test.csv', encoding='utf-8', index=False, header=True)
# Quit driver
driver.quit()
