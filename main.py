# Jerry Sandhu
# Student ID: 011714138
# C950 Data Structures and Algorithms 2
# Program to find the shortest route for a delivery truck

import datetime
import csv
from Hashtable import HashTable
from Package import Package
from Truck import Truck
import os

# This will load the required CSV files containing data for addresses and distances
with open("Dataset/Address.csv") as CSV_address:
    AddressCSV = csv.reader(CSV_address)
    AddressCSV = list(AddressCSV)
with open("Dataset/Distance.csv") as CSV_distance:
    DistanceCSV = csv.reader(CSV_distance)
    DistanceCSV = list(DistanceCSV)


# Collect address from Address.csv
def get_address_id(address):
    for line in AddressCSV:
        if address in line[2]:
            return int(line[0])


# Collect distances from Distance.csv and find the difference between depot address and destination address
def space_between(src, dst):
    depot = get_address_id(src)
    destination = get_address_id(dst)
    distance = DistanceCSV[depot][destination]
    if distance == '':
        distance = DistanceCSV[destination][depot]
    return float(distance)


# Collect package information from Package.csv
def pkg_loader(pkg_hashtable):
    with open("data/Package.csv") as CSV_package:
        info_package = csv.reader(CSV_package)
        for info in info_package:
            status = "Awaiting shipment"
            pkg_info = int(info[0])
            pkg_addr = info[1]
            zipcode = info[4]
            pkg_comment = info[7]
            pkg_city = info[2]
            pkg_state = info[3]
            leave_time = ""
            delivered_time = ""
            pkg_dl = info[5]
            package = Package(pkg_info, pkg_addr, pkg_city, pkg_state, zipcode, pkg_dl,
                              pkg_comment, status, leave_time, delivered_time)

            pkg_hashtable.insert(pkg_info, package)


# Collect information about the package to get details on its status
def pkg_get(pkg_track, cur_time=datetime.timedelta(hours=20)):
    package = pkg_hashtable.search(pkg_track)
    package.set_status(cur_time)
    print(str(package))


# All information about each package is stored in the pkg_hashtable
pkg_hashtable = HashTable()
# Function to load information about packages
pkg_loader(pkg_hashtable)


# Puts packages into different trucks based off given criteria
# Generate a list of packages in each truck
# Includes placeholders for extra trucks
def pkg_on_truck():
    packages = []
    # Packages that are less important
    packages_extra = []
    pkg_truck1 = []
    pkg_truck2 = []
    pkg_truck3 = []
    pkg_truck4 = []
    pkg_truck5 = []
    pkg_truck6 = []
    pkg_truck7 = []
    pkg_truck8 = []
    pkg_truck9 = []
    pkg_truck10 = []

    # All packages are collected to find which truck they should be loaded on
    for pkg_track in range(1, 41):
        # The hashtable is searched for package ID information
        packages.append(pkg_hashtable.search(pkg_track))

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    for pkg_holder in packages:
        if pkg_holder.comment == 'DELAYED_905':
            pkg_truck2.append(pkg_holder)
        elif pkg_holder.comment == 'DELAYED_1020':
            pkg_truck3.append(pkg_holder)
        elif pkg_holder.comment == 'GROUP':
            pkg_truck1.append(pkg_holder)
        elif pkg_holder.deadline != 'EOD':
            pkg_truck1.append(pkg_holder)
        elif pkg_holder.comment == 'TRUCK2':
            pkg_truck2.append(pkg_holder)
        else:
            packages_extra.append(pkg_holder)

    # Loop to add package to truck 1 if it meets the conditions
    for pkg_holder in packages_extra:
        for assigned_package in pkg_truck1:
            # Make sure the distance is less than 2.1 and truck has less than 16 packages
            if space_between(assigned_package.address, pkg_holder.address) < 2.1 and len(pkg_truck1) < 16:
                # Assign the temporary package to truck 1
                pkg_truck1.append(pkg_holder)
                # Remove the package from the temporary holder
                packages_extra.remove(pkg_holder)
                break

    # Loop to add package to truck 2 if it meets the conditions
    for pkg_holder in packages_extra:
        for assigned_package in pkg_truck2:
            # Make sure the distance is less than 2.1 and truck has less than 16 packages
            if space_between(assigned_package.address, pkg_holder.address) < 2.1 and len(pkg_truck2) < 16:
                # Assign the temporary package to truck 1
                pkg_truck2.append(pkg_holder)
                # Remove the package from the temporary holder
                packages_extra.remove(pkg_holder)
                break

    # All leftover packages get assigned to truck 3
    # More trucks can be added, so truck 3 is temporarily treated as the last truck
    for pkg_holder in packages_extra:
        pkg_truck3.append(pkg_holder)

    # Return the list of trucks with their loaded packages
    return (
        pkg_truck1,
        pkg_truck2,
        pkg_truck3
    )


# Function to find what time a package will both ship out and be delivered
def delivery_function(truck):
    # A list to sort the packages
    sorting_list = []

    # Go through all the known packages and sort them into the sorting list
    for package in truck.packages:
        sorting_list.append(package)
    # Remove the packages from the queue as they have been put into the sorted list
    truck.packages.clear()
    # Future addition to add error check to make sure the packages were cleared

    # While there are packages to be sorted, sort them with the nearest neighbour algorithm
    while len(sorting_list) > 0:
        # Temporary values
        # Holds the nearest address to the truck
        addr_near = 1000
        # Holds the nearest package to that address
        pkg_near = None

        for package in sorting_list:
            # Assigns the distance between the truck and the packages delivery address
            pkg_how_far = space_between(truck.addr_now, package.address)
            # If the packages csv address is closer than the current address, then assign the closest address to it
            if pkg_how_far <= addr_near:
                # This will mean that packages delivery address will be the trucks new target
                addr_near = pkg_how_far
                pkg_near = package

        # The nearest package will be assigned to a truck
        truck.packages.append(pkg_near.pkg_track)
        # Remove the package from the temporary list as it will no longer need to be sorted
        sorting_list.remove(pkg_near)
        # Truck will now head to the nearest delivery address
        pkg_near.depart = truck.truck_depart
        # The trucks current address is the package delivery address
        truck.addr_now = pkg_near.address
        # Add the miles traveled by the truck to the running total
        truck.total_distance += addr_near
        # set package arrival to truck's arrival time; package is now delivered and truck is departing
        truck.truck_depart += datetime.timedelta(hours=addr_near / 18)
        pkg_near.arrive = truck.truck_depart


# User interface to print out information and allow user input
def user_interface():
    print()
    print('~~~~~~~~~~~~~~~~~~~~~~')
    print('(っ◕‿◕)っ Welcome to the package delivery service! Choose from the following options to print (1-4):')
    print('1 - Every package and the distance each truck traveled')
    print('2 - The status of a package at a given time')
    print('3 - The status of every package at a given time')
    print('4 - Exit')
    print('~~~~~~~~~~~~~~~~~~~~~~')


# print_package_header() - print header for packages; makes the main program code cleaner
def pkg_info_printer():
    print('Pkg_Id, Address, City, State, ZipCode, Deadline, Weight, Notes, Status, Departure Time, Arrival Time')
    print('****************************************************************************************************')


class Program:
    # Create truck instances; previous runs show that truck 1 finishes by 930, so assigning truck 3 to start 1 hour later
    # Could potentially modify Truck class to track their last package delivery time to assign that as the start time for truck3
    truck1 = Truck(1, [], 0, '4001 South 700 East', datetime.timedelta(hours=8))
    truck2 = Truck(2, [], 0, '4001 South 700 East', datetime.timedelta(hours=9, minutes=5))
    truck3 = Truck(3, [], 0, '4001 South 700 East', datetime.timedelta(hours=10, minutes=30))

    # Load trucks
    truck1.packages, truck2.packages, truck3.packages = pkg_on_truck()

    # Simulate truck deliveries
    delivery_function(truck1)
    delivery_function(truck2)
    delivery_function(truck3)

    ## Debugging check
    # print('Truck1: ' + str(truck1))
    # print('Truck2: ' + str(truck2))
    # print('Truck3: ' + str(truck3))

    # Beginning of user interaction; prompt loops until the user chooses valid input (including exit)
    while True:
        user_interface()

        choice = input('Please select your desired option: ')

        if choice == '1':  # Print all packages, assuming "end of shift" time of 1700, allowing for 0800-1700 window for deliveries
            print()
            print('Displaying ALL package statuses by the end of the business day (1700): ')
            print('Truck1: ' + str(truck1.total_distance) + ' miles total. ')
            pkg_info_printer()

            for pkg_track in truck1.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=17))

            print()
            print('Truck2: ' + str(truck2.total_distance) + ' miles total. ')
            pkg_info_printer()

            for pkg_track in truck2.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=17))

            print()
            print('Truck3: ' + str(truck3.total_distance) + ' miles total. ')
            pkg_info_printer()

            for pkg_track in truck3.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=17))

        elif choice == '2':  # Print one package's status at a specified time
            print()
            pkg_track = int(input('Please select your desired package: '))
            package = pkg_hashtable.search(choice)

            choice = input('Please specify your time (HH:MM:SS) : ')
            (h, m, s) = choice.split(':')

            print()
            print(f'Displaying package {pkg_track} at the time ({h}:{m}:{s})')
            pkg_info_printer()
            pkg_get(pkg_track, datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)))

        elif choice == '3':  # Print ALL packages' status at a specified time
            print()
            choice = input('Please specify your time (HH:MM:SS) : ')
            (h, m, s) = choice.split(':')
            print()
            print(f'Displaying all packages at the time ({h}:{m}:{s})')
            print()
            print('Truck1: ' + str(truck1.total_distance) + ' miles total. ')
            pkg_info_printer()

            for pkg_track in truck1.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)))

            print()
            print('Truck2: ' + str(truck2.total_distance) + ' miles total. ')
            pkg_info_printer()

            for pkg_track in truck2.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)))

            print()
            print('Truck3: ' + str(truck3.total_distance) + ' miles total. ')
            pkg_info_printer()

            for pkg_track in truck3.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)))

        elif choice == '4':  # Exit request
            exit()
