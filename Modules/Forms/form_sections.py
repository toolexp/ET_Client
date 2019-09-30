from tkinter import Label, LabelFrame, Frame, Text, Button, Listbox, messagebox, PhotoImage
from tkinter.constants import *
from tkinter.ttk import Treeview, Combobox
from Modules.Config.Data import Message, wrap_text, CreateToolTip

TITLE_FONT = ("Arial", 18)
SUBTITLE_FONT = ("Arial", 14)
LABEL_FONT = ("Arial", 10)
TEXT_FONT = ("Arial", 10)


class FormParentSection:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildSection(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Sections administration')
        lbl_experimenter_title.config(fg="#222cb3", font=TITLE_FONT)
        lbl_experimenter_title.grid(row=0, column=0, columnspan=9, pady=50)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)
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
        self.frm_child_crud.config(fg="#222cb3", font=SUBTITLE_FONT)
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
        defaultbg = self.frm_child_crud.cget('bg')

        # Components for List FRM
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=10, padx=10, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New section')
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=1, column=0, pady=10, padx=10, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete section')
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=2, column=0, pady=10, padx=10, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit section')
        frm_aux4.grid(row=1, column=0, pady=35, padx=20, sticky=NW)
        self.trv_available = Treeview(self.frm_child_list, height=7, columns=('Name', 'Description', 'Data Type'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.heading('#3', text='Data Type', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.column('#3', width=200, minwidth=200, stretch=NO)
        self.trv_available.grid(row=1, column=1, columnspan=5, rowspan=10, sticky=W, padx=50, pady=25)

        # Components for CRUD FRM
        self.frm_aux1 = Frame(self.frm_child_crud)
        lbl_type = Label(self.frm_aux1, text='Data type             ')
        lbl_type.config(fg="#222cb3", font=LABEL_FONT)
        lbl_type.grid(pady=10, padx=50, sticky=W)
        lbl_name = Label(self.frm_aux1, text='Name')
        lbl_name.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_description = Label(self.frm_aux1, text='Description')
        lbl_description.config(fg="#222cb3", font=LABEL_FONT)
        lbl_description.grid(pady=10, padx=50, sticky=W)
        self.cbx_data = Combobox(self.frm_aux1, state="readonly")
        self.cbx_data['values'] = ['Text', 'File', 'Classification']
        self.cbx_data.grid(row=0, column=1, pady=10, padx=10, sticky=W)
        self.cbx_data.bind("<<ComboboxSelected>>", self.cbx_data_selected)
        self.txt_name = Text(self.frm_aux1, height=1, width=60, font=TEXT_FONT)
        self.txt_name.grid(row=1, column=1, padx=10, sticky=W)
        self.txt_description = Text(self.frm_aux1, height=6, width=60, font=TEXT_FONT)
        self.txt_description.grid(row=2, column=1, padx=10, rowspan=6, pady=10, sticky=W)
        btn_save = Button(self.frm_aux1, image=self.save_icon, command=self.click_save)
        btn_save.grid(row=0, column=3, padx=40)
        btn_save_ttp = CreateToolTip(btn_save, 'Save section')
        btn_cancel = Button(self.frm_aux1, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel.grid(row=1, column=3, padx=40)
        btn_cancel_ttp = CreateToolTip(btn_cancel, 'Cancel')
        self.frm_aux1.grid(row=1, column=0, pady=20, padx=10, columnspan=5, rowspan=10)

        # Frame for showing available classifications
        self.frm_aux2 = Frame(self.frm_aux1)
        lbl_class = Label(self.frm_aux2, text='Select classification')
        lbl_class.config(fg="#222cb3", font=LABEL_FONT)
        lbl_class.grid(pady=10, padx=50, sticky=W)
        lbl_category = Label(self.frm_aux2, text='Categories')
        lbl_category.config(fg="#222cb3", font=LABEL_FONT)
        lbl_category.grid(pady=10, padx=50, sticky=NW)
        self.cbx_classification = Combobox(self.frm_aux2, state="readonly")
        self.cbx_classification.bind("<<ComboboxSelected>>", self.cbx_class_selected)
        self.cbx_classification.grid(row=0, column=1, pady=10, padx=10, sticky=NW)
        self.lbx_category = Listbox(self.frm_aux2, font=TEXT_FONT, height=8, width=40, selectmode='none')
        self.lbx_category.config(bg=defaultbg)
        self.lbx_category.grid(row=1, column=1, pady=10, padx=10, sticky=W)
        #self.frm_aux2.grid(row=20, column=0, pady=20, padx=10, columnspan=5, rowspan=10)

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=32, information=[])
        self.connection = self.directive.send_directive(self.connection)
        # Adding elements into the list
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1], wrap_text(elements[2],75) ,
                                                                           elements[3]))

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
                self.directive = Message(action=34, information=[self.id_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:
                    messagebox.showwarning(title='Fail deleting',
                                           message='The section cant be deleted, it may be used in a template')
                self.retrieve_list()
        else:
            messagebox.showwarning(title='No selection', message='You must select an item')

    def click_new(self):
        self.decide = True
        self.frm_child_list.grid_forget()
        self.txt_name.focus_set()
        self.frm_child_crud['text'] = 'New section'
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.decide = False
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            self.frm_child_list.grid_forget()
            self.directive = Message(action=35, information=[self.id_selected])
            self.connection = self.directive.send_directive(self.connection)
            self.txt_name.insert('1.0', self.connection.message.information[0])
            self.txt_description.insert('1.0', self.connection.message.information[1])
            self.cbx_data.set(self.connection.message.information[2])
            if self.connection.message.information[2] == 'Classification':
                id_class = self.connection.message.information[3]
                self.retrieve_classifications()
                self.directive = Message(action=70, information=[id_class])
                self.connection = self.directive.send_directive(self.connection)
                self.cbx_classification.set(self.connection.message.information[0])
                self.cbx_class_selected()
                self.frm_aux2.grid(row=9, column=0, pady=20, padx=10, columnspan=5, rowspan=10, sticky=W)
            self.frm_child_crud['text'] = 'Update section'
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(title='No selection', message='You must select an item')

    def click_save(self):
        if self.validate_section_fields():
            decision = messagebox.askyesno(title='Confirmation', message='Are you sure you want to save the changes?')
            if decision:
                name_aux = self.txt_name.get('1.0', 'end-1c')
                description_aux = self.txt_description.get('1.0', 'end-1c')
                type_aux = self.cbx_data.get()
                if self.decide:
                    if type_aux == 'Classification':
                        id_class = self.classifications[self.cbx_classification.current()]
                        self.directive = Message(action=31, information=[name_aux, description_aux, type_aux, id_class])
                    else:
                        self.directive = Message(action=31, information=[name_aux, description_aux, type_aux])
                else:
                    if type_aux == 'Classification':
                        id_class = self.classifications[self.cbx_classification.current()]
                        self.directive = Message(action=33,information=[self.id_selected, name_aux, description_aux,
                                                                        type_aux, id_class])
                    else:
                        self.directive = Message(action=33, information=[self.id_selected, name_aux, description_aux,
                                                                         type_aux])
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

    def cbx_data_selected(self, event):
        if self.cbx_data.get() == 'Classification':
            self.retrieve_classifications()
            self.frm_aux2.grid(row=9, column=0, pady=20, padx=10, columnspan=5, rowspan=10, sticky=W)
        else:
            self.frm_aux2.grid_forget()
        self.txt_name.focus_set()

    def cbx_class_selected(self, event=None):
        id_class = self.classifications[self.cbx_classification.current()]
        self.directive = Message(action=72, information=[id_class])
        self.connection = self.directive.send_directive(self.connection)
        self.lbx_category.delete(0, END)
        for item in self.connection.message.information:
            item = item.split('¥')
            self.lbx_category.insert(END, '{}'.format(item[1]))

    def retrieve_classifications(self):
        self.classifications = []
        self.lbx_category.delete(0, END)
        self.directive = Message(action=67, information=[])
        self.connection = self.directive.send_directive(self.connection)
        self.cbx_classification['values'] = []
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.cbx_classification['values'] += ('{}'.format(elements[1]),)
            self.classifications.append(int(elements[0]))

    def validate_section_fields(self):
        if (self.cbx_classification.get()) != 0:
            if len(self.txt_name.get('1.0','end-1c')) != 0 and len(self.txt_description.get('1.0','end-1c')) != 0:
                if self.cbx_data.get() == 'Classification':
                    if self.cbx_classification.get() != 0:
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def clear_fields(self):
        self.txt_name.delete('1.0', 'end-1c')
        self.txt_description.delete('1.0', 'end-1c')
        self.cbx_data.set('')
        self.cbx_classification.set('')
        self.lbx_category.delete(0, END)
        self.frm_aux2.grid_forget()