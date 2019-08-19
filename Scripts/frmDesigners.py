from tkinter import *

class FrmHome:
    def __init__(self):
        # Configuration of the window
        self.window = Tk()
        self.window.title('Tool for experimenting')
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry('%dx%d+0+0' % (w, h))
        self.window.resizable(0, 0)

        # Configuration of the top Menu bar
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)
        administration_menu = Menu(menu_bar)
        administration_menu.add_command(label='Experimenters')
        administration_menu.add_command(label='Designers')
        experiment_menu = Menu(administration_menu)
        experiment_menu.add_command(label='Experiment administration')
        experiment_menu.add_command(label='Experiment configuration')
        administration_menu.add_cascade(label='Experiment', menu=experiment_menu)
        menu_bar.add_cascade(label='Administration', menu=administration_menu)
        menu_bar.add_command(label='Log out')

        #Example of menubar
        '''menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)'''

        # Configuration of the existing frames, one for each command in the menu bar
        self.frm_experimenter = LabelFrame(self.window)
        self.frm_experimenter.grid(row=0, column=0, pady=10, padx=10, sticky=NW+NE)
        #self.frameExperimenter.place(x = 10, y = 10, width=1820, height=950)
        lbl_experimenter_title = Label(self.frm_experimenter, text='Experimenters administration')
        lbl_experimenter_title.config(fg="#222cb3", font=10, width=1820, height=950)
        lbl_experimenter_title.grid(sticky=N)

        self.frm_experimenter_list = LabelFrame(self.frm_experimenter)
        self.frm_experimenter_list.grid(column=0, pady=10, padx=10, sticky=NW+NE)

        #lbl_fel_1 = Label(self.frm_experimenter_list, text='Available Experimenters')
        #lbl_fel_1.config(fg="#222cb3", font=10)
        #lbl_fel_1.grid(pady=300, padx=100)
        # self.frameExperimenter.place_forget()

        #lblName = Label(self.frameExperimenter, text='Name').pack()
        #lblName.config(fg="blue", font=("Verdana", 24))


        #self.txtName = Entry(self.frameExperimenter)
        #self.txtName.grid(row=1, column=1)

        '''self.lblSurname = Label(self.frame, text='Surname')
        self.lblSurname.grid(row=2, column=0)

        self.txtSurname = Entry(self.frame)
        self.txtSurname.grid(row=2, column=1)

        self.lblEmail = Label(self.frame, text='E-mail')
        self.lblEmail.grid(row=3, column=0)

        self.txtEmail = Entry(self.frame)
        self.txtEmail.grid(row=3, column=1)

        self.lblPsswd = Label(self.frame, text='Password')
        self.lblPsswd.grid(row=4, column=0)

        self.txtPsswd = Entry(self.frame)
        self.txtPsswd.grid(row=4, column=1)

        self.btnSave = Button(self.frame, text='Save')
        self.btnSave.grid(row=5)'''


if __name__=='__main__':
    app = FrmHome()
    app.window.mainloop()