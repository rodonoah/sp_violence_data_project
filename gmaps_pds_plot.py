import numpy as np
import gmplot
import pandas as pd

# Reading file and changing column type to int for desired columns
df = pd.read_csv('large_df_20:26:08.csv')
ocurrences_column_names = df.columns.values.tolist()[4:]
for column in ocurrences_column_names:
    df[column] = pd.to_numeric(df[column], errors='coerce')

# Total crime ocurrences column
df['Total Ocorrencias'] = df.iloc[:, 4:].sum(axis=1)

# Grouping total ocurrences by PD
df = df.groupby(['DP', 'Coordenadas', 'Ano'])[
    'Total Ocorrencias'].sum().reset_index()


# Rank column
df['Rank'] = df.groupby(
    'Ano')['Total Ocorrencias'].rank(ascending=False)

# print(df)

# Filtering for specific year
df = df.loc[df['Ano'] == 2021]

# print(df)

a = df['Total Ocorrencias'].quantile(0.2)
b = df['Total Ocorrencias'].quantile(0.4)
c = df['Total Ocorrencias'].quantile(0.6)
d = df['Total Ocorrencias'].quantile(0.8)

print(a)
print(b)
print(c)
print(d)
df['Group'] = np.where(df['Total Ocorrencias'] < a, 1, np.where(df['Total Ocorrencias'] < b, 2, np.where(
    df['Total Ocorrencias'] < c, 3, np.where(df['Total Ocorrencias'] < d, 4, 5))))


df['Color'] = np.where(df['Group'] == 1, '#00FF7F', np.where(df['Group'] == 2, '#3BCA6D', np.where(
    df['Group'] == 3, '#77945C', np.where(df['Group'] == 4, '#B25F4A', '#ED2938'))))
print(df)

# Exporting lists
pds_final_list = df['Coordenadas'].to_list()
pds_final_list = [e.replace('[', "") for e in pds_final_list]
pds_final_list = [e.replace(']', "") for e in pds_final_list]
colors = df['Color'].to_list()

# Cleaning up lats and longs
lats = []
longs = []
for item in pds_final_list:
    lats.append(item.split(', ')[0])
    longs.append(item.split(', ')[1])
lats = [float(lat) for lat in lats]
longs = [float(long) for long in longs]
# pds = list(zip(lats, longs))
# pair = dict(zip(pds, colors))

# dps = zip(*pds)

trio = zip(lats, longs, colors)
# print(pds)
# print(dps)


# Create the map plotter:
apikey = 'AIzaSyCdfNQ_FYCH1CMsYw0Hq6PU31GRLAVbPEM'  # (your API key here)

# Coordinates of Sao Paulo
gmap = gmplot.GoogleMapPlotter(-23.533773, -46.625290, 11, apikey=apikey)

# gmap.heatmap(*dps, radius=30, weights=ranking,
#              gradient=[(0, 0, 255, 0), (0, 255, 0, 0.9), (255, 0, 0, 1)])

for item in trio:
    gmap.circle(item[0], item[1], 600, edge_alpha=0, color=item[2])

gmap.draw('map.html')
