from tkinter import Label, LabelFrame, Entry, Text, Button, messagebox, PhotoImage, Frame, Scrollbar
from tkinter.constants import *
from tkinter.ttk import Treeview, Separator
from Modules.Config.Data import Message, CreateToolTip, Classification, summarize_text
from Modules.Config.Visual import *


class FormParentClassification:
    def __init__(self, window, connection):
        self.frm_parent = Frame(window)
        self.initialize_components()
        self.frm_child = FormChildClassification(self.frm_parent, connection)

    def initialize_components(self):
        lbl_title = Label(self.frm_parent, text='Classifications')
        lbl_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_title.grid(row=0, column=0, pady=20, padx=20)

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

        # Components for List FRM
        lbl_sep1 = Label(self.frm_child_list)
        lbl_sep1.grid(row=0, column=0, padx=10, pady=25)
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
        self.txt_name_class = Entry(self.frm_child_crud, width=50, font=TEXT_FONT)
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

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=67)
        self.connection = self.directive.send_directive(self.connection)
        # Adding elements into the list
        for index, item in enumerate(self.connection.message.information):
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(index+1, summarize_text(elements[1], 200),
                                                                           summarize_text(elements[2], 150)))
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
        self.classification = Classification()
        self.frm_child_crud['text'] = 'New Classification'
        self.txt_name_class.focus_set()
        self.btn_save.grid(row=0, column=5, padx=20)
        self.btn_cancel.grid(row=1, column=5, padx=20)
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_view(self):
        if len(self.trv_available.selection()) == 1:
            id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            # Retrieve selected classification from the database
            self.directive = Message(action=70, information=[id_selected])
            self.connection = self.directive.send_directive(self.connection)
            self.classification = Classification(id=id_selected, name=self.connection.message.information[0],
                                                 categories=self.connection.message.information[1])
            # Insert information into visual components
            self.txt_name_class.insert(0, self.classification.name)
            # Section to insert categories in textbox
            length_string = 0
            for item in self.classification.categories:
                elements = item.split('¥')
                self.txt_categories.insert('end-1c', elements[1] + '\n')
                length_string += len(elements[1]) + 1
            self.txt_categories.delete('end-2c', 'end')
            self.frm_child_crud['text'] = 'View classification'
            self.txt_name_class['bg'] = DISABLED_COLOR
            self.txt_categories['bg'] = DISABLED_COLOR
            self.txt_name_class['state'] = DISABLED
            self.txt_categories['state'] = DISABLED
            self.btn_back.grid(row=0, column=5, padx=20)
            self.frm_child_list.grid_forget()
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_update(self):
        if len(self.trv_available.selection()) == 1:
            id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            self.directive = Message(action=70, information=[id_selected, 'validate'])
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.action == 5:     # An error ocurred while trying to update the item
                messagebox.showerror(parent=self.frm_child_list, title='Can not update the item',
                                     message=self.connection.message.information[0])
            else:
                self.classification = Classification(id=id_selected, name=self.connection.message.information[0],
                                                     categories=self.connection.message.information[1])
                self.txt_name_class.insert(0, self.classification.name)
                # Section to insert categories in textbox
                length_string = 0
                for item in self.classification.categories:
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
                id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
                self.directive = Message(action=69, information=[id_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:  # An error ocurred while deleting the item
                    messagebox.showerror(parent=self.frm_child_list, title='Can not delete the item',
                                         message=self.connection.message.information[0])
                else:
                    self.retrieve_list()
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_save(self):
        if self.validate_fields():
            self.classification.name = self.txt_name_class.get()
            if self.classification.id == 0:     # Creating a new classification
                self.directive = Message(action=66, information=[self.classification.name])
                self.connection = self.directive.send_directive(self.connection)
                self.classification.id = self.connection.message.information[0]
                self.classification.categories = self.txt_categories.get('1.0', 'end-1c').split('\n')
                for item in self.classification.categories:
                    if item:    # None blank space will be saved
                        self.directive = Message(action=71, information=[item, self.classification.id])
                        self.connection = self.directive.send_directive(self.connection)
            else:   # Updating a classification
                self.directive = Message(action=68, information=[self.classification.id, self.classification.name])
                self.connection = self.directive.send_directive(self.connection)
                # Delete categories associated with the current classification
                self.directive = Message(action=74, information=[self.classification.id])
                self.connection = self.directive.send_directive(self.connection)
                # Create categories for the current classification
                self.classification.categories = self.txt_categories.get('1.0', 'end-1c').split('\n')
                for item in self.classification.categories:
                    if item:  # None blank space will be saved
                        self.directive = Message(action=71, information=[item, self.classification.id])
                        self.connection = self.directive.send_directive(self.connection)
            self.click_back()

    def click_back(self):
        self.clear_fields()
        self.frm_child_crud.grid_forget()
        self.show_frm()

    def click_cancel(self):
        decision = True
        categories_aux = len(self.txt_categories.get('1.0', 'end-1c').split('\n'))
        categories_aux = categories_aux - 1 if self.classification.id == 0 else categories_aux
        if self.txt_name_class.get() != self.classification.name or \
                categories_aux != len(self.classification.categories):
            decision = messagebox.askyesno(parent=self.frm_child_crud, title='Cancel',
                                           message='Are you sure you want to cancel?')
        if decision:
            self.click_back()

    def validate_fields(self):
        if len(self.txt_name_class.get()) == 0:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='You must insert a name for the classification')
            return False
        if len(self.txt_categories.get('1.0', 'end-1c')) != 0:
            categories_aux = self.txt_categories.get('1.0', 'end-1c').split('\n')
            for item in categories_aux:
                for char in item:
                    if char.isspace() or char == '\t' or not char or char == '\n':
                        messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                               message='A category can not be empty')
                        return False
            return True
        else:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='You must insert at least one category')
            return False

    def clear_fields(self):
        self.btn_save.grid_forget()
        self.btn_cancel.grid_forget()
        self.btn_back.grid_forget()
        self.txt_name_class['state'] = NORMAL
        self.txt_categories['state'] = NORMAL
        self.txt_name_class['bg'] = ENABLED_COLOR
        self.txt_categories['bg'] = ENABLED_COLOR
        self.txt_name_class.delete(0, END)
        self.txt_categories.delete('1.0', 'end-1c')