import datetime
from datetime import timedelta


# Class that holds all the data that the truck will use
class Truck:
    def __init__(self, truck, package, distance, location, leave_time):
        self.truck = truck
        self.package = package
        self.distance = distance
        self.location = location
        self.leave_time = leave_time

    def __str__(self):
        return '%s, %s, %s, %s, %s' % (self.truck, self.package, self.distance, self.location, self.leave_time)


'''
***Extra Notes***
truck = the truck currently delivering the package
package = the package tracked by its id
distance = the total distance traveled by the truck
location = current location of the truck
leave_time = what time the truck left with the package
'''
