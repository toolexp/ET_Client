from tkinter import ttk
from tkinter import *
from Modules.Config.Message import Message
from Modules.Config.Pattern import Pattern

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
        self.pattern = Pattern()
        self.templates = []
        self.idx_section = None
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
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=500, minwidth=500, stretch=NO)
        self.trv_available.grid(row=2, column=1, columnspan=5, rowspan=10, sticky=W, padx=100)
        Button(self.frm_child_list, text='New', command=self.click_new).grid(row=2, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Delete', command=self.click_delete).grid(row=3, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Update', command=self.click_update).grid(row=4, column=7, columnspan=2, padx=25, sticky=W)

        # Components for CRUD FRM
        frm_aux1 = Frame(self.frm_child_crud)
        self.frm_aux2 = LabelFrame(self.frm_child_crud, text='Manage Content')
        self.frm_aux2.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name = Label(frm_aux1, text='Pattern Name')
        lbl_name.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_template = Label(frm_aux1, text='Template')
        lbl_template.config(fg="#222cb3", font=LABEL_FONT)
        lbl_template.grid(pady=10, padx=50, sticky=W)
        self.txt_name = Text(frm_aux1, height=1, width=60)
        self.txt_name.grid(row=0, column=1, padx=10, sticky=W)
        self.cbx_template = ttk.Combobox(frm_aux1, state="readonly", width=70)
        self.cbx_template.grid(row=1, column=1, pady=10, padx=10, sticky=W)
        self.cbx_template.bind("<<ComboboxSelected>>", self.cbx_template_selected)
        Button(frm_aux1, text='Save', command=self.click_save).grid(row=0, column=2, padx=30)
        Button(frm_aux1, text='Cancel', command=self.click_cancel).grid(row=1, column=2, padx=30)
        lbl_section = Label(self.frm_aux2, text='Section')
        lbl_section.config(fg="#222cb3", font=LABEL_FONT)
        lbl_section.grid(pady=10, padx=50, sticky=W)
        self.cbx_section = ttk.Combobox(self.frm_aux2, state="readonly", width=60)
        self.cbx_section.grid(columnspan=2, pady=10, padx=50, sticky=NW+NE)
        self.cbx_section.bind("<<ComboboxSelected>>", self.cbx_section_selected)
        self.txt_desc_section = Text(self.frm_aux2, height=3, width=60)
        self.txt_desc_section.grid(columnspan=2, pady=10, padx=50, sticky=NW+NE)
        self.lbl_data = Label(self.frm_aux2, text='Text')
        #self.lbl_data.config(fg="#222cb3", font=TEXT_FONT)
        self.lbl_data.grid(pady=20, padx=50, sticky=W)
        self.lbl_optional = Label(self.frm_aux2, text='Optional')
        #self.lbl_optional.config(fg="#222cb3", font=TEXT_FONT)
        self.lbl_optional.grid(row=3, column=1, pady=20, padx=50, sticky=E)
        lbl_section = Label(self.frm_aux2, text='Content')
        lbl_section.config(fg="#222cb3", font=LABEL_FONT)
        lbl_section.grid(row=4, column=0, padx=50, sticky=W)
        self.txt_section = Text(self.frm_aux2, height=6, width=80)
        self.txt_section.grid(row=5, column=0, columnspan=2, padx=50, pady=20, sticky=W)
        frm_aux1.grid(row=1, column=0, pady=20, padx=10, columnspan=3, rowspan=3)
        self.frm_aux2.grid(row=4, column=0, pady=20, padx=10, columnspan=3, rowspan=10)

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        msg = Message(action=42, information=[])
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.receive_message()
        for i in range(0, len(self.connection.message.information)):
            elements = self.connection.message.information[i].split('¥')
            print(elements[1])
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1],))

    def show_frm(self):
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        self.click_cancel()
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
        self.decide = True
        for child in self.frm_aux2.winfo_children():
            child.configure(state='disable')
        msg = Message(action=37)
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.receive_message()
        self.templates = self.connection.message.information
        self.cbx_template['values'] = []
        for i in range(0, len(self.templates)):
            elements = self.templates[i].split('¥')
            self.cbx_template['values'] += ('{}: {}'.format(elements[1], elements[2]),)
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

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
            self.pattern.name = self.connection.message.information[0]
            self.pattern.template = self.connection.message.information[1]
            self.txt_name.insert('1.0', self.pattern.name)
            id_template = self.set_cbx_template(self.connection.message.information[1])
            self.cbx_template['state'] = DISABLED
            msg = Message(action=40, information=[id_template])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.set_cbx_sections(self.connection.message.information[2])
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_save(self):
        self.save_section()
        if self.validate_fields():
            if self.decide:
                msg = Message(action=41, information=[self.pattern.name, int(self.pattern.template.split('¥')[0])])
                self.connection.create_message(msg)
                self.connection.send_message()
                self.connection.receive_message()
                id_pattern = self.connection.message.information[0]
                for i in range(0, len(self.pattern.content)):
                    msg = Message(action=46, information=[self.pattern.content[i], id_pattern, int(self.pattern.sections[i].split('¥')[0]), None])
                    self.connection.create_message(msg)
                    self.connection.send_message()
                    self.connection.receive_message()
            else:
                msg = Message(action=43, information=[int(self.id_selected), self.pattern.name])
                self.connection.create_message(msg)
                self.connection.send_message()
                self.connection.receive_message()
                for i in range(0, len(self.pattern.content)):
                    elements = self.pattern.content[i].split('¥')
                    msg = Message(action=48, information=[int(elements[0]), elements[1], None])
                    self.connection.create_message(msg)
                    self.connection.send_message()
                    self.connection.receive_message()
            self.click_cancel()

    def click_cancel(self):
        for child in self.frm_aux2.winfo_children():
            child.configure(state='normal')
        self.pattern = Pattern()
        self.txt_name.delete('1.0', 'end-1c')
        self.cbx_template['state'] = ACTIVE
        self.cbx_template.set('')
        self.cbx_template['values'] = []
        self.cbx_section.set('')
        self.cbx_section['values'] = []
        self.txt_desc_section['state'] = NORMAL
        self.txt_desc_section.delete('1.0','end-1c')
        self.txt_section.delete('1.0','end-1c')
        self.lbl_data['text'] = '-----'
        self.lbl_optional['text'] = '-----'
        self.frm_child_crud.grid_forget()
        self.show_frm()

    def set_cbx_template(self, text):
        text = text.split('¥')
        self.cbx_template['values'] = []
        self.cbx_template.set('{}: {}'.format(text[1], text[2]))
        return int(text[0])

    def set_cbx_sections(self, sections):
        self.pattern.sections = sections
        if self.decide:
            self.pattern.content = []
        else:
            msg = Message(action=47, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.pattern.content = self.connection.message.information
            if int(self.pattern.content[0].split('¥')[0]) > int(self.pattern.content[1].split('¥')[0]):
                self.pattern.content.reverse()
        self.idx_section = None
        self.cbx_section.set('')
        self.cbx_section['values'] = []
        for i in range(0, len(sections)):
            if self.decide:
                self.pattern.content.append(None)
            self.cbx_section['values'] += (sections[i].split('¥')[1],)
        self.txt_desc_section['state'] = DISABLED

    def cbx_template_selected(self, event):
        for child in self.frm_aux2.winfo_children():
            child.configure(state='normal')
        self.pattern.template = self.templates[int(self.cbx_template.current())]
        id_template = self.templates[int(self.cbx_template.current())].split('¥')[0]
        msg = Message(action=40, information=[int(id_template)])
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.receive_message()
        self.set_cbx_sections(self.connection.message.information[2])
        self.txt_desc_section['state'] = NORMAL
        self.txt_desc_section.delete('1.0', 'end-1c')
        self.txt_section.delete('1.0', 'end-1c')
        self.lbl_data['text'] = '-----'
        self.lbl_optional['text'] = '-----'

    def cbx_section_selected(self, event):
        self.txt_desc_section['state'] = NORMAL
        self.txt_desc_section.delete('1.0', 'end-1c')
        elements = self.pattern.sections[int(self.cbx_section.current())].split('¥')
        self.txt_desc_section.insert('1.0', elements[2])
        self.txt_desc_section['state'] = DISABLED
        self.lbl_data['text'] = 'Data type: ' + elements[3]
        self.lbl_optional['text'] = 'This section is: ' + elements[4]
        self.save_section()
        self.txt_section.focus_set()

    def save_section(self):
        if self.idx_section is not None:
            if self.decide:
                self.pattern.content[self.idx_section] = self.txt_section.get('1.0','end-1c')
            else:
                self.pattern.content[self.idx_section] = self.pattern.content[self.idx_section].split('¥')
                self.pattern.content[self.idx_section][1] = self.txt_section.get('1.0','end-1c')
                self.pattern.content[self.idx_section] = '¥'.join(self.pattern.content[self.idx_section])
            self.txt_section.delete('1.0', 'end-1c')
            if self.pattern.content[int(self.cbx_section.current())] is not None:
                if self.decide:
                    self.txt_section.insert('1.0', self.pattern.content[int(self.cbx_section.current())])
                else:
                    self.txt_section.insert('1.0', self.pattern.content[int(self.cbx_section.current())].split('¥')[1])
        elif not self.decide:
            self.txt_section.insert('1.0', self.pattern.content[int(self.cbx_section.current())].split('¥')[1])
        self.idx_section = int(self.cbx_section.current())

    def validate_fields(self):
        if len(self.txt_name.get('1.0','end-1c')) != 0:
            self.pattern.name = self.txt_name.get('1.0','end-1c')
            for item in self.pattern.content:
                if item is None or item == '':
                    if self.pattern.sections[self.pattern.content.index(item)].split('¥')[-1] == 'Mandatory':
                        return False
            return True
        else:
            return False
