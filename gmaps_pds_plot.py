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

# Filtering for specific year
df = df.loc[df['Ano'] == 2021]

a = df['Total Ocorrencias'].quantile(1/6)
b = df['Total Ocorrencias'].quantile(1/3)
c = df['Total Ocorrencias'].quantile(1/5)
d = df['Total Ocorrencias'].quantile(2/3)
e = df['Total Ocorrencias'].quantile(5/6)

df['Group'] = np.where(df['Total Ocorrencias'] < a, 1, np.where(df['Total Ocorrencias'] < b, 2, np.where(
    df['Total Ocorrencias'] < c, 3, np.where(df['Total Ocorrencias'] < d, 4, np.where(df['Total Ocorrencias'] < e, 5, 6)))))


df['Color'] = np.where(df['Group'] == 1, '#69B34C', np.where(df['Group'] == 2, '#ACB334', np.where(
    df['Group'] == 3, '#FAB733', np.where(df['Group'] == 4, '#FF8E15', np.where(df['Group'] == 5, '#FF4E11', '#FF0D0D')))))
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

trio = zip(lats, longs, colors)

# Create the map plotter:
apikey = 'AIzaSyCdfNQ_FYCH1CMsYw0Hq6PU31GRLAVbPEM'  # (your API key here)

# Coordinates of Sao Paulo
gmap = gmplot.GoogleMapPlotter(-23.533773, -46.625290, 11, apikey=apikey)

# Considering a 5km2 area coverage for each DP
for item in trio:
    gmap.circle(item[0], item[1], 1260, edge_alpha=0, color=item[2])

gmap.draw('map.html')
