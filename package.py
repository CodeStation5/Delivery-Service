import datetime

class Package:

    def __init__(self, ID, street, city, state, postal,end_Time,weight, notes, status,depart_Time,deliver_Time):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.postal = postal
        self.end_Time = end_Time
        self.weight = weight
        self.notes = notes
        self.status = status
        self.depart_Time = None 
        self.deliver_Time = None 

    def __str__(self):
        return "ID: %s, %-20s, %s, %s,%s, End Time: %s,%s,%s,Departure Time: %s,Delivery Time: %s" % (self.ID, self.street, self.city, self.state, self.zip, self.end_Time, self.weight, self.status, self.departureTime, self.deliveryTime)   
    #This method will update the status of a package depending on the time entered
    def statusUpdate(self, timeChange):
        if self.deliver_Time == None:
            self.status = "At the hub"
        elif timeChange < self.depart_Time:
            self.status = "At the hub"   
        elif timeChange < self.deliver_Time:
            self.status = "En route"     
        else:
            self.status = "Delivered" 
        if self.ID == 9:          #will change the address for package 9 to the correct address once it's been received
            if timeChange > datetime.timedelta (hours=10, minutes= 20):
                self.street = "410 S State St"  
                self.postal = "84111"  
            else:
                self.street = "300 State St"
                self.postal = "84103"     
