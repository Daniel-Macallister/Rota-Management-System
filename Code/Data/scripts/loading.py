import copy
from user import User
from rota import Rota

def save(filenumb,all_users,all_rotas,pathtype):
    file = "Data" + pathtype + "Rota_Storage" + pathtype + "rota" + str(filenumb) + ".txt"
    rotafile = open(file,"w")
    templine = ""
    temp = ""
    temp2 = []
    for i in range(0,len(all_rotas)):
        temp = all_rotas[i][0].get_rota_id()
        templine = templine + str(temp) + ","
        temp = all_rotas[i][0].get_rota_name()
        templine = templine + str(temp) + ","
        temp = all_rotas[i][0].get_rota_times()
        templine = templine + str(temp) + ","
        temp2 = copy.copy(all_rotas[i][0].get_rota_users())
        for j in range(0,len(temp2)):
            templine = templine + str(temp2[j])
            if j != (len(temp2)-1):
                templine = templine + ","
        letter = []
        for z in range(0,len(templine)):
            letter.append(templine[z])
            value = ord(letter[z]) + 132
            letter[z] = chr(value)
        templine = ""
        for y in range(0,len(letter)):
            templine = templine + letter[y]
        rotafile.write(templine)
        rotafile.write("\n")
        templine = ""
    rotafile.close()
    file = "Data" + pathtype + "User_Storage" + pathtype + "user" + str(filenumb) + ".txt"
    userfile = open(file,"w")
    templine = ""
    temp = ""
    temp2 = []
    for i in range(0,len(all_users)):
        temp = all_users[i][0].get_user_id()
        templine = templine + str(temp) + ","
        temp = all_users[i][0].get_user_name()
        templine = templine + str(temp)
        letter = []
        for z in range(0,len(templine)):
            letter.append(templine[z])
            value = ord(letter[z]) + 132
            letter[z] = chr(value)
        templine = ""
        for y in range(0,len(letter)):
            templine = templine + letter[y]
        userfile.write(templine)
        userfile.write("\n")
        templine = ""
    userfile.close()
    
def load(filenumb,all_users,all_rotas,pathtype):
    for q in range(len(all_users)):
        del all_users[q][0]
    del all_users
    all_users = []
    for w in range(len(all_rotas)):
        del all_rotas[w][0]
    del all_rotas
    all_rotas = []
    file = "Data" + pathtype + "Rota_Storage" + pathtype + "rota" + str(filenumb) + ".txt"
    rotafile = open(file,"r")
    try:
        del rotas
    except:
        pass
    rotas = []
    for i in rotafile:
        temp = i.split("\n")
        try:
            del(temp[1])
        except:
            pass
        rotas.append(temp)
    for p in range(0,len(rotas)):
        letter = []
        for o in range(0,len(rotas[p][0])):
            letter.append(rotas[p][0][o])
            value = ord(letter[o]) - 132
            letter[o] = chr(value)
        rotas[p][0] = ""
        for r in range(0,len(letter)):
            rotas[p][0] = rotas[p][0] + letter[r]
    for j in range((len(rotas))):
        temp = rotas[j][0]
        temp = temp.split(",")
        rota1 = copy.copy(temp)
        all_rotas.append([copy.copy(rota1[0]),copy.copy(rota1[1])])
        all_rotas[j][0] = Rota()
        all_rotas[j][0].set_rota_name(copy.copy(rota1[1]))
        all_rotas[j][0].set_rota_times(copy.copy(rota1[2]))
        all_rotas[j][0].reset_rota_id(copy.copy(rota1[0]))
        for m in range(3,len(rota1)):
            all_rotas[j][0].add_rota_users(copy.copy(rota1[m]))
    rotafile.close()
    file = "Data" + pathtype + "User_Storage" + pathtype + "user" + str(filenumb) + ".txt"
    userfile = open(file,"r")
    try:
        del users
    except:
        pass
    users = []
    for i in userfile:
        temp = i.split("\n")
        try:
            del(temp[1])
        except:
            pass
        users.append(temp)
    for v in range(0,len(users)):
        letter = []
        for b in range(0,len(users[v][0])):
            letter.append(users[v][0][b])
            value = ord(letter[b]) - 132
            letter[b] = chr(value)
        users[v][0] = ""
        for h in range(0,len(letter)):
            users[v][0] = users[v][0] + letter[h]
    for j in range((len(users))):
        temp = users[j][0]
        temp = temp.split(",")
        user1 = copy.copy(temp)
        all_users.append([copy.copy(user1[0]),copy.copy(user1[1])])
        all_users[j][0] = User()
        all_users[j][0].set_user_name(copy.copy(user1[1]))
        all_users[j][0].reset_user_id(copy.copy(user1[0]))
    userfile.close()
    return all_users,all_rotas
