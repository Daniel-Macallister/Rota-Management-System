import copy
class User():

    def __init__(self):
        self.name = None
        self.dates = []
        self.id = None

    def set_user_name(self,name):
        self.name = name

    def get_user_name(self):
        name = self.name
        return name

    def set_user_id(self,all_users):
        self.id = (len(all_users)+1)
        all_users.append([self.id,self.name,self])

    def reset_user_id(self,userid):
        self.id = userid

    def get_user_id(self):
        userid = self.id
        return userid
        
#date in form [dd,mm,yyyy]
    def create_dates(self,starting_date):
        current_date = starting_date[:]
        (self.dates).append([starting_date,True])
        for i in range(1,16):
            current_date = copy.copy(current_date)
            current_date = update(current_date)
            (self.dates).append([current_date,True])

    def get_user_dates(self):
        user_dates = self.dates
        return user_dates

    def remove_date(self,unavailable_date):
        dates = self.get_user_dates()
        dates_position = None
        for i in range(len(dates)):
            if unavailable_date == dates[i][0]:
                  dates_position = i
        if dates_position != None:
            self.dates[dates_position][1] = False
            print(self.dates[dates_position])

def update(current_date):
    current_date[0] += 7
    if (current_date[0] > 30) and (current_date[1] in [9,4,6,11]):
        current_date[0] = current_date[0] - 30
        current_date[1] = current_date[1] + 1
    elif (current_date[0] > 31) and (current_date[1] in [1,3,5,7,8,10,12]):
        current_date[0] = current_date[0] - 31
        current_date[1] = current_date[1] + 1
    elif (current_date[1] == 2) and (current_date[0] > 29) and (current_date[2] % 4 == 0):
        current_date[0] = current_date[0] - 29
        current_date[1] = current_date[1] + 1
    elif (current_date[1] == 2) and ((current_date[0] > 28)) and (current_date[2] % 4 != 0):
        current_date[0] = current_date[0] - 28
        current_date[1] = current_date[1] + 1
    if current_date[1] > 12:
        current_date[1] = 1
        current_date[2] += 1
    return current_date
