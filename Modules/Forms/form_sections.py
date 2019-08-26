from tkinter import ttk
from tkinter import *
from Modules.Config.Message import Message

TITLE_FONT = ("Arial", 14, "bold")
SUBTITLE_FONT = ("Arial", 12, "bold")
ERROR_FONT = ("Arial", 10, "italic")
LABEL_FONT = ("Arial", 10)


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
        self.decide = True
        self.id_selected = 0
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_crud = LabelFrame(frm_parent)
        self.initialize_components()

    def initialize_components(self):
        # Components for List FRM
        lbl_available = Label(self.frm_child_list, text='Available sections')
        lbl_available.config(fg="#222cb3", font=SUBTITLE_FONT)
        lbl_available.grid(row=0, column=1, columnspan=4, rowspan=2, sticky=NW+SW, pady=50, padx=100)
        self.trv_available = ttk.Treeview(self.frm_child_list, height=20, columns=('Name', 'Description'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.column('#0', width=50, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.grid(row=2, column=1, columnspan=5, rowspan=10, sticky=W, padx=100)
        Button(self.frm_child_list, text='New', command=self.click_new).grid(row=2, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Delete', command=self.click_delete).grid(row=3, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Update', command=self.click_update).grid(row=4, column=7, columnspan=2, padx=25, sticky=W)

        # Components for CRUD FRM
        frm_aux = Frame(self.frm_child_crud)
        lbl_name = Label(frm_aux, text='Name')
        lbl_name.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_description = Label(frm_aux, text='Description')
        lbl_description.config(fg="#222cb3", font=LABEL_FONT)
        lbl_description.grid(pady=10, padx=50, sticky=W)
        lbl_type = Label(frm_aux, text='Data type')
        lbl_type.config(fg="#222cb3", font=LABEL_FONT)
        lbl_type.grid(row=7, column=0, pady=10, padx=50, sticky=W)
        self.var_check = IntVar()
        self.check_optional = Checkbutton(frm_aux, text="This section is optional", variable=self.var_check)
        self.check_optional.grid(row=8, column=0, pady=20, padx=50, sticky=W)
        self.txt_name = Text(frm_aux, height=1, width=60)
        self.txt_name.grid(row=0, column=1, padx=10, sticky=W)
        self.txt_description = Text(frm_aux, height=6, width=60)
        self.txt_description.grid(row=1, column=1, padx=10, rowspan=6, pady=10, sticky=W)
        self.cbx_data = ttk.Combobox(frm_aux, state="readonly")
        self.cbx_data['values'] = ['Text', 'URL', 'Image']
        self.cbx_data.grid(row=7, column=1, pady=10, padx=10, sticky=W)
        Button(frm_aux, text='Save', command=self.click_save).grid(row=7, column=3, padx=40)
        Button(frm_aux, text='Cancel', command=self.click_cancel).grid(row=8, column=3, padx=40)
        frm_aux.grid(row=1, column=0, pady=20, padx=10, columnspan=5, rowspan=10)

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        msg = Message(action=32, information=[])
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.receive_message()
        for i in range(0, len(self.connection.message.information)):
            elements = self.connection.message.information[i].split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1], elements[2]))

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
            msg = Message(action=34, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.retrieve_list()

    def click_new(self):
        self.decide = True
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            self.decide = False
            self.frm_child_list.grid_forget()
            msg = Message(action=35, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.txt_name.insert('1.0', self.connection.message.information[0])
            self.txt_description.insert('1.0', self.connection.message.information[1])
            self.set_cbx_data(self.connection.message.information[2])
            if self.connection.message.information[3]:
                self.var_check.set(0)
            else:
                self.var_check.set(1)
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_save(self):
        if self.validate_fields():
            name_aux = self.txt_name.get('1.0','end-1c')
            description_aux = self.txt_description.get('1.0','end-1c')
            type_aux = self.cbx_data.get()
            if self.var_check.get() == 1:
                aux_option = False
            else:
                aux_option = True
            if self.decide:
                msg = Message(action=31, information=[name_aux, description_aux, type_aux, aux_option])
            else:
                msg = Message(action=33, information=[int(self.id_selected), name_aux, description_aux, type_aux, aux_option])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.txt_name.delete('1.0', 'end-1c')
            self.txt_description.delete('1.0', 'end-1c')
            self.cbx_data.set('')
            self.var_check.set(0)
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def click_cancel(self):
        self.txt_name.delete('1.0', 'end-1c')
        self.txt_description.delete('1.0', 'end-1c')
        self.cbx_data.set('')
        self.var_check.set(0)
        self.frm_child_crud.grid_forget()
        self.show_frm()

    def set_cbx_data(self, text):
        if text == 'Text':
            self.cbx_data.current(0)
        elif text == 'URL':
            self.cbx_data.current(1)
        elif text == 'Image':
            self.cbx_data.current(2)
        else:
            self.cbx_data.current(2)

    def validate_fields(self):
        if len(self.txt_name.get('1.0','end-1c')) != 0 and len(self.txt_description.get('1.0','end-1c')) != 0 and \
                len(self.cbx_data.get()) != 0:
            return True
        else:
            return False
