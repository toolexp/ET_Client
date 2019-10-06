from tkinter import Label, LabelFrame, Text, Button, messagebox, PhotoImage, Frame
from tkinter.constants import *
from tkinter.ttk import Treeview
from Modules.Config.Data import Message, CreateToolTip

TITLE_FONT = ("Arial", 18)
SUBTITLE_FONT = ("Arial", 14)
LABEL_FONT = ("Arial", 10)
TEXT_FONT = ("Arial", 10)

TEXT_COLOR = "#1B5070"

class FormParentClassification:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildClassification(self.frm_parent, connection)

    def initialize_components(self):
        lbl_title = Label(self.frm_parent, text='Classifications')
        lbl_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_title.grid(row=0, column=0, columnspan=9, pady=50)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildClassification:
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

        # Components for List FRM
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=10, padx=10, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New classification')
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=1, column=0, pady=10, padx=10, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete classification')
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=2, column=0, pady=10, padx=10, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit classification')
        frm_aux4.grid(row=1, column=0, pady=35, padx=20, sticky=NW)
        self.trv_available = Treeview(self.frm_child_list, height=7, columns=('Name', '# categories'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='# categories', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.grid(row=1, column=1, columnspan=5, rowspan=10, sticky=W, padx=50, pady=25)

        # Components CRUD
        self.frm_class = LabelFrame(self.frm_child_crud, text='New classification')
        self.frm_class.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_class = Label(self.frm_child_crud, text='Name')
        lbl_class.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_class.grid(pady=10, padx=50, sticky=W)
        lbl_desc_categories = Label(self.frm_child_crud, text='Enter categories separated by a comma ","')
        lbl_desc_categories.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_desc_categories.grid(pady=10, padx=50, columnspan=2, sticky=W)
        lbl_categories = Label(self.frm_child_crud, text='Categories')
        lbl_categories.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_categories.grid(pady=10, padx=50, sticky=NW)
        self.txt_name_class = Text(self.frm_child_crud, height=1, width=50, font=TEXT_FONT)
        self.txt_name_class.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        self.txt_categories = Text(self.frm_child_crud, height=10, width=50, font=TEXT_FONT)
        self.txt_categories.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        btn_save = Button(self.frm_child_crud, image=self.save_icon, command=self.click_save)
        btn_save.grid(row=0, column=3, padx=20)
        btn_save_ttp = CreateToolTip(btn_save, 'Save classification')
        btn_cancel = Button(self.frm_child_crud, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel.grid(row=1, column=3, padx=20)
        btn_cancel_ttp = CreateToolTip(btn_cancel, 'Cancel')

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=67, information=[])
        self.connection = self.directive.send_directive(self.connection)
        # Adding elements into the list
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1], elements[2]))

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
                self.directive = Message(action=69, information=[self.id_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:
                    messagebox.showwarning(title='Fail deleting',
                                           message='The classification cant be deleted, it may be used in a section')
                self.retrieve_list()
        else:
            messagebox.showwarning(title='No selection', message='You must select an item')

    def click_new(self):
        self.decide = True
        self.frm_child_list.grid_forget()
        self.frm_child_crud['text'] = 'New Classification'
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.decide = False
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            self.directive = Message(action=70, information=[self.id_selected])
            self.connection = self.directive.send_directive(self.connection)
            self.txt_name_class.insert('1.0', self.connection.message.information[0])
            # Section to insert categories in textbox
            length_string = 0
            for item in self.connection.message.information[1]:
                elements = item.split('¥')
                self.txt_categories.insert('end-1c', elements[1] + ',')
                length_string += len(elements[1]) + 1
            self.txt_categories.delete('end-2c','end')
            self.frm_child_crud['text'] = 'Update classification'
            self.frm_child_list.grid_forget()
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(title='No selection', message='You must select an item')

    def click_save(self):
        if self.validate_fields():
            decision = messagebox.askyesno(title='Confirmation', message='Are you sure you want to save the changes?')
            name_aux = self.txt_name_class.get('1.0', 'end-1c')
            if decision:
                if self.decide:
                    self.directive = Message(action=66, information=[name_aux])
                    self.connection = self.directive.send_directive(self.connection)
                    id_classification = self.connection.message.information[0]
                    categories_aux = self.txt_categories.get('1.0', 'end-1c').split(',')
                    for item in categories_aux:
                        self.directive = Message(action=71, information=[item, id_classification])
                        self.connection = self.directive.send_directive(self.connection)
                else:
                    # Update classification name
                    self.directive = Message(action=68, information=[self.id_selected, name_aux])
                    self.connection = self.directive.send_directive(self.connection)
                    # Delete categories associated with the current classification
                    self.directive = Message(action=74, information=[self.id_selected])
                    self.connection = self.directive.send_directive(self.connection)
                    # Create categories for the current classification
                    categories_aux = self.txt_categories.get('1.0', 'end-1c').split(',')
                    for item in categories_aux:
                        self.directive = Message(action=71, information=[item, self.id_selected])
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
        if len(self.txt_name_class.get('1.0','end-1c')) != 0 and len(self.txt_categories.get('1.0','end-1c')) != 0:
            return True
        else:
            return False

    def clear_fields(self):
        self.txt_name_class.delete('1.0', 'end-1c')
        self.txt_categories.delete('1.0', 'end-1c')