import datetime
from datetime import timedelta


# Class that holds all the data that the truck will use
class Truck:
    def __init__(self, truck, packages, total_distance, addr_now, truck_depart):
        self.truck = truck
        self.packages = packages
        self.total_distance = total_distance
        self.addr_now = addr_now
        self.truck_depart = truck_depart

    # Defining the truck function to be used in the main class with placeholder values
    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.truck, self.packages, self.total_distance, self.addr_now, self.truck_depart)


'''
***Extra Notes***
truck = the truck currently delivering the package
package = the package tracked by its id
distance = the total distance traveled by the truck
location = current location of the truck
leave_time = what time the truck left with the package
'''
