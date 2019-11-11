from tkinter import Label, LabelFrame, Frame, Text, Button, messagebox, PhotoImage, Scrollbar
from tkinter.constants import *
from tkinter.ttk import Treeview
from Modules.Config.Data import Message, CreateToolTip

TITLE_FONT = ("Arial", 18)
SUBTITLE_FONT = ("Arial", 14)
LABEL_FONT = ("Arial", 10)
TEXT_FONT = ("Arial", 10)

TEXT_COLOR = "#1B5070"


class FormParentDG:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildDG(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Designers groups')
        lbl_experimenter_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
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
        self.directive = Message()
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
        self.add_icon = PhotoImage(file=r"./Resources/right.png")
        self.delete_icon = PhotoImage(file=r"./Resources/left.png")

        # Components for List FRM
        lbl_sep1 = Label(self.frm_child_list)
        lbl_sep1.grid(row=0, column=0, padx=25, pady=25)
        self.trv_available = Treeview(self.frm_child_list, height=7, columns=('Name', 'Description', '# members'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.heading('#3', text='# members', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.column('#3', width=100, minwidth=100, stretch=NO)
        self.trv_available.grid(row=0, column=1, sticky=W, pady=25)
        vsb_trv_av = Scrollbar(self.frm_child_list, orient="vertical", command=self.trv_available.yview)
        vsb_trv_av.grid(row=0, column=2, pady=25, sticky=NS)
        self.trv_available.configure(yscrollcommand=vsb_trv_av.set)
        lbl_sep2 = Label(self.frm_child_list)
        lbl_sep2.grid(row=0, column=3, padx=25, pady=25)
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=10, padx=10, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New designers group')
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=1, column=0, pady=10, padx=10, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit designers group')
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=2, column=0, pady=10, padx=10, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete designers group')
        frm_aux4.grid(row=0, column=4, pady=25, padx=25, sticky=NW)

        # Components for CRUD FRM
        frm_aux1 = Frame(self.frm_child_crud)
        frm_aux2 = Frame(self.frm_child_crud)
        lbl_name = Label(frm_aux1, text='Name')
        lbl_name.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_description = Label(frm_aux1, text='Description')
        lbl_description.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_description.grid(pady=10, padx=50, sticky=NW)
        self.txt_name = Text(frm_aux1, height=1, width=60, font=TEXT_FONT)
        self.txt_name.grid(row=0, column=1, padx=50, sticky=W)
        self.txt_description = Text(frm_aux1, height=6, width=60, font=TEXT_FONT)
        self.txt_description.grid(row=1, column=1, padx=50, sticky=W)
        lbl_available_d = Label(frm_aux2, text='Available designers')
        lbl_available_d.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_available_d.grid(row=0, column=0, pady=10, sticky=W)
        lbl_selected_d = Label(frm_aux2, text='Selected designers')
        lbl_selected_d.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_selected_d.grid(row=0, column=5, pady=10, sticky=W)
        self.trv_available_designers = Treeview(frm_aux2, height=5, columns=('Name', 'Surname'))
        self.trv_available_designers.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_designers.heading('#1', text='Name', anchor=CENTER)
        self.trv_available_designers.heading('#2', text='Surname', anchor=CENTER)
        self.trv_available_designers.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_available_designers.column('#1', width=100, minwidth=100, stretch=NO)
        self.trv_available_designers.column('#2', width=150, minwidth=150, stretch=NO)
        self.trv_available_designers.bind("<Button-1>", self.click_trv_adesigners)
        self.trv_available_designers.grid(row=1, column=0, rowspan=10, sticky=W, pady=10)
        vsb_trv_avd = Scrollbar(frm_aux2, orient="vertical", command=self.trv_available_designers.yview)
        vsb_trv_avd.grid(row=1, column=1, rowspan=10, pady=10, sticky=NS)
        self.trv_available_designers.configure(yscrollcommand=vsb_trv_avd.set)
        lbl_sep3 = Label(frm_aux2)
        lbl_sep3.grid(row=1, column=2, padx=10, pady=10)
        lbl_sep4 = Label(frm_aux2)
        lbl_sep4.grid(row=1, column=4, padx=10, pady=10)
        self.trv_selected_designers = Treeview(frm_aux2, height=5, columns=('Name', 'Surname'))
        self.trv_selected_designers.heading('#0', text='ID', anchor=CENTER)
        self.trv_selected_designers.heading('#1', text='Name', anchor=CENTER)
        self.trv_selected_designers.heading('#2', text='Surname', anchor=CENTER)
        self.trv_selected_designers.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_selected_designers.column('#1', width=100, minwidth=100, stretch=NO)
        self.trv_selected_designers.column('#2', width=150, minwidth=150, stretch=NO)
        self.trv_selected_designers.bind("<Button-1>", self.click_trv_sdesigners)
        self.trv_selected_designers.grid(row=1, column=5, rowspan=10, sticky=W, pady=10)
        vsb_trv_avs = Scrollbar(frm_aux2, orient="vertical", command=self.trv_selected_designers.yview)
        vsb_trv_avs.grid(row=1, column=6, rowspan=10, pady=10, sticky=NS)
        self.trv_selected_designers.configure(yscrollcommand=vsb_trv_avs.set)
        btn_add = Button(frm_aux2, image=self.add_icon, command=self.click_add)
        btn_add.grid(row=4, column=3)
        btn_add_ttp = CreateToolTip(btn_add, 'Add designer')
        btn_remove = Button(frm_aux2, image=self.delete_icon, command=self.click_remove)
        btn_remove.grid(row=5, column=3)
        btn_remove_ttp = CreateToolTip(btn_remove, 'Remove designer')
        btn_save = Button(self.frm_child_crud, image=self.save_icon, command=self.click_save)
        btn_save.grid(row=1, column=5, padx=25)
        btn_save_ttp = CreateToolTip(btn_save, 'Save designers group')
        btn_cancel = Button(self.frm_child_crud, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel.grid(row=2, column=5, padx=25)
        btn_cancel_ttp = CreateToolTip(btn_cancel, 'Cancel')
        frm_aux1.grid(row=1, column=0, pady=20, padx=40, columnspan=5, rowspan=5)
        frm_aux2.grid(row=8, column=0, pady=20, padx=40, columnspan=5, rowspan=10)

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=27, information=[])
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available.insert('','end',text=elements[0], values=(elements[1], elements[2], elements[3]))

    def show_frm(self):
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        self.clear_fields()
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid_forget()

    def click_delete(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            decision = messagebox.askyesno(title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
                self.directive = Message(action=29, information=[self.id_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:  # An error ocurred while deleting the item
                    messagebox.showerror(title='Can not delete the item',
                                         message=self.connection.message.information[0])
                else:
                    self.retrieve_list()
        else:
            messagebox.showwarning(title='No selection', message='You must select an item')

    def click_new(self):
        self.decide = True
        self.directive = Message(action=22, information=[])
        self.connection = self.directive.send_directive(self.connection)
        a_designers = self.connection.message.information
        self.retrieve_designers([], a_designers)
        self.frm_child_list.grid_forget()
        self.frm_child_crud['text'] = 'New designers group'
        self.txt_name.focus_set()
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.decide = False
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            self.directive = Message(action=30, information=[self.id_selected])
            self.connection = self.directive.send_directive(self.connection)
            self.txt_name.insert('1.0', self.connection.message.information[0])
            self.txt_description.insert('1.0', self.connection.message.information[1])
            s_designers = self.connection.message.information[2]
            self.directive = Message(action=22, information=[])
            self.connection = self.directive.send_directive(self.connection)
            a_designers = self.connection.message.information
            self.retrieve_designers(s_designers, a_designers)
            self.frm_child_list.grid_forget()
            self.frm_child_crud['text'] = 'Update designers group'
            self.txt_name.focus_set()
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(title='No selection', message='You must select an item')

    def retrieve_designers(self, s_designers, a_designers):
        for item in self.trv_available_designers.get_children():
            self.trv_available_designers.delete(item)
        for item in self.trv_selected_designers.get_children():
            self.trv_selected_designers.delete(item)
        for item in s_designers:
            if item in a_designers:
                a_designers.remove(item)
        for item in a_designers:
            elements = item.split('¥')
            self.trv_available_designers.insert('', 'end', text=elements[0], values=(elements[1], elements[2]))
        for item in s_designers:
            elements = item.split('¥')
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
            name_aux = self.txt_name.get('1.0', 'end-1c')
            description_aux = self.txt_description.get('1.0', 'end-1c')
            if self.decide:
                self.directive = Message(action=26, information=[name_aux, description_aux, []])
                for item in self.trv_selected_designers.get_children():
                    self.directive.information[2].append(int(self.trv_selected_designers.item(item)['text']))
            else:
                self.directive = Message(action=28, information=[self.id_selected, name_aux, description_aux, []])
                for item in self.trv_selected_designers.get_children():
                    self.directive.information[3].append(int(self.trv_selected_designers.item(item)['text']))
            self.connection = self.directive.send_directive(self.connection)
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()
        else:
            messagebox.showwarning(title='Missing information',
                                   message='There are mandatory fields that need to be filled!')

    def click_cancel(self):
        decision = messagebox.askyesno(title='Cancel', message='Are you sure you want to cancel?')
        if decision:
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def validate_fields(self):
        if len(self.txt_name.get('1.0', 'end-1c')) != 0 and len(self.txt_description.get('1.0', 'end-1c')) != 0:
            if len(self.trv_selected_designers.get_children()) != 0:
                return True
            else:
                return False
        else:
            return False

    def clear_fields(self):
        self.txt_name.delete('1.0', 'end-1c')
        self.txt_description.delete('1.0', 'end-1c')
