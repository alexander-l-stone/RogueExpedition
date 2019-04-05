#Minutes, Days, Hours stay the same
#Each Month is 5 Weeks
#Each Year is 10 Months

import math


#TODO: Test this file
class Timer:
    def __init__(self, minutes=0):
        self.minutes = minutes
        self.weekday_data = {0 : "Monday", 1 : "Tuesday", 2 : "Wednesday", 3 : "Thursday", 4 : "Friday", 5 : "Saturday", 6 : "Sunday"}
        self.month_data = {0 : "January", 1 : "March", 2 : "April", 3 : "May", 4 : "June", 5 : "August", 6 : "September", 7 : "October", 8 : "November", 9 : "December"}
        self.day_ending = {}
        for key in range(0,35):
            self.day_ending[key] = "th"
        self.day_ending[0] = "st"
        self.day_ending[1] = "nd"
        self.day_ending[2] = "rd"
        self.day_ending[20] = "st"
        self.day_ending[21] = "nd"
        self.day_ending[22] = "rd"
        self.day_ending[30] = "st"
        self.day_ending[31] = "nd"
        self.day_ending[32] = "rd"

    def add_hours(self, hours):
        self.minutes += 60*hours

    def add_days(self, days):
        self.minutes += days*self.add_hours(20)

    def add_weeks(self, weeks):
        self.minutes += weeks*self.add_days(7)

    def add_months(self, months):
        self.months += months*self.add_weeks(5)

    def get_hour(self):
        return (math.floor(self.minutes/60)%20)

    def get_weekday(self):
        return (math.floor(self.minutes/1440)%7)

    def get_day(self):
        return (math.floor(self.minutes/1440)%35)

    def get_week(self):
        return (math.floor(self.minutes/10080)%5)

    def get_month(self):
        return (math.floor(self.minutes/50400)%10)

    def get_year(self):
        return math.floor(self.minutes/504000)

    def get_text(self):
        return self.weekday_data[self.get_weekday()] + ", " + str(int(self.get_day() + 1)) + self.day_ending[self.get_day()] + " of " + self.month_data[self.get_month()] + " " + str(int(self.get_year())) + " A.C."

    def to_json(self):
        json_data = {
            'minutes' : self.minutes
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        timer = Timer(json_data['minutes'])
        return timer
