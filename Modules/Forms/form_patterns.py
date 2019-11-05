from tkinter import Label, LabelFrame, Frame, Text, Button, filedialog, Canvas, messagebox, PhotoImage
from tkinter.constants import *
from tkinter.ttk import Treeview, Notebook, Combobox, Style, Separator
from Modules.Config.Data import CreateToolTip, Message, Template, Pattern, Category, File, wrap_text, Section
from PIL import Image, ImageTk
import os
import shutil

TITLE_FONT = ("Arial", 18)
SUBTITLE_FONT = ("Arial", 14)
LABEL_FONT = ("Arial", 10)
TEXT_FONT = ("Arial", 10)

TEXT_COLOR = "#1B5070"


class FormParentPattern:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildPattern(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Patterns')
        lbl_experimenter_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
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
        self.templates = []
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
        self.open_icon = PhotoImage(file=r"./Resources/open.png")
        self.style = Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", foreground="gray", rowheight=50)
        #self.style.layout('TNotebook.Tab', [])  # turn off tabs
        defaultbg = self.frm_child_crud.cget('bg')

        # Components for List FRM
        self.trv_available = Treeview(self.frm_child_list, height=7, columns='Pattern')
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Pattern', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=300, minwidth=300, stretch=NO)
        self.trv_available.bind("<ButtonRelease-1>", self.select_pattern_summary)
        self.trv_available.grid(row=1, column=0, columnspan=10, rowspan=9, sticky=W, padx=50, pady=25)
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=10, padx=10, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New pattern')
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=1, column=0, pady=10, padx=10, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit pattern')
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=2, column=0, pady=10, padx=10, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete pattern')
        frm_aux4.grid(row=1, column=10, pady=35, padx=20, rowspan=3, sticky=NW)
        sep_pattern = Separator(self.frm_child_list, orient=VERTICAL)
        sep_pattern.grid(row=0, column=11, sticky=NS, rowspan=21, padx=5)
        lbl_details = Label(self.frm_child_list, text='Details')
        lbl_details.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_details.grid(row=1, column=12, sticky=W, padx=50, pady=25)
        self.trv_list_summary = Treeview(self.frm_child_list, height=5, columns=('Section', 'Content'),
                                         selectmode='none')
        self.trv_list_summary.heading('#0', text='ID', anchor=CENTER)
        self.trv_list_summary.heading('#1', text='Section', anchor=CENTER)
        self.trv_list_summary.heading('#2', text='Content', anchor=CENTER)
        self.trv_list_summary.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_list_summary.column('#1', width=100, minwidth=100, stretch=NO)
        self.trv_list_summary.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_list_summary.grid(row=2, column=12, columnspan=5, rowspan=20, sticky=NW, padx=50, pady=25)

        # Components for CRUD FRM
        frm_aux1 = Frame(self.frm_child_crud)

        lbl_template = Label(frm_aux1, text='Select a template')
        lbl_template.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_template.grid(pady=10, padx=10, sticky=W)

        self.cbx_template = Combobox(frm_aux1, state="readonly", width=125)
        self.cbx_template.config(font=TEXT_FONT)
        self.cbx_template.grid(row=0, column=1, columnspan=3, pady=10, padx=10, sticky=W)
        self.cbx_template.bind("<<ComboboxSelected>>", self.cbx_template_selected)
        btn_save = Button(frm_aux1, image=self.save_icon, command=self.click_save)
        btn_save.grid(row=0, column=4, padx=30)
        btn_save_ttp = CreateToolTip(btn_save, 'Save pattern')
        btn_cancel = Button(frm_aux1, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel.grid(row=1, column=4, padx=30)
        btn_cancel_ttp = CreateToolTip(btn_cancel, 'Cancel')

        self.frm_aux2 = Frame(self.frm_child_crud)

        lbl_section = Label(self.frm_aux2, text='Select a section')
        lbl_section.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_section.grid(pady=10, padx=10, sticky=NW)

        self.trv_summary = Treeview(self.frm_aux2, height=6, columns=('Section', 'Mandatory', 'Completed'))
        self.trv_summary.heading('#0', text='ID', anchor=CENTER)
        self.trv_summary.heading('#1', text='Section', anchor=CENTER)
        self.trv_summary.heading('#2', text='Mandatory', anchor=CENTER)
        self.trv_summary.heading('#3', text='Completed', anchor=CENTER)
        self.trv_summary.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_summary.column('#1', width=80, minwidth=80, stretch=NO)
        self.trv_summary.column('#2', width=80, minwidth=80, stretch=NO, anchor=CENTER)
        self.trv_summary.column('#3', width=80, minwidth=80, stretch=NO, anchor=CENTER)
        self.trv_summary.bind("<ButtonRelease-1>", self.trv_section_selected)
        self.trv_summary.grid(row=0, column=1, rowspan=3, sticky=W, padx=10)

        lbl_desc_section = Label(self.frm_aux2, text='Description')
        lbl_desc_section.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_desc_section.grid(row=0, column=2, pady=10, padx=50, sticky=NE)

        self.txt_desc_section = Text(self.frm_aux2, height=4, width=65)
        self.txt_desc_section.config(background=defaultbg, font=TEXT_FONT)
        self.txt_desc_section.grid(row=0, column=3, pady=10, padx=20, sticky=W)

        lbl_section = Label(self.frm_aux2, text='Content')
        lbl_section.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_section.grid(row=1, column=2, pady=10, padx=50, sticky=NE)

        self.tab_control = Notebook(self.frm_aux2)
        tab_desc = Frame(self.tab_control)
        self.tab_control.add(tab_desc)
        self.txt_section = Text(tab_desc, height=9, width=60)
        self.txt_section.config(font=TEXT_FONT)
        self.txt_section.bind("<Key>", self.txt_section_modified)
        self.txt_section.grid(row=0, column=0, padx=20, pady=20, sticky=W)

        tab_file = Frame(self.tab_control)
        self.tab_control.add(tab_file)
        lbl_upload = Label(tab_file, text='Load a file for this section: ')
        lbl_upload.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_upload.grid(row=0, column=0, padx=20, pady=20, sticky=W)
        btn_open = Button(tab_file, image=self.open_icon, command=self.click_upload)
        btn_open.grid(row=1, column=0, padx=20, pady=5, sticky=W)
        btn_open_ttp = CreateToolTip(btn_open, 'Open file')
        btn_quit = Button(tab_file, image=self.remove_icon, command=self.click_remove)
        btn_quit.grid(row=2, column=0, padx=20, pady=5, sticky=W)
        btn_quit_ttp = CreateToolTip(btn_quit, 'Remove file')
        self.canvas = Canvas(tab_file, width=160, height=160)
        self.canvas.config(background='white', borderwidth=1)
        self.canvas.grid(row=0, column=1, padx=20, pady=10, rowspan=5, sticky=E)

        tab_classification = Frame(self.tab_control)
        self.tab_control.add(tab_classification)
        lbl_category = Label(tab_classification, text='Select a category for this section: ')
        lbl_category.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_category.grid(row=0, column=0, padx=20, pady=20, sticky=W)
        self.cbx_category = Combobox(tab_classification, state="readonly", width=30)
        self.cbx_category.config(font=TEXT_FONT)
        self.cbx_category.grid(row=1, column=0, pady=20, padx=20, sticky=W)
        self.cbx_category.bind("<<ComboboxSelected>>", self.cbx_category_selected)

        self.tab_control.grid(row=1, column=3, padx=20, pady=10, sticky=W)
        self.tab_control.tab(0, state='disabled')
        self.tab_control.tab(1, state='disabled')
        self.tab_control.tab(2, state='disabled')
        frm_aux1.grid(row=1, column=0, pady=20, padx=10, columnspan=4, rowspan=3, sticky=E)
        self.frm_aux2.grid(row=5, column=0, pady=10, padx=10, columnspan=3, rowspan=10, sticky=E)

    def initialize_variables(self):
        """
        Method that set the local variables to its initial state (empty)
        """
        self.directive = Message()
        self.new_pattern = None
        self.file = None
        self.selected_section = None

    def get_patterns(self):
        """
        Method that retrieve available patterns, contents and categories, so they can be showed in the initial list and
        in the summary box, and also can be managed
        """
        self.initialize_variables()
        # Retrieve list of templates from DB
        self.templates = []
        self.directive = Message(action=37)
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information:
            elements = item.split('¥')
            template_aux = Template(int(elements[0]), elements[1], elements[2])
            self.templates.append(template_aux)

        # Retrieve list of patterns from DB
        self.patterns = Pattern.get_available_patterns(self.connection)

    def retrieve_list(self):
        """
        Method that retrieve available patterns from the server and displays them in the TreeView from
        the List Form
        """
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        # Adding elements in the list
        for item in self.patterns:
            content = item.get_content_name()
            self.trv_available.insert('', 'end', text=item.id, values=(content,))
        # Remove existing elements in the list
        for item in self.trv_list_summary.get_children():
            self.trv_list_summary.delete(item)

    def show_frm(self):
        """
        Show the List form when the Patterns administration is called
        """
        self.get_patterns()
        self.retrieve_list()
        self.trv_available.selection_set(self.trv_available.get_children()[0])
        self.select_pattern_summary(None)
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        """
        Hide the Patterns administration Forms
        """
        # self.click_cancel()
        self.frm_child_list.grid_forget()
        # self.frm_child_crud.grid_forget()

    def select_pattern_summary(self, event):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            id_selected = int(self.trv_available.item(self.trv_available.selection())[
                                  'text'])  # Retrieve id of selected item from TreeView
            for item in self.patterns:
                if id_selected == item.id:
                    current_pattern = item
                    break
            # Remove existing elements in the list
            for item in self.trv_list_summary.get_children():
                self.trv_list_summary.delete(item)
            # Adding elements in the list
            for item in current_pattern.sections:
                self.trv_list_summary.insert('', 'end', text='', values=(item.name, wrap_text(item.content, 72)))

    def restart_components(self):
        self.txt_desc_section['state'] = NORMAL
        self.txt_desc_section.delete('1.0', 'end-1c')
        self.txt_section.delete('1.0', 'end-1c')
        for item in self.trv_summary.get_children():
            self.trv_summary.delete(item)
        if self.file is not None:  # if an image was already loaded
            self.canvas.delete(self.file.image)
            self.file = None
        self.cbx_category['values'] = []
        self.new_pattern = None
        self.selected_section = None
        self.tab_control.tab(0, state='disabled')
        self.tab_control.tab(1, state='disabled')
        self.tab_control.tab(2, state='disabled')

    def click_delete(self):
        """
        Method that removes a selected pattern from the initial list (changes are updated in DB)
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            decision = messagebox.askyesno(title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
                self.directive = Message(action=44, information=[id_selected])
                self.connection = self.directive.send_directive(self.connection)
                self.go_back_form()
        else:
            messagebox.showwarning(title='No selection', message='You must select an item')

    def click_new(self):
        """
        Initialize CRUD Form for creating a new pattern. It uploads available templates to the combobox
        """
        self.initialize_variables()
        self.decide = True
        for child in self.frm_aux2.winfo_children():
            try:
                child.configure(state=DISABLED)
            except:
                pass
        self.cbx_template['values'] = []
        for item in self.templates:
            self.cbx_template['values'] += ('{}: {}'.format(item.name, item.description),)
        self.frm_child_list.grid_forget()
        self.frm_child_crud['text'] = 'New Pattern'
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.initialize_variables()
            id_selected_pattern = int(self.trv_available.item(self.trv_available.selection())[
                                          'text'])  # Retrieve id of selected item from TreeView
            self.decide = False
            self.frm_child_list.grid_forget()
            # Retrieve pattern from the list of available patterns
            for item in self.patterns:
                if item.id == id_selected_pattern:
                    self.new_pattern = item
                    break
            # Retrieve content if neccesary
            for index, item in enumerate(self.new_pattern.sections):
                if item.diagram_id != 0:
                    self.directive = Message(action=65,
                                             information=[item.diagram_id])  # Ask for the diagram of this section
                    self.connection = self.directive.send_directive(self.connection)
                    file_aux = File()
                    file_aux.write_file(self.connection.message.information[0], self.connection.message.information[1])
                    self.new_pattern.sections[index].file = file_aux
                elif item.category_id != 0:
                    self.directive = Message(action=75,
                                             information=[item.category_id])  # Ask for the category of this section
                    self.connection = self.directive.send_directive(self.connection)
                    category_aux = Category(item.category_id, self.connection.message.information[0],
                                            self.connection.message.information[1])
                    self.new_pattern.sections[index].category = category_aux

            # Fill visual components with pattern info
            self.cbx_template.set(
                '{}: {}'.format(self.new_pattern.template.name, self.new_pattern.template.description))
            self.cbx_template['state'] = DISABLED
            self.set_trv_summary(self.new_pattern.sections)
            self.frm_child_crud['text'] = 'Update Pattern'
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(title='No selection', message='You must select an item')

    def click_save(self):
        if self.new_pattern is not None and self.selected_section is not None:
            self.save_section_local('save')
            if self.validate_fields():
                decision = messagebox.askyesno(title='Confirmation',
                                               message='Are you sure you want to save the changes?')
                if decision:
                    if self.decide:
                        self.directive = Message(action=41, information=[self.new_pattern.template.id])
                        self.connection = self.directive.send_directive(self.connection)
                        id_pattern = self.connection.message.information[0]
                        for item in self.new_pattern.sections:
                            if item.data_type == 'Text':
                                self.directive = Message(action=46,
                                                         information=[item.content, id_pattern, item.temp_section_id,
                                                                      None, None])
                                self.connection = self.directive.send_directive(self.connection)
                            elif item.data_type == 'File':
                                if item.file is not None:
                                    self.directive = Message(action=61,
                                                             information=[item.file.file_bytes, item.file.name])
                                    self.connection = self.directive.send_directive(self.connection)
                                    id_diagram = self.connection.message.information[0]
                                    content_aux = '<File>'
                                else:
                                    id_diagram = None
                                    content_aux = ''
                                self.directive = Message(action=46,
                                                         information=[content_aux, id_pattern, item.temp_section_id,
                                                                      id_diagram, None])
                                self.connection = self.directive.send_directive(self.connection)
                            elif item.data_type == 'Classification':
                                if item.category is not None:
                                    self.directive = Message(action=46, information=['<' + item.category.name + '>',
                                                                                     id_pattern, item.temp_section_id,
                                                                                     None,
                                                                                     item.category.id])
                                else:
                                    self.directive = Message(action=46,
                                                             information=['', id_pattern, item.temp_section_id, None,
                                                                          None])
                                self.connection = self.directive.send_directive(self.connection)
                            else:
                                raise Exception('Error retrieving data type of section to be created')
                    else:
                        for item in self.new_pattern.sections:
                            if item.data_type == 'Text':
                                self.directive = Message(action=48,
                                                         information=[item.pattern_section_id, item.content, None,
                                                                      None])
                                self.connection = self.directive.send_directive(self.connection)
                            elif item.data_type == 'File':
                                # Remove existing file in DB
                                if item.diagram_id != 0:
                                    self.directive = Message(action=64,
                                                             information=[item.diagram_id, 'just remove path'])
                                    self.connection = self.directive.send_directive(self.connection)
                                if item.file is not None:
                                    self.directive = Message(action=61,
                                                             information=[item.file.file_bytes, item.file.name])
                                    self.connection = self.directive.send_directive(self.connection)
                                    id_diagram = self.connection.message.information[0]
                                    content_aux = '<File>'
                                else:
                                    id_diagram = None
                                    content_aux = ''
                                self.directive = Message(action=48,
                                                         information=[item.pattern_section_id, content_aux, id_diagram,
                                                                      None])
                                self.connection = self.directive.send_directive(self.connection)
                            elif item.data_type == 'Classification':
                                if item.category is not None:
                                    self.directive = Message(action=48, information=[item.pattern_section_id,
                                                                                     '<' + item.category.name + '>',
                                                                                     None, item.category.id])
                                else:
                                    self.directive = Message(action=48, information=[item.pattern_section_id, '', None,
                                                                                     None])
                                self.connection = self.directive.send_directive(self.connection)
                            else:
                                raise Exception('Error retrieving data type of section to be created')
                    self.go_back_form()
            else:
                messagebox.showwarning(title='Missing information',
                                       message='There are mandatory fields that need to be filled!')

    def click_cancel(self):
        decision = messagebox.askyesno(title='Cancel', message='Are you sure you want to cancel?')
        if decision:
            self.go_back_form()

    def go_back_form(self):
        shutil.rmtree('./Resources/temp/')
        os.mkdir('./Resources/temp/')
        self.cbx_template['state'] = ACTIVE
        self.cbx_template.set('')
        self.cbx_template['values'] = []
        self.restart_components()
        self.initialize_variables()
        self.frm_child_crud.grid_forget()
        self.trv_available.focus_set()
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
            # Section to change the information of the summary treeview when the section is filled
            id_section = self.selected_section.temp_section_id
            for item in self.trv_summary.get_children():
                if int(self.trv_summary.item(item)['text']) == id_section:
                    values = self.trv_summary.item(item)['values']
                    self.trv_summary.item(item, values=(values[0], values[1], '✓'))
                    break

    def click_remove(self):
        """
        Remove an uploaded file from the system validating it is already uploaded. This method also delete
        any image in the canvas that may be fulfilled with an image.
        """
        if self.file is not None:  # if an image was already loaded
            self.canvas.delete(self.file.image)
            self.file = None
        # Section to change the information of the summary treeview when the section is filled
        id_section = self.selected_section.temp_section_id
        for item in self.trv_summary.get_children():
            if self.trv_summary.item(item)['text'] == id_section:
                values = self.trv_summary.item(item)['values']
                self.trv_summary.item(item, values=(values[0], values[1], ''))
                break

    def cbx_template_selected(self, event):
        for child in self.frm_aux2.winfo_children():
            try:
                child.configure(state=NORMAL)
            except:
                pass
        self.tab_control.tab(0, state='disabled')
        self.tab_control.tab(1, state='disabled')
        self.tab_control.tab(2, state='disabled')
        self.restart_components()
        self.new_pattern = Pattern()
        self.new_pattern.template = self.templates[
            int(self.cbx_template.current())]  # The selected template is associated with the local pattern object
        self.directive = Message(action=40, information=[self.new_pattern.template.id])
        self.connection = self.directive.send_directive(self.connection)
        # Create sections associated with the selected template for the new pattern object
        for item in self.connection.message.information[2]:
            elements = item.split('¥')
            section_aux = Section(temp_section_id=int(elements[0]), template_id=int(elements[1]),
                                  section_id=int(elements[2]),
                                  name=elements[3], description=elements[4], data_type=elements[5],
                                  position=int(elements[6]), mandatory=elements[7], classification_id=elements[8])
            self.new_pattern.sections.append(section_aux)
        self.set_trv_summary(self.new_pattern.sections)

    def set_trv_summary(self, sections):
        """
        Set trv_summary visual component according to sections

        :param sections:
            Sections associated with the template of the new pattern handled object
        """
        for item in self.trv_summary.get_children():
            self.trv_summary.delete(item)
        for item in sections:
            if item.content == '':
                self.trv_summary.insert('', 'end', text=item.temp_section_id, values=(item.name, item.mandatory, ''))
            else:
                self.trv_summary.insert('', 'end', text=item.temp_section_id, values=(item.name, item.mandatory, '✓'))
        self.txt_desc_section['state'] = DISABLED

    def trv_section_selected(self, event):
        """
        Stores current information inserted by the user in visual components into the local pattern object.
        Displays content associated with the selected section (trv_summary) if it is not empty.
        :param event:
        """
        if self.trv_summary.item(self.trv_summary.selection())['text'] != '':
            # This call_back function saves the current info inserted by the user into the local pattern object. Before
            # it is deleted and replaced by info from the selected section.
            self.save_section_local('not_save_yet')

            # This block locates the selected section (trv_summary) in the local pattern object, so it can be handled by
            # other functions
            id_selected_section = int(self.trv_summary.item(self.trv_summary.selection())['text'])
            for item in self.new_pattern.sections:
                if item.temp_section_id == id_selected_section:
                    self.selected_section = item
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
        if self.selected_section is not None:  # Necessary to avoid trouble when the treeview is selected for the first time
            for index, item in enumerate(self.new_pattern.sections):
                if item.temp_section_id == self.selected_section.temp_section_id:
                    break
            if self.selected_section.data_type == 'Text':
                self.new_pattern.sections[index].content = self.txt_section.get('1.0', 'end-1c')
                if text_decision != 'save':
                    self.txt_section.delete('1.0', 'end-1c')
            elif self.selected_section.data_type == 'File':
                self.new_pattern.sections[index].file = self.file
                if text_decision != 'save':
                    if self.file is not None:
                        self.canvas.delete(self.file.image)
                        self.file = None
            elif self.selected_section.data_type == 'Classification':
                if self.cbx_category.get() != '':
                    self.new_pattern.sections[index].category = self.categories[self.cbx_category.current()]
                    if text_decision != 'save':
                        self.cbx_category.set('')

    def display_section_local(self):
        """
        Displays the information of the new selected_section and its content (if it is not empty) into the visual
        components of the form.
        """
        # This block retrieve the description of the selection section, so it can be showed as a guide for the
        # user of the GUI.
        self.txt_desc_section['state'] = NORMAL
        self.txt_desc_section.delete('1.0', 'end-1c')
        self.txt_desc_section.insert('1.0', self.selected_section.description)
        self.txt_desc_section['state'] = DISABLED

        # This section retrieve the content of the selected section and displays (depending of the data_type) it
        # into the visual components if it is not empty.
        if self.selected_section.data_type == 'Text':
            self.tab_control.tab(0, state='normal')
            self.tab_control.select(0)
            if self.selected_section.content != '':
                self.txt_section.insert('1.0', self.selected_section.content)
            self.txt_section.focus_set()
        elif self.selected_section.data_type == 'File':
            self.tab_control.tab(1, state='normal')
            self.tab_control.select(1)
            if self.selected_section.file is not None:
                self.file = self.selected_section.file
                self.show_file(self.selected_section.file)
        elif self.selected_section.data_type == 'Classification':
            self.tab_control.tab(2, state='normal')
            self.tab_control.select(2)
            self.directive = Message(action=72, information=[self.selected_section.classification_id])
            self.connection = self.directive.send_directive(self.connection)
            self.set_cbx_categories(self.connection.message.information)
            if self.selected_section.category is not None:
                self.cbx_category.set(self.selected_section.category.name)

    def txt_section_modified(self, event):
        id_section = self.selected_section.temp_section_id
        for item in self.trv_summary.get_children():
            if int(self.trv_summary.item(item)['text']) == id_section:
                values = self.trv_summary.item(item)['values']
                if self.txt_section.get('1.0', 'end-1c') != '':
                    self.trv_summary.item(item, values=(values[0], values[1], '✓'))
                else:
                    self.trv_summary.item(item, values=(values[0], values[1], ''))
                break

    def set_cbx_categories(self, categories):
        self.categories = []
        for item in categories:
            elements = item.split('¥')
            category_aux = Category(int(elements[0]), elements[1], int(elements[2]))
            self.categories.append(category_aux)
        self.cbx_category['values'] = []
        for item in self.categories:
            self.cbx_category['values'] += ('{}'.format(item.name),)

    def cbx_category_selected(self, event):
        id_section = self.selected_section.temp_section_id
        for item in self.trv_summary.get_children():
            if int(self.trv_summary.item(item)['text']) == id_section:
                values = self.trv_summary.item(item)['values']
                self.trv_summary.item(item, values=(values[0], values[1], '✓'))
                break

    def show_file(self, file):
        """
        Show the image in the visual canvas of the form only if it is empty

        :param file:
        """
        load = Image.open(file.filename)
        load = load.resize((160, 160), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(load)
        if self.file.image is not None:  # if an image was already loaded
            self.canvas.delete(self.file.image)  # remove the previous image
        self.file.image = self.canvas.create_image(0, 0, anchor='nw', image=self.render)

    def validate_fields(self):
        """
        Validates empty fields and not fullfilled fields in sections from the handled pattern object when
        these are mandatory.
        :return: boolean
        """
        for item in self.new_pattern.sections:
            if item.mandatory == '✓':
                if item.data_type == 'Text':
                    if item.content == '' or item.content is None:
                        return False
                elif item.data_type == 'File':
                    if item.file is None:
                        return False
                elif item.data_type == 'Classification':
                    if item.category is None:
                        return False
        return True
