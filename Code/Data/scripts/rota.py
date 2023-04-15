class Rota():

    def __init__(self):
        self.name = None
        self.users = []
        self.sep_am = None
        self.id = None
        self.rota = []

    def set_rota_name(self,name):
        self.name = name

    def get_rota_name(self):
        name = self.name
        return name

    def set_rota_times(self,sep):
        self.sep_am = sep

    def get_rota_times(self):
        sep = self.sep_am
        return sep

    def add_rota_users(self,userid):
        (self.users).append(userid)

    def get_rota_users(self):
        users = self.users
        if len(users) == 1 and users[0] == '':
            del users[0]
            return users
        for i in range(0,len(users)):
            temp = int(users[i])
            users[i] = temp
        self.merge(users)
        for j in range(0,len(users)):
            temp = str(users[j])
            users[j] = temp
        return users

    def lower_rota_user(self,pos):
        self.users[pos] = str(int(self.users[pos]) - 1)

    def remove_rota_users(self,user_id):
        users = self.users
        for i in range((len(users)-1),-1,-1):
            if users[i] == user_id:
                del users[i]
        self.users = users

    def set_rota_id(self,all_rotas):
        self.id = (len(all_rotas)+1)
        all_rotas.append([self.id,self.name,self])

    def reset_rota_id(self,rotaid):
        self.id = rotaid

    def get_rota_id(self):
        rotaid = self.id
        return rotaid

    def set_rota_data(self,rota_data):
        self.rota = rota_data

    def get_rota_data(self):
        rota_data = self.rota
        return rota_data

    def sort_rotas(self):
        users = self.users
        merge(users)
        self.users = None
        self.users = users

    def merge(self,array):
        if len(array) > 1:
            left = []
            right = []
            midpoint = int(len(array) / 2)
            for i in range(0,midpoint):
                left.append(array[i])
            for j in range(midpoint,len(array)):
                right.append(array[j])

            self.merge(left)
            self.merge(right)

            x = 0
            y = 0
            z = 0

            while x < len(left) and y < len(right):
                if left[x] <= right[y]:
                    array[z] = left[x]
                    x = x + 1
                else:
                    array[z] = right[y]
                    y = y + 1
                z = z + 1
            while x < len(left):
                array[z] = left[x]
                x = x + 1
                z = z + 1
            while y < len(right):
                array[z] = right[y]
                y = y + 1
                z = z + 1
