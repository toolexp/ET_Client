from tkinter import Label, LabelFrame, Frame, Text, Button, Listbox, messagebox
from tkinter.constants import *
from tkinter.ttk import Treeview, Combobox
from Modules.Config.Data import Message

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
        # Components for List FRM
        self.trv_available = Treeview(self.frm_child_list, height=7, columns=('Name', 'Description', 'Data Type'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.heading('#3', text='Data Type', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.column('#3', width=200, minwidth=200, stretch=NO)
        self.trv_available.grid(row=1, column=1, columnspan=5, rowspan=10, sticky=W, padx=100, pady=100)
        Button(self.frm_child_list, text='New', command=self.click_new).grid(row=3, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Delete', command=self.click_delete).grid(row=4, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Update', command=self.click_update).grid(row=5, column=7, columnspan=2, padx=25, sticky=W)

        # Components for CRUD FRM
        self.frm_aux1 = Frame(self.frm_child_crud)
        lbl_name = Label(self.frm_aux1, text='Name')
        lbl_name.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_description = Label(self.frm_aux1, text='Description')
        lbl_description.config(fg="#222cb3", font=LABEL_FONT)
        lbl_description.grid(pady=10, padx=50, sticky=W)
        lbl_type = Label(self.frm_aux1, text='Data type')
        lbl_type.config(fg="#222cb3", font=LABEL_FONT)
        lbl_type.grid(row=7, column=0, pady=10, padx=50, sticky=W)
        self.txt_name = Text(self.frm_aux1, height=1, width=60, font=TEXT_FONT)
        self.txt_name.grid(row=0, column=1, padx=10, sticky=W)
        self.txt_description = Text(self.frm_aux1, height=6, width=60, font=TEXT_FONT)
        self.txt_description.grid(row=1, column=1, padx=10, rowspan=6, pady=10, sticky=W)
        self.cbx_data = Combobox(self.frm_aux1, state="readonly")
        self.cbx_data['values'] = ['Text', 'File', 'Classification']
        self.cbx_data.grid(row=7, column=1, pady=10, padx=10, sticky=W)
        self.cbx_data.bind("<<ComboboxSelected>>", self.cbx_data_selected)
        Button(self.frm_aux1, text='Save', command=self.click_save).grid(row=0, column=3, padx=40)
        Button(self.frm_aux1, text='Cancel', command=self.click_cancel).grid(row=1, column=3, padx=40)
        self.btn_new_class = Button(self.frm_aux1, text='New Classification', command=self.click_new_class)
        self.frm_aux1.grid(row=1, column=0, pady=20, padx=10, columnspan=5, rowspan=10)

        # Frame for showing available classifications
        self.frm_aux2 = LabelFrame(self.frm_aux1, text='Select a classification')
        self.frm_aux2.config(fg="#222cb3", font=SUBTITLE_FONT)
        lbl_class = Label(self.frm_aux2, text='Classification:')
        lbl_class.config(fg="#222cb3", font=LABEL_FONT)
        lbl_class.grid(pady=10, padx=20, sticky=W)
        lbl_category = Label(self.frm_aux2, text='Categories:')
        defaultbg = self.frm_child_crud.cget('bg')
        lbl_category.config(bg=defaultbg, fg="#222cb3", font=LABEL_FONT)
        lbl_category.grid(row=0, column=1, pady=10, padx=20, sticky=W)
        self.cbx_classification = Combobox(self.frm_aux2, state="readonly")
        self.cbx_classification.bind("<<ComboboxSelected>>", self.cbx_class_selected)
        self.cbx_classification.grid(row=1, column=0, pady=10, padx=20, sticky=NW)
        self.lbx_category = Listbox(self.frm_aux2, font=TEXT_FONT, height=8, width=40)
        self.lbx_category.grid(row=1, column=1, pady=10, padx=20)
        #self.frm_aux2.grid(row=20, column=0, pady=20, padx=10, columnspan=5, rowspan=10)

        # Fram to create a new classification
        self.frm_class = LabelFrame(self.frm_child_crud, text='New classification')
        self.frm_class.config(fg="#222cb3", font=SUBTITLE_FONT)
        lbl_class = Label(self.frm_class, text='Name')
        lbl_class.config(fg="#222cb3", font=LABEL_FONT)
        lbl_class.grid(pady=10, padx=50, sticky=W)
        lbl_desc_categories = Label(self.frm_class, text='ENTER CATEGORIES SEPARATED BY A COMMA (NOT SPACES)')
        lbl_desc_categories.config(fg="#222cb3", font=LABEL_FONT)
        lbl_desc_categories.grid(pady=10, padx=50, columnspan=2, sticky=W)
        lbl_categories = Label(self.frm_class, text='Categories')
        lbl_categories.config(fg="#222cb3", font=LABEL_FONT)
        lbl_categories.grid(pady=10, padx=50, sticky=NW)
        self.txt_name_class = Text(self.frm_class, height=1, width=60, font=TEXT_FONT)
        self.txt_name_class.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        self.txt_categories = Text(self.frm_class, height=3, width=60, font=TEXT_FONT)
        self.txt_categories.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        Button(self.frm_class, text='Save', command=self.click_save_class).grid(row=0, column=3, padx=20)
        Button(self.frm_class, text='Cancel', command=self.click_cancel_class).grid(row=1, column=3, padx=20)
        #self.frm_aux3.grid(row=1, column=0, pady=20, padx=10, columnspan=5, rowspan=10)

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=32, information=[])
        self.connection = self.directive.send_directive(self.connection)
        # Adding elements into the list
        for i in range(0, len(self.connection.message.information)):
            elements = self.connection.message.information[i].split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1], elements[2], elements[3]))

    def show_frm(self):
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid_forget()

    def click_delete(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            self.directive = Message(action=34, information=[int(self.id_selected)])
            self.connection = self.directive.send_directive(self.connection)
            self.retrieve_list()

    def click_new(self):
        self.decide = True
        self.frm_child_list.grid_forget()
        self.frm_child_crud['text'] = 'New section'
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            self.decide = False
            self.frm_child_list.grid_forget()
            self.directive = Message(action=35, information=[int(self.id_selected)])
            self.connection = self.directive.send_directive(self.connection)
            self.txt_name.insert('1.0', self.connection.message.information[0])
            self.txt_description.insert('1.0', self.connection.message.information[1])
            self.cbx_data.set(self.connection.message.information[2])
            self.frm_child_crud['text'] = 'Update template'
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_save(self):
        if self.validate_section_fields():
            decision = messagebox.askyesno(title='Confirmation', message='Are you sure you want to save the changes?')
            if decision:
                type_aux = self.cbx_data.get()
                if type_aux == 'Classification':
                    id_class = self.cbx_classification.get().split(':')[0]
                    self.directive = Message(action=70, information=[int(id_class)])
                    self.connection = self.directive.send_directive(self.connection)
                    name_aux = self.connection.message.information[0]
                    description_aux = ''
                    if self.decide:
                        self.directive = Message(action=31, information=[name_aux, description_aux, type_aux, int(id_class)])
                    else:
                        self.directive = Message(action=33,
                                                 information=[int(self.id_selected), name_aux, description_aux, type_aux,
                                                              int(id_class)])

                else:
                    name_aux = self.txt_name.get('1.0','end-1c')
                    description_aux = self.txt_description.get('1.0','end-1c')
                    if self.decide:
                        self.directive = Message(action=31, information=[name_aux, description_aux, type_aux])
                    else:
                        self.directive = Message(action=33, information=[int(self.id_selected), name_aux, description_aux, type_aux])
                self.connection = self.directive.send_directive(self.connection)
                self.txt_name.delete('1.0', 'end-1c')
                self.txt_description.delete('1.0', 'end-1c')
                self.cbx_data.set('')
                self.frm_child_crud.grid_forget()
                self.show_frm()

    def click_cancel(self):
        decision = messagebox.askyesno(title='Cancel', message='Are you sure you want to cancel?')
        if decision:
            self.txt_name.delete('1.0', 'end-1c')
            self.txt_description.delete('1.0', 'end-1c')
            self.cbx_data.set('')
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def click_new_class(self):
        self.frm_aux1.grid_forget()
        self.txt_name_class.focus_set()
        self.frm_class.grid(row=1, column=0, pady=20, padx=10, columnspan=5, rowspan=10)\

    def click_save_class(self):
        if self.validate_class_fields():
            name_aux = self.txt_name_class.get('1.0', 'end-1c')
            categories_aux = self.txt_categories.get('1.0', 'end-1c')
            categories_aux = categories_aux.split(',')
            self.directive = Message(action=66, information=[name_aux])
            self.connection = self.directive.send_directive(self.connection)
            id_class = self.connection.message.information[0].split('¥')[0]
            for item in categories_aux:
                self.directive = Message(action=71, information=[item, int(id_class)])
                self.connection = self.directive.send_directive(self.connection)
            self.txt_name_class.delete('1.0', 'end-1c')
            self.txt_categories.delete('1.0', 'end-1c')
            self.frm_class.grid_forget()
            self.retrieve_classifications()
            self.frm_aux1.grid(row=1, column=0, pady=20, padx=10, columnspan=5, rowspan=10)

    def click_cancel_class(self):
        self.frm_class.grid_forget()
        self.frm_aux1.grid(row=1, column=0, pady=20, padx=10, columnspan=5, rowspan=10)

    def cbx_data_selected(self, event):
        if self.cbx_data.get() == 'Classification':
            self.txt_name.delete('1.0', 'end-1c')
            self.txt_name['state'] = DISABLED
            self.txt_description.delete('1.0', 'end-1c')
            self.txt_description['state'] = DISABLED
            self.retrieve_classifications()
            self.btn_new_class.grid(row=7, column=1, padx=40)
            self.frm_aux2.grid(row=9, column=0, pady=20, padx=10, columnspan=10, rowspan=10 )
        else:
            self.txt_name.focus_set()
            self.txt_name['state'] = NORMAL
            self.txt_description['state'] = NORMAL
            self.btn_new_class.grid_forget()
            self.frm_class.grid_forget()
            self.frm_aux2.grid_forget()

    def cbx_class_selected(self, event):
        item = self.cbx_classification.get().split(':')[0]
        self.directive = Message(action=72, information=[int(item)])
        self.connection = self.directive.send_directive(self.connection)
        self.lbx_category.delete(0, END)
        for item in self.connection.message.information:
            item = item.split('¥')
            self.lbx_category.insert(END, '{}: {}'.format(item[0], item[1]))

    def retrieve_classifications(self):
        self.lbx_category.delete(0, END)
        self.directive = Message(action=67, information=[])
        self.connection = self.directive.send_directive(self.connection)
        self.cbx_classification['values'] = []
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.cbx_classification['values'] += ('{}: {}'.format(elements[0], elements[1]),)

    def validate_section_fields(self):
        if (self.cbx_classification.get()) != 0:
            if self.cbx_data.get() == 'Classification':
                return True
            else:
                if len(self.txt_name.get('1.0','end-1c')) != 0 and len(self.txt_description.get('1.0','end-1c')) != 0:
                        return True
                else:
                    return False
        else:
            return False

    def validate_class_fields(self):
        if len(self.txt_name_class.get('1.0','end-1c')) != 0 and len(self.txt_categories.get('1.0','end-1c')) != 0:
            return True
        else:
            return False

