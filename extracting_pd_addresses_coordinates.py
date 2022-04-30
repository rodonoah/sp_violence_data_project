import time
import gmplot
import json
import requests
from bs4 import BeautifulSoup


def get_pds_addresses_list(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    address_list = []
    for ultag in soup.find_all('ul'):
        for litag in ultag.find_all('li'):
            address_list.append(litag.text)
    address_list = [adr for adr in address_list if 'ª' in adr]
    ordered = sorted(address_list, key=lambda x: int((x.split()[0])[:-1]))
    only_address = [" ".join(word.split()[2:])for word in ordered]
    # Fixing inaccurate addresses
    clean_address = [e.replace('Arquitº', 'Arquiteto') for e in only_address]
    clean_address = [e.replace(' – Campo Grande', '') for e in clean_address]
    clean_address = [e.replace(' – Socorro', '') for e in clean_address]
    return clean_address


data = get_pds_addresses_list(
    'https://pt.wikipedia.org/wiki/Distritos_policiais_da_cidade_de_S%C3%A3o_Paulo')

# Geocoding
apikey = ''  # (your GCP API key here)
coordinates = [gmplot.GoogleMapPlotter.geocode(e, apikey=apikey) for e in data]

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

# Save coordinates to file:
with open(f'pds_coordinates{current_time}.txt', 'w') as f:
    f.write(json.dumps(coordinates))
