from tkinter import Label, LabelFrame, Frame, Entry, Button, messagebox
from tkinter.constants import *
from tkinter.ttk import Treeview
from Modules.Config.Data import Message

TITLE_FONT = ("Arial", 18)
SUBTITLE_FONT = ("Arial", 14)
LABEL_FONT = ("Arial", 10)
TEXT_FONT = ("Arial", 10)


class FormParentAED:
    def __init__(self, window, title, connection):
        self.frm_parent = LabelFrame(window)
        self.title = title
        self.initialize_components()
        self.frm_child = FormChildAED(self.frm_parent, title, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text=self.title + 's administration')
        lbl_experimenter_title.config(fg="#222cb3", font=TITLE_FONT)
        lbl_experimenter_title.grid(row=0, column=0, columnspan=9, pady=50)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildAED:
    def __init__(self, frm_parent, title, connection):
        self.connection = connection
        self.title = title
        self.decide = True
        self.id_selected = 0
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_crud = LabelFrame(frm_parent)
        self.frm_child_crud.config(fg="#222cb3", font=SUBTITLE_FONT)
        self.initialize_components()

    def initialize_components(self):
        # Components for List FRM
        self.trv_available = Treeview(self.frm_child_list, height=7, columns=('Name', 'Surname'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Surname', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.grid(row=1, column=1, columnspan=5, rowspan=10, sticky=W, padx=100, pady=100)
        Button(self.frm_child_list, text='New', command=self.click_new).grid(row=3, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Delete', command=self.click_delete).grid(row=4, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Update', command=self.click_update).grid(row=5, column=7, columnspan=2, padx=25, sticky=W)

        # Components for CRUD FRM
        frm_aux = Frame(self.frm_child_crud)
        lbl_name = Label(frm_aux, text='Name')
        lbl_name.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=100, sticky=W)
        lbl_surname = Label(frm_aux, text='Surname')
        lbl_surname.config(fg="#222cb3", font=LABEL_FONT)
        lbl_surname.grid(pady=10, padx=100, sticky=W)
        lbl_email = Label(frm_aux, text='E-mail')
        lbl_email.config(fg="#222cb3", font=LABEL_FONT)
        lbl_email.grid(pady=10, padx=100, sticky=W)
        lbl_passwd = Label(frm_aux, text='Password')
        lbl_passwd.config(fg="#222cb3", font=LABEL_FONT)
        lbl_passwd.grid(pady=10, padx=100, sticky=W)
        self.txt_name = Entry(frm_aux)
        self.txt_name.grid(row=0, column=1, padx=100)
        self.txt_surname = Entry(frm_aux)
        self.txt_surname.grid(row=1, column=1, padx=100)
        self.txt_email = Entry(frm_aux)
        self.txt_email.grid(row=2, column=1, padx=100)
        self.txt_passwd = Entry(frm_aux, show="*")
        self.txt_passwd.grid(row=3, column=1, padx=100)
        Button(self.frm_child_crud, text='Save', command=self.click_save).grid(row=4, column=5, padx=20)
        Button(self.frm_child_crud, text='Cancel', command=self.click_cancel).grid(row=5, column=5, padx=20)
        frm_aux.grid(row=1, column=0, pady=20, padx=100, columnspan=5,rowspan=10)

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        if self.title == 'Experimenter':
            msg = Message(action=17, information=[])
        elif self.title == 'Designer':
            msg = Message(action=22, information=[])
        elif self.title == 'Administrator':
            msg = Message(action=12, information=[])
        else:
            msg = Message(action=22, information=[])
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.receive_message()
        for i in range(0, len(self.connection.message.information)):
            elements = self.connection.message.information[i].split('¥')
            self.trv_available.insert('','end',text=elements[0], values=(elements[1], elements[2]))

    def show_frm(self):
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid_forget()

    def click_delete(self):
        if  self.trv_available.item(self.trv_available.selection())['text'] != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            if self.title == 'Experimenter':
                msg = Message(action=19, information=[int(self.id_selected)])
            elif self.title == 'Designer':
                msg = Message(action=24, information=[int(self.id_selected)])
            elif self.title == 'Administrator':
                msg = Message(action=14, information=[int(self.id_selected)])
            else:
                msg = Message(action=24, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.retrieve_list()

    def click_new(self):
        self.decide = True
        self.frm_child_list.grid_forget()
        self.frm_child_crud['text'] = 'New ' + self.title.lower()
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        if  self.trv_available.item(self.trv_available.selection())['text'] != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            self.decide = False
            self.frm_child_list.grid_forget()
            self.frm_child_crud['text'] = 'Update ' + self.title.lower()
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
            if self.title == 'Experimenter':
                msg = Message(action=20, information=[int(self.id_selected)])
            elif self.title == 'Designer':
                msg = Message(action=25, information=[int(self.id_selected)])
            elif self.title == 'Administrator':
                msg = Message(action=15, information=[int(self.id_selected)])
            else:
                msg = Message(action=25, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.txt_name.delete(0, END)
            self.txt_name.insert(0, self.connection.message.information[0])
            self.txt_surname.delete(0, END)
            self.txt_surname.insert(0, self.connection.message.information[1])
            self.txt_email.delete(0, END)
            self.txt_email.insert(0, self.connection.message.information[2])
            self.txt_passwd.delete(0, END)
            self.txt_passwd.insert(0, self.connection.message.information[3])

    def click_save(self):
        if self.validate_fields():
            decision = messagebox.askyesno(title='Confirmation', message='Are you sure you want to save the changes?')
            if decision:
                name_aux = self.txt_name.get()
                surname_aux = self.txt_surname.get()
                email_aux = self.txt_email.get()
                passwd_aux = self.txt_passwd.get()
                if self.decide:
                    if self.title == 'Experimenter':
                        msg = Message(action=16, information=[name_aux, surname_aux, email_aux, passwd_aux])
                    elif self.title == 'Designer':
                        msg = Message(action=21, information=[name_aux, surname_aux, email_aux, passwd_aux])
                    elif self.title == 'Administrator':
                        msg = Message(action=11, information=[name_aux, surname_aux, email_aux, passwd_aux])
                    else:
                        msg = Message(action=21, information=[name_aux, surname_aux, email_aux, passwd_aux])
                else:
                    if self.title == 'Experimenter':
                        msg = Message(action=18, information=[int(self.id_selected), name_aux, surname_aux, email_aux, passwd_aux])
                    elif self.title == 'Designer':
                        msg = Message(action=23, information=[int(self.id_selected), name_aux, surname_aux, email_aux, passwd_aux])
                    elif self.title == 'Administrator':
                        msg = Message(action=13, information=[int(self.id_selected), name_aux, surname_aux, email_aux, passwd_aux])
                    else:
                        msg = Message(action=23, information=[int(self.id_selected), name_aux, surname_aux, email_aux, passwd_aux])
                self.txt_name.delete(0, END)
                self.txt_surname.delete(0, END)
                self.txt_email.delete(0, END)
                self.txt_passwd.delete(0, END)
                self.connection.create_message(msg)
                self.connection.send_message()
                self.connection.receive_message()
                self.frm_child_crud.grid_forget()
                self.show_frm()

    def click_cancel(self):
        decision = messagebox.askyesno(title='Cancel', message='Are you sure you want to cancel?')
        if decision:
            self.txt_name.delete(0, END)
            self.txt_surname.delete(0, END)
            self.txt_email.delete(0, END)
            self.txt_passwd.delete(0, END)
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def validate_fields(self):
        if len(self.txt_name.get()) != 0 and len(self.txt_surname.get()) != 0 and len(self.txt_email.get()) != 0 and len(self.txt_passwd.get()) != 0:
            return True
        else:
            return False
