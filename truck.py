class Truck:
    def __init__(self, speed, mileage, location, leave_Time, package):
        self.speed = speed
        self.mileage = mileage
        self.location = location
        self.time = leave_Time
        self.leave_Time = leave_Time
        self.package = package

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self.speed, self.mileage, self.location, self.time, self.leave_Time, self.packages)
