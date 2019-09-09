from tkinter import Label, LabelFrame, Frame, Text, Button, Entry, messagebox
from tkinter.constants import *
from tkinter.ttk import Treeview
from Modules.Config.Data import Message

TITLE_FONT = ("Arial", 18)
SUBTITLE_FONT = ("Arial", 14)
LABEL_FONT = ("Arial", 10)
TEXT_FONT = ("Arial", 10)


class FormParentDG:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildDG(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Designers groups administration')
        lbl_experimenter_title.config(fg="#222cb3", font=TITLE_FONT)
        lbl_experimenter_title.grid(row=0, column=0, columnspan=9, pady=50)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildDG:
    def __init__(self, frm_parent, connection):
        self.connection = connection
        self.decide = True
        self.id_selected = 0
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_crud = LabelFrame(frm_parent)
        self.initialize_components()

    def initialize_components(self):
        # Components for List FRM
        self.trv_available = Treeview(self.frm_child_list, height=7, columns=('Name', 'Description', '# members'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.heading('#3', text='# members', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.column('#3', width=100, minwidth=100, stretch=NO)
        self.trv_available.grid(row=1, column=1, columnspan=5, rowspan=10, sticky=W, padx=100, pady=100)
        Button(self.frm_child_list, text='New', command=self.click_new).grid(row=3, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Delete', command=self.click_delete).grid(row=4, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Update', command=self.click_update).grid(row=5, column=7, columnspan=2, padx=25, sticky=W)

        # Components for CRUD FRM
        frm_aux1 = Frame(self.frm_child_crud)
        frm_aux2 = Frame(self.frm_child_crud)
        lbl_name = Label(frm_aux1, text='Name')
        lbl_name.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_description = Label(frm_aux1, text='Description')
        lbl_description.config(fg="#222cb3", font=LABEL_FONT)
        lbl_description.grid(pady=10, padx=50, sticky=NW)
        self.txt_name = Entry(frm_aux1)
        self.txt_name.grid(row=0, column=1, padx=50, sticky=W)
        self.txt_description = Text(frm_aux1, height=6, width=60, font=TEXT_FONT)
        self.txt_description.grid(row=1, column=1, padx=50, sticky=W)
        lbl_available_d = Label(frm_aux2, text='Available designers')
        lbl_available_d.config(fg="#222cb3", font=LABEL_FONT)
        lbl_available_d.grid(row=0, column=0, pady=10, sticky=W)
        lbl_selected_d = Label(frm_aux2, text='Selected designers')
        lbl_selected_d.config(fg="#222cb3", font=LABEL_FONT)
        lbl_selected_d.grid(row=0, column=2, pady=10, sticky=W)
        self.trv_available_designers = Treeview(frm_aux2, height=5, columns=('Name', 'Surname'))
        self.trv_available_designers.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_designers.heading('#1', text='Name', anchor=CENTER)
        self.trv_available_designers.heading('#2', text='Surname', anchor=CENTER)
        self.trv_available_designers.column('#0', width=20, minwidth=20, stretch=NO)
        self.trv_available_designers.column('#1', width=100, minwidth=100, stretch=NO)
        self.trv_available_designers.column('#2', width=150, minwidth=150, stretch=NO)
        self.trv_available_designers.bind("<Button-1>", self.click_trv_adesigners)
        self.trv_available_designers.grid(row=1, column=0, rowspan=10, sticky=W, padx=10)
        self.trv_selected_designers = Treeview(frm_aux2, height=5, columns=('Name', 'Surname'))
        self.trv_selected_designers.heading('#0', text='ID', anchor=CENTER)
        self.trv_selected_designers.heading('#1', text='Name', anchor=CENTER)
        self.trv_selected_designers.heading('#2', text='Surname', anchor=CENTER)
        self.trv_selected_designers.column('#0', width=20, minwidth=20, stretch=NO)
        self.trv_selected_designers.column('#1', width=100, minwidth=100, stretch=NO)
        self.trv_selected_designers.column('#2', width=150, minwidth=150, stretch=NO)
        self.trv_selected_designers.bind("<Button-1>", self.click_trv_sdesigners)
        self.trv_selected_designers.grid(row=1, column=2, rowspan=10, sticky=W, padx=10)
        Button(frm_aux2, text='Add', command=self.click_add).grid(row=4, column=1)
        Button(frm_aux2, text='Remove', command=self.click_remove).grid(row=5, column=1)
        Button(self.frm_child_crud, text='Save', command=self.click_save).grid(row=4, column=5, padx=25)
        Button(self.frm_child_crud, text='Cancel', command=self.click_cancel).grid(row=5, column=5, padx=25)
        frm_aux1.grid(row=1, column=0, pady=20, padx=40, columnspan=5, rowspan=5)
        frm_aux2.grid(row=8, column=0, pady=20, padx=40, columnspan=5, rowspan=10)

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        msg = Message(action=27, information=[])
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.receive_message()
        for i in range(0, len(self.connection.message.information)):
            elements = self.connection.message.information[i].split('¥')
            self.trv_available.insert('','end',text=elements[0], values=(elements[1], elements[2], elements[3]))

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
            msg = Message(action=29, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.retrieve_list()

    def click_new(self):
        self.decide = True
        self.frm_child_list.grid_forget()
        self.txt_name.delete(0, END)
        self.txt_description.delete('1.0', 'end-1c')
        msg = Message(action=22, information=[])
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.receive_message()
        a_designers = self.connection.message.information
        self.retrieve_designers([], a_designers)
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            self.decide = False
            self.frm_child_list.grid_forget()
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
            msg = Message(action=30, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.txt_name.delete(0, END)
            self.txt_name.insert(0, self.connection.message.information[0])
            self.txt_description.delete('1.0', 'end-1c')
            self.txt_description.insert('1.0', self.connection.message.information[1])
            s_designers = self.connection.message.information[2]
            msg = Message(action=22, information=[])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            a_designers = self.connection.message.information
            self.retrieve_designers(s_designers, a_designers)

    def retrieve_designers(self, s_designers, a_designers):
        for item in self.trv_available_designers.get_children():
            self.trv_available_designers.delete(item)
        for item in self.trv_selected_designers.get_children():
            self.trv_selected_designers.delete(item)
        for item in s_designers:
            if item in a_designers:
                a_designers.remove(item)
        for i in range(0, len(a_designers)):
            elements = a_designers[i].split('¥')
            self.trv_available_designers.insert('', 'end', text=elements[0], values=(elements[1], elements[2]))
        for i in range(0, len(s_designers)):
            elements = s_designers[i].split('¥')
            self.trv_selected_designers.insert('', 'end', text=elements[0], values=(elements[1], elements[2]))

    def click_add(self):
        if self.trv_available_designers.item(self.trv_available_designers.selection())['text'] != '' and self.trv_selected_designers.item(self.trv_selected_designers.selection())['text'] == '':
            self.trv_selected_designers.insert('', 'end', text=self.trv_available_designers.item(
                self.trv_available_designers.focus())['text'], values=self.trv_available_designers.item(
                self.trv_available_designers.focus())['values'])
            self.trv_available_designers.delete(self.trv_available_designers.selection())

    def click_remove(self):
        if self.trv_selected_designers.item(self.trv_selected_designers.selection())['text'] != '' and self.trv_available_designers.item(self.trv_available_designers.selection())['text'] == '':
            self.trv_available_designers.insert('', 'end', text=self.trv_selected_designers.item(
                self.trv_selected_designers.focus())['text'], values=self.trv_selected_designers.item(
                self.trv_selected_designers.focus())['values'])
            self.trv_selected_designers.delete(self.trv_selected_designers.selection())

    def click_trv_adesigners(self, event):
        self.trv_selected_designers.selection_remove(self.trv_selected_designers.selection())

    def click_trv_sdesigners(self, event):
        self.trv_available_designers.selection_remove(self.trv_available_designers.selection())

    def click_save(self):
        if self.validate_fields():
            decision = messagebox.askyesno(title='Confirmation', message='Are you sure you want to save the changes?')
            if decision:
                name_aux = self.txt_name.get()
                description_aux = self.txt_description.get('1.0', 'end-1c')
                if self.decide:
                    msg = Message(action=26, information=[name_aux, description_aux, []])
                    for item in self.trv_selected_designers.get_children():
                        msg.information[2].append(int(self.trv_selected_designers.item(item)['text']))
                else:
                    msg = Message(action=28, information=[int(self.id_selected), name_aux, description_aux, []])
                    for item in self.trv_selected_designers.get_children():
                        msg.information[3].append(int(self.trv_selected_designers.item(item)['text']))
                self.connection.create_message(msg)
                self.connection.send_message()
                self.connection.receive_message()
                self.frm_child_crud.grid_forget()
                self.show_frm()

    def click_cancel(self):
        decision = messagebox.askyesno(title='Cancel', message='Are you sure you want to cancel?')
        if decision:
            self.txt_name.delete(0, END)
            self.txt_description.delete('1.0', 'end-1c')
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def validate_fields(self):
        if len(self.txt_name.get()) != 0 and len(self.txt_description.get('1.0', 'end-1c')) != 0:
            if len(self.trv_selected_designers.get_children()) != 0:
                return True
            else:
                return False
        else:
            return False
