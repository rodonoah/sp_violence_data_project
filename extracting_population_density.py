import pandas as pd
import time
import requests
from re import search
from bs4 import BeautifulSoup

r = requests.get(
    'https://www.prefeitura.sp.gov.br/cidade/secretarias/subprefeituras/subprefeituras/dados_demograficos/index.php?p=12758')
soup = BeautifulSoup(r.text, 'html.parser')
pop_density = []
table_div = soup.find('div', {'class': 'post-text'})
table = table_div.find('table')

rows = table.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    pop_density.append(cols if len(cols) < 5 else cols[1:])

df = pd.DataFrame(pop_density)
df = df.iloc[1:, :]
df.set_axis(['distrito', 'area', 'pop', 'population_density'],
            axis=1, inplace=True)
df = df[df["distrito"] != "TOTAL"]

# Save to file
t = time.localtime()
current_time = time.strftime("%b%d%Y%H:%M:%S", t)
df.to_csv(f'population_density_sp{current_time}.csv',
          encoding='utf-8', index=False, header=True)
