from tkinter import Label, LabelFrame, Text, Button, messagebox, PhotoImage, Frame, Scrollbar
from tkinter.constants import *
from tkinter.ttk import Treeview, Separator
from Modules.Config.Data import Message, CreateToolTip
from Modules.Config.Visual import *


class FormParentClassification:
    def __init__(self, window, connection):
        self.frm_parent = Frame(window)
        self.initialize_components()
        self.frm_child = FormChildClassification(self.frm_parent, connection)

    def initialize_components(self):
        lbl_title = Label(self.frm_parent, text='Classifications')
        lbl_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_title.grid(row=0, column=0, pady=20)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0)
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
        self.view_icon = PhotoImage(file=r"./Resources/view.png")
        self.modify_icon = PhotoImage(file=r"./Resources/modify.png")
        self.remove_icon = PhotoImage(file=r"./Resources/delete.png")
        self.save_icon = PhotoImage(file=r"./Resources/save.png")
        self.back_icon = PhotoImage(file=r"./Resources/back.png")
        self.cancel_icon = PhotoImage(file=r"./Resources/cancel.png")
        self.disabled_color = self.frm_child_list.cget('bg')

        # Components for List FRM
        lbl_sep1 = Label(self.frm_child_list)
        lbl_sep1.grid(row=0, column=0, padx=25, pady=25)
        self.trv_available = Treeview(self.frm_child_list, height=15, columns=('N', 'Name', '# categories'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='N', anchor=CENTER)
        self.trv_available.heading('#2', text='Name', anchor=CENTER)
        self.trv_available.heading('#3', text='# categories', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#3', width=150, minwidth=150, stretch=NO)
        self.trv_available.grid(row=0, column=1, sticky=W, pady=25)
        vsb_trv_av = Scrollbar(self.frm_child_list, orient="vertical", command=self.trv_available.yview)
        vsb_trv_av.grid(row=0, column=2, pady=25, sticky=NS)
        self.trv_available.configure(yscrollcommand=vsb_trv_av.set)
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New classification')
        btn_view = Button(frm_aux4, image=self.view_icon, command=self.click_view)
        btn_view.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_view_ttp = CreateToolTip(btn_view, 'View classification')
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit classification')
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=3, column=0, pady=5, padx=5, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete classification')
        frm_aux4.grid(row=0, column=4, pady=25, padx=25, sticky=NW)

        # Components CRUD
        self.frm_class = LabelFrame(self.frm_child_crud)
        self.frm_class.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_class = Label(self.frm_child_crud, text='Name*')
        lbl_class.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_class.grid(row=0, column=0, pady=10, padx=20, sticky=W)
        lbl_desc_categories = Label(self.frm_child_crud, text='Enter categories separated by an Enter (\\n)')
        lbl_desc_categories.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_desc_categories.grid(row=1, column=0, pady=10, padx=20, columnspan=4, sticky=W)
        lbl_categories = Label(self.frm_child_crud, text='Categories*')
        lbl_categories.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_categories.grid(row=2, column=0, pady=10, padx=20, sticky=NW)
        lbl_sep2 = Label(self.frm_child_crud)
        lbl_sep2.grid(row=2, column=1, padx=20, pady=10)
        self.txt_name_class = Text(self.frm_child_crud, height=1, width=50, font=TEXT_FONT)
        self.txt_name_class.grid(row=0, column=2, columnspan=2, pady=10, sticky=W)
        self.txt_categories = Text(self.frm_child_crud, height=10, width=50, font=TEXT_FONT)
        self.txt_categories.grid(row=2, column=2, pady=10, sticky=W)
        vsb_txt_cat = Scrollbar(self.frm_child_crud, orient="vertical", command=self.txt_categories.yview)
        vsb_txt_cat.grid(row=2, column=3, pady=10, sticky=NS)
        self.txt_categories.configure(yscrollcommand=vsb_txt_cat.set)
        sep_aux1 = Separator(self.frm_child_crud, orient=VERTICAL)
        sep_aux1.grid(row=0, column=4, sticky=NS, rowspan=3, padx=20)
        self.btn_save = Button(self.frm_child_crud, image=self.save_icon, command=self.click_save)
        btn_save_ttp = CreateToolTip(self.btn_save, 'Save classification')
        self.btn_back = Button(self.frm_child_crud, image=self.back_icon, command=self.click_back)
        btn_back_ttp = CreateToolTip(self.btn_back, 'Go back')
        self.btn_cancel = Button(self.frm_child_crud, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel_ttp = CreateToolTip(self.btn_cancel, 'Cancel')
        self.enabled_color = self.txt_name_class.cget('bg')

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=67, information=[])
        self.connection = self.directive.send_directive(self.connection)
        # Adding elements into the list
        for index, item in enumerate(self.connection.message.information):
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(index+1, elements[1], elements[2]))
        if len(self.trv_available.get_children()) != 0:
            self.trv_available.selection_set(self.trv_available.get_children()[0])

    def show_frm(self):
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        self.clear_fields()
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid_forget()

    def click_new(self):
        self.decide = True
        self.frm_child_crud['text'] = 'New Classification'
        self.txt_name_class.focus_set()
        self.btn_save.grid(row=0, column=5, padx=20)
        self.btn_cancel.grid(row=1, column=5, padx=20)
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_view(self):
        if len(self.trv_available.selection()) == 1:
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            self.directive = Message(action=70, information=[self.id_selected])
            self.connection = self.directive.send_directive(self.connection)
            # Insert information into visual components
            self.txt_name_class.insert('1.0', self.connection.message.information[0])
            # Section to insert categories in textbox
            length_string = 0
            for item in self.connection.message.information[1]:
                elements = item.split('¥')
                self.txt_categories.insert('end-1c', elements[1] + '\n')
                length_string += len(elements[1]) + 1
            self.txt_categories.delete('end-2c', 'end')
            self.frm_child_crud['text'] = 'View classification'
            self.txt_name_class['bg'] = self.disabled_color
            self.txt_categories['bg'] = self.disabled_color
            self.txt_name_class['state'] = DISABLED
            self.txt_categories['state'] = DISABLED
            self.btn_back.grid(row=0, column=5, padx=20)
            self.frm_child_list.grid_forget()
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_update(self):
        if len(self.trv_available.selection()) == 1:
            self.decide = False
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            self.directive = Message(action=70, information=[self.id_selected, 'validate'])
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.action == 5:     # An error ocurred while trying to update the item
                messagebox.showerror(parent=self.frm_child_list, title='Can not update the item',
                                     message=self.connection.message.information[0])
            else:
                self.txt_name_class.insert('1.0', self.connection.message.information[0])
                # Section to insert categories in textbox
                length_string = 0
                for item in self.connection.message.information[1]:
                    elements = item.split('¥')
                    self.txt_categories.insert('end-1c', elements[1] + '\n')
                    length_string += len(elements[1]) + 1
                self.txt_categories.delete('end-2c', 'end')
                self.frm_child_crud['text'] = 'Update classification'
                self.txt_name_class.focus_set()
                self.btn_save.grid(row=0, column=5, padx=20)
                self.btn_cancel.grid(row=1, column=5, padx=20)
                self.frm_child_list.grid_forget()
                self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_delete(self):
        if len(self.trv_available.selection()) == 1:
            decision = messagebox.askyesno(parent=self.frm_child_list, title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
                self.directive = Message(action=69, information=[self.id_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:  # An error ocurred while deleting the item
                    messagebox.showerror(parent=self.frm_child_list, title='Can not delete the item',
                                         message=self.connection.message.information[0])
                else:
                    self.retrieve_list()
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_save(self):
        validation_opt = self.validate_fields()
        if validation_opt == 0:
            name_aux = self.txt_name_class.get('1.0', 'end-1c')
            if self.decide:
                self.directive = Message(action=66, information=[name_aux])
                self.connection = self.directive.send_directive(self.connection)
                id_classification = self.connection.message.information[0]
                categories_aux = self.txt_categories.get('1.0', 'end-1c').split('\n')
                for item in categories_aux:
                    if item:    # None blank space will be saved
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
                categories_aux = self.txt_categories.get('1.0', 'end-1c').split('\n')
                for item in categories_aux:
                    if item:
                        self.directive = Message(action=71, information=[item, self.id_selected])
                        self.connection = self.directive.send_directive(self.connection)
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()
        elif validation_opt == 1:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='There are mandatory fields that need to be filled!')
        else:
            messagebox.showwarning(parent=self.frm_child_crud, title='Category problem',
                                   message='A category can not be empty!')

    def click_back(self):
        self.txt_name_class['state'] = NORMAL
        self.txt_categories['state'] = NORMAL
        self.txt_name_class['bg'] = self.enabled_color
        self.txt_categories['bg'] = self.enabled_color
        self.clear_fields()
        self.frm_child_crud.grid_forget()
        self.show_frm()

    def click_cancel(self):
        decision = messagebox.askyesno(parent=self.frm_child_crud, title='Cancel',
                                       message='Are you sure you want to cancel?')
        if decision:
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def validate_fields(self):
        if len(self.txt_name_class.get('1.0', 'end-1c')) != 0 and len(self.txt_categories.get('1.0', 'end-1c')) != 0:
            categories_aux = self.txt_categories.get('1.0', 'end-1c').split('\n')
            for item in categories_aux:
                for char in item:
                    if char.isspace() or char == '\t' or not char or char == '\n':
                        return 2
            return 0
        else:
            return 1

    def clear_fields(self):
        self.btn_save.grid_forget()
        self.btn_cancel.grid_forget()
        self.btn_back.grid_forget()
        self.txt_name_class.delete('1.0', 'end-1c')
        self.txt_categories.delete('1.0', 'end-1c')