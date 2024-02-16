# Jerry Sandhu
# Program to find the shortest route for a delivery truck

import csv
import datetime
import truck
import package
import hashtable

# This will load the required CSV files containing data
with open("Data/address.csv") as CSV_address:
    AddressCSV = csv.reader(CSV_address)
    AddressCSV = list(address)
with open("Data/distance.csv") as CSV_distance:
    DistanceCSV = csv.reader(CSV_distance)
    DistanceCSV = list(distance)   
    
#Creating the Packages with info from the CSV to go into the Hash Table
def loadPackageData(filename):
    with open(filename) as packagess:
        packageInfo = csv.reader(packagess,delimiter=',')
        next (packageInfo)
        for package in packageInfo:
            pID = int(package[0])
            #print(pID)
            pStreet = package[1]
            #print(pStreet)
            pCity = package[2]
            #print(pCity)
            pState = package[3]
            #print(pState)
            pZip = package[4]
            #print(pZip)
            pDeadline = package[5]
            #print(pDeadline)
            pWeight = package[6]
            #print(pWeight)
            pNotes = package[7]
            #print(pNotes)
            pStatus = "At the Hub"
            pDepartureTime = None
            pDeliveryTime = None

            #Inserting Package info into the hash
            p = Packages(pID, pStreet, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus, pDepartureTime, pDeliveryTime)
            #print (p)
            packageHash.insert(pID, p)

#Hash table for the packages
packageHash = hashtable() 

#finds the minimum distance for the next address
def addresss(address):
    for row in AddressCSV:
        if address in row[2]:
           return int(row[0])


#finds the distance between two addresses
def Betweenst(addy1,addy2):
    distance = DistanceCSV[addy1][addy2]
    if distance == '':
        distance = DistanceCSV[addy2][addy1]
    return float(distance)


#pulls data from CSV into the function
loadPackageData('CSVFiles/packageCSV.csv')

#manually loading the trucks and assigning them a departure time
truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),[1,13,14,15,16,19,20,27,29,30,31,34,37,40])
truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),[2,3,4,5,9,18,26,28,32,35,36,38])
truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),[6,7,8,10,11,12,17,21,22,23,24,25,33,39])


#algorithm to deliver the packages on the truck
def truckDeliverPackages(truck):
    print("Hello!")
    #creates a list for all the packages that need to be delivered
    enroute = []
    #puts packages from the hash table into the enroute list
    for packageID in truck.packages:
        package = packageHash.search(packageID)
        enroute.append(package)

    truck.packages.clear()
    #while there are packages left to be delivered the algorithm will run
    while len(enroute) > 0:
        nextAddy = 2000
        nextPackage = None
        for package in enroute:
            if package.ID in [25, 6]:
                nextPackage = package
                nextAddy = Betweenst(addresss(truck.currentLocation), addresss(package.street))
                break
            if Betweenst(addresss(truck.currentLocation), addresss(package.street)) <= nextAddy:
                nextAddy = Betweenst(addresss(truck.currentLocation), addresss(package.street))
                nextPackage = package
        truck.packages.append(nextPackage.ID)    
        enroute.remove(nextPackage)
        truck.miles += nextAddy
        truck.currentLocation = nextPackage.street
        truck.time += datetime.timedelta(hours=nextAddy / 18)
        nextPackage.deliveryTime = truck.time
        nextPackage.departureTime = truck.departTime

     
        #enroute.remove(nextPackage)
        #print(nextPackage.street)
                      
    

#Actually calls the trucks to leave to being delivering packages
truckDeliverPackages(truck1)
truckDeliverPackages(truck3)
#ensures truck 2 won't leave until either truck 1 or 2 have returned
truck2.departTime = min(truck1.time, truck3.time)
truckDeliverPackages(truck2)

#title
print("The fastest delivery service by truck")
#total miles for all of the trucks
print ("The mileage for 3 trucks are:", (truck1.miles + truck2.miles + truck3.miles))

while True:
    
    #print(truck1.miles + truck2.miles + truck3.miles)
    #pazzazz
    userTime = input("Enter a time value in the Hour:Minute format to view the truck positions: ")
    (h, m) = userTime.split(":")
    timeChange = datetime.timedelta(hours=int(h), minutes=int(m))
    try:
        singleEntry = [int(input("Input the ID for a package to track it: "))]
    except ValueError:
        singleEntry =  range(1, 41)
    for packageID in singleEntry:
        package = packageHash.search(packageID)
        package.statusUpdate(timeChange)
        print(str(package))                    

