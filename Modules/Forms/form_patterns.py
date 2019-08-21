from tkinter import ttk
from tkinter import *
from Modules.Config.Message import Message

TITLE_FONT = ("Arial", 14, "bold")
SUBTITLE_FONT = ("Arial", 12, "bold")
TEXT_FONT = ("Arial", 10, "italic")
LABEL_FONT = ("Arial", 10)


class FormParentPattern:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildPattern(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Patterns administration')
        lbl_experimenter_title.config(fg="#222cb3", font=TITLE_FONT)
        lbl_experimenter_title.grid(row=0, column=0, columnspan=9, pady=50)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildPattern:
    def __init__(self, frm_parent, connection):
        self.connection = connection
        self.decide = True
        self.id_selected = 0
        self.sections = []
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_crud = LabelFrame(frm_parent)
        self.initialize_components()

    def initialize_components(self):
        # Components for List FRM
        lbl_available = Label(self.frm_child_list, text='Available patterns')
        lbl_available.config(fg="#222cb3", font=SUBTITLE_FONT)
        lbl_available.grid(row=0, column=1, columnspan=4, rowspan=2, sticky=NW+SW, pady=50, padx=100)
        self.trv_available = ttk.Treeview(self.frm_child_list, height=20, columns='Name')
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.column('#0', width=50, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=400, minwidth=400, stretch=NO)
        self.trv_available.grid(row=2, column=1, columnspan=5, rowspan=10, sticky=W, padx=100)
        Button(self.frm_child_list, text='New', command=self.click_new).grid(row=2, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Delete', command=self.click_delete).grid(row=3, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Update', command=self.click_update).grid(row=4, column=7, columnspan=2, padx=25, sticky=W)

        # Components for CRUD FRM
        frm_aux1 = Frame(self.frm_child_crud)
        frm_aux2 = LabelFrame(self.frm_child_crud, text='Manage Content')
        lbl_name = Label(frm_aux1, text='Pattern Name')
        lbl_name.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_template = Label(frm_aux1, text='Template')
        lbl_template.config(fg="#222cb3", font=LABEL_FONT)
        lbl_template.grid(pady=10, padx=50, sticky=W)
        self.txt_name = Text(frm_aux1, height=1, width=60)
        self.txt_name.grid(row=0, column=1, padx=10, sticky=W)
        self.cbx_template = ttk.Combobox(frm_aux1, state="readonly", width=60)
        self.cbx_template.grid(row=1, column=1, pady=10, padx=10, sticky=W)
        Button(frm_aux1, text='Save', command=self.click_save).grid(row=0, column=2, padx=30)
        Button(frm_aux1, text='Cancel', command=self.click_cancel).grid(row=1, column=2, padx=30)
        lbl_section = Label(frm_aux2, text='Section')
        lbl_section.config(fg="#222cb3", font=LABEL_FONT)
        lbl_section.grid(pady=10, padx=50, sticky=W)
        self.cbx_section = ttk.Combobox(frm_aux2, state="readonly", width=60)
        self.cbx_section.grid(columnspan=2, pady=10, padx=50, sticky=NW+NE)
        self.cbx_section.bind("<<ComboboxSelected>>", self.cbx_section_selected)
        self.txt_desc_section = Text(frm_aux2, height=3, width=60)
        self.txt_desc_section.grid(columnspan=2, pady=10, padx=50, sticky=NW+NE)
        self.lbl_data = Label(frm_aux2, text='Text')
        self.lbl_data.config(fg="#222cb3", font=TEXT_FONT)
        self.lbl_data.grid(pady=20, padx=50, sticky=W)
        self.lbl_optional = Label(frm_aux2, text='Optional')
        self.lbl_optional.config(fg="#222cb3", font=TEXT_FONT)
        self.lbl_optional.grid(row=3, column=1, pady=20, padx=50, sticky=E)
        lbl_section = Label(frm_aux2, text='Content')
        lbl_section.config(fg="#222cb3", font=LABEL_FONT)
        lbl_section.grid(row=4, column=0, padx=50, sticky=W)
        self.txt_section = Text(frm_aux2, height=5, width=60)
        self.txt_section.grid(row=5, column=0, padx=50, pady=20, sticky=W)
        frm_aux1.grid(row=1, column=0, pady=20, padx=10, columnspan=3, rowspan=3)
        frm_aux2.grid(row=4, column=0, pady=20, padx=10, columnspan=3, rowspan=10)

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        msg = Message(action=42, information=[])
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.receive_message()
        for i in range(0, len(self.connection.message.information)):
            elements = self.connection.message.information[i].split(':')
            self.trv_available.insert('', 'end', text=elements[0], values=elements[1])

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
            msg = Message(action=44, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.retrieve_list()

    def click_new(self):
        '''self.decide = True
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)'''
        pass

    def click_update(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            self.decide = False
            self.frm_child_list.grid_forget()
            msg = Message(action=45, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.txt_name.insert('1.0', self.connection.message.information[0])
            id_template = self.set_cbx_template(self.connection.message.information[1])
            self.cbx_template['state'] = DISABLED
            msg = Message(action=40, information=[id_template])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.set_cbx_sections(self.connection.message.information[2])
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_save(self):
        '''if self.validate_fields():
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
            self.set_cbx_data('Text')
            self.var_check.set(0)
            self.frm_child_crud.grid_forget()
            self.show_frm()'''
        pass

    def click_cancel(self):
        self.txt_name.delete('1.0', 'end-1c')
        self.cbx_template['state'] = ACTIVE
        self.cbx_template['values'] = []
        self.cbx_section['values'] = []
        self.txt_desc_section['state'] = NORMAL
        self.txt_desc_section.delete('1.0','end-1c')
        self.txt_section.delete('1.0','end-1c')
        self.lbl_data['text'] = '-----'
        self.lbl_optional['text'] = '-----'
        self.frm_child_crud.grid_forget()
        self.show_frm()

    def set_cbx_template(self, text):
        text = text.split(':')
        self.cbx_template['values'] = []
        self.cbx_template.set('{}: {}'.format(text[1], text[2]))
        return int(text[0])

    def set_cbx_sections(self, sections):
        self.sections = sections
        self.cbx_section['values'] = []
        for i in range(0, len(sections)):
            elements = sections[i].split(':')
            self.cbx_section['values'] += (elements[1],)
        self.txt_desc_section['state'] = DISABLED

    def cbx_section_selected(self, event):
        self.txt_desc_section['state'] = NORMAL
        self.txt_desc_section.delete('1.0', 'end-1c')
        index = int(self.cbx_section.current())
        elements = self.sections[index].split(':')
        self.txt_desc_section.insert('1.0', elements[2])
        self.txt_desc_section['state'] = DISABLED
        self.lbl_data['text'] = elements[3]
        self.lbl_optional['text'] = elements[4]

    def validate_fields(self):
        '''if len(self.txt_name.get('1.0','end-1c')) != 0 and len(self.txt_description.get('1.0','end-1c')) != 0 and \
                len(self.cbx_data.get()) != 0:
            return True
        else:
            return False'''
        pass
