from tkinter import Label, LabelFrame, Frame, Text, Button, filedialog, Canvas, messagebox, PhotoImage, Scrollbar, \
    Toplevel
from tkinter.constants import *
from tkinter.ttk import Treeview, Combobox, Separator
from Modules.Config.Data import CreateToolTip, Message, Template, Pattern, Category, File, summarize_text, Section
from PIL import Image, ImageTk
from Modules.Config.Visual import *
import os




class FormParentPattern:
    def __init__(self, window, connection):
        self.frm_parent = Frame(window)
        self.initialize_components()
        self.frm_child = FormChildPattern(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Patterns')
        lbl_experimenter_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_experimenter_title.grid(row=0, column=0, pady=20)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0)
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
        self.tlevel_diagram_summary = Toplevel(frm_parent)
        self.tlevel_diagram_summary.title('Diagram')
        self.tlevel_diagram_summary.protocol("WM_DELETE_WINDOW", self.close_tlevel_diagram)
        self.tlevel_diagram_summary.withdraw()
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
        self.open_icon = PhotoImage(file=r"./Resources/open.png")

        # Components for List FRM
        lbl_sep1 = Label(self.frm_child_list)
        lbl_sep1.grid(row=0, column=0, padx=10, pady=25)
        self.trv_available = Treeview(self.frm_child_list, height=20, columns=('N', 'M. section 1', 'M. section 2',
                                                                               'M. section 3'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='N', anchor=CENTER)
        self.trv_available.heading('#2', text='M. section 1', anchor=CENTER)
        self.trv_available.heading('#3', text='M. section 2', anchor=CENTER)
        self.trv_available.heading('#4', text='M. section 3', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available.column('#2', width=125, minwidth=125, stretch=NO)
        self.trv_available.column('#3', width=125, minwidth=125, stretch=NO)
        self.trv_available.column('#4', width=125, minwidth=125, stretch=NO)
        self.trv_available.bind("<ButtonRelease-1>", self.select_pattern_summary)
        self.trv_available.grid(row=0, column=1, sticky=W, pady=25)
        vsb_trv_av = Scrollbar(self.frm_child_list, orient="vertical", command=self.trv_available.yview)
        vsb_trv_av.grid(row=0, column=2, pady=25, sticky=NS)
        self.trv_available.configure(yscrollcommand=vsb_trv_av.set)
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New pattern')
        btn_view_exp = Button(frm_aux4, image=self.view_icon, command=self.click_view)
        btn_view_exp.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_view_exp_ttp = CreateToolTip(btn_view_exp, 'View pattern')
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit pattern')
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=3, column=0, pady=5, padx=5, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete pattern')
        frm_aux4.grid(row=0, column=3, pady=25, padx=25, sticky=NW)
        sep_pattern = Separator(self.frm_child_list, orient=VERTICAL)
        sep_pattern.grid(row=0, column=4, sticky=NS, padx=25)
        frm_aux3 = Frame(self.frm_child_list)
        lbl_sep3 = Label(frm_aux3)
        lbl_sep3.grid(row=0, column=0, padx=10, pady=25, rowspan=3)
        lbl_details = Label(frm_aux3, text='Details')
        lbl_details.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_details.grid(row=0, column=1, sticky=W, pady=25)
        self.btn_view_diagram = Button(frm_aux3, text='View >>\ndiagram', command=self.click_expand_diagram)
        self.txt_summary = Text(frm_aux3, height=22, width=50)
        self.txt_summary.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_summary.grid(row=1, column=1, columnspan=2)
        vsb_txt_sum = Scrollbar(frm_aux3, orient="vertical", command=self.txt_summary.yview)
        vsb_txt_sum.grid(row=1, column=3, sticky=NS)
        self.txt_summary.configure(yscrollcommand=vsb_txt_sum.set)
        lbl_sep4 = Label(frm_aux3)
        lbl_sep4.grid(row=0, column=4, padx=10, pady=25, rowspan=3)
        lbl_sep5 = Label(frm_aux3)
        lbl_sep5.grid(row=2, column=1, pady=5, columnspan=3)
        frm_aux3.grid(row=0, column=5)

        # Components for expanded diagram
        self.canvas_summary = Canvas(self.tlevel_diagram_summary, width=500, height=500)
        self.canvas_summary.config(background='white', borderwidth=1)
        self.canvas_summary.grid()

        # Components for CRUD FRM
        frm_aux1 = Frame(self.frm_child_crud)
        lbl_template = Label(frm_aux1, text='1)Select a template')
        lbl_template.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_template.grid(pady=10, padx=20, sticky=W)
        self.cbx_template = Combobox(frm_aux1, state="readonly", width=60)
        self.cbx_template.config(font=TEXT_FONT)
        self.cbx_template.grid(row=0, column=1, columnspan=3, pady=10, padx=10, sticky=W)
        self.cbx_template.bind("<<ComboboxSelected>>", self.cbx_template_selected)
        frm_aux1.grid(row=0, column=0, sticky=W)
        sep_aux2 = Separator(self.frm_child_crud, orient=VERTICAL)
        sep_aux2.grid(row=0, column=1, sticky=NS, rowspan=3)
        self.frm_aux2 = Frame(self.frm_child_crud)  # Frame that contains components for sections configuration
        sep_aux1 = Separator(self.frm_aux2, orient=HORIZONTAL)
        sep_aux1.grid(row=0, column=0, sticky=EW, columnspan=7)
        lbl_section = Label(self.frm_aux2, text='2)Select a section')
        lbl_section.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_section.grid(row=1, column=1, pady=10, sticky=NW)
        lbl_sep5 = Label(self.frm_aux2)
        lbl_sep5.grid(row=2, column=0, padx=10, pady=10)
        self.trv_summary = Treeview(self.frm_aux2, height=15, columns=('N', 'Section', 'Mandatory', 'Completed'))
        self.trv_summary.heading('#0', text='ID', anchor=CENTER)
        self.trv_summary.heading('#1', text='N', anchor=CENTER)
        self.trv_summary.heading('#2', text='Section', anchor=CENTER)
        self.trv_summary.heading('#3', text='Mandatory', anchor=CENTER)
        self.trv_summary.heading('#4', text='Completed', anchor=CENTER)
        self.trv_summary.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_summary.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_summary.column('#2', width=100, minwidth=100, stretch=NO)
        self.trv_summary.column('#3', width=70, minwidth=70, stretch=NO, anchor=CENTER)
        self.trv_summary.column('#4', width=70, minwidth=70, stretch=NO, anchor=CENTER)
        self.trv_summary.bind("<ButtonRelease-1>", self.trv_section_selected)
        self.trv_summary.grid(row=2, column=1, rowspan=3, sticky=W, pady=10)
        vsb_trv_sum = Scrollbar(self.frm_aux2, orient="vertical", command=self.trv_summary.yview)
        vsb_trv_sum.grid(row=2, column=2, rowspan=3, pady=10, sticky=NS)
        self.trv_summary.configure(yscrollcommand=vsb_trv_sum.set)
        lbl_sep6 = Label(self.frm_aux2)
        lbl_sep6.grid(row=2, column=3, padx=20, pady=10)
        lbl_desc_section = Label(self.frm_aux2, text='Description')
        lbl_desc_section.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_desc_section.grid(row=1, column=4, pady=10, sticky=NW)
        self.txt_desc_section = Text(self.frm_aux2, height=4, width=60)
        self.txt_desc_section.config(background=DISABLED_COLOR, font=TEXT_FONT)
        self.txt_desc_section.grid(row=2, column=4, pady=10, sticky=W)
        vsb_txt_desc = Scrollbar(self.frm_aux2, orient="vertical", command=self.txt_desc_section.yview)
        vsb_txt_desc.grid(row=2, column=5, pady=10, sticky=NS)
        self.txt_desc_section.configure(yscrollcommand=vsb_txt_desc.set)
        lbl_sep7 = Label(self.frm_aux2)
        lbl_sep7.grid(row=2, column=6, padx=20, pady=10)
        lbl_section = Label(self.frm_aux2, text='3)Content')
        lbl_section.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_section.grid(row=3, column=4, pady=10, sticky=NW)
        # Frame for section of text data type
        self.frm_text = Frame(self.frm_aux2)
        self.txt_section = Text(self.frm_text, height=9, width=60)
        self.txt_section.config(font=TEXT_FONT)
        self.txt_section.bind("<KeyRelease>", self.txt_section_modified)
        self.txt_section.grid(row=0, column=0, pady=20, sticky=W)
        vsb_txt_sec = Scrollbar(self.frm_text, orient="vertical", command=self.txt_section.yview)
        vsb_txt_sec.grid(row=0, column=1, pady=20, sticky=NS)
        self.txt_section.configure(yscrollcommand=vsb_txt_sec.set)
        # Frame for section of file data type
        self.frm_file = Frame(self.frm_aux2)
        lbl_upload = Label(self.frm_file, text='Load an image for this section: ')
        lbl_upload.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_upload.grid(row=0, column=0, pady=20, sticky=W)
        self.btn_open = Button(self.frm_file, image=self.open_icon, command=self.click_upload)
        btn_open_ttp = CreateToolTip(self.btn_open, 'Open image')
        self.btn_quit = Button(self.frm_file, image=self.remove_icon, command=self.click_remove)
        btn_quit_ttp = CreateToolTip(self.btn_quit, 'Remove image')
        self.btn_view_diagram_section = Button(self.frm_file, image=self.view_icon, command=self.click_view_diagram)
        btn_view_diagram_section_ttp = CreateToolTip(self.btn_view_diagram_section, 'View image')
        self.canvas = Canvas(self.frm_file, width=160, height=160)
        self.canvas.config(background='white', borderwidth=1)
        self.canvas.grid(row=0, column=1, padx=20, pady=10, rowspan=5, sticky=E)
        # Frame for section of classification data type
        self.frm_classification = Frame(self.frm_aux2)
        lbl_category = Label(self.frm_classification, text='Select a category for this section: ')
        lbl_category.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_category.grid(row=0, column=0, pady=20, sticky=W)
        self.cbx_category = Combobox(self.frm_classification, state="readonly", width=30)
        self.cbx_category.config(font=TEXT_FONT)
        self.cbx_category.grid(row=1, column=0, pady=20, sticky=EW)
        self.cbx_category.bind("<<ComboboxSelected>>", self.cbx_category_selected)
        lbl_sep8 = Label(self.frm_classification)
        lbl_sep8.grid(row=2, column=0, pady=22)

        frm_aux3 = Frame(self.frm_child_crud)
        self.btn_save = Button(frm_aux3, image=self.save_icon, command=self.click_save)
        btn_save_ttp = CreateToolTip(self.btn_save, 'Save pattern')
        self.btn_back = Button(frm_aux3, image=self.back_icon, command=self.go_back_form)
        btn_back_ttp = CreateToolTip(self.btn_back, 'Go back')
        self.btn_cancel = Button(frm_aux3, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel_ttp = CreateToolTip(self.btn_cancel, 'Cancel')
        frm_aux3.grid(row=0, column=2, sticky=E, pady=5)

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
        for index, item in enumerate(self.patterns):
            pattern_main_sections = item.get_main_sections()
            self.trv_available.insert('', 'end', text=item.id, values=(index+1,
                                                                       summarize_text(pattern_main_sections[0], 125),
                                                                       summarize_text(pattern_main_sections[1], 125),
                                                                       summarize_text(pattern_main_sections[2], 125)))
        if len(self.trv_available.get_children()) != 0:
            self.trv_available.selection_set(self.trv_available.get_children()[0])
            self.select_pattern_summary()

    def show_frm(self):
        """
        Show the List form when the Patterns administration is called
        """
        self.get_patterns()
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        """
        Hide the Patterns administration Forms
        """
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid_forget()
        self.go_back_form(decision='hide')

    def select_pattern_summary(self, event=None):
        if len(self.trv_available.selection()) == 1:
            self.id_selected_pattern = int(self.trv_available.item(self.trv_available.selection())['text'])  # Retrieve id of selected item from TreeView
            for item in self.patterns:
                if self.id_selected_pattern == item.id:
                    current_pattern = item
                    break
            # Clear summary txt box
            self.btn_view_diagram.grid_forget()
            self.txt_summary['state'] = NORMAL
            self.txt_summary.delete('1.0', 'end-1c')
            # Adding elements in the list
            for item in current_pattern.sections:
                if item.data_type == 'File':    # If pattern has an associated diagram
                    if item.diagram_id != 0:
                        self.btn_view_diagram.grid(row=0, column=2, padx=10, sticky=E)
                        self.txt_summary.insert('end-1c', "{}:\nClick up button to see diagram ^\n\n".
                                                format(item.name))
                        self.directive = Message(action=65, information=[item.diagram_id])  # Ask for the diagram of this section
                        self.connection = self.directive.send_directive(self.connection)
                        self.file_summary = File()
                        self.file_summary.write_file(self.connection.message.information[0],
                                                     self.connection.message.information[1])
                    else:
                        self.txt_summary.insert('end-1c',
                                                "{}:\nNo configured diagram\n\n".format(item.name))
                else:
                    self.txt_summary.insert('end-1c', "{}:\n{}\n\n".format(item.name, item.content))
            self.txt_summary['state'] = DISABLED

    def restart_components(self):
        self.txt_desc_section['state'] = NORMAL
        self.txt_desc_section.delete('1.0', 'end-1c')
        self.txt_section['state'] = NORMAL
        self.txt_section['bg'] = ENABLED_COLOR
        self.txt_section.delete('1.0', 'end-1c')
        for item in self.trv_summary.get_children():
            self.trv_summary.delete(item)
        if self.file is not None:  # if an image was already loaded
            self.canvas.delete(self.file.image)
            self.render_s_diagram = None
            self.file = None
        self.cbx_category['state'] = ACTIVE
        self.cbx_category['values'] = []
        self.cbx_category.set('')
        self.new_pattern = None
        self.selected_section = None
        self.frm_text.grid_forget()
        self.frm_file.grid_forget()
        self.frm_classification.grid_forget()

    def click_new(self):
        """
        Initialize CRUD Form for creating a new pattern. It uploads available templates to the combobox
        """
        self.initialize_variables()
        self.decide = True
        self.decide_view = False
        for child in self.frm_aux2.winfo_children():
            try:
                child.configure(state=DISABLED)
            except:
                pass
        self.cbx_template['values'] = []
        for item in self.templates:
            self.cbx_template['values'] += ('{}: {}'.format(item.name, item.description),)
        self.frm_child_list.grid_forget()
        self.btn_save.grid(row=0, column=2, padx=20, pady=5)
        self.btn_cancel.grid(row=1, column=2, padx=20, pady=5)
        self.btn_open.grid(row=1, column=0, padx=20, pady=5, sticky=E)
        self.btn_quit.grid(row=2, column=0, padx=20, pady=5, sticky=E)
        self.frm_child_crud['text'] = 'New Pattern'
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_view(self):
        if len(self.trv_available.selection()) == 1:
            # Just to check if the pattern is not associated to other components
            self.directive = Message(action=45, information=[self.id_selected_pattern])
            self.connection = self.directive.send_directive(self.connection)
            self.initialize_variables()
            self.decide_view = True
            # Retrieve pattern from the list of available patterns
            for item in self.patterns:
                if item.id == self.id_selected_pattern:
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
            self.txt_section['bg'] = DISABLED_COLOR
            self.frm_child_crud['text'] = 'View Pattern'
            self.btn_back.grid(row=0, column=2, padx=20, pady=5)
            self.btn_view_diagram_section.grid(row=1, column=0, padx=20, pady=5, sticky=E)
            self.frm_aux2.grid(row=2, column=0, sticky=E)
            self.frm_child_list.grid_forget()
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_update(self):
        if len(self.trv_available.selection()) == 1:
            # Just to check if the pattern is not associated to other components
            self.directive = Message(action=45, information=[self.id_selected_pattern, 'validate'])
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.action == 5:  # An error ocurred while trying to update the item
                messagebox.showerror(parent=self.frm_child_list, title='Can not update the item',
                                     message=self.connection.message.information[0])
            else:
                self.initialize_variables()
                self.decide = False
                self.decide_view = False
                # Retrieve pattern from the list of available patterns
                for item in self.patterns:
                    if item.id == self.id_selected_pattern:
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
                self.frm_aux2.grid(row=2, column=0, sticky=E)
                self.btn_save.grid(row=0, column=2, padx=20, pady=5)
                self.btn_cancel.grid(row=1, column=2, padx=20, pady=5)
                self.btn_open.grid(row=1, column=0, padx=20, pady=5, sticky=E)
                self.btn_quit.grid(row=2, column=0, padx=20, pady=5, sticky=E)
                self.frm_child_list.grid_forget()
                self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_delete(self):
        """
        Method that removes a selected pattern from the initial list (changes are updated in DB)
        """
        if len(self.trv_available.selection()) == 1:
            decision = messagebox.askyesno(parent=self.frm_child_list, title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                self.directive = Message(action=44, information=[self.id_selected_pattern])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:  # An error ocurred while deleting the item
                    messagebox.showerror(parent=self.frm_child_list, title='Can not delete the item',
                                         message=self.connection.message.information[0])
                else:
                    self.go_back_form()
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_save(self):
        if self.new_pattern is not None and self.selected_section is not None:
            self.save_section_local('save')
            if self.validate_fields():
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
                                                         information=[item.file.file_bytes, item.file.name, 'pattern'])
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
                                                         information=[item.file.file_bytes, item.file.name, 'pattern'])
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
                messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                       message='There are mandatory sections that need to be filled!')

    def click_cancel(self):
        decision = messagebox.askyesno(parent=self.frm_child_crud, title='Cancel',
                                       message='Are you sure you want to cancel?')
        if decision:
            self.go_back_form()

    def go_back_form(self, decision='back'):
        self.btn_back.grid_forget()
        self.btn_cancel.grid_forget()
        self.btn_save.grid_forget()
        self.btn_open.grid_forget()
        self.btn_quit.grid_forget()
        self.btn_view_diagram_section.grid_forget()
        self.frm_aux2.grid_forget()
        self.cbx_template['state'] = ACTIVE
        self.cbx_template.set('')
        self.cbx_template['values'] = []
        self.restart_components()
        self.initialize_variables()
        self.frm_child_crud.grid_forget()
        self.trv_available.focus_set()
        if decision != 'hide':
            self.show_frm()

    def click_upload(self):
        """
        Create a File object that is uploaded by the user, validating that there is not a file uploaded already.
        """
        if self.file is None:
            filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select image file",
                                                  filetypes=[("Diagrams", ".jpg .png .tiff")])
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
                    self.trv_summary.item(item, values=(values[0], values[1], values[2], '✓'))
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
                self.trv_summary.item(item, values=(values[0], values[1], values[2], ''))
                break

    def cbx_template_selected(self, event):
        for child in self.frm_aux2.winfo_children():
            try:
                child.configure(state=NORMAL)
            except:
                pass
        self.frm_text.grid_forget()
        self.frm_file.grid_forget()
        self.frm_classification.grid_forget()
        if self.decide:
            self.frm_aux2.grid_forget()
            self.frm_aux2.grid(row=2, column=0, sticky=E)
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
                                  section_id=int(elements[2]), name=elements[3], description=elements[4],
                                  data_type=elements[5], position=int(elements[6]), mandatory=elements[7],
                                  main=elements[8], classification_id=elements[9])
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
        for index, item in enumerate(sections):
            if item.content == '':
                self.trv_summary.insert('', 'end', text=item.temp_section_id, values=(index+1,
                                                                                      summarize_text(item.name, 100),
                                                                                      item.mandatory, ''))
            else:
                self.trv_summary.insert('', 'end', text=item.temp_section_id, values=(index+1,
                                                                                      summarize_text(item.name, 100),
                                                                                      item.mandatory, '✓'))
        self.txt_desc_section['state'] = DISABLED
        self.trv_summary.selection_set(self.trv_summary.get_children()[0])
        self.trv_section_selected()

    def trv_section_selected(self, event=None):
        """
        Stores current information inserted by the user in visual components into the local pattern object.
        Displays content associated with the selected section (trv_summary) if it is not empty.
        :param event:
        """
        if len(self.trv_summary.selection()) == 1:
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
                if self.decide_view:  # With viewing option have to enable text box
                    self.txt_section['state'] = NORMAL
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
                if self.decide_view:  # With viewing option have to enable text box
                    self.cbx_category['state'] = ACTIVE
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
        self.frm_text.grid_forget()
        self.frm_file.grid_forget()
        self.frm_classification.grid_forget()
        if self.selected_section.data_type == 'Text':
            self.frm_text.grid(row=4, column=4, pady=10, columnspan=2, sticky=W)
            self.txt_section.focus_set()
            if self.selected_section.content != '':
                self.txt_section.insert('1.0', self.selected_section.content)
            if self.decide_view:    # With viewing option have to disable text box
                self.txt_section['state'] = DISABLED
            else:
                self.txt_section.focus_set()
        elif self.selected_section.data_type == 'File':
            self.frm_file.grid(row=4, column=4, pady=10, columnspan=2, sticky=W)
            if self.selected_section.file is not None:
                self.file = self.selected_section.file
                self.show_file(self.selected_section.file)
        elif self.selected_section.data_type == 'Classification':
            self.frm_classification.grid(row=4, column=4, pady=10, columnspan=2, sticky=W)
            self.directive = Message(action=72, information=[self.selected_section.classification_id])
            self.connection = self.directive.send_directive(self.connection)
            self.set_cbx_categories(self.connection.message.information)
            if self.selected_section.category is not None:
                self.cbx_category.set(self.selected_section.category.name)
            if self.decide_view:    # With viewing option have to disable text box
                self.cbx_category['state'] = DISABLED

    def txt_section_modified(self, event):
        id_section = self.selected_section.temp_section_id
        for item in self.trv_summary.get_children():
            if int(self.trv_summary.item(item)['text']) == id_section:
                values = self.trv_summary.item(item)['values']
                if self.txt_section.get('1.0', 'end-1c') != '':
                    self.trv_summary.item(item, values=(values[0], values[1], values[2], '✓'))
                else:
                    self.trv_summary.item(item, values=(values[0], values[1], values[2], ''))
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
                self.trv_summary.item(item, values=(values[0], values[1], values[2], '✓'))
                break

    def show_file(self, file):
        """
        Show the image in the visual canvas of the form only if it is empty

        :param file:
        """
        load = Image.open(file.filename)
        load = load.resize((160, 160), Image.ANTIALIAS)
        self.render_s_diagram = ImageTk.PhotoImage(load)
        if self.file.image is not None:  # if an image was already loaded
            self.canvas.delete(self.file.image)  # remove the previous image
        self.file.image = self.canvas.create_image(0, 0, anchor='nw', image=self.render_s_diagram)

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

    def click_expand_diagram(self):
        # Fill summary problem canvas with retrieved image
        load = Image.open(self.file_summary.filename)
        load = load.resize((500, 500), Image.ANTIALIAS)
        self.render_summary = ImageTk.PhotoImage(load)
        self.canvas_summary.delete()
        self.file_summary.image = self.canvas_summary.create_image(0, 0, anchor='nw', image=self.render_summary)  # and display new image
        self.tlevel_diagram_summary.deiconify()
        self.tlevel_diagram_summary.grab_set()

    def click_view_diagram(self):
        if self.file is not None:
            load = Image.open(self.file.filename)
            load = load.resize((500, 500), Image.ANTIALIAS)
            self.render_diagram = ImageTk.PhotoImage(load)
            self.canvas_summary.delete()
            self.file.image = self.canvas_summary.create_image(0, 0, anchor='nw', image=self.render_diagram)  # and display new image
            self.tlevel_diagram_summary.deiconify()
            self.tlevel_diagram_summary.grab_set()
        else:
            messagebox.showwarning(parent=self.frm_child_crud, title='No diagram',
                                   message='No diagram uploaded in this section')

    def close_tlevel_diagram(self):
        self.tlevel_diagram_summary.grab_release()
        self.tlevel_diagram_summary.withdraw()