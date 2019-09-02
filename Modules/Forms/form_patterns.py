from tkinter import Label, LabelFrame, Frame, Text, Button, filedialog, Canvas
from tkinter.constants import *
from tkinter.ttk import Treeview, Notebook, Combobox, Style
from Modules.Config.Data import Message, Pattern, File, Section
from PIL import Image, ImageTk
import os

TITLE_FONT = ("Arial", 18)
SUBTITLE_FONT = ("Arial", 14)
LABEL_FONT = ("Arial", 10)
TEXT_FONT = ("Arial", 10)


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
        self.initialize_variables()
        self.id_selected = 0
        self.templates = []
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_crud = LabelFrame(frm_parent)
        self.frm_child_crud.config(fg="#222cb3", font=SUBTITLE_FONT)
        self.initialize_components()

    def initialize_components(self):
        """
        Method that initialize the visual components for each form associated with the local administration
        """
        # Components for List FRM
        self.trv_available = Treeview(self.frm_child_list, height=20, columns='Name')
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=500, minwidth=500, stretch=NO)
        self.trv_available.grid(row=1, column=1, columnspan=5, rowspan=10, sticky=W, padx=100, pady=100)
        Button(self.frm_child_list, text='New', command=self.click_new).grid(row=2, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Delete', command=self.click_delete).grid(row=3, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Update', command=self.click_update).grid(row=4, column=7, columnspan=2, padx=25, sticky=W)

        # Components for CRUD FRM
        frm_aux1 = Frame(self.frm_child_crud)
        self.frm_aux2 = LabelFrame(self.frm_child_crud, text='Pattern content')
        self.frm_aux2.config(fg="#222cb3", font=SUBTITLE_FONT)
        lbl_name = Label(frm_aux1, text='Pattern Name')
        lbl_name.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_template = Label(frm_aux1, text='Template')
        lbl_template.config(fg="#222cb3", font=LABEL_FONT)
        lbl_template.grid(pady=10, padx=50, sticky=W)
        self.txt_name = Text(frm_aux1, height=1, width=60)
        self.txt_name.config(font=TEXT_FONT)
        self.txt_name.grid(row=0, column=1, padx=10, sticky=W)
        self.cbx_template = Combobox(frm_aux1, state="readonly", width=70)
        self.cbx_template.config(font=TEXT_FONT)
        self.cbx_template.grid(row=1, column=1, pady=10, padx=10, sticky=W)
        self.cbx_template.bind("<<ComboboxSelected>>", self.cbx_template_selected)
        Button(frm_aux1, text='Save', command=self.click_save).grid(row=0, column=2, padx=30)
        Button(frm_aux1, text='Cancel', command=self.click_cancel).grid(row=1, column=2, padx=30)
        lbl_section = Label(self.frm_aux2, text='Section')
        lbl_section.config(fg="#222cb3", font=LABEL_FONT)
        lbl_section.grid(pady=10, padx=50, sticky=W)
        self.cbx_section = Combobox(self.frm_aux2, state="readonly", width=60)
        self.cbx_section.config(font=TEXT_FONT)
        self.cbx_section.grid(columnspan=2, pady=10, padx=50, sticky=NW+NE)
        self.cbx_section.bind("<<ComboboxSelected>>", self.cbx_section_selected)
        self.txt_desc_section = Text(self.frm_aux2, height=3, width=60)
        defaultbg = self.frm_child_crud.cget('bg')
        self.txt_desc_section.config(background=defaultbg, font=TEXT_FONT)
        self.txt_desc_section.grid(columnspan=2, pady=10, padx=50, sticky=NW+NE)
        self.lbl_data = Label(self.frm_aux2, text='Text')
        self.lbl_data.config(fg="#222cb3", font=LABEL_FONT)
        self.lbl_data.grid(pady=10, padx=50, sticky=W)
        self.lbl_optional = Label(self.frm_aux2, text='Optional')
        self.lbl_optional.config(fg="#222cb3", font=LABEL_FONT)
        self.lbl_optional.grid(row=3, column=1, pady=10, padx=50, sticky=E)
        lbl_section = Label(self.frm_aux2, text='Content')
        lbl_section.config(fg="#222cb3", font=LABEL_FONT)
        lbl_section.grid(row=4, column=0, padx=50, sticky=W)

        style = Style()
        style.theme_use("clam")
        style.configure("Treeview", foreground="gray")
        style.layout('TNotebook.Tab', [])  # turn off tabs
        self.tab_control = Notebook(self.frm_aux2)
        tab_desc = Frame(self.tab_control)
        self.tab_control.add(tab_desc)
        self.txt_section = Text(tab_desc, height=8, width=80)
        self.txt_section.config(font=TEXT_FONT)
        self.txt_section.grid(row=0, column=0, columnspan=2, padx=50, pady=20, sticky=W)
        tab_file = Frame(self.tab_control)
        self.tab_control.add(tab_file)
        lbl_upload = Label(tab_file, text='Load a file for this section: ')
        lbl_upload.config(fg="#222cb3", font=LABEL_FONT)
        lbl_upload.grid(row=0, column=0, padx=20, pady=20, sticky=W)
        Button(tab_file, text='Upload', command=self.click_upload).grid(row=1, column=0, padx=20, pady=5, sticky=W)
        Button(tab_file, text='Delete', command=self.click_remove).grid(row=2, column=0, padx=20, pady=5, sticky=W)
        self.canvas = Canvas(tab_file, width=160, height=160)
        self.canvas.config(background = 'white', borderwidth=1)
        self.canvas.grid(row=0, column=3, padx=20, pady=10, columnspan=5, rowspan=10, sticky=E)
        self.tab_control.grid(row=4, column=0, columnspan=2, rowspan=10, padx=50, pady=10, sticky=W)
        self.trv_summary = Treeview(self.frm_child_crud, height=10, columns=('Section', 'Mandatory','Complete'))
        #self.trv_summary.config(bg=defaultbg)
        self.trv_summary.heading('#0', text='ID', anchor=CENTER)
        self.trv_summary.heading('#1', text='Section', anchor=CENTER)
        self.trv_summary.heading('#2', text='Mandatory', anchor=CENTER)
        self.trv_summary.heading('#3', text='Complete', anchor=CENTER)
        self.trv_summary.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_summary.column('#1', width=80, minwidth=80, stretch=NO)
        self.trv_summary.column('#2', width=80, minwidth=80, stretch=NO, anchor=CENTER)
        self.trv_summary.column('#3', width=80, minwidth=80, stretch=NO, anchor=CENTER)
        self.trv_summary.grid(row=6, column=4, columnspan=1, rowspan=5, sticky=W, padx=10)
        frm_aux1.grid(row=1, column=0, pady=20, padx=10, columnspan=3, rowspan=3)
        self.frm_aux2.grid(row=4, column=0, pady=10, padx=10, columnspan=3, rowspan=10)

    def initialize_variables(self):
        """
        Method that set the local variables to its initial state (empty)
        """
        self.directive = Message()
        self.pattern = Pattern()
        self.file = None
        self.image = None
        self.selected_section = Section()
        self.decide = True

    def retrieve_list(self):
        """
        Method that retrieve available patterns from the server and displays them in the TreeView from
        the List Form
        """
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        # Retrieve elements from the server
        self.directive = Message(action=42, information=[])
        self.connection = self.directive.send_directive(self.connection)
        # Adding elements in the list
        for i in range(0, len(self.connection.message.information)):
            elements = self.connection.message.information[i].split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1],))

    def show_frm(self):
        """
        Show the List form when the Patterns administration called
        """
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        """
        Hide the Patterns administration Forms
        """
        self.click_cancel()
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid_forget()

    def restart_components(self):
        self.txt_name.delete('1.0', 'end-1c')
        self.cbx_section.set('')
        self.cbx_section['values'] = []
        self.txt_desc_section['state'] = NORMAL
        self.txt_desc_section.delete('1.0','end-1c')
        self.txt_section.delete('1.0','end-1c')
        self.lbl_data['text'] = '-----'
        self.lbl_optional['text'] = '-----'
        if self.image is not None:
            self.canvas.delete(self.image)
            self.image = None
        self.tab_control.select(0)

    def click_delete(self):
        """
        Method that removes a selected pattern from the initial list (changes are updated in DB)
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            self.directive = Message(action=44, information=[int(self.id_selected)])
            self.connection = self.directive.send_directive(self.connection)
            self.retrieve_list()

    def click_new(self):
        """
        Initialize CRUD Form for creating a new pattern. It uploads available templates to the combobox
        """
        self.decide = True
        for child in self.frm_aux2.winfo_children():
            try:
                child.configure(state=DISABLED)
            except:
                pass
        self.tab_control.tab(0, state='disabled')
        self.tab_control.tab(1, state='disabled')
        self.directive = Message(action=37)
        self.connection = self.directive.send_directive(self.connection)
        self.templates = self.connection.message.information
        self.cbx_template['values'] = []
        for i in range(0, len(self.templates)):
            elements = self.templates[i].split('¥')
            self.cbx_template['values'] += ('{}: {}'.format(elements[1], elements[2]),)
        self.frm_child_list.grid_forget()
        self.frm_child_crud['text'] = 'New Pattern'
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        '''if self.trv_available.item(self.trv_available.selection())['text'] != '':
            item = self.trv_available.item(self.trv_available.selection()) # Retrieve selected item from TreeView
            self.id_selected = item['text'] # Obtain id of the selected item
            self.decide = False
            self.frm_child_list.grid_forget()
            self.directive = Message(action=45, information=[int(self.id_selected)]) # Ask for the information of selected pattern to the server
            self.connection = self.directive.send_directive(self.connection)
            # Save received information in local Pattern object
            self.pattern.name = self.connection.message.information[0]
            self.pattern.template = self.connection.message.information[1]
            # Fill visual components with pattern info
            self.txt_name.insert('1.0', self.pattern.name)
            id_template = self.set_cbx_template(self.pattern.template)
            self.directive = Message(action=40, information=[id_template]) # Ask for the sections of the selected pattern to the server
            self.connection = self.directive.send_directive(self.connection)
            self.set_cbx_sections(self.connection.message.information[2]) # Get data for sections of the pattern and its content, and store them in the local pattern object
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)'''

    def click_save(self):
        self.save_section_local('save')
        if self.validate_fields():
            if self.decide:
                self.directive = Message(action=41, information=[self.pattern.name, int(self.pattern.template.split('¥')[0])])
                self.connection = self.directive.send_directive(self.connection)
                id_pattern = self.connection.message.information[0]
                for i in range(0, len(self.pattern.text_content)):
                    self.directive = Message(action=46, information=[self.pattern.text_content[i], id_pattern, None])
                    self.connection = self.directive.send_directive(self.connection)
                for i in range(0, len(self.pattern.file_content)):
                    self.directive = Message(action=61, information=[self.pattern.file_content[i].file_bytes,
                                                                     self.pattern.file_content[i].name])
                    self.connection = self.directive.send_directive(self.connection)
                    id_diagram = self.connection.message.information[0]
                    self.directive = Message(action=46, information=[None, id_pattern, id_diagram])
                    self.connection = self.directive.send_directive(self.connection)
            '''else:
                msg = Message(action=43, information=[int(self.id_selected), self.pattern.name])
                self.connection.create_message(msg)
                self.connection.send_message()
                self.connection.receive_message()
                for i in range(0, len(self.pattern.content)):
                    elements = self.pattern.content[i].split('¥')
                    msg = Message(action=48, information=[int(elements[0]), elements[1], None])
                    self.connection.create_message(msg)
                    self.connection.send_message()
                    self.connection.receive_message()'''
            self.click_cancel()

    def click_cancel(self):
        '''for child in self.frm_aux2.winfo_children():
            child.configure(state='normal')'''
        self.initialize_variables()
        for item in self.trv_summary.get_children():
            self.trv_summary.delete(item)
        self.cbx_template['state'] = ACTIVE
        self.cbx_template.set('')
        self.cbx_template['values'] = []
        self.restart_components()
        self.frm_child_crud.grid_forget()
        self.show_frm()

    def click_upload(self):
        """
        Create a File object that is uploaded by the user, validating that there is not a file uploaded already.
        """
        if self.file is None:
            filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select JPEG file",
                                                  filetypes=[("jpeg", "*.jpg")])
            if not filename:
                return  # user cancelled; stop this method
            self.file = File()
            self.file.read_file(filename)
            self.show_file(self.file)

    def click_remove(self):
        """
        Remove an uploaded file from the system validating it is already uploaded. This method also delete
        any image in the canvas that may be fulfilled with an image.
        """
        if self.file is not None:
            if self.image is not None:  # if an image was already loaded
                self.canvas.delete(self.image)
                self.image = None
            self.file = None

    def set_cbx_template(self, text):
        text = text.split('¥')
        self.cbx_template['values'] = []
        self.cbx_template.set('{}: {}'.format(text[1], text[2]))
        self.cbx_template['state'] = DISABLED
        return int(text[0])

    def cbx_template_selected(self, event):
        for child in self.frm_aux2.winfo_children():
            try:
                child.configure(state=NORMAL)
            except:
                pass
        self.tab_control.tab(0, state='normal')
        self.tab_control.tab(1, state='normal')
        self.initialize_variables()
        self.restart_components()
        self.pattern.template = self.templates[int(self.cbx_template.current())] # The selected template is associated with the local pattern object
        id_template = self.pattern.template.split('¥')[0]
        self.directive = Message(action=40, information=[int(id_template)])
        self.connection = self.directive.send_directive(self.connection)
        self.set_cbx_sections(self.connection.message.information[2])

    def set_cbx_sections(self, sections):
        """
        Set cbx_section visual component depending of the selection (New or update pattern)
        and stores this information in local pattern object for future handling

        :param sections:
            Sections associated with the template of the handled pattern
        """

        # Loop that filter sections by their data type, so they can be correctly handled.
        # The section is saved in the correspondent "type"_section of the local pattern
        # object.
        for item in sections:
            item_data_type = item.split('¥')[5]
            if item_data_type == 'Text':
                self.pattern.text_sections.append(item)
            elif item_data_type == 'File':
                self.pattern.file_sections.append(item)

        # Block that retrieve the content of correspondent section and save it in the
        # "type"_content of the local pattern object when self.decision = False (Update pattern),
        # otherwise (New pattern) the "type"_content of the local pattern object wil be
        # initialized empty.
        if self.decide:
            self.pattern.text_content = []
            self.pattern.file_content = []
            for item in sections:
                item_data_type = item.split('¥')[5]
                if item_data_type == 'Text':
                    self.pattern.text_content.append(None)
                elif item_data_type == 'File':
                    self.pattern.file_content.append(None)
        else:
            self.directive = Message(action=47, information=[int(self.id_selected)]) # Ask for the content of each section of the selected pattern to the server
            self.connection = self.directive.send_directive(self.connection)
            content = self.connection.message.information
            for item in content:
                item_content_type_diagram = item.split('¥')[3]
                item_content_type_text = item.split('¥')[2]
                if item_content_type_text != 'None':
                    self.pattern.text_content.append(item)
                elif item_content_type_diagram != 'None':
                    """Aqui recuperar el diagrama, guardarlo localmente y poner el path en contenido junto con el id del contenido"""
                    self.directive = Message(action=47, information=[int(
                        self.id_selected)])  # Ask for the content of each section of the selected pattern to the server
                    self.connection = self.directive.send_directive(self.connection)
                    self.pattern.file_content.append(item)
            '''if int(self.pattern.content[0].split('¥')[0]) > int(self.pattern.content[1].split('¥')[0]):
                self.pattern.content.reverse()'''

        # Set visual components
        for item in self.trv_summary.get_children():
            self.trv_summary.delete(item)
        self.cbx_section.set('')
        self.cbx_section['values'] = []
        for item in sections:
            elements = item.split('¥')
            self.cbx_section['values'] += (elements[3],)
            self.trv_summary.insert('', 'end', text=elements[2], values=(elements[3],elements[-1],''))
        self.txt_desc_section['state'] = DISABLED


    def cbx_section_selected(self, event):
        """
        Stores current information inserted by the user in visual components into the local pattern object.
        Displays content associated with the selected combobox item if it is not empty.
        :param event:
        """
        # This call_back function saves the current info inserted by the user into the local pattern object. Before
        # it is deleted and replaced by info from the selected section.
        self.save_section_local('not_save_yet')

        # This block locates the selected section in the text_sections or file_section of the local pattern object
        # and display that info in the visual components, so the user knows what kind of data has to insert.
        # It also saves the current index and data type of the selected field for saving later the inserted info in the
        # local pattern object.
        self.txt_desc_section['state'] = NORMAL
        self.txt_desc_section.delete('1.0', 'end-1c')
        selected_section = self.cbx_section.get()
        not_found = True
        for item in self.pattern.text_sections:
            if item.split('¥')[3] == selected_section:
                self.selected_section = Section(int(self.pattern.text_sections.index(item)), 'Text', item)
                self.tab_control.select(0)
                not_found = False
                break
        if not_found:
            for item in self.pattern.file_sections:
                if item.split('¥')[3] == selected_section:
                    self.selected_section = Section(int(self.pattern.file_sections.index(item)), 'File', item)
                    self.tab_control.select(1)
                    not_found = False
                    break

        # This call_back function displays the content of the current selected section that is stored in the local
        # pattern object. If it is null, then the visual content components will be showed empty.
        self.display_section_local()

    def save_section_local(self, text_decision):
        """
        This function stores all the content inserted in the current visual components into the local pattern object
        depending of the data type of the selected_section, before it is deleted and replaced with the information
        of the new selected_section. If "text_decision" == "save" it wont be necessary to empty visual fields
        :parameter: text_decision: string: auxiliary to tell if the function was called from the event "push save button"
        :return:
        """
        if self.selected_section.index is not None: # Necessary to avoid trouble when the combobox is selected for the first time
            if self.decide:
                if self.selected_section.data_type == 'Text':
                    self.pattern.text_content[self.selected_section.index] = self.txt_section.get('1.0','end-1c')
                    id_section = self.selected_section.section.split('¥')[2]
                    for item in self.trv_summary.get_children():
                        if self.trv_summary.item(item)['text'] == id_section:
                            values = self.trv_summary.item(item)['values']
                            if self.txt_section.get('1.0', 'end-1c') != '':
                                self.trv_summary.item(item, values=(values[0], values[1], '✓'))
                            else:
                                self.trv_summary.item(item, values=(values[0], values[1], ''))
                    if text_decision != 'save':
                        self.txt_section.delete('1.0', 'end-1c')
                elif self.selected_section.data_type == 'File':
                    self.pattern.file_content[self.selected_section.index] = self.file
                    id_section = self.selected_section.section.split('¥')[2]
                    for item in self.trv_summary.get_children():
                        if self.trv_summary.item(item)['text'] == id_section:
                            values = self.trv_summary.item(item)['values']
                            if self.file is not None:
                                self.trv_summary.item(item, values=(values[0], values[1], '✓'))
                            else:
                                self.trv_summary.item(item, values=(values[0], values[1], ''))
                    if text_decision != 'save':
                        if self.image is not None:
                            self.canvas.delete(self.image)
                            self.image = None
                        self.file = None
            else:
                '''self.pattern.content[self.id_selected_section] = self.pattern.content[self.id_selected_section].split('¥')
                self.pattern.content[self.id_selected_section][1] = self.txt_section.get('1.0','end-1c')
                self.pattern.content[self.id_selected_section] = '¥'.join(self.pattern.content[self.id_selected_section])
            self.txt_section.delete('1.0', 'end-1c')
            if self.pattern.content[int(self.cbx_section.current())] is not None:
                if self.decide:
                    self.txt_section.insert('1.0', self.pattern.content[int(self.cbx_section.current())])
                else:
                    self.txt_section.insert('1.0', self.pattern.content[int(self.cbx_section.current())].split('¥')[1])
        elif not self.decide:
            self.txt_section.insert('1.0', self.pattern.content[int(self.cbx_section.current())].split('¥')[1])'''

    def display_section_local(self):
        """
        Displays the information of the new selected_section and its content (if it is not empty) into the visual
        components of the form, depending of the data type of this section.
        """
        # This section retrieve the information of the selection section, so it can be showed as a guide for the
        # user of the GUI.
        elements = self.selected_section.section.split('¥')
        self.txt_desc_section.insert('1.0', elements[4])
        self.txt_desc_section['state'] = DISABLED
        self.lbl_data['text'] = 'Data type: ' + elements[5]
        if elements[6] == '✓':
            aux = 'mandatory'
        else:
            aux = 'optional'
        self.lbl_optional['text'] = 'This section is ' + aux

        # This section retrieve the content of the selected section and displays (depending of the data_type) it
        # into the visual components if it is not empty.
        if self.selected_section.data_type == 'Text':
            if self.pattern.text_content[self.selected_section.index] is not None:
                self.txt_section.insert('1.0', self.pattern.text_content[self.selected_section.index])
                self.txt_section.focus_set()
        elif self.selected_section.data_type == 'File':
            if self.pattern.file_content[self.selected_section.index] is not None:
                self.file = self.pattern.file_content[self.selected_section.index]
                self.show_file(self.pattern.file_content[self.selected_section.index])

    def show_file(self, file):
        """
        Show the image in the visual canvas of the form only if it is empty

        :param file:
        """
        load = Image.open(file.filename)
        #load = load.resize((160,160), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(load)
        if self.image is not None:  # if an image was already loaded
            self.canvas.delete(self.image)  # remove the previous image
        self.image = self.canvas.create_image((160, 160), image=self.render)

    def validate_fields(self):
        """
        Validates empty fields and not fullfilled fields in sections when these are mandatory. I also stores
        the name of the pattern to the local pattern object.
        :return: boolean
        """
        if len(self.txt_name.get('1.0','end-1c')) != 0:
            self.pattern.name = self.txt_name.get('1.0','end-1c')
            for item in self.pattern.text_content:
                if item is None or item == '':
                    if self.pattern.text_sections[self.pattern.text_content.index(item)].split('¥')[-1] == '✓':
                        return False
            for item in self.pattern.file_content:
                if item is None or item == '':
                    if self.pattern.file_sections[self.pattern.file_content.index(item)].split('¥')[-1] == '✓':
                        return False
            return True
        else:
            return False
