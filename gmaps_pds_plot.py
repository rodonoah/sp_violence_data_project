import gmplot

# Create the map plotter:
apikey = ''  # (your API key here)
gmap = gmplot.GoogleMapPlotter(-23.533773, -46.625290, 12, apikey=apikey)

lat_1, long_1 = gmplot.GoogleMapPlotter.geocode(
    'RUA DA GLÓRIA, 410', apikey=apikey)

lat_2, long_2 = gmplot.GoogleMapPlotter.geocode(
    'RUA JARAGUÁ, 383', apikey=apikey)

dps = zip(*[
    (lat_1, long_1),
    (lat_2, long_2)
])

gmap.heatmap(
    *dps,
    radius=40,
    weights=[10, 1],
    gradient=[(0, 255, 0, 0), (0, 255, 0, 0.5), (255, 0, 0, 1)]
)

gmap.draw('map.html')


# Mark a hidden gem:
# gmap.marker(37.770776, -122.461689, color='cornflowerblue')

# Highlight some attractions:
# attractions_lats, attractions_lngs = zip(*[
#     (37.769901, -122.498331),
#     (37.768645, -122.475328),
#     (37.771478, -122.468677),
#     (37.769867, -122.466102),
#     (37.767187, -122.467496),
#     (37.770104, -122.470436)
# ])
# gmap.scatter(attractions_lats, attractions_lngs,
#              color='#3B0B39', size=40, marker=False)

# Outline the Golden Gate Park:
# golden_gate_park = zip(*[
#     (37.771269, -122.511015),
#     (37.773495, -122.464830),
#     (37.774797, -122.454538),
#     (37.771988, -122.454018),
#     (37.773646, -122.440979),
#     (37.772742, -122.440797),
#     (37.771096, -122.453889),
#     (37.768669, -122.453518),
#     (37.766227, -122.460213),
#     (37.764028, -122.510347)
# ])
# gmap.polygon(*golden_gate_park, color='cornflowerblue', edge_width=10)

# Draw the map to an HTML file:
# gmap.draw('map.html')
