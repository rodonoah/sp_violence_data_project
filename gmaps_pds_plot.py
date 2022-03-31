import gmplot
import pandas as pd

# Reading file and changing column type to int for desired columns
df = pd.read_csv('large_df_22:25:30.csv')
ocurrences_column_names = df.columns.values.tolist()[4:]
for column in ocurrences_column_names:
    df[column] = pd.to_numeric(df[column], errors='coerce')

# Total ocurrences column
df['Total Ocorrencias'] = df.iloc[:, 4:].sum(axis=1)

# Grouping total ocurrences by PD
grouped_pd_year = df.groupby(['DP', 'Coordenadas', 'Ano'])[
    'Total Ocorrencias'].sum().reset_index()

# Rank column for weights
grouped_pd_year['Rank'] = grouped_pd_year.groupby(
    'Ano')['Total Ocorrencias'].rank(ascending=False)

# Filtering for specific year
one_year = grouped_pd_year.loc[grouped_pd_year['Ano'] == 2021]

# Exporting lists
pds_final_list = one_year['Coordenadas'].to_list()
pds_final_list = [e.replace('[', "") for e in pds_final_list]
pds_final_list = [e.replace(']', "") for e in pds_final_list]
ranking = one_year['Rank'].to_list()

# Cleaning up lats and longs
lats = []
longs = []
for item in pds_final_list:
    lats.append(item.split(', ')[0])
    longs.append(item.split(', ')[1])
lats = [float(lat) for lat in lats]
longs = [float(long) for long in longs]

pds = list(zip(lats, longs))

# Create the map plotter:
apikey = ''  # (your API key here)

gmap = gmplot.GoogleMapPlotter(-23.533773, -46.625290, 11, apikey=apikey)

dps = zip(*pds)

gmap.heatmap(*dps, radius=30, weights=ranking,
             gradient=[(0, 0, 255, 0), (0, 255, 0, 0.9), (255, 0, 0, 1)])

gmap.draw('map.html')
