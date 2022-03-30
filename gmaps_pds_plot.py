from dataclasses import replace
import gmplot
import pandas as pd

# Reading file and changing column type to int for desired columns
df = pd.read_csv('large_df_22:25:30.csv')
ocurrences_column_names = df.columns.values.tolist()[4:]
for column in ocurrences_column_names:
    df[column] = pd.to_numeric(df[column], errors='coerce')
# print(df.info())

# print(df.type())
# Total ocurrences column
df['Total Ocorrencias'] = df.iloc[:, 4:].sum(axis=1)
# print(df)

# Grouping total ocurrences by PD
grouped_pd_year = df.groupby(['DP', 'Coordenadas', 'Ano'])[
    'Total Ocorrencias'].sum().reset_index()

# print(grouped_pd_year)

# Filtering for specific year
one_year = grouped_pd_year.loc[grouped_pd_year['Ano'] == 2021]

# print(one_year)

# Exporting lists
pds_final_list = one_year['Coordenadas'].to_list()
pds_final_list = [e.replace('[', "") for e in pds_final_list]
pds_final_list = [e.replace(']', "") for e in pds_final_list]
# pds_final_list = [tuple(item) for item in pds_final_list]
total_occurences_list = one_year['Total Ocorrencias'].to_list()


# Need to use a rank as oppose to big number
# total_occurences_list = [4, 12, 37]

# Cleaning up lats and longs
lats = []
longs = []
for item in pds_final_list:
    lats.append(item.split(', ')[0])
    longs.append(item.split(', ')[1])
lats = [float(lat) for lat in lats]
longs = [float(long) for long in longs]
# print(lats)
# print(longs)
# print(pds_final_list)
# print(total_occurences_list)
pds = list(zip(lats, longs))

print(pds)
# Create the map plotter:
apikey = ''  # (your API key here)

gmap = gmplot.GoogleMapPlotter(-23.533773, -46.625290, 12, apikey=apikey)

dps = zip(*pds)

gmap.heatmap(*dps, radius=40, weights=total_occurences_list,
             gradient=[(0, 0, 255, 0), (0, 255, 0, 0.9), (255, 0, 0, 1)])

gmap.draw('map.html')
