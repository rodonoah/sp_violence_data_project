import gmplot
import pprint

craco = ['Av. São João, 377 - República, São Paulo - SP, 01035-000', 'Av. Cásper Líbero, 42 - Centro Histórico de São Paulo, São Paulo - SP, 01033-000', 'Praça da Luz, 1, Luz, São Paulo - SP',
         'Praça Júlio Prestes - Campos Elíseos, São Paulo - SP, 01218-020', 'Alameda Eduardo Prado, 61 - Campos Elíseos, São Paulo - SP, 01218-011', 'R. Barra Funda, 161 - Barra Funda, São Paulo - SP, 01152-000']

apikey = ''  # (your API key here)

gmap = gmplot.GoogleMapPlotter(-23.547, -46.63, 12, apikey=apikey)

coordinates = [gmplot.GoogleMapPlotter.geocode(
    e, apikey=apikey) for e in craco]

pprint.pprint(coordinates)

cracolandia = zip(*coordinates)

# pprint.pprint(*cracolandia)

gmap.polygon(*cracolandia, face_color='pink',
             edge_color='cornflowerblue', edge_width=5)
