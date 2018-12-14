


class Corhort:

    def __init__(self,attendees, month, facilitators, duration):
        self.attendees = attendees
        self.month = month
        self.facilitators = facilitators
        self.duration = duration

    def add_learners(self, new_learners):
        self.attendees += new_learners


ande35 = Corhort(70, "dec", 2, "3weeks")
print(ande35.attendees)
print(ande35.month)
print(ande35.duration)
# print(ande35.add_learners(3)) 

