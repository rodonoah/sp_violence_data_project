import numpy as np
import gmplot
import pandas as pd
import time

# Reading file and changing column type to int for desired columns
# df = pd.read_csv('') # csv file here
ocurrences_column_names = df.columns.values.tolist()[4:]
for column in ocurrences_column_names:
    df[column] = pd.to_numeric(df[column], errors='coerce')

# Dropping columns containing the number of victims
df = df[df.columns.drop(list(df.filter(regex='Nº DE VÍTIMAS')))]

# Dropping column duplicates
df = df.drop(['ESTUPRO DE VULNERÁVEL', 'ESTUPRO', 'ROUBO - OUTROS'], axis=1)

# For "Crimes violentos" only drop columns contanining culposo and furtos
# df = df[df.columns.drop(list(df.filter(regex='CULPOS')))]
# df = df[df.columns.drop(list(df.filter(regex='FURTO')))]

# Total crime ocurrences column
df['Total Ocorrencias'] = df.iloc[:, 4:].sum(axis=1)

# Grouping total ocurrences by PD
df = df.groupby(['DP', 'Coordenadas', 'Ano'])[
    'Total Ocorrencias'].sum().reset_index()

# Getting occurences for all 20 years
df = df.groupby(['DP', 'Coordenadas'])['Total Ocorrencias'].sum().reset_index()
df['Rank'] = df['Total Ocorrencias'].rank(ascending=False)
df = df.sort_values(by=['Rank'])

# For retrieving only year specific records
# # Rank column
# df['Rank'] = df.groupby(
#     'Ano')['Total Ocorrencias'].rank(ascending=False)

# # Filtering for specific year
# df = df.loc[df['Ano'] == 2021]

# Bucketing into sextiles
a = df['Total Ocorrencias'].quantile(1/6)
b = df['Total Ocorrencias'].quantile(1/3)
c = df['Total Ocorrencias'].quantile(1/2)
d = df['Total Ocorrencias'].quantile(2/3)
e = df['Total Ocorrencias'].quantile(5/6)

df['Group'] = np.where(df['Total Ocorrencias'] < a, 1, np.where(df['Total Ocorrencias'] < b, 2, np.where(
    df['Total Ocorrencias'] < c, 3, np.where(df['Total Ocorrencias'] < d, 4, np.where(df['Total Ocorrencias'] < e, 5, 6)))))


df['Color'] = np.where(df['Group'] == 1, '#69B34C', np.where(df['Group'] == 2, '#ACB334', np.where(
    df['Group'] == 3, '#FAB733', np.where(df['Group'] == 4, '#FF8E15', np.where(df['Group'] == 5, '#FF4E11', '#FF0D0D')))))
print(df)

# Filter for specific group of color
# df = df[df['Group'].isin([5, 6])]

# Save to csv
t = time.localtime()
current_time = time.strftime("%b%d%Y%H:%M:%S", t)
df.to_csv(f'plotingtotalcrimesrank_{current_time}.csv',
          encoding='utf-8', index=False, header=True)

# Exporting lists
pds_final_list = df['Coordenadas'].to_list()
pds_final_list = [e.replace('[', "") for e in pds_final_list]
pds_final_list = [e.replace(']', "") for e in pds_final_list]
colors = df['Color'].to_list()

lats = []
longs = []
for item in pds_final_list:
    lats.append(item.split(', ')[0])
    longs.append(item.split(', ')[1])
lats = [float(lat) for lat in lats]
longs = [float(long) for long in longs]

trio = zip(lats, longs, colors)

# Create the map plotter:
apikey = ''  # (your GCP API key here)

# Coordinates of Sao Paulo
gmap = gmplot.GoogleMapPlotter(-23.547, -46.63, 12, apikey=apikey)

# Considering a 5km2 area coverage for each DP
for item in trio:
    gmap.circle(item[0], item[1], 1260, edge_alpha=0, color=item[2])

# Including cracolandia on the map
craco_addresses = ['Av. São João, 377 - República, São Paulo - SP, 01035-000', 'Av. Cásper Líbero, 42 - Centro Histórico de São Paulo, São Paulo - SP, 01033-000', 'Praça da Luz, 1, Luz, São Paulo - SP',
                   'Praça Júlio Prestes - Campos Elíseos, São Paulo - SP, 01218-020', 'Alameda Eduardo Prado, 61 - Campos Elíseos, São Paulo - SP, 01218-011', 'R. Barra Funda, 161 - Barra Funda, São Paulo - SP, 01152-000']

coordinates = [gmplot.GoogleMapPlotter.geocode(
    e, apikey=apikey) for e in craco_addresses]

cracolandia = zip(*coordinates)

gmap.polygon(*cracolandia, face_color='pink',
             edge_color='cornflowerblue', edge_width=5)

gmap.draw('map.html')
