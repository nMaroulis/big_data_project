import numpy as np
import pandas as pd
import gmplot
import sys
import csv
from haversine import haversine
import fileinput
import webbrowser  # opens browser automatically

input_file = "../datasets/train_set.csv"
gm_apikey = "AIzaSyBnmIhYbd-k4GbntUuVThxDEQRLxUinuso"
gmplot_color = ['#a60000', '#f4dd00', '#4da300', '#fc929b', 'cornflowerblue']
gmap = gmplot.GoogleMapPlotter(53.350140, -6.266155, 11, gm_apikey)
output_trips = '../datasets/trips.csv'
output_tripsClean = '../datasets/tripsClean.csv'
map_url = 'http://localhost:63342/data_mining/my_map.html'
chromium_path = '/usr/bin/chromium-browser %s'


def clean_csv(input_csv):
    for line in fileinput.input(input_csv, inplace=True):
        line = line.replace('\'', '')
        print(line)


def main():

    df = pd.read_csv(input_file, header=0)
    original_headers = list(df.columns.values)
    df = df[df.journeyPatternId.notnull()]  # remove Null items
    df = pd.DataFrame(df)

    trip_df = df.sort_values(['journeyPatternId', 'vehicleID', 'timestamp'], ascending=[False, False, True])
    trip_df = trip_df.assign(tripInfo = '[' + df.timestamp.astype(str) + ', ' + df.longitude.astype(str) + ', ' + df.latitude.astype(str) + ']')

    trip_df = trip_df.groupby(['journeyPatternId', 'vehicleID'])['tripInfo'].apply(list)
    trip_df = trip_df.reset_index()

    trip_df = trip_df.drop(['vehicleID'], axis=1)
    trip_df.index.name = 'tripId'

    print('OUTPUT: Trips.csv has ' + str(len(trip_df.index)) + ' items')
    trip_df.to_csv(output_trips, sep='\t', encoding='utf-8')
    clean_csv(output_trips)

    tripClean_df = trip_df
    indexes_to_be_removed = []
    remove_count = 0
    remove_count1 = 0

    for index, row in tripClean_df.iterrows():
        total_distance = 0
        max_distance = 0
        for coords in range(len(row['tripInfo']) - 1):
            trip1 = eval(row['tripInfo'][coords])
            trip2 = eval(row['tripInfo'][coords + 1])
            haversine_in_km = haversine((float(trip1[2]), float(trip1[1])), (float(trip2[2]), float(trip2[1])))
            total_distance += haversine_in_km
            if haversine_in_km > max_distance:
                max_distance = haversine_in_km
        if total_distance < 2 or max_distance > 2:
            indexes_to_be_removed.append(index)
            if total_distance < 2:
                remove_count += 1
            else:
                remove_count1 += 1

    print(len(indexes_to_be_removed), ' Total Items Removed.')
    print('Cause: \n\t> Total Distance < 2km:', remove_count, '\n\t> Max Distance > 2km:', remove_count1)
    tripClean_df.drop(tripClean_df.index[indexes_to_be_removed], inplace=True)
    tripClean_df = tripClean_df.reset_index()
    tripClean_df = tripClean_df.drop(['tripId'], axis=1)

    print('OUTPUT: tripClean.csv has ' + str(len(tripClean_df.index)) + ' items')
    tripClean_df.to_csv(output_tripsClean, sep=';', encoding='utf-8')
    clean_csv(output_tripsClean)

    color = 0
    for index, row in tripClean_df.iterrows():
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
    webbrowser.get(chromium_path).open(map_url)  # open utl automatically


if __name__ == "__main__":
    main()
