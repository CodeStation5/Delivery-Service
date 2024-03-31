# Jerry Sandhu
# Student ID: 011714138
# C950 Data Structures and Algorithms 2
# Program to find the shortest route for a delivery truck

import datetime
import csv
from Hashtable import HashTable
from Package import Package
from Truck import Truck

# time_var is a placeholder value
time_var = 0


# User interface to print out information and allow user input
def user_interface():
    print('\n(っ◕‿◕)っ Welcome to the package delivery service! Choose from the following options to print (1-4)')
    print('1 - Every package and the distance each truck traveled')
    print('2 - The status of a package at a given time')
    print('3 - The status of every package at a given time')
    print('4 - Exit')
    print('***NOTE that time must be entered in the format HH:MM:SS for this program***')


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
    with open("Dataset/Package.csv") as CSV_package:
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
def pkg_get(pkg_track, cur_time=datetime.timedelta(hours=17)):
    package = pkg_hashtable.search(pkg_track)
    package.set_pkg_state(cur_time)
    print(str(package))


# Print headings for each package in a specific format
def pkg_info_printer():
    print('PackageID, Address, City, State, AreaCode, Deadline, Weight, Comments, Status, Departed, Delivered')


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

    # Choose which truck a package will ship on
    for pkg_holder in packages:
        # If 9:05 delay, then ship on 2nd truck
        if pkg_holder.comment == '905delay':
            pkg_truck2.append(pkg_holder)
        # If delayed due to label error then ship on 3rd truck (last)
        elif pkg_holder.comment == 'delay_again':
            pkg_truck3.append(pkg_holder)
        # Packages that ship together will ship early on the 1st truck
        elif pkg_holder.comment == 'together':
            pkg_truck1.append(pkg_holder)
        # Packages with End of Day go on 1st truck to ensure they get delivered
        elif pkg_holder.deadline != 'EOD':
            pkg_truck1.append(pkg_holder)
        # For packages that have a requirement to ship on truck 2
        elif pkg_holder.comment == '2ndtruck':
            pkg_truck2.append(pkg_holder)
        # Packages that don't have anywhere to go are temporarily held
        else:
            packages_extra.append(pkg_holder)

    # Loop to add package to truck 1 if it meets the conditions
    for pkg_holder in packages_extra:
        for assigned_package in pkg_truck1:
            # Make sure the distance is less than 2.1 and truck has less than 16 packages
            if space_between(assigned_package.address, pkg_holder.address) < 2.0 and len(pkg_truck1) < 16:
                # Assign the temporary package to truck 1
                pkg_truck1.append(pkg_holder)
                # Remove the package from the temporary holder
                packages_extra.remove(pkg_holder)
                break

    # Loop to add package to truck 2 if it meets the conditions
    for pkg_holder in packages_extra:
        for assigned_package in pkg_truck2:
            # Make sure the distance is less than 2.1 and truck has less than 16 packages
            if space_between(assigned_package.address, pkg_holder.address) < 2.0 and len(pkg_truck2) < 16:
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
        addr_near = 999
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
        truck.packages.append(pkg_near.package)
        # Remove the package from the temporary list as it will no longer need to be sorted
        sorting_list.remove(pkg_near)
        # Truck will now head to the nearest delivery address
        pkg_near.depart = truck.truck_depart
        # The trucks current address is the package delivery address
        truck.addr_now = pkg_near.address
        # Add the miles traveled by the truck to the running total
        truck.total_distance += addr_near
        # Package and truck will have the same times implying delivery
        truck.truck_depart += datetime.timedelta(hours=addr_near / 18)
        # Trucks leave time from location is when the package is delivered
        pkg_near.deliver_time = truck.truck_depart


class Program:
    # Create a trial run of all 3 trucks
    pkg_truck_run1 = Truck(1, [], 0, '4001 South 700 East', datetime.timedelta(hours=8))
    pkg_truck_run2 = Truck(2, [], 0, '4001 South 700 East', datetime.timedelta(hours=9, minutes=5))
    pkg_truck_run3 = Truck(3, [], 0, '4001 South 700 East', datetime.timedelta(hours=10, minutes=30))

    # Load trucks
    pkg_truck_run1.packages, pkg_truck_run2.packages, pkg_truck_run3.packages = pkg_on_truck()
    # Runs a delivery route for 3 trucks
    delivery_function(pkg_truck_run1)
    delivery_function(pkg_truck_run2)
    delivery_function(pkg_truck_run3)
    # More truck runs can be added

    # Beginning of user interaction; prompt loops until the user chooses to exit
    while True:
        # Runs the user ui routine that offers users options to choose from
        user_interface()
        # Takes in user input from the user ui options given
        option = input('Option: ')

        # Prints to screen the status of all packages and the distance traveled in miles
        if option == '1':
            print('\nStatus of all packages: ')
            print('\n1st truck: ' + str(pkg_truck_run1.total_distance) + ' miles of distance traveled ')
            # print package header
            pkg_info_printer()
            # For each package in the trucks package log, get its information
            for pkg_track in pkg_truck_run1.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=17))
            print('\nTruck2: ' + str(pkg_truck_run2.total_distance) + ' miles of distance traveled ')
            # print package header
            pkg_info_printer()
            # For each package in the trucks package log, get its information
            for pkg_track in pkg_truck_run2.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=17))
            print('\nTruck3: ' + str(pkg_truck_run3.total_distance) + ' miles of distance traveled ')
            # print package header
            pkg_info_printer()
            # For each package in the trucks package log, get its information
            for pkg_track in pkg_truck_run3.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=17))

        # Prints to screen the status of 1 package at a given time
        elif option == '2':
            pkg_track = int(input('\nEnter the package you would like to see the status of: '))
            package = pkg_hashtable.search(option)
            option = input('Enter the time you want to see: ')
            # Splits the time entered by the user with ':' as the seperator
            (h, m, s) = option.split(':')
            print(f'\nPackage {pkg_track} at ({h}:{m}:{s}) is as follows...')
            # print package header
            pkg_info_printer()
            pkg_get(pkg_track, datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)))

        # Prints to screen the status of all packages at a given time
        elif option == '3':
            option = input('\nEnter a time to see all packages at that time : ')
            # Splits the time entered by the user with ':' as the seperator
            (h, m, s) = option.split(':')
            print(f'\nHere are all the packages at the time your entered, ({h}:{m}:{s})')
            print('\n1st truck: ' + str(pkg_truck_run1.total_distance) + ' miles of distance traveled ')
            # print package header
            pkg_info_printer()
            # For each package in the trucks package log, get its information
            for pkg_track in pkg_truck_run1.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)))
            print('\n2nd truck: ' + str(pkg_truck_run2.total_distance) + ' miles of distance traveled ')
            # print package header
            pkg_info_printer()
            # For each package in the trucks package log, get its information
            for pkg_track in pkg_truck_run2.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)))
            print('\n3rd truck: ' + str(pkg_truck_run3.total_distance) + ' miles of distance traveled ')
            # print package header
            pkg_info_printer()
            # For each package in the trucks package log, get its information
            for pkg_track in pkg_truck_run3.packages:
                pkg_get(pkg_track, datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)))

        # Exits the program
        elif option == '4':
            print('\nThe program will now exit')
            exit()

        # If 1-4 is not chosen as an option, gives user an error message
        else:
            print('\nInvalid option chosen. Please try again')
