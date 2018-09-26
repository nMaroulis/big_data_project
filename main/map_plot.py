import pandas as pd
import gmplot
import csv

input_file = "../datasets/trips.csv"
gm_apikey = "AIzaSyBnmIhYbd-k4GbntUuVThxDEQRLxUinuso"
gmplot_color = ['#a60000', '#f4dd00', '#4da300', '#fc929b', 'cornflowerblue']
gmap = gmplot.GoogleMapPlotter(53.350140, -6.266155, 11, gm_apikey)

df = pd.read_csv(input_file, sep='\t')
# df = df.replace(['\''], [''], regex=True)

original_headers = list(df.columns.values)
df = pd.DataFrame(df)
# print(df)


color = 0
for index, row in df.iterrows():
    print(row)
    if index == 34 or index == 235 or index == 1208 or index == 750 or index == 1000:
        gm_list = []
        for trip in row['tripInfo']:
            trip_list = eval(trip)
            gm_list.append((float(trip_list[2]), float(trip_list[1])))
        trip_lats, trip_lons = zip(*gm_list)
        gmap.scatter(trip_lats, trip_lons, gmplot_color[color], size=5, marker=False)
        gmap.plot(trip_lats, trip_lons, gmplot_color[color], edge_width=5)
        color += 1

gmap.draw("my_map.html")
