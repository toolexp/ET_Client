from tkinter import Label, LabelFrame, Frame, Text, Button, Listbox, messagebox, PhotoImage, Scrollbar
from tkinter.constants import *
from tkinter.ttk import Treeview, Combobox, Separator
from Modules.Config.Data import Message, wrap_text, CreateToolTip, Section
from Modules.Config.Visual import *


class FormParentSection:
    def __init__(self, window, connection):
        self.frm_parent = Frame(window)
        self.initialize_components()
        self.frm_child = FormChildSection(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Sections')
        lbl_experimenter_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_experimenter_title.grid(row=0, column=0, pady=20)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildSection:
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
        self.cancel_icon = PhotoImage(file=r"./Resources/cancel.png")
        self.back_icon = PhotoImage(file=r"./Resources/back.png")
        self.disabled_color = self.frm_child_list.cget('bg')

        # Components for List FRM
        lbl_sep1 = Label(self.frm_child_list)
        lbl_sep1.grid(row=0, column=0, padx=25, pady=25)
        self.trv_available = Treeview(self.frm_child_list, height=15, columns=('N', 'Name', 'Description', 'Data Type'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='N', anchor=CENTER)
        self.trv_available.heading('#2', text='Name', anchor=CENTER)
        self.trv_available.heading('#3', text='Description', anchor=CENTER)
        self.trv_available.heading('#4', text='Data Type', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#3', width=400, minwidth=400, stretch=NO)
        self.trv_available.column('#4', width=200, minwidth=200, stretch=NO)
        self.trv_available.grid(row=0, column=1, sticky=W, pady=25)
        vsb_trv_av = Scrollbar(self.frm_child_list, orient="vertical", command=self.trv_available.yview)
        vsb_trv_av.grid(row=0, column=2, pady=25, sticky=NS)
        self.trv_available.configure(yscrollcommand=vsb_trv_av.set)
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New section')
        btn_view = Button(frm_aux4, image=self.view_icon, command=self.click_view)
        btn_view.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_view_ttp = CreateToolTip(btn_view, 'View section')
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit section')
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=3, column=0, pady=5, padx=5, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete section')
        frm_aux4.grid(row=0, column=4, pady=25, padx=25, sticky=NW)

        # Components for CRUD FRM
        self.frm_aux1 = Frame(self.frm_child_crud)
        lbl_type = Label(self.frm_aux1, text='Data type*')
        lbl_type.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_type.grid(row=0, column=0, pady=10, padx=50, sticky=W)
        lbl_name = Label(self.frm_aux1, text='Name*')
        lbl_name.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name.grid(row=1, column=0, pady=10, padx=50, sticky=W)
        lbl_description = Label(self.frm_aux1, text='Description*\t')
        lbl_description.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_description.grid(row=2, column=0, pady=10, padx=50, sticky=NW)
        self.cbx_data = Combobox(self.frm_aux1, state="readonly")
        self.cbx_data['values'] = ['Text', 'File', 'Classification']
        self.cbx_data.grid(row=0, column=2, pady=10, sticky=W)
        self.cbx_data.bind("<<ComboboxSelected>>", self.cbx_data_selected)
        self.txt_name = Text(self.frm_aux1, height=1, width=60, font=TEXT_FONT)
        self.txt_name.grid(row=1, column=2, pady=10, sticky=W)
        lbl_sep2 = Label(self.frm_aux1)
        lbl_sep2.grid(row=0, column=1, rowspan=3, padx=10, pady=10)
        self.txt_description = Text(self.frm_aux1, height=6, width=60, font=TEXT_FONT)
        self.txt_description.grid(row=2, column=2, pady=10, sticky=W)
        vsb_txt_desc = Scrollbar(self.frm_aux1, orient="vertical", command=self.txt_description.yview)
        vsb_txt_desc.grid(row=2, column=3, pady=10, sticky=NS)
        self.txt_description.configure(yscrollcommand=vsb_txt_desc.set)
        sep_aux1 = Separator(self.frm_aux1, orient=VERTICAL)
        sep_aux1.grid(row=0, column=4, sticky=NS, rowspan=4, padx=20)
        self.btn_save = Button(self.frm_aux1, image=self.save_icon, command=self.click_save)
        btn_save_ttp = CreateToolTip(self.btn_save, 'Save section')
        self.btn_back = Button(self.frm_aux1, image=self.back_icon, command=self.click_back)
        btn_back_ttp = CreateToolTip(self.btn_back, 'Go back')
        self.btn_cancel = Button(self.frm_aux1, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel_ttp = CreateToolTip(self.btn_cancel, 'Cancel')
        self.frm_aux1.grid()

        # Frame for showing available classifications
        self.frm_aux2 = Frame(self.frm_aux1)
        lbl_class = Label(self.frm_aux2, text='Classification\t')
        lbl_class.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_class.grid(row=0, column=0, pady=10, padx=50, sticky=W)
        lbl_category = Label(self.frm_aux2, text='Categories')
        lbl_category.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_category.grid(row=1, column=0, pady=10, padx=50, sticky=NW)
        lbl_sep3 = Label(self.frm_aux2)
        lbl_sep3.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
        self.cbx_classification = Combobox(self.frm_aux2, state="readonly")
        self.cbx_classification.bind("<<ComboboxSelected>>", self.cbx_class_selected)
        self.cbx_classification.grid(row=0, column=2, pady=10, sticky=NW)
        self.lbx_category = Listbox(self.frm_aux2, font=TEXT_FONT, height=10, width=50, selectmode='none')
        self.lbx_category.config(bg=self.disabled_color)
        self.lbx_category.grid(row=1, column=2, pady=10, sticky=W)
        vsb_lbx_cat = Scrollbar(self.frm_aux2, orient="vertical", command=self.lbx_category.yview)
        vsb_lbx_cat.grid(row=1, column=3, pady=10, sticky=NS)
        self.lbx_category.configure(yscrollcommand=vsb_lbx_cat.set)
        self.enabled_color = self.txt_name.cget('bg')

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=32)
        self.connection = self.directive.send_directive(self.connection)
        # Adding elements into the list
        for index, item in enumerate(self.connection.message.information):
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(index+1, elements[1], elements[2], elements[3]))
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
        self.section = Section()
        self.txt_name.focus_set()
        self.frm_child_crud['text'] = 'New section'
        self.btn_save.grid(row=0, column=5, padx=20)
        self.btn_cancel.grid(row=1, column=5, padx=20)
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_view(self):
        if len(self.trv_available.selection()) == 1:
            id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            self.directive = Message(action=35, information=[id_selected])
            self.connection = self.directive.send_directive(self.connection)
            self.section = Section(section_id=id_selected, name=self.connection.message.information[0],
                                   description=self.connection.message.information[1],
                                   data_type=self.connection.message.information[2])
            self.txt_name.insert('1.0', self.section.name)
            self.txt_description.insert('1.0', self.section.description)
            self.cbx_data.set(self.section.data_type)
            if self.section.data_type == 'Classification':
                self.section.classification_id = self.connection.message.information[3]
                self.retrieve_classifications()
                self.directive = Message(action=70, information=[self.section.classification_id])
                self.connection = self.directive.send_directive(self.connection)
                self.cbx_classification.set(self.connection.message.information[0])
                self.cbx_class_selected()
                self.frm_aux2.grid(row=3, column=0, columnspan=4, sticky=W)
            self.txt_name['bg'] = self.disabled_color
            self.txt_description['bg'] = self.disabled_color
            self.lbx_category['bg'] = self.disabled_color
            self.txt_name['state'] = DISABLED
            self.txt_description['state'] = DISABLED
            self.cbx_data['state'] = DISABLED
            self.cbx_classification['state'] = DISABLED
            self.lbx_category['state'] = DISABLED
            self.frm_child_crud['text'] = 'View section'
            self.btn_back.grid(row=0, column=5, padx=20)
            self.frm_child_list.grid_forget()
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_update(self):
        if len(self.trv_available.selection()) == 1:
            id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            self.directive = Message(action=35, information=[id_selected, 'validate'])
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.action == 5:  # An error ocurred while trying to update the item
                messagebox.showerror(parent=self.frm_child_list, title='Can not update the item',
                                     message=self.connection.message.information[0])
            else:
                self.section = Section(section_id=id_selected, name=self.connection.message.information[0],
                                       description=self.connection.message.information[1],
                                       data_type=self.connection.message.information[2])
                self.txt_name.insert('1.0', self.section.name)
                self.txt_description.insert('1.0', self.section.description)
                self.cbx_data.set(self.section.data_type)
                if self.section.data_type == 'Classification':
                    self.section.classification_id = self.connection.message.information[3]
                    self.retrieve_classifications()
                    self.directive = Message(action=70, information=[self.section.classification_id])
                    self.connection = self.directive.send_directive(self.connection)
                    self.cbx_classification.set(self.connection.message.information[0])
                    self.cbx_class_selected()
                    self.frm_aux2.grid(row=3, column=0, columnspan=4, sticky=W)
                self.frm_child_crud['text'] = 'Update section'
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
                self.directive = Message(action=34, information=[id_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:  # An error ocurred while deleting the item
                    messagebox.showerror(parent=self.frm_child_list, title='Can not delete the item',
                                         message=self.connection.message.information[0])
                else:
                    self.retrieve_list()
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_save(self):
        if self.validate_section_fields():
            self.section.name = self.txt_name.get('1.0', 'end-1c')
            self.section.description = self.txt_description.get('1.0', 'end-1c')
            self.section.data_type = self.cbx_data.get()
            if self.section.section_id == 0:    # If creating a section
                if self.section.data_type == 'Classification':
                    id_class = self.classifications[self.cbx_classification.current()]
                    self.directive = Message(action=31, information=[self.section.name, self.section.description,
                                                                     self.section.data_type, id_class])
                else:
                    self.directive = Message(action=31, information=[self.section.name, self.section.description,
                                                                     self.section.data_type])
            else:   # If updating a section
                if self.section.data_type == 'Classification':
                    id_class = self.classifications[self.cbx_classification.current()]
                    self.directive = Message(action=33, information=[self.section.section_id, self.section.name,
                                                                     self.section.description, self.section.data_type,
                                                                     id_class])
                else:
                    self.directive = Message(action=33, information=[self.section.section_id, self.section.name,
                                                                     self.section.description, self.section.data_type])
            self.connection = self.directive.send_directive(self.connection)
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def click_back(self):
        self.txt_name['state'] = NORMAL
        self.txt_description['state'] = NORMAL
        self.cbx_data['state'] = NORMAL
        self.cbx_classification['state'] = NORMAL
        self.lbx_category['state'] = NORMAL
        self.txt_name['bg'] = self.enabled_color
        self.txt_description['bg'] = self.enabled_color
        self.lbx_category['bg'] = self.enabled_color
        self.clear_fields()
        self.frm_child_crud.grid_forget()
        self.show_frm()

    def click_cancel(self):
        decision = True
        if self.txt_name.get('1.0', 'end-1c') != self.section.name or \
                self.txt_description.get('1.0', 'end-1c') != self.section.description or \
                self.cbx_data.get() != self.section.data_type:
            decision = messagebox.askyesno(parent=self.frm_child_crud, title='Cancel',
                                           message='Are you sure you want to cancel?')
        if decision:
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def cbx_data_selected(self, event):
        if self.cbx_data.get() == 'Classification':
            self.retrieve_classifications()
            self.frm_aux2.grid(row=3, column=0, columnspan=4, sticky=W)
        else:
            self.frm_aux2.grid_forget()
        self.txt_name.focus_set()

    def cbx_class_selected(self, event=None):
        id_class = self.classifications[self.cbx_classification.current()]
        self.directive = Message(action=72, information=[id_class])
        self.connection = self.directive.send_directive(self.connection)
        self.lbx_category.delete(0, END)
        for index, item in enumerate(self.connection.message.information):
            item = item.split('¥')
            self.lbx_category.insert(END, '{}) {}'.format(index+1, item[1]))

    def retrieve_classifications(self):
        self.classifications = []
        self.lbx_category.delete(0, END)
        self.directive = Message(action=67)
        self.connection = self.directive.send_directive(self.connection)
        self.cbx_classification['values'] = []
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.cbx_classification['values'] += ('{}'.format(elements[1]),)
            self.classifications.append(int(elements[0]))

    def validate_section_fields(self):
        if len(self.txt_name.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='You must insert a name for the section')
            return False
        if len(self.txt_description.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='You must insert a description for the section')
            return False
        if len(self.cbx_data.get()) == 0:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='You must select data type for the section')
            return False
        if self.cbx_data.get() == 'Classification' and len(self.cbx_classification.get()) == 0:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='You must select a classification for this section')
            return False
        return True

    def clear_fields(self):
        self.btn_save.grid_forget()
        self.btn_cancel.grid_forget()
        self.btn_back.grid_forget()
        self.txt_name.delete('1.0', 'end-1c')
        self.txt_description.delete('1.0', 'end-1c')
        self.cbx_data.set('')
        self.cbx_classification.set('')
        self.lbx_category.delete(0, END)
        self.frm_aux2.grid_forget()