import datetime


# Holds the class information for packages
class Package:
    def __init__(self, package, address, city, state, postal_code, deadline, comment,
                 package_state, leave_time, deliver_time):
        self.package = package
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.deadline = deadline
        self.comment = comment
        self.package_state = package_state
        self.leave_time = leave_time
        self.deliver_time = deliver_time

    # Holds the current state of the package
    # Users can check the current status of their delivery throughout the day
    def set_pkg_state(self, time):
        # If the package has a delivery time before the current time, it's delivered
        if self.deliver_time < time:
            self.package_state = 'Delivered'
        # If the package is in a truck before the current time, it's on track to be delivered
        elif self.leave_time < time:
            self.package_state = 'Out for delivery'
        # Error check placeholder
        elif self.leave_time > 9999999:
            self.package_state = 'ERROR'
        # Otherwise the package is still at the center and not on a vehicle
        else:
            self.package_state = 'Awaiting shipping'

    # Defining the truck function to be used in the main class with placeholder values
    def __str__(self):
        return '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % (self.package, self.address, self.city,
                                                           self.state, self.postal_code, self.deadline,
                                                           self.comment, self.package_state,
                                                           self.leave_time, self.deliver_time)


'''
***Extra Notes***
package = the package tracked by its id
address = address of the recipient
city = city of the recipient
state = state/province of the recipient
postal_code = postal code or area code of the recipient
d
c
package_state = the status of the package, whether it's delivered, being delivered or not out for delivery
leave_time = what time the truck left with the package
deliver_time = what time the package was delivered
'''
