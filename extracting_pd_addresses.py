import requests
from bs4 import BeautifulSoup
import pprint


def get_pds_addresses_list(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    address_list = []
    for ultag in soup.find_all('ul'):
        for litag in ultag.find_all('li'):
            address_list.append(litag.text)
    address_list = [adr for adr in address_list if 'ª' in adr]
    ordered = sorted(address_list, key=lambda x: int((x.split()[0])[:-1]))
    # pprint.pprint(ordered)
    only_address = [" ".join(word.split()[2:])for word in ordered]
    # pprint.pprint(only_address)
    clean_address = [e.replace(' –', ',') for e in only_address]
    # pprint.pprint(clean_address)
    return clean_address


data = get_pds_addresses_list(
    'https://pt.wikipedia.org/wiki/Distritos_policiais_da_cidade_de_S%C3%A3o_Paulo')

pprint.pprint(data)
