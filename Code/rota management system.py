import sys, random, copy, platform, time, subprocess, math
import tkinter as tk
global pathtype
subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
pathtype = "\\" if platform.system() == "Windows" else "/"
sys.path.insert(1,'Data' + pathtype + 'scripts')
from Document import create_docx
from user import User
from rota import Rota
from user import update
from loading import *

global all_users
all_users = []
global all_rotas
all_rotas = []
global rotas
rotas = []
global rota1
rota1 = []
global users
users = []
global user1
user1 = []
global list_of_dates
list_of_dates = []
global return_address
return_address = ""
global filenumb
filenumb = ""
global filetype
filetype = ""

class MenuPage(tk.Frame):
    def __init__(self, window, controller):
        tk.Frame.__init__(self, window)
        title_image = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "title.png")
        title = tk.Label(self,
                        background = "white",
                        image = title_image
                        )
        title.image = title_image
        title.grid(column=20,row=370)
        New_Sys_Button_Image = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "NewSystemButton.png")
        new_sys_button = tk.Button(self,
                                   text = "Create a New Rota System",
                                   image = New_Sys_Button_Image,
                                   command = lambda : MenuPage.name_rota(self,controller)
                                   )
        new_sys_button.image = New_Sys_Button_Image
        new_sys_button.grid(column=20,row=600)
        Old_Sys_Button_Image = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "OldSystemButton.png")
        old_sys_button = tk.Button(self,
                                   text = "Load an old Rota System",
                                   image = Old_Sys_Button_Image,
                                   command = lambda : MenuPage.select_rota(self,controller)
                                   )
        old_sys_button.image = Old_Sys_Button_Image
        old_sys_button.grid(column=20,row=800)
        
        exit_picture = tk.PhotoImage(file="Data" + pathtype + "assets" + pathtype + "exit_button.png")
        leave = tk.Button(self,
                          command = lambda : self.close(),
                          image = exit_picture
                          )
        leave.image = exit_picture
        leave.grid(column=1420,row=0,)

    def close(self):
        window.destroy()

    def select_rota(self,controller):
        old_sys_select = tk.Entry(self,
                                  bg = "white",
                                  fg = "gray23",
                                  width = 35
                                  )
        old_sys_select.grid(column=30,row=800)
        old_sys_select.insert(0,"Enter the number of the rota system")

        load_button = tk.Button(self,
                                text = "load",
                                bg = "gray23",
                                fg = "white",
                                command = lambda : MenuPage.loadrotab(self,controller,old_sys_select,error_text,load_button)
                                )
        load_button.grid(column = 40,row=800)

        error_text = tk.Label(self,
                              text="",
                              fg = "red",
                              )
        error_text.grid(column = 50, row = 800)

    def loadrotab(self,controller,old_sys_select,error_text,load_button):
        global filenumb
        filenumb = old_sys_select.get()
        file = "Data" + pathtype + "Rota_Storage" + pathtype + "rota" + str(filenumb) + ".txt"
        try:
            testfile = open(file,"r")
        except FileNotFoundError:
            error_text["text"] = "Rota system cannot be found in files"
        else:
            testfile.close()
            global all_users
            global all_rotas
            all_users,all_rotas = load(filenumb,all_users,all_rotas,pathtype)
            load_button.grid_forget()
            old_sys_select.grid_forget()
            MainView.show(controller,LoadPage)

    def newrotab(self,controller,new_sys_select,error_text_2,create_button):
        global filenumb
        filenumb = new_sys_select.get()
        file = "Data" + pathtype + "Rota_Storage" + pathtype + "rota" + str(filenumb) + ".txt"
        try:
            testfile = open(file,"r")
        except FileNotFoundError:
            global all_rotas
            global all_users
            for q in range(0,len(all_rotas)):
                del all_rotas[q][0]
            del all_rotas
            all_rotas = []
            for w in range(0,len(all_users)):
                del all_users[w][0]
            del all_users
            all_users = []
            create_button.grid_forget()
            new_sys_select.grid_forget()
            MainView.show(controller,NewSystemPage)
        else:
            testfile.close()
            error_text_2["text"] = "A rota system already exists with this name"
            
    def name_rota(self,controller):
        new_sys_select = tk.Entry(self,
                                  text = "Enter the number of the rota system you want to create",
                                  bg = "white",
                                  fg = "gray23",
                                  width = 35
                                  )
        new_sys_select.grid(column=30,row=600)
        new_sys_select.insert(0,"Enter the number of the rota system you want to create")

        create_button = tk.Button(self,
                                text = "create",
                                bg = "gray23",
                                fg = "white",
                                command = lambda : MenuPage.newrotab(self,controller,new_sys_select,error_text_2,create_button)
                                )
        create_button.grid(column = 40,row=600)

        error_text_2 = tk.Label(self,
                                text="",
                                fg = "red",
                                )
        error_text_2.grid(column = 50, row = 600)        


class LoadPage(tk.Frame):
    def __init__(self, window, controller):
        tk.Frame.__init__(self,window)

        return_arrow = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "return_arrow.png")
        return_button = tk.Button(self,
                                  image = return_arrow,
                                  command = lambda : self.returning(controller),
                                  text = "return"
                                  )
        return_button.image = return_arrow
        return_button.grid(column = 0, row = 100)
        

        
        exit_picture = tk.PhotoImage(file="Data" + pathtype + "assets" + pathtype + "exit_button.png")
        leave = tk.Button(self,
                          command = lambda : self.close(),
                          image = exit_picture
                          )
        leave.image = exit_picture
        leave.grid(column=1000,row=0,)

        edit_rotas_image = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "EditSystemButton.png")
        edit_button = tk.Button(self,
                                command = lambda : self.edit_old_rota(controller),
                                text = "edit the current rota system",
                                image = edit_rotas_image
                                )
        edit_button.image = edit_rotas_image
        edit_button.grid(column = 100,row = 20)

        run_rota_image = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "GenerateRotasButton.png")
        run_rota_button = tk.Button(self,
                                    command = lambda : self.run_old_rota(controller),
                                    text = "create a set of rotas",
                                    image = run_rota_image
                                    )
        run_rota_button.image = run_rota_image
        run_rota_button.grid(row = 100,column = 60)

        view_data_image = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "ViewAnalyticsButton.png")
        view_data_button = tk.Button(self,
                                     command = lambda : self.view_user_data(controller),
                                     text = "View User Data",
                                     image = view_data_image
                                     )
        view_data_button.image = view_data_image
        view_data_button.grid(column = 100,row = 100)
                                  

    def close(self):
        window.destroy()

    def returning(self,controller):
        MainView.show(controller,MenuPage)

    def edit_old_rota(self,controller):
        MainView.show(controller,EditRotaPage)

    def run_old_rota(self,controller):
        MainView.show(controller,CreateRotasPage)

    def view_user_data(self,controller):
        MainView.show(controller,AnalysisPage)

class NewSystemPage(tk.Frame):
    def __init__(self, window, controller):
        tk.Frame.__init__(self,window)

        create_rota_image_b = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "NewSysNewRotaButton.png")
        create_rota_button_b = tk.Button(self,
                                         text = "create a new rota for this new system",
                                         command = lambda :self.create_new_rota_c(controller,NewSystemPage),
                                         image = create_rota_image_b
                                         )
        create_rota_button_b.image = create_rota_image_b
        create_rota_button_b.grid(row = 10, column = 10)
        create_user_image_b = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "NewSysNewUserButton.png")
        create_user_button_b = tk.Button(self,
                                         text = "create a new rota for this new system",
                                         command = lambda : self.create_new_user_c(controller,NewSystemPage),
                                         image = create_user_image_b
                                         )
        create_user_button_b.image = create_user_image_b
        create_user_button_b.grid(row = 20, column = 10)

        return_arrow = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "return_arrow.png")
        return_button = tk.Button(self,
                                  text = "go back",
                                  command = lambda : self.main_page(controller),
                                  image = return_arrow
                                  )
        return_button.image = return_arrow
        return_button.grid(row = 1000,column = 0)
        
        exit_picture = tk.PhotoImage(file="Data" + pathtype + "assets" + pathtype + "exit_button.png")
        leave = tk.Button(self,
                          command = lambda : self.close(),
                          image = exit_picture
                          )
        leave.image = exit_picture
        leave.grid(column=1000,row=0,)

    def main_page(self,controller):
        MainView.show(controller,MenuPage,NewSystemPage)

    def create_new_rota_c(self,controller,NewSystemPage):
        global return_address
        return_address = "NewSystemPage"
        MainView.show(controller,AddRotaPage)

    def create_new_user_c(self,controller,NewSystemPage):
        global return_address
        return_address = "NewSystemPage"
        MainView.show(controller,AddUserPage)

    def close(self):
        window.destroy()
        
class EditRotaPage(tk.Frame):
    def __init__(self, window, controller):
        tk.Frame.__init__(self,window)

        create_rota_image = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "OldSysNewRotaButton.png")
        create_rota_button = tk.Button(self,
                                       text = "create a new rota for the current system",
                                       command = lambda : self.createnewrotab(controller,EditRotaPage),
                                       image = create_rota_image
                                       )
        create_rota_button.image = create_rota_image
        create_rota_button.grid(row = 10,column = 10)
        create_user_image = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "OldSysNewUserButton.png")
        create_user_button = tk.Button(self,
                                       text = "create a new user for the system",
                                       command = lambda : self.createnewuserb(controller,EditRotaPage),
                                       image = create_user_image
                                       )
        create_user_button.image = create_user_image
        create_user_button.grid(row = 10,column = 20)
        delete_user_image = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "DeleteUserImage.png")
        delete_user_button = tk.Button(self,
                                       text = "Delete a user from the system",
                                       command = lambda : self.removeuserb(controller,EditRotaPage),
                                       image = delete_user_image
                                       )
        delete_user_button.grid(row = 20,column = 20)
        delete_user_button.image = delete_user_image
        delete_rota_image = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "DeleteRotaImage.png")
        delete_rota_button = tk.Button(self,
                                       command = lambda : self.removerotab(controller,EditRotaPage),
                                       image = delete_rota_image
                                       )
        delete_rota_button.image = delete_rota_image
        delete_rota_button.grid(row = 20, column = 10)

        return_arrow = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "return_arrow.png")
        return_button = tk.Button(self,
                                  text = "go back",
                                  command = lambda : self.load_page(controller),
                                  image = return_arrow
                                  )
        return_button.image = return_arrow
        
        return_button.grid(row = 1000,column = 0)
        
        exit_picture = tk.PhotoImage(file="Data" + pathtype + "assets" + pathtype + "exit_button.png")
        leave = tk.Button(self,
                          command = lambda : self.close(),
                          image = exit_picture
                          )
        leave.image = exit_picture
        leave.grid(column=1000,row=0,)

    def close(self):
        window.destroy()

    def load_page(self,controller):
        MainView.show(controller,LoadPage)

    def removeuserb(self,controller,EditRotaPage):
        MainView.show(controller,RemoveUserPage)

    def removerotab(self,controller,EditRotaPage):
        MainView.show(controller,RemoveRotaPage)

    def createnewuserb(self,controller,EditRotaPage):
        global return_address
        return_address = "EditRotaPage"
        MainView.show(controller,AddUserPage)

    def createnewrotab(self,controller,EditRotaPage):
        global return_address
        return_address = "EditRotaPage"
        MainView.show(controller,AddRotaPage)

class AddUserPage(tk.Frame):
    def __init__(self,window,controller):
        tk.Frame.__init__(self,window)
        self.Add_Rota_User = None
        self.Add_Rota_User_Button = None
        self.Add_Rota_User_List = None

        user_name_enter = tk.Entry(self,
                                   text = "User Name"
                                   )
        user_name_enter.grid(row=100,column=100)
        user_name_text = tk.Label(self,
                                  text = "Enter the Name of the User"
                                  )
        user_name_text.grid(row=100,column = 50)
        
        exit_picture = tk.PhotoImage(file="Data" + pathtype + "assets" + pathtype + "exit_button.png")
        leave = tk.Button(self,
                          command = lambda : self.close(),
                          image = exit_picture
                          )
        leave.image = exit_picture
        leave.grid(column=1420,row=0)
        begin_user_button = tk.Button(self,
                                      text = "Press Me",
                                      command = lambda : self.updateU(begin_user_button)
                                      )
        begin_user_button.grid(row = 150, column = 50)

        return_arrow = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "return_arrow.png")
        Return_Button = tk.Button(self,
                                  text = "Go Back",
                                  command = lambda : self.reset_page(begin_user_button,controller),
                                  image = return_arrow
                                  )
        Return_Button.image = return_arrow
        Return_Button.grid(row = 2000,column = 0)

        save_user_button = tk.Button(self,
                                     text = "Save this User to the system",
                                     command = lambda : self.save_data(user_name_enter,begin_user_button,controller)
                                     )
        save_user_button.grid(row = 1000, column = 1000)

    def updateU(self,begin_user_button):
        rotas_list = []
        try:
            begin_user_button.grid_forget()
        except:
            pass
        for i in range(0,len(all_rotas)):
            rotas_list.append(all_rotas[i][1])
        if len(rotas_list) == 0:
            rotas_list.append("-")
        variable = tk.StringVar(window)
        variable.set("Select a Rota to add this User to")
        self.Add_Rota_User = tk.OptionMenu(self,
                                      variable,
                                      *rotas_list
                                      )
        self.Add_Rota_User.config(bg = "Cyan")
        self.Add_Rota_User.grid(row = 300,column = 300)

        self.Add_Rota_User_List = tk.Label(self,
                                      text = None
                                      )
        self.Add_Rota_User_List.grid(row = 400, column = 400)

        self.Add_Rota_User_Button = tk.Button(self,
                                         text = "Add the User to the select Rota",
                                         command = lambda : save_rota(self,rotas_list,variable)
                                         )
        self.Add_Rota_User_Button.grid(row = 400,column = 300)
        
        def save_rota(self,rotas_list,variable):
            temp = variable.get()
            if temp != "Select a Rota to add this User to":
                temp2 = self.Add_Rota_User_List.cget('text')
                temp3 = temp2 + "\n" + temp
                self.Add_Rota_User_List.config(text = temp3)
                for i in range(0,len(rotas_list)):
                    if rotas_list[i] == temp:
                        del rotas_list[i]
                        break
                refresh_options(rotas_list,variable)
                
        def refresh_options(rotas_list,variable):
            variable.set("Select a Rota to add this User to")
            self.Add_Rota_User['menu'].delete(0, 'end')
            for i in rotas_list:
                self.Add_Rota_User['menu'].add_command(label=i, command=tk._setit(variable, i))

    def reset_page(self,begin_user_button,controller):
        begin_user_button.grid(row = 150,column = 50)
        try:
            self.Add_Rota_User.grid_forget()
            self.Add_Rota_User_List.grid_forget()
            self.Add_Rota_User_Button.grid_forget()
        except:
            pass
        self.leave(controller)

    def save_data(self,user_name_enter,begin_user_button,controller):
        user_name = user_name_enter.get()
        if user_name == "" or user_name == None:
            return
        for i in range(0,len(all_users)):
            if user_name == all_users[i][1]:
                return
        user_rotas = []
        temp_list = self.Add_Rota_User_List.cget('text')
        user_rotas = temp_list.splitlines()
        if len(user_rotas) != 0:
            del user_rotas[0]
        self.add_user(user_rotas,user_name)
        save(filenumb,all_users,all_rotas,pathtype)
        self.reset_page(begin_user_button,controller)

    def add_user(self,user_rotas,user_name):
        global all_users
        global all_rotas
        user_id = len(all_users) + 1
        all_users.append([user_id,user_name])
        for i in range(len(all_rotas)):
            if all_rotas[i][1] in(user_rotas):
                all_rotas[i][0].add_rota_users(user_id)
        position = len(all_users)-1
        all_users[position][0] = User()
        all_users[position][0].set_user_name(user_name)
        all_users[position][0].reset_user_id(user_id)

        
    def close(self):
        window.destroy()        
        
    def leave(self,controller):
        if return_address == "EditRotaPage":
            MainView.show(controller,EditRotaPage)
        if return_address == "NewSystemPage":
            MainView.show(controller,NewSystemPage)


class AddRotaPage(tk.Frame):
    def __init__(self, window, controller):
        tk.Frame.__init__(self,window)
        self.rota_times = ""
        self.Add_User_Rota = None
        self.Add_User_Rota_AM = None
        self.Add_User_Rota_PM = None
        self.Add_User_Rota_List = None
        self.Add_User_Rota_List_AM = None
        self.Add_User_Rota_List_PM = None
        self.Add_User_Rota_Button = None
        self.Add_User_Rota_Button_AM = None
        self.Add_User_Rota_Button_PM = None
        
        combined_button = tk.Button(self,
                                    text = "combined AM and PM",
                                    command = lambda : self.updateC(seperate_button,combined_button)
                                    )
        combined_button.grid(row = 100, column = 150)
        seperate_button = tk.Button(self,
                                    text = "seperate AM and PM",
                                    command = lambda : self.updateS(seperate_button,combined_button)
                                    )
        seperate_button.grid(row = 150,column = 150)
        return_arrow = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "return_arrow.png")
        cancle_button = tk.Button(self,
                                  text = "return to previous page",
                                  image = return_arrow,
                                  command = lambda : self.reset_page(seperate_button,combined_button,controller)
                                  )
        cancle_button.image = return_arrow
        cancle_button.grid(row=1000,column = 0)

        rota_name_enter = tk.Entry(self,
                                   text = "Rota Name",
                                   )
        rota_name_enter.grid(row = 100,column = 100)
        rota_name_title = tk.Label(self,
                                   text ="Input Rota Name"
                                   )
        rota_name_title.grid(row=100,column = 0)

        continue_button = tk.Button(self,
                                    text = "continue",
                                    command = lambda : self.save_data(rota_name_enter,seperate_button,combined_button,controller)
                                    )
        continue_button.grid(row = 1500,column = 50)

        exit_picture = tk.PhotoImage(file="Data" + pathtype + "assets" + pathtype + "exit_button.png")
        leave = tk.Button(self,
                          command = lambda : self.close(),
                          image = exit_picture
                          )
        leave.image = exit_picture
        leave.grid(column=1420,row=0)
        
        
    def updateC(self,seperate_button,combined_button):
        users_list = []
        try:
            seperate_button.grid_forget()
            combined_button.grid_forget()
        except:
            pass
        for i in range(0,len(all_users)):
            users_list.append(all_users[i][1])
        if len(users_list) == 0:
            users_list.append("-")
        variable = tk.StringVar(window)
        variable.set("Select a User to add to the Rota")
        self.Add_User_Rota = tk.OptionMenu(self,
                                      variable,
                                      *users_list
                                      )
        self.Add_User_Rota.config(bg = "Cyan")
        self.Add_User_Rota.grid(row = 300,column = 300)

        self.Add_User_Rota_List = tk.Label(self,
                                      text = None
                                      )
        self.Add_User_Rota_List.grid(row = 400, column = 400)

        self.Add_User_Rota_Button = tk.Button(self,
                                         text = "Add the selected user to the rota",
                                         command = lambda : save_user(self,users_list,variable)
                                         )
        self.Add_User_Rota_Button.grid(row = 400,column = 300)

        self.rota_times = "Combined"

        def save_user(self,users_list,variable):
            temp = variable.get()
            if temp != "Select a User to add to the Rota":
                temp2 = self.Add_User_Rota_List.cget('text')
                temp3 = temp2 + "\n" + temp
                self.Add_User_Rota_List.config(text = temp3)
                for i in range(0,len(users_list)):
                    if users_list[i] == temp:
                        del users_list[i]
                        break
                refresh_options(users_list,variable)
                
        def refresh_options(users_list,variable):
            variable.set("Select a User to Add to the Rota")
            self.Add_User_Rota['menu'].delete(0, 'end')
            for i in users_list:
                self.Add_User_Rota['menu'].add_command(label=i, command=tk._setit(variable, i))    

    def updateS(self,seperate_button,combined_button):
        users_list_AM = []
        try:
            seperate_button.grid_forget()
            combined_button.grid_forget()
        except:
            pass
        for i in range(0,len(all_users)):
            users_list_AM.append(all_users[i][1])
        if len(users_list_AM) == 0:
            users_list.append("-")
        variable_AM = tk.StringVar(window)
        variable_AM.set("Select a User to add to the AM Rota")
        self.Add_User_Rota_AM = tk.OptionMenu(self,
                                         variable_AM,
                                         *users_list_AM
                                         )
        self.Add_User_Rota_AM.config(bg = "Cyan")
        self.Add_User_Rota_AM.grid(row = 350,column = 300)
        
        self.Add_User_Rota_List_AM = tk.Label(self,
                                      text = None
                                      )
        self.Add_User_Rota_List_AM.grid(row = 450, column = 300)

        self.Add_User_Rota_Button_AM = tk.Button(self,
                                         text = "Add the selected user to the AM rota",
                                         command = lambda : save_userAM(self,users_list_AM,variable_AM)
                                         )
        self.Add_User_Rota_Button_AM.grid(row = 400,column = 300)
        
        users_list_PM = []
        for i in range(0,len(all_users)):
            users_list_PM.append(all_users[i][1])
        if len(users_list_PM) == 0:
            users_list_PM.append("-")
        variable_PM = tk.StringVar(window)
        variable_PM.set("Select a User to add to the PM Rota")
        self.Add_User_Rota_PM = tk.OptionMenu(self,
                                         variable_PM,
                                         *users_list_PM
                                         )
        self.Add_User_Rota_PM.config(bg = "Cyan")
        self.Add_User_Rota_PM.grid(row = 350,column = 350)
        
        self.Add_User_Rota_List_PM = tk.Label(self,
                                      text = None
                                      )
        self.Add_User_Rota_List_PM.grid(row = 450, column = 350)

        self.Add_User_Rota_Button_PM = tk.Button(self,
                                         text = "Add the selected user to the PM rota",
                                         command = lambda : save_userPM(self,users_list_PM,variable_PM)
                                         )
        self.Add_User_Rota_Button_PM.grid(row = 400,column = 350)

        self.rota_times = "Seperate"
        
        def save_userAM(self,users_list_AM,variable_AM):
            temp = variable_AM.get()
            if temp != "Select a User to Add to the AM Rota":
                temp2 = self.Add_User_Rota_List_AM.cget('text')
                temp3 = temp2 + "\n" + temp
                self.Add_User_Rota_List_AM.config(text = temp3)
                for i in range(0,len(users_list_AM)):
                    if users_list_AM[i] == temp:
                        del users_list_AM[i]
                        break
                refresh_optionsAM(users_list_AM,variable_AM)
            
        def refresh_optionsAM(users_list_AM,variable_AM):
            variable_AM.set("Select a User to Add")
            self.Add_User_Rota_AM['menu'].delete(0, 'end')
            for i in users_list_AM:
                self.Add_User_Rota_AM['menu'].add_command(label=i, command=tk._setit(variable_AM, i)) 

        def save_userPM(self,users_list_PM,variable_PM):
            temp = variable_PM.get()
            if temp != "Select a User to Add to the PM Rota":
                temp2 = self.Add_User_Rota_List_PM.cget('text')
                temp3 = temp2 + "\n" + temp
                self.Add_User_Rota_List_PM.config(text = temp3)
                for i in range(0,len(users_list_PM)):
                    if users_list_PM[i] == temp:
                        del users_list_PM[i]
                        break
                refresh_optionsPM(users_list_PM,variable_PM)
            
        def refresh_optionsPM(users_list_PM,variable_PM):
            variable_PM.set("Select a User to Add to the PM Rota")
            self.Add_User_Rota_PM['menu'].delete(0, 'end')
            for i in users_list_PM:
                self.Add_User_Rota_PM['menu'].add_command(label=i, command=tk._setit(variable_PM, i))
                
    def close(self):
        window.destroy()

    def save_data(self,rota_name_enter,seperate_button,combined_button,controller):
        rota_name = rota_name_enter.get()
        if rota_name == "" or rota_name == None:
            return
        for i in range(0,len(all_rotas)):
            if all_rotas[i][1] == rota_name:
                return
        for j in range(0,len(all_rotas)):
            if all_rotas[j][1] == (rota_name + " AM"):
                return
        for k in range(0,len(all_rotas)):
            if all_rotas[k][1] == (rota_name + " PM"):
                return
        rota_users = []
        rota_users_AM = []
        rota_users_PM = []
        if self.rota_times == "Combined":
            temp_list = self.Add_User_Rota_List.cget('text')
            rota_users = temp_list.splitlines()
            try:
                del rota_users[0]
            except:
                pass
        if self.rota_times == "Seperate":
            temp_list_AM = self.Add_User_Rota_List_AM.cget('text')
            rota_users_AM = temp_list_AM.splitlines()
            try:
                del rota_users_AM[0]
            except:
                pass
            temp_list_PM = self.Add_User_Rota_List_PM.cget('text')
            rota_users_PM = temp_list_PM.splitlines()
            try:
                del rota_users_PM[0]
            except:
                pass
        self.add_rota(rota_users,rota_users_AM,rota_users_PM,rota_name)
        save(filenumb,all_users,all_rotas,pathtype)
        self.reset_page(seperate_button,combined_button,controller)
            
    def reset_page(self,seperate_button,combined_button,controller):
        combined_button.grid(row = 100, column = 150)
        seperate_button.grid(row = 150,column = 150)
        if self.rota_times == "Combined":
            self.Add_User_Rota.grid_forget()
            self.Add_User_Rota_List.grid_forget()
            self.Add_User_Rota_Button.grid_forget()
        elif self.rota_times == "Seperate":
            self.Add_User_Rota_AM.grid_forget()
            self.Add_User_Rota_PM.grid_forget()
            self.Add_User_Rota_List_AM.grid_forget()
            self.Add_User_Rota_List_PM.grid_forget()
            self.Add_User_Rota_Button_AM.grid_forget()
            self.Add_User_Rota_Button_PM.grid_forget()
        self.leave(controller)
    
    def leave(self,controller):
        if return_address == "EditRotaPage":
            MainView.show(controller,EditRotaPage)
        if return_address == "NewSystemPage":
            MainView.show(controller,NewSystemPage)

    def add_rota(self,rota_users,rota_users_AM,rota_users_PM,rota_name):
        global all_rotas
        global all_users
        if self.rota_times == "Seperate":
            name = rota_name + " AM"
            rota_users = copy.copy(rota_users_AM)
            looped = True
        else:
            name = rota_name
            looped = False
        loop = True
        while loop == True:
            rota_id = len(all_rotas) + 1
            position = len(all_rotas)
            all_rotas.append([rota_id,name])
            all_rotas[position][0] = Rota()
            all_rotas[position][0].set_rota_name(name)
            all_rotas[position][0].reset_rota_id(rota_id)
            for i in range(len(all_users)):
                if all_users[i][1] in(rota_users):
                    user_id = all_users[i][0].get_user_id()
                    all_rotas[position][0].add_rota_users(user_id)
            all_rotas[position][0].set_rota_times(self.rota_times)
            if looped == False:
                loop = False
            elif looped == True:
                name = rota_name + " PM"
                del rota_users
                rota_users = copy.copy(rota_users_PM)
                looped = False

class CreateRotasPage(tk.Frame):
    def __init__(self, window, controller):
        tk.Frame.__init__(self, window)
        self.Select_Start_User_L = None
        self.Select_Start_User_B = None
        self.counter = 0
        global all_users
        starting_users = []
        self.unavailble_list = []
        Unavailble_Button = None
        
        title = tk.Label(self,
                         text = "Create your set of rotas"
                         )
        title.grid(row = 100,column = 100)
        start_button = tk.Button(self,
                                 text = "Press me to begin",
                                 command = lambda : self.starting_user(start_button,Rota_Title,variable_user,starting_users,Select_Day,Select_Month,Select_Year,Un_Day,Un_Month,Un_Year,variable_unday,variable_unmonth,Unavailble_Button,Select_Un_User,variable_unavailble,controller)
                                 )
        start_button.grid(row = 200,column = 200)
        Rota_Title = tk.Label(self,
                              text = "",
                              )
        Rota_Title.grid(row = 150,column = 150)

        days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        variable_day = tk.StringVar(window)
        variable_day.set("Select the day you want the rota to start")
        Select_Day = tk.OptionMenu(self,
                                   variable_day,
                                   *days
                                   )
        Select_Day.config(bg = "Cyan")
        Select_Day.grid(row = 110,column = 100)
        months = [1,2,3,4,5,6,7,8,9,10,11,12]
        variable_month = tk.StringVar(window)
        variable_month.set("Select the month you want the rota to start")
        Select_Month = tk.OptionMenu(self,
                                     variable_month,
                                     *months
                                     )
        Select_Month.config(bg = "Cyan")
        Select_Month.grid(row = 110,column = 110)                
        Select_Year = tk.Entry(self,
                               text = "Enter the year you want the rota to start"
                               )
        Select_Year.grid(row = 110,column = 120)
        variable_user = tk.StringVar(window)
        self.user_in_rota = [' ']
        self.Select_Start_User_L = tk.OptionMenu(self,
                                            variable_user,
                                            *self.user_in_rota)
        self.Select_Start_User_L.grid(column = 200,row = 150)

        unavailble_days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        variable_unday = tk.StringVar(window)
        variable_unday.set("Select the day of unavailibility")
        Un_Day = tk.OptionMenu(self,
                               variable_unday,
                               *unavailble_days
                               )
        Un_Day.config(bg = "Cyan")
        unavailble_months = [1,2,3,4,5,6,7,8,9,10,11,12]
        variable_unmonth = tk.StringVar(window)
        variable_unmonth.set("Select the month of unavailbility")
        Un_Month = tk.OptionMenu(self,
                                 variable_unmonth,
                                 *unavailble_months
                                 )
        Un_Month.config(bg = "Cyan")             
        Un_Year = tk.Entry(self,
                           text = "Enter the year of unavailbility"
                           )
        variable_unavailble = tk.StringVar(window)
        unavailble_users = ['']
        Select_Un_User = tk.OptionMenu(self,
                                        variable_unavailble,
                                        *unavailble_users
                                        )
        Select_Un_User.grid(column = 200,row = 150)
        return_button = tk.Button(self,
                                  text = "go back",
                                  command = lambda : self.go_back(start_button,Rota_Title,variable_user,variable_day,variable_month,controller)
                                  )
        return_button.grid(row = 1000,column = 0)
        exit_picture = tk.PhotoImage(file="Data" + pathtype + "assets" + pathtype + "exit_button.png")
        leave = tk.Button(self,
                          command = lambda : self.close(),
                          image = exit_picture
                          )
        leave.image = exit_picture
        leave.grid(column=1420,row=0)
        
    def close(self):
        window.destroy()  
        
    def go_back(self,start_button,Rota_Title,variable_user,variable_day,variable_month,controller):
        self.counter = 0
        try:
            self.Select_Start_User_B.grid_forget()
        except:
            pass
        self.Select_Start_User_L['menu'].delete(0, 'end')
        variable_user.set("")
        variable_day.set("Select the day you want the rota to start")
        variable_month.set("Select the month you want the rota to start")
        Rota_Title.config(text = "")
        start_button.grid(row = 200,column = 200)
        MainView.show(controller,LoadPage)

    def starting_user(self,start_button,Rota_Title,variable_user,starting_users,Select_Day,Select_Month,Select_Year,Un_Day,Un_Month,Un_Year,variable_unday,variable_unmonth,Unavailble_Button,Select_Un_User,variable_unavailble,controller):
        global all_rotas
        global all_users
        print(all_users)
        start_button.grid_forget()
        starter = self.Select_Start_User_L.cget('text')
        if starter != "":
            starting_users.append(starter)
        if self.counter == len(all_rotas):
            self.counter = 0
            self.Select_Start_User_B.grid_forget()
            self.Select_Start_User_L['menu'].delete(0, 'end')
            variable_user.set("")
            start_button.grid(row = 150,column = 150)
            Rota_Title.config(text = "")
            day = int(Select_Day.cget('text'))
            month = int(Select_Month.cget('text'))
            year = int(Select_Year.get())
            current_date = [day,month,year]
            CreateRotasPage.generate_rotas(self,all_rotas,current_date,starting_users,controller)
        else:
            try:
                Un_Day.grid_forget()
                Un_Month.grid_forget()
                Un_Year.grid_forget()
                Unavailble_Button.grid_forget()
            except:
                pass
            Select_Un_User['menu'].delete(0, 'end')
            variable_unavailble.set("Select the person who is not availble")
            try:
                del unavailble_users
            except:
                pass
            unavailble_users = []
            for m in range(0,len(all_users)):
                unavailble_users.append(all_users[m][1])
            for i in unavailble_users:
                Select_Un_User['menu'].add_command(label=i, command=tk._setit(variable_unavailble, i))        
            Select_Un_User.grid(column = 100,row = 150)
            Unavailble_Button = tk.Button(self,
                                          text = "press to confirm the unavailbility",
                                          command = lambda : CreateRotasPage.add_unavailbility(self,Un_Day,Un_Month,Un_Year,Select_Un_User)
                                          )
            Unavailble_Button.grid(row = 500,column = 130)
            Un_Day.grid(row = 500,column = 100)
            Un_Month.grid(row = 500,column = 110)
            Un_Year.grid(row = 500,column = 120)
            rota_name = all_rotas[self.counter][0].get_rota_name()
            Rota_Title.config(text = rota_name)
            users_in_rota = all_rotas[self.counter][0].get_rota_users()
            if len(users_in_rota) == 0:
                self.counter = self.counter + 1
            else:
                try:
                    del self.user_in_rota
                except:
                    pass
                self.user_in_rota = []
                for i in range(0,len(users_in_rota)):
                    temp = int(users_in_rota[i]) - 1
                    temp2 = all_users[temp][0].get_user_name()
                    self.user_in_rota.append(temp2)
                self.Select_Start_User_L['menu'].delete(0, 'end')
                variable_user.set(self.user_in_rota[0])
                for i in self.user_in_rota:
                    self.Select_Start_User_L['menu'].add_command(label=i, command=tk._setit(variable_user, i))        
                self.Select_Start_User_L.grid(column = 200,row = 150)
                self.counter = self.counter + 1
                try:
                    self.Select_Start_User_B.grid_forget()
                except:
                    pass
                self.Select_Start_User_B = tk.Button(self,
                                                text = "Press me when you have selected the user you want",
                                                command = lambda : CreateRotasPage.starting_user(self,start_button,Rota_Title,variable_user,starting_users,Select_Day,Select_Month,Select_Year,Un_Day,Un_Month,Un_Year,variable_unday,variable_unmonth,Unavailble_Button,Select_Un_User,variable_unavailble,controller)
                                                )
            if self.counter == len(all_rotas):
                self.Select_Start_User_B['text'] = "Press here to Generate the set of rotas"
            self.Select_Start_User_B.grid(row=150,column = 250)
        return starting_users

    def add_unavailbility(self,Un_Day,Un_Month,Un_Year,Select_Un_User):
        day = int(Un_Day.cget('text'))
        month = int(Un_Month.cget('text'))
        year = int(Un_Year.get())
        unavailble_day = [day,month,year]
        user = Select_Un_User.cget('text')
        self.unavailble_list.append([user,unavailble_day])
        

    def generate_rotas(self,all_rotas,current_date,starting_users,controller):
        global list_of_dates
        global all_users
        CreateRotasPage.generate_dates(self,all_users,current_date)
        all_users = CreateRotasPage.unavailble_dates(self,all_users)
        rota_counter = 0
        for i in range(len(all_rotas)):
            print(starting_users)
            print(all_users)
            CreateRotasPage.create_rota(self,all_rotas,all_users,rota_counter,starting_users)
            rota_counter += 1
        MainView.show(controller,DisplayPage)

    def unavailble_dates(self,all_users):
        print("unavailble_dates")
        print(self.unavailble_list)
        for n in range(0,len(self.unavailble_list)):
            user = self.unavailble_list[n][0]
            userid = None
            for i in range(len(all_users)):
                if all_users[i][1] == user:
                    userid = i
            if userid != None:
                unavailable_date = self.unavailble_list[n][1]
                all_users[userid][0].remove_date(unavailable_date)
        return all_users

    def generate_dates(self,all_users,current_date):
        list_of_dates.append(copy.copy(current_date))
        starting_date = copy.copy(current_date)
        for i in range(1,16):
            current_date = update(current_date)
            list_of_dates.append(copy.copy(current_date))
        current_date = starting_date
        for j in range(len(all_users)):
            all_users[j][0].create_dates(current_date)

    def create_rota(self,all_rotas,all_users,rota_counter,starting_users):
        print(all_users)
        print(starting_users)
        users2 = []
        users = all_rotas[rota_counter][0].get_rota_users()
        print(users)
        if len(users) == 0:
            return
        rota_name = all_rotas[rota_counter][0].get_rota_name()
        for i in range(len(users)):
            for j in range(len(all_users)):
                temp2 = all_users[j][0].get_user_id()
                if temp2 == users[i]:
                    temp = all_users[j][0].get_user_name()
                    print(temp)
            users2.append([copy.copy(users[i]),temp])
        print(users2)
        starting_person = starting_users[rota_counter]
        for k in range(len(users2)):
            if users2[k][1] == starting_person:
                startpoint = k
        clashes = 0
        shuffles = 0
        rota_users_order = []
        loop = True
        start_time = time.time()
        max_time = 10
        shuffelled = 0
        while loop == True:
            rota_users_order = []
            clash = False
            currentpoint = startpoint
            for i in range(0,16):
                print(currentpoint)
                temp_user = copy.copy(users2[currentpoint][1])
                temp_date = list_of_dates[i]
                rota_users_order.append([temp_user,temp_date])
                temp_data = int(users2[currentpoint][0])-1
                temp_dates_list = all_users[temp_data][0].get_user_dates()
                if temp_dates_list[i][1] == False:
                    clash = True
                currentpoint = currentpoint + 1
                if currentpoint >= len(users2):
                    currentpoint = 0
            if clash == True:
                startpoint = startpoint + 1
                if startpoint == len(users2):
                    startpoint = 0
                clashes = clashes + 1
                if clashes == len(users2):
                    random.shuffle(users2)
                    shuffelled = shuffelled + 1
            if (time.time() > (start_time + max_time)%60) and (shuffelled > 0):
                clash = False
            if clash == False:
                loop = False
                rota_data = copy.copy(rota_users_order)
                all_rotas[rota_counter][0].set_rota_data(rota_data)
                currentpoint = startpoint
                for i in range(0,16):
                    print(currentpoint)
                    temp_user = copy.copy(users2[(currentpoint)][1])
                    temp_date = list_of_dates[i]
                    temp_data = int(users2[currentpoint][0])-1
                    all_users[temp_data][0].remove_date(temp_date)
                    currentpoint = currentpoint + 1
                    if currentpoint >= len(users2):
                        currentpoint = 0
                rota_info = all_rotas[rota_counter][0].get_rota_data()
                user_info = all_users[0][0].get_user_dates()
                CreateRotasPage.save_rota(self,rota_info,user_info,rota_name)

    def save_rota(self,rota_info,user_info,rota_name):
        global filetype
        filename = rota_name + "_" + str(rota_info[0][1][0]) + "_" + str(rota_info[0][1][1]) + "_" + str(rota_info[0][1][2])
        filename = "Output" + pathtype + filename
        dates = []
        names = []
        for i in range(len(rota_info)):
            dates.append(rota_info[i][1])
            names.append(rota_info[i][0])
        title = rota_name
        print(dates)
        print(names)
        print(title)
        print(filename)
        try:
            create_docx(title,dates,names,filename)
            filetype = "docx"
        except:
            temp_rota_file = open(filename,"w")
            for i in range(len(rota_info)):
                line = str(rota_info[i][1])
                line = line + "   "
                line = line + str(rota_info[i][0])
                temp_rota_file.write(line)
                temp_rota_file.write("\n")
            temp_rota_file.close()
            filetype = "text"

class DisplayPage(tk.Frame):
    def __init__(self, window, controller):
        tk.Frame.__init__(self, window)
        exit_picture = tk.PhotoImage(file="Data" + pathtype + "assets" + pathtype + "exit_button.png")
        leave = tk.Button(self,
                          command = lambda : self.close(),
                          image = exit_picture
                          )
        leave.image = exit_picture
        leave.grid(column=1420,row=0)

        menu_picture = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "MenuButton.png")
        menu_button = tk.Button(self,
                                command = lambda : self.menu(controller),
                                image = menu_picture
                                )
        menu_button.image = menu_picture
        menu_button.grid(column = 100,row = 100)

        info = tk.Label(self,
                        text = "Your Rotas have been created",
                        fg = "medium turquoise"
                        )
        info.grid(row = 0,column = 100)

        print_button = tk.Button(self,
                                 command = lambda : self.printer()
                                 )

    def menu(self,controller):
        MainView.show(controller,MenuPage)
        
    def close(self):
        window.destroy()

    def printer(self):
        global filetype
        global all_rotas
        if filetype =="text":
            for i in range(0,len(all_users)):
                subprocess.call(['notepad', '/p', filename])
        elif filetype == "docx":
            for j in range(0,len(all_users)):
                subprocess.call(['word','/p',filename])

class RemoveUserPage(tk.Frame):
    def __init__(self, window, controller):
        tk.Frame.__init__(self,window)
        self.Remove_User = None
        self.Remove_User_Button = None

        return_arrow = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "return_arrow.png")
        back_button = tk.Button(self,
                                command = lambda : self.back(controller,remove_button),
                                text = "Go back",
                                image = return_arrow
                                )
        back_button.image = return_arrow
        back_button.grid(row = 500,column = 0)

        remove_button = tk.Button(self,
                                  command = lambda : self.begin(remove_button,controller),
                                  text = "Press to remove a User"
                                  )
        remove_button.grid(row = 2,column = 4)
        
        exit_picture = tk.PhotoImage(file="Data" + pathtype + "assets" + pathtype + "exit_button.png")
        leave = tk.Button(self,
                          command = lambda : self.close(),
                          image = exit_picture
                          )
        leave.image = exit_picture
        leave.grid(column=1000,row=0)

    def close(self):
        window.destroy()
        
    def begin(self,remove_button,controller):
        remove_button.grid_forget()
        users_list = []
        for i in range(0,len(all_users)):
            users_list.append(all_users[i][1])
        variable = tk.StringVar(window)
        variable.set("Select the User you would like to remove")
        self.Remove_User = tk.OptionMenu(self,
                                    variable,
                                    *users_list
                                    )
        self.Remove_User.config(bg = "Cyan")
        self.Remove_User.grid(row = 0,column = 0)

        self.Remove_User_Button = tk.Button(self,
                                       text ="Press to remove this user",
                                       command = lambda : self.remove(remove_button,controller))
        self.Remove_User_Button.grid(row = 0,column = 10)

    def back(self,controller,remove_button):
        remove_button.grid(row = 2, column = 4)
        try:
            self.Remove_User.grid_forget()
            self.Remove_User_Button.grid_forget()
        except:
            pass
        MainView.show(controller,EditRotaPage)

    def remove(self,remove_button,controller):
        username = self.Remove_User.cget('text')
        if username == "Select the User you would like to remove":
            return
        remove_button.grid(row = 500, column = 0)
        self.Remove_User.grid_forget()
        self.Remove_User_Button.grid_forget()
        user_id = None
        for i in range(0,len(all_users)):
            if all_users[i][1] == username:
                user_id = all_users[i][0].get_user_id()
        if user_id != None:
            deleted = False
            length = len(all_users) - 1
            l = 0
            r = length
            loop = True
            midpoint = int(length / 2)
            while loop == True:
                if all_users[midpoint][0].get_user_id() < user_id:
                    l = midpoint + 1
                elif all_users[midpoint][0].get_user_id() > user_id:
                    r = midpoint - 1
                elif all_users[midpoint][0].get_user_id() == user_id:
                    loop = False
                    pos = midpoint
                    deleted = True
                midpoint = int((r + l) / 2)
            if deleted == True:
                temp3 = pos
                del all_users[temp3][0]
                del all_users[temp3]
                for j in range(0,len(all_rotas)):
                    length = len(all_rotas[j])
                    for m in range(3,length):
                        n = (length - m) + 2
                        if all_rotas[j][n] == user_id:
                            del all_rotas[j][n]
                    all_rotas[j][0].remove_rota_users(user_id)
                for y in range(len(all_users)):
                    temp1 = all_users[y][0].get_user_id()
                    if temp1 > user_id:
                        temp2 = str(int(temp1) - 1)
                        all_users[y][0].reset_user_id(temp2)
                for z in range(0,len(all_rotas)):
                    user_list = all_rotas[z][0].get_rota_users()
                    for d in range(0,len(user_list)):
                        if user_list[d] > user_id:
                            pos = d
                            all_rotas[z][0].lower_rota_user(pos)
            else:
                print("no user found")
        save(filenumb,all_users,all_rotas,pathtype)
        self.back(controller,remove_button)

class RemoveRotaPage(tk.Frame):
    def __init__(self, window, controller):
        tk.Frame.__init__(self,window)
        self.Remove_Rota = None
        self.Remove_Rota_Button = None
        return_arrow = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "return_arrow.png")
        back_button = tk.Button(self,
                                command = lambda : self.back(controller,remove_button),
                                text = "Go back",
                                image = return_arrow
                                )
        back_button.image = return_arrow
        back_button.grid(row = 500,column = 0)

        remove_button = tk.Button(self,
                                  command = lambda : self.begin(remove_button,controller),
                                  text = "Press to remove a Rota"
                                  )
        remove_button.grid(row = 2,column = 4)

        exit_picture = tk.PhotoImage(file="Data" + pathtype + "assets" + pathtype + "exit_button.png")
        leave = tk.Button(self,
                          command = lambda : self.close(),
                          image = exit_picture
                          )
        leave.image = exit_picture
        leave.grid(column=1000,row=0,)

    def close(self):
        window.destroy()

        
    def begin(self,remove_button,controller):
        remove_button.grid_forget()
        rotas_list = []
        for i in range(0,len(all_rotas)):
            rotas_list.append(all_rotas[i][1])
        variable = tk.StringVar(window)
        variable.set("Select the Rota you would like to remove")
        self.Remove_Rota = tk.OptionMenu(self,
                                    variable,
                                    *rotas_list
                                    )
        self.Remove_Rota.config(bg = "Cyan")
        self.Remove_Rota.grid(row = 0,column = 0)

        self.Remove_Rota_Button = tk.Button(self,
                                       text = "Press to remove this Rota",
                                       command = lambda : self.remove(remove_button,controller))
        self.Remove_Rota_Button.grid(row = 0,column = 10)

    def back(self,controller,remove_button):
        self.Remove_Rota.grid_forget()
        self.Remove_Rota_Button.grid_forget()
        remove_button.grid(row = 2, column = 4)
        MainView.show(controller,EditRotaPage)

    def remove(self,remove_button,controller):
        rotaname = self.Remove_Rota.cget('text')
        if rotaname == "Select the Rota you would like to remove":
            return
        remove_button.grid(row = 500, column = 0)
        self.Remove_Rota.grid_forget()
        self.Remove_Rota_Button.grid_forget()
        rota_id = None
        for i in range(0,len(all_rotas)):
            if all_rotas[i][1] == rotaname:
                rota_id = all_rotas[i][0].get_rota_id()
        if rota_id != None:
            deleted = False
            length = len(all_rotas) - 1
            l = 0
            r = length
            loop = True
            midpoint = int(length / 2)
            while loop == True:
                print(midpoint)
                if all_rotas[midpoint][0].get_rota_id() < rota_id:
                    l = midpoint + 1
                elif all_rotas[midpoint][0].get_rota_id() > rota_id:
                    r = midpoint - 1
                elif all_rotas[midpoint][0].get_rota_id() == rota_id:
                    loop = False
                    pos = midpoint
                    deleted = True
                midpoint = int((r + l) / 2)
            if deleted == True:
                del all_rotas[pos][0]
                del all_rotas[pos]
                for y in range(len(all_rotas)):
                    temp1 = all_rotas[y][0].get_rota_id()
                    if temp1 > rota_id:
                        temp2 = str(int(temp1)-1)
                        all_rotas[y][0].reset_rota_id(temp2)
        save(filenumb,all_users,all_rotas,pathtype)
        self.back(controller,remove_button)

class AnalysisPage(tk.Frame):
    def __init__(self, window, controller):
        tk.Frame.__init__(self, window)
        self.Select_User_Analysis = None
        self.Select_User_Analysis_Button = None
        self.User_Analytics_Display = None
        self.User_Graph = []
        begin_button = tk.Button(self,
                                 text = "Press here to begin",
                                 command = lambda: self.begin(begin_button)
                                 )
        begin_button.grid(row = 10,column = 10)
        return_arrow = tk.PhotoImage(file = "Data" + pathtype + "assets" + pathtype + "return_arrow.png")
        back_button = tk.Button(self,
                                command = lambda : self.back(controller,begin_button),
                                text = "Go back",
                                image = return_arrow
                                )
        back_button.image = return_arrow
        back_button.grid(row = 21,column = 0)
        exit_picture = tk.PhotoImage(file="Data" + pathtype + "assets" + pathtype + "exit_button.png")
        leave = tk.Button(self,
                          command = lambda : self.close(),
                          image = exit_picture
                          )
        leave.image = exit_picture
        leave.grid(column=1000,row=0,)

    def close(self):
        window.destroy()

    def back(self,controller,begin_button):
        begin_button.grid(row = 10, column = 10)
        try:
            self.canvas.grid_forget()
            for m in range(0,len(self.key_list)):
                self.key_list[m].grid_forget()
            del self.key_list
        except:
            pass
        try:
            self.Select_User_Analysis.grid_forget()
            self.Select_User_Analysis_Button.grid_forget()
            self.User_Analytics_Display.grid_forget()
        except:
            pass
        try:
            for k in range(0,len(User_Graph)):
                self.User_Graph[k].grid_forget()
            del self.User_Graph
        except:
            pass
        try:
            del self.User_Graph
        except:
            pass
        self.User_Graph = []
        MainView.show(controller,LoadPage)

    def begin(self,begin_button):
        begin_button.grid_forget()
        users_list = []
        for i in range(0,len(all_users)):
            users_list.append(all_users[i][1])
        variable = tk.StringVar(window)
        variable.set("Select the User you would like to the data of")
        self.Select_User_Analysis = tk.OptionMenu(self,
                                                  variable,
                                                  *users_list
                                                  )
        self.Select_User_Analysis.config(bg = "cyan")
        self.Select_User_Analysis.grid(row = 0,column = 5)
        self.Select_User_Analysis_Button = tk.Button(self,
                                                text = "Press to see the data of this User",
                                                command = lambda : self.data())
        self.Select_User_Analysis_Button.grid(row = 0,column = 10)
        self.graph()

    def graph(self):
        self.User_Graph.append("temp")
        self.User_Graph[0] = tk.Label(self,
                                 bg = 'grey',
                                 fg = 'black',
                                 width = (16*4),
                                 height = 1,
                                 text = "",
                                 borderwidth=2,
                                 relief="groove"
                                 )
        self.User_Graph[0].grid(row = 21,column = 100, sticky = 'w')
        for j in range(0,len(all_users)):
            user_id = all_users[j][0].get_user_id()
            username = all_users[j][0].get_user_name()
            total = 0
            for i in range(0,len(all_rotas)):
                temp = self.average(user_id,i)
                total = total + temp
            self.User_Graph.append("temp")
            self.User_Graph[j] = tk.Label(self,
                                     bg = 'cyan',
                                     fg = 'black',
                                     width = int((total)*4),
                                     height = 4,
                                     text = username,
                                     borderwidth=2,
                                     relief="groove",
                                     )
            if total > 16:
                self.User_Graph[j].config(bg = 'red')
            if total == 16:
                self.User_Graph[j].config(bg = 'yellow')
            self.User_Graph[j].grid(row = (22 + j),column = 100, sticky = 'w')

            
    def get_id(self,name):
        user_id = None
        for i in range(0,len(all_users)):
            if all_users[i][1] == name:
                user_id = all_users[i][0].get_user_id()
        if user_id != None:
            length = len(all_users) - 1
            l = 0
            r = length
            loop = True
            midpoint = int(length / 2)
            while loop == True:
                if all_users[midpoint][0].get_user_id() < user_id:
                    l = midpoint + 1
                elif all_users[midpoint][0].get_user_id() > user_id:
                    r = midpoint - 1
                elif all_users[midpoint][0].get_user_id() == user_id:
                    loop = False
                    pos = midpoint
                midpoint = int((r + l) / 2)
        return pos, user_id

    def data(self):
        name = self.Select_User_Analysis.cget('text')
        pos, user_id = self.get_id(name)
        total = 0
        for i in range(0,len(all_rotas)):
            temp = self.average(user_id,i)
            total = total + temp
        total = int(10 * total)
        total = total / 10
        words = name + " will appear an average of \n" + str(total) + " times over the next 16 weeks"
        try:
            self.User_Analytics_Display.grid_forget()
        except:
            pass
        self.User_Analytics_Display = tk.Label(self,
                                          text = words,
                                          fg = "cyan"
                                          )
        self.User_Analytics_Display.config(font=("Ariel", 30))
        self.User_Analytics_Display.grid(row = 20,column = 100)
        self.pie(pos,user_id)

    def pie(self,pos,user_id):
        try:
            self.canvas.grid_forget()
            for m in range(0,len(self.key_list)):
                self.key_list[m].grid_forget()
            del self.key_list
        except:
            pass
        self.canvas = tk.Canvas(self, width=150, height=150)
        self.canvas.grid(row = 20, column = 101)
        proportions = []
        total = 0
        for i in range(0,len(all_rotas)):
            temp = self.average(user_id,i)
            if temp != 0:
                rota_name = all_rotas[i][0].get_rota_name()
                proportions.append([temp,rota_name])
            total = total + temp
        origin = 0
        colours_list = ["firebrick1","DarkOrange1","goldenrod1","green2","deep sky blue","DarkOrchid2","hot pink","aquamarine2","dark salmon","white","grey"]
        if len(proportions) == 1:
            self.canvas.create_oval(1,1,149,149,fill = "firebrick1")
        else:
            for j in range(0,len(proportions)):
                temp2 = proportions[j][0]
                length = (temp2 / total) * 360
                turn = length + origin
                colour = colours_list[j]
                self.canvas.create_arc(1, 1, 149, 149, start = origin, extent = length, fill = colour)
                origin = turn
        self.key_list = []
        for a in range(0,len(proportions)):
            self.key_list.append("temp")
            name = proportions[a][1]
            colour = colours_list[a]
            self.key_list[a] = tk.Label(self,
                                   text = name,
                                   bg = colour,
                                   fg = "black"
                                   )
            self.key_list[a].grid(row = (22 + a), column = 101)
                                   
        
    def average(self,user_id,i):
        user_list = all_rotas[i][0].get_rota_users()
        found = False
        for u in range(0,len(user_list)):
            if user_list[u] == user_id:
                found = True
        if found == False:
            return 0
        elif found == True:
            user_length = len(user_list)
            average = (16 / user_length)
            return average
            
        
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side = "top",fill = "both",expand = True)
        container.configure(bg='firebrick1')
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        for _frame in (MenuPage, LoadPage, EditRotaPage, AddRotaPage, AddUserPage, CreateRotasPage, DisplayPage ,NewSystemPage, RemoveUserPage, RemoveRotaPage, AnalysisPage):
            frame = _frame(container, self)
            self.frames[_frame] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")            
        self.show(MenuPage)

    def show(self,Page, *args, **kwargs):
        frame = self.frames[Page]
        frame.tkraise()
    
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Rota Management System")
    window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
    window.configure(bg = 'slate gray')
    main = MainView(window)
    main.pack(side="top", fill="both", expand=True)
    
    window.mainloop()
