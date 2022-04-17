import pandas as pd
import time
import gmplot
import json
import requests
from bs4 import BeautifulSoup
import pprint

r = requests.get(
    'https://www.agenteimovel.com.br/mercado-imobiliario/a-venda/sp/sao-paulo/#')
soup = BeautifulSoup(r.text, 'html.parser')
m2_price = []
table = soup.find('table', {"class": "bairro"})
# table_body = table.find('tbody')

rows = table.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    m2_price.append([ele for ele in cols if ele])  # Get rid of empty values

df = pd.DataFrame(m2_price)
df = df.iloc[1:, :]
df.set_axis(['bairro', 'alteracao_mensal', 'preco_m2',
            'preco_medio'], axis=1, inplace=True)

# print(df)

t = time.localtime()
current_time = time.strftime("%b%d%Y%H:%M:%S", t)
df.to_csv(f'preco_m2_bairros_{current_time}.csv',
          encoding='utf-8', index=False, header=True)
