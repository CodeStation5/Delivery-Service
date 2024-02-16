# Jerry Sandhu
# Program to find the shortest route for a delivery truck

import csv
import datetime

# This will load the required CSV files containing data
with open("Data/address.csv") as CSV_address:
    AddressCSV = csv.reader(CSV_address)
    AddressCSV = list(address)
with open("Data/distance.csv") as CSV_distance:
    DistanceCSV = csv.reader(CSV_distance)
    DistanceCSV = list(distance)   