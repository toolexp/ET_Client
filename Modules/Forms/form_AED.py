from tkinter import Label, LabelFrame, Frame, Entry, Button, messagebox, PhotoImage, Scrollbar
from tkinter.constants import *
from tkinter.ttk import Treeview, Separator
from Modules.Config.Data import Message, CreateToolTip
from Modules.Config.Visual import *
import hashlib


class FormParentAED:
    def __init__(self, window, title, connection):
        self.frm_parent = LabelFrame(window)
        self.title = title
        self.initialize_components()
        self.frm_child = FormChildAED(self.frm_parent, title, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text=self.title + 's')
        lbl_experimenter_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_experimenter_title.grid(row=0, column=0, pady=30)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0, pady=10, padx=10, sticky=NSEW)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildAED:
    def __init__(self, frm_parent, title, connection):
        self.connection = connection
        self.directive = Message()
        self.title = title
        self.decide = True
        self.id_selected = 0
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_crud = LabelFrame(frm_parent)
        self.frm_child_crud.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        self.initialize_components()

    def initialize_components(self):
        """
        Method that initialize the visual components for each form associated with the local administration
        """
        # Resources for the Forms
        self.new_icon = PhotoImage(file=r"./Resources/create.png")
        self.modify_icon = PhotoImage(file=r"./Resources/modify.png")
        self.remove_icon = PhotoImage(file=r"./Resources/delete.png")
        self.save_icon = PhotoImage(file=r"./Resources/save.png")
        self.cancel_icon = PhotoImage(file=r"./Resources/cancel.png")

        # Components for List Form
        lbl_sep1 = Label(self.frm_child_list)
        lbl_sep1.grid(row=0, column=0, padx=25, pady=25)
        self.trv_available = Treeview(self.frm_child_list, height=7, columns=('Name', 'Surname', 'E-mail'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Surname', anchor=CENTER)
        self.trv_available.heading('#3', text='E-mail', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#3', width=400, minwidth=400, stretch=NO)
        self.trv_available.grid(row=0, column=1, sticky=W, pady=25)
        vsb_trv_av = Scrollbar(self.frm_child_list, orient="vertical", command=self.trv_available.yview)
        vsb_trv_av.grid(row=0, column=2, pady=25, sticky=NS)
        self.trv_available.configure(yscrollcommand=vsb_trv_av.set)
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New ' + self.title.lower())
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit ' + self.title.lower())
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete ' + self.title.lower())
        frm_aux4.grid(row=0, column=4, pady=25, padx=25, sticky=NW)

        # Components for CRUD FRM
        frm_aux = Frame(self.frm_child_crud)
        lbl_name = Label(frm_aux, text='Name')
        lbl_name.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name.grid(row=0, column=0, pady=10, padx=20, sticky=W)
        lbl_surname = Label(frm_aux, text='Surname')
        lbl_surname.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_surname.grid(row=1, column=0, pady=10, padx=20, sticky=W)
        lbl_email = Label(frm_aux, text='E-mail')
        lbl_email.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_email.grid(row=2, column=0, pady=10, padx=20, sticky=W)
        self.lbl_old_passwd = Label(frm_aux, text='Old password')
        self.lbl_old_passwd.config(fg=TEXT_COLOR, font=LABEL_FONT)
        self.lbl_passwd = Label(frm_aux, text='New password')
        self.lbl_passwd.config(fg=TEXT_COLOR, font=LABEL_FONT)
        self.lbl_passwd_conf = Label(frm_aux, text='Confirm new password')
        self.lbl_passwd_conf.config(fg=TEXT_COLOR, font=LABEL_FONT)
        self.txt_name = Entry(frm_aux)
        self.txt_name.grid(row=0, column=1, padx=20)
        self.txt_surname = Entry(frm_aux)
        self.txt_surname.grid(row=1, column=1, padx=20)
        self.txt_email = Entry(frm_aux)
        self.txt_email.grid(row=2, column=1, padx=20)
        self.txt_old_passwd= Entry(frm_aux, show="*")
        self.txt_passwd = Entry(frm_aux, show="*")
        self.txt_passwd_conf = Entry(frm_aux, show="*")
        frm_aux.grid(row=0, column=0, pady=10, padx=20, rowspan=10)

        sep_aux2 = Separator(self.frm_child_crud, orient=VERTICAL)
        sep_aux2.grid(row=0, column=1, sticky=NS, rowspan=10)

        btn_save = Button(self.frm_child_crud, image=self.save_icon, command=self.click_save)
        btn_save.grid(row=1, column=2, padx=20)
        btn_save_ttp = CreateToolTip(btn_save, 'Save ' + self.title.lower())
        btn_cancel = Button(self.frm_child_crud, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel.grid(row=2, column=2, padx=20)
        btn_cancel_ttp = CreateToolTip(btn_cancel, 'Cancel')

    def retrieve_list(self):
        """
        Method that retrieve users information from the server and displays them in the TreeView from
        the List Form
        """
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        # Retrieve information from the server
        if self.title == 'Experimenter':
            self.directive = Message(action=17, information=[])
        elif self.title == 'Designer':
            self.directive = Message(action=22, information=[])
        elif self.title == 'Administrator':
            self.directive = Message(action=12, information=[])
        else:
            raise Exception('Error en recuperacion: tipo de usuario')
        self.connection = self.directive.send_directive(self.connection)
        # Adding elements in the list
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1], elements[2], elements[3]))

    def show_frm(self):
        """
        Show the List form when the User administration is called
        """
        self.retrieve_list()
        if len(self.trv_available.get_children()) != 0:
            self.trv_available.selection_set(self.trv_available.get_children()[0])
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        """
        Hide the User administration Forms
        """
        self.clear_fields()
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid_forget()

    def click_delete(self):
        """
        Method that removes a selected user from the initial list (changes are updated in DB)
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            decision = messagebox.askyesno(parent=self.frm_child_list, title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
                if self.title == 'Experimenter':
                    self.directive = Message(action=19, information=[self.id_selected])
                elif self.title == 'Designer':
                    self.directive = Message(action=24, information=[self.id_selected])
                elif self.title == 'Administrator':
                    self.directive = Message(action=14, information=[self.id_selected])
                else:
                    raise Exception('Error en recuperacion: tipo de usuario')
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:     # An error ocurred while deleting the item
                    messagebox.showerror(parent=self.frm_child_list, title='Can not delete the item',
                                         message=self.connection.message.information[0])
                else:
                    self.retrieve_list()
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select an item')

    def click_new(self):
        """
        Initialize CRUD Form for creating a new user.
        """
        self.decide = True
        self.frm_child_list.grid_forget()
        self.txt_name.focus_set()
        self.frm_child_crud['text'] = 'New ' + self.title.lower()
        self.lbl_passwd.grid(row=3, column=0, pady=10, padx=20, sticky=W)
        self.lbl_passwd_conf.grid(row=4, column=0, pady=10, padx=20, sticky=W)
        self.txt_passwd.grid(row=3, column=1, padx=20)
        self.txt_passwd_conf.grid(row=4, column=1, padx=20)
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        """
        Initialize CRUD Form for updating a user. It loads information of selected User into visual components
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.decide = False
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            if self.title == 'Experimenter':
                self.directive = Message(action=20, information=[self.id_selected])
            elif self.title == 'Designer':
                self.directive = Message(action=25, information=[self.id_selected, 'validate'])
            elif self.title == 'Administrator':
                self.directive = Message(action=15, information=[self.id_selected])
            else:
                raise Exception('Error en recuperacion: tipo de usuario')
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.action == 5:  # An error ocurred while trying to update the item
                messagebox.showerror(parent=self.frm_child_list, title='Can not update the item',
                                     message=self.connection.message.information[0])
            else:
                self.txt_name.insert(0, self.connection.message.information[0])
                self.txt_surname.insert(0, self.connection.message.information[1])
                self.txt_email.insert(0, self.connection.message.information[2])
                self.current_password = self.connection.message.information[3]
                self.frm_child_list.grid_forget()
                self.txt_name.focus_set()
                self.frm_child_crud['text'] = 'Update ' + self.title.lower()
                self.lbl_old_passwd.grid(row=3, column=0, pady=10, padx=20, sticky=W)
                self.lbl_passwd.grid(row=4, column=0, pady=10, padx=20, sticky=W)
                self.lbl_passwd_conf.grid(row=5, column=0, pady=10, padx=20, sticky=W)
                self.txt_old_passwd.grid(row=3, column=1, padx=20)
                self.txt_passwd.grid(row=4, column=1, padx=20)
                self.txt_passwd_conf.grid(row=5, column=1, padx=20)
                self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select an item')

    def click_save(self):
        """
        Saves information of the user inserted into the visual components and sends to the server
        """
        validation_option = self.validate_fields()
        if validation_option == 0:
            name_aux = self.txt_name.get()
            surname_aux = self.txt_surname.get()
            email_aux = self.txt_email.get()
            passwd_aux = self.txt_passwd.get()
            if self.decide:
                if self.title == 'Experimenter':
                    self.directive = Message(action=16, information=[name_aux, surname_aux, email_aux,
                                                                     hashlib.sha1(passwd_aux.encode()).hexdigest()])
                elif self.title == 'Designer':
                    self.directive = Message(action=21, information=[name_aux, surname_aux, email_aux,
                                                                     hashlib.sha1(passwd_aux.encode()).hexdigest()])
                elif self.title == 'Administrator':
                    self.directive = Message(action=11, information=[name_aux, surname_aux, email_aux,
                                                                     hashlib.sha1(passwd_aux.encode()).hexdigest()])
                else:
                    raise Exception('Error en guardar: tipo de usuario')
            else:
                if self.title == 'Experimenter':
                    self.directive = Message(action=18, information=[self.id_selected, name_aux, surname_aux, email_aux,
                                                                     hashlib.sha1(passwd_aux.encode()).hexdigest()])
                elif self.title == 'Designer':
                    self.directive = Message(action=23, information=[self.id_selected, name_aux, surname_aux, email_aux,
                                                                     hashlib.sha1(passwd_aux.encode()).hexdigest()])
                elif self.title == 'Administrator':
                    self.directive = Message(action=13, information=[self.id_selected, name_aux, surname_aux, email_aux,
                                                                     passwd_aux])
                else:
                    raise Exception('Error en guardar: tipo de usuario')
            self.connection = self.directive.send_directive(self.connection)
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()
        elif validation_option == 1:
            messagebox.showwarning(parent=self.frm_child_crud, title='Password field',
                                   message='The passwords you provided are not the same')
        elif validation_option == 3:
            messagebox.showwarning(parent=self.frm_child_crud, title='Old password field',
                                   message='The old password is incorrect')
        else:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='There are mandatory fields that need to be filled!')

    def click_cancel(self):
        """

        """
        decision = messagebox.askyesno(parent=self.frm_child_crud, title='Cancel',
                                       message='Are you sure you want to cancel?')
        if decision:
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def validate_fields(self):
        if len(self.txt_name.get()) != 0 and len(self.txt_surname.get()) != 0 and len(self.txt_email.get()) != 0 and \
                len(self.txt_passwd.get()) != 0 and len(self.txt_passwd_conf.get()) != 0:
            if self.decide:
                if self.txt_passwd.get() == self.txt_passwd_conf.get():
                    return 0
                else:
                    return 1
            else:
                if self.current_password == hashlib.sha1(self.txt_old_passwd.get().encode()).hexdigest():
                    if self.txt_passwd.get() == self.txt_passwd_conf.get():
                        return 0
                    else:
                        return 1
                else:
                    return 3
        else:
            return 2

    def clear_fields(self):
        self.txt_name.delete(0, END)
        self.txt_surname.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_old_passwd.delete(0, END)
        self.txt_passwd.delete(0, END)
        self.txt_passwd_conf.delete(0, END)
        self.lbl_old_passwd.grid_forget()
        self.lbl_passwd.grid_forget()
        self.lbl_passwd_conf.grid_forget()
        self.txt_old_passwd.grid_forget()
        self.txt_passwd.grid_forget()
        self.txt_passwd_conf.grid_forget()
