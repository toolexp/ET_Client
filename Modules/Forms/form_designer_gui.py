from tkinter import Label, LabelFrame, Frame, Text, Button, filedialog, Canvas, messagebox, PhotoImage, Toplevel, Listbox
from tkinter.constants import *
import datetime
from tkinter.ttk import Treeview, Notebook, Combobox, Style, Separator
from Modules.Config.Data import CreateToolTip, Message, Template, Pattern, Category, File, wrap_text, Section, \
    ExperimentalSC, ScenarioComponent
from PIL import Image, ImageTk
import os
import shutil

TITLE_FONT = ("Arial", 18)
SUBTITLE_FONT = ("Arial", 14)
LABEL_FONT = ("Arial", 11)
TEXT_FONT = ("Arial", 10)

TEXT_COLOR = "#1B5070"

class FormParentDesigner:
    def __init__(self, window, connection):
        self.id_designer = 1
        self.connection = connection
        self.frm_parent = LabelFrame(window)
        self.tlevel_auth_scenario = Toplevel(window)
        self.tlevel_auth_scenario.protocol("WM_DELETE_WINDOW", self.click_authenticate_cancel)
        self.tlevel_auth_scenario.withdraw()
        self.frm_general = LabelFrame(window)
        self.tlevel_image_exp = Toplevel(window)
        self.tlevel_image_exp.title('Diagram')
        self.tlevel_image_exp.protocol("WM_DELETE_WINDOW", self.close_tlevel_image)
        self.tlevel_image_exp.withdraw()
        self.initialize_components()

    def initialize_components(self):
        # Resources for the Forms
        self.new_icon = PhotoImage(file=r"./Resources/create.png")
        self.modify_icon = PhotoImage(file=r"./Resources/modify.png")
        self.remove_icon = PhotoImage(file=r"./Resources/delete.png")
        self.save_icon = PhotoImage(file=r"./Resources/save.png")
        self.cancel_icon = PhotoImage(file=r"./Resources/cancel.png")
        self.add_icon = PhotoImage(file=r"./Resources/right.png")
        self.delete_icon = PhotoImage(file=r"./Resources/left.png")
        self.next_icon = PhotoImage(file=r"./Resources/next.png")
        self.back_icon = PhotoImage(file=r"./Resources/back.png")
        self.copy_icon = PhotoImage(file=r"./Resources/copy.png")
        self.open_icon = PhotoImage(file=r"./Resources/open.png")
        defaultbg = self.frm_parent.cget('bg')

        # Initialize visual components for displaying available experiment scenarios
        lbl_title = Label(self.frm_parent, text='Experimental scenarios')
        lbl_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_title.grid(row=0, column=0, columnspan=3, pady=50, sticky=EW)
        lbl_experimental_trv = Label(self.frm_parent, text='Select a scenario')
        lbl_experimental_trv.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_experimental_trv.grid(row=1, column=0, pady=25, padx=50, sticky=NW)
        lbl_problem_desc = Label(self.frm_parent, text='Information')
        lbl_problem_desc.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_problem_desc.grid(row=2, column=0, pady=25, padx=50, sticky=NW)
        self.trv_available = Treeview(self.frm_parent, height=4, columns=('Scenario', 'Description'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Scenario', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.bind("<ButtonRelease-1>", self.select_experimental_scenario)
        self.trv_available.grid(row=1, column=1, sticky=W, padx=20, pady=25)
        self.txt_scenario_desc = Text(self.frm_parent, height=6, width=85)
        self.txt_scenario_desc.config(font=TEXT_FONT, bg=defaultbg)
        self.txt_scenario_desc.grid(row=2, column=1, padx=20, pady=25, sticky=NW)
        btn_access = Button(self.frm_parent, image=self.next_icon, command=self.click_enter_scenario)
        btn_access.grid(row=1, column=2, padx=50, pady=25, sticky=N)
        btn_access_ttp = CreateToolTip(btn_access, 'Go')

        # Window dialog to authenticate the selected experimental scenario
        lbl_access_auth = Label(self.tlevel_auth_scenario, text='Insert access code: ')
        lbl_access_auth.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_access_auth.grid(pady=10, padx=20, sticky=W)
        self.txt_auth_scenario = Text(self.tlevel_auth_scenario, height=1, width=50)
        self.txt_auth_scenario.config(font=TEXT_FONT)
        self.txt_auth_scenario.grid(row=0, column=1, padx=20, pady=10, sticky=W)
        btn_access_auth = Button(self.tlevel_auth_scenario, image=self.next_icon, command=self.click_authenticate_scenario)
        btn_access_auth.grid(row=0, column=2, padx=20, pady=10, sticky=W)
        btn_access_auth_ttp = CreateToolTip(btn_access_auth, 'Go')
        btn_cancel_auth = Button(self.tlevel_auth_scenario, image=self.cancel_icon, command=self.click_authenticate_cancel)
        btn_cancel_auth.grid(row=1, column=2, padx=20, pady=10, sticky=W)
        btn_cancel_auth_ttp = CreateToolTip(btn_cancel_auth, 'Cancel')

        # Experiment form
        frm_aux1 = Frame(self.frm_general)
        lbl_title_exp = Label(frm_aux1, text='Design a solution')
        lbl_title_exp.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_title_exp.grid(row=0, column=0, columnspan=3, pady=5, sticky=EW)
        lbl_hints = Label(frm_aux1, text='Indications')
        lbl_hints.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_hints.grid(row=1, column=0, pady=10, padx=50, sticky=NW)
        sep_aux1 = Separator(frm_aux1, orient=HORIZONTAL)
        sep_aux1.grid(row=2, column=0, sticky=EW, columnspan=3, pady=5)
        lbl_problem = Label(frm_aux1, text='Problem')
        lbl_problem.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_problem.grid(row=3, column=0, pady=10, padx=50, sticky=NW)
        lbl_problem_info = Label(frm_aux1, text='Description')
        lbl_problem_info.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_problem_info.grid(row=4, column=0, pady=10, padx=50, sticky=NW)
        sep_aux2 = Separator(frm_aux1, orient=HORIZONTAL)
        sep_aux2.grid(row=5, column=0, sticky=EW, columnspan=3, pady=5)
        self.txt_hints = Text(frm_aux1, height=4, width=85)
        self.txt_hints.config(font=TEXT_FONT, bg=defaultbg)
        self.txt_hints.grid(row=1, column=1, padx=20, pady=10, sticky=NW)
        self.lbl_problem_title = Label(frm_aux1)
        self.lbl_problem_title.config(font=LABEL_FONT)
        self.lbl_problem_title.grid(row=3, column=1, pady=10, padx=20, sticky=NW)
        self.txt_problem_desc = Text(frm_aux1, height=6, width=85)
        self.txt_problem_desc.config(font=TEXT_FONT, bg=defaultbg)
        self.txt_problem_desc.grid(row=4, column=1, padx=20, pady=10, sticky=NW)
        self.btn_next_scenario = Button(frm_aux1, image=self.next_icon, command=self.click_next_scenario)
        self.btn_next_scenario.grid(row=1, column=2, padx=20, pady=10, sticky=W)
        btn_next_scenario_ttp = CreateToolTip(self.btn_next_scenario, 'Next problem')
        frm_aux1.grid(row=1, column=0, pady=20, padx=10, columnspan=4, rowspan=3, sticky=E)

        frm_aux2 = Frame(self.frm_general)
        lbl_solution = Label(frm_aux2, text='Solution')
        lbl_solution.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_solution.grid(row=0, column=0, padx=50, pady=10, sticky=W)
        self.tab_control = Notebook(frm_aux2)

        tab_desc = Frame(self.tab_control)
        self.tab_control.add(tab_desc, text="Description", padding=10)
        self.txt_solution_desc = Text(tab_desc, height=10, width=120)
        self.txt_solution_desc.config(font=TEXT_FONT)
        self.txt_solution_desc.grid(row=0, column=0, padx=20, pady=20, sticky=W)

        tab_file = Frame(self.tab_control)
        self.tab_control.add(tab_file, text="File", padding=10)
        lbl_upload = Label(tab_file, text='Attach a file to the solution: ')
        lbl_upload.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_upload.grid(row=0, column=0, padx=20, pady=20, sticky=W)
        btn_open = Button(tab_file, image=self.open_icon, command=self.click_attach_file)
        btn_open.grid(row=1, column=0, padx=20, pady=10, sticky=E)
        btn_open_ttp = CreateToolTip(btn_open, 'Attach file')
        btn_quit = Button(tab_file, image=self.remove_icon, command=self.click_remove_file)
        btn_quit.grid(row=2, column=0, padx=20, pady=10, sticky=E)
        btn_quit_ttp = CreateToolTip(btn_quit, 'Remove file')
        self.canvas = Canvas(tab_file, width=200, height=200)
        self.canvas.config(background='white', borderwidth=1)
        self.canvas.grid(row=0, column=1, padx=10, pady=10, rowspan=10, sticky=NS)

        tab_patterns = Frame(self.tab_control)
        self.tab_control.add(tab_patterns, text="Design patterns", padding=10)
        lbl_av_patterns = Label(tab_patterns, text='Patterns browser')
        lbl_av_patterns.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_av_patterns.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        lbl_pattern_section = Label(tab_patterns, text='Pattern sections')
        lbl_pattern_section.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_pattern_section.grid(row=0, column=1, pady=10, padx=5, sticky=W)
        lbl_content = Label(tab_patterns, text='Content')
        lbl_content.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_content.grid(row=0, column=2, pady=10, padx=10, sticky=W)
        lbl_sel_patterns = Label(tab_patterns, text='Selected patterns')
        lbl_sel_patterns.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_sel_patterns.grid(row=0, column=4, pady=10, padx=10, sticky=W)
        self.lbx_av_patterns = Listbox(tab_patterns, height=10, width=35, exportselection=0)
        self.lbx_av_patterns.grid(row=1, column=0, padx=10, pady=10, sticky=W, rowspan=5)
        self.lbx_av_patterns.bind('<<ListboxSelect>>', self.select_available_pattern)
        self.lbx_sections = Listbox(tab_patterns, height=10, width=20, exportselection=0)
        self.lbx_sections.grid(row=1, column=1, padx=10, pady=10, sticky=W, rowspan=5)
        self.lbx_sections.bind('<<ListboxSelect>>', self.select_pattern_section)
        content_frame = Frame(tab_patterns, height=10, width=30)
        self.txt_section_content = Text(content_frame, height=10, width=30)
        self.txt_section_content.config(font=TEXT_FONT)
        self.file_canvas = Canvas(content_frame, width=150, height=150)
        self.file_canvas.config(background='white', borderwidth=1)
        self.file_canvas.bind("<Button-1>", self.expand_image)
        content_frame.grid(row=1, column=2, padx=10, pady=10, sticky=W, rowspan=5)
        self.lbx_sel_paterns = Listbox(tab_patterns, height=10, width=35, exportselection=0)
        self.lbx_sel_paterns.grid(row=1, column=4, padx=10, pady=10, sticky=W, rowspan=5)
        btn_add = Button(tab_patterns, image=self.add_icon, command=self.click_add_patt)
        btn_add.grid(row=2, column=3)
        btn_add_ttp = CreateToolTip(btn_add, 'Add pattern')
        btn_remove = Button(tab_patterns, image=self.delete_icon, command=self.click_remove_patt)
        btn_remove.grid(row=4, column=3)
        btn_remove_ttp = CreateToolTip(btn_remove, 'Remove pattern')
        self.tab_control.grid(row=1, column=0, padx=20, pady=10, sticky=W)
        frm_aux2.grid(row=5, column=0, pady=10, padx=10, columnspan=4, rowspan=3, sticky=E)

        self.canvas_expanded = Canvas(self.tlevel_image_exp, width=500, height=500)
        self.canvas_expanded.config(background='white', borderwidth=1)
        self.canvas_expanded.grid()

    def show_frm(self):
        self.retrieve_list()
        if len(self.trv_available.get_children()) != 0:
            self.trv_available.selection_set(self.trv_available.get_children()[0])
            self.select_experimental_scenario(None)
        self.frm_parent.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_general.grid_forget()

    def retrieve_list(self):
        """
        This function shows the existing 'Experimental sscenarios for the specified designer' in the home TreeView
        """
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=82, information=[1, self.id_designer])
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1], wrap_text(elements[2], 72)))

    def select_experimental_scenario(self, event):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.id_selected_ex_scenario = int(self.trv_available.item(self.trv_available.selection())['text'])  # Retrieve id of selected item from TreeView
            self.directive = Message(action=85, information=[self.id_selected_ex_scenario])
            self.connection = self.directive.send_directive(self.connection)
            self.experimental_scenario = ExperimentalSC(id=self.id_selected_ex_scenario,
                                                        name=self.connection.message.information[0],
                                                        description=self.connection.message.information[1],
                                                        access_code=self.connection.message.information[2],
                                                        start_time=self.connection.message.information[3],
                                                        end_time=self.connection.message.information[4],
                                                        scenario_availability=self.connection.message.information[5],
                                                        scenario_lock=self.connection.message.information[6],
                                                        id_experiment=self.connection.message.information[7],
                                                        id_control_group=self.connection.message.information[8],
                                                        id_experimental_group=self.connection.message.information[9],
                                                        connection=self.connection)
            # Retrieve scenario components
            self.scenario_components = []
            self.directive = Message(action=87, information=[self.id_selected_ex_scenario, 1])
            self.connection = self.directive.send_directive(self.connection)
            for item in self.connection.message.information:
                elements = item.split('¥')
                self.scenario_components.append(
                    ScenarioComponent(id_DB=int(elements[0]), id_exp_scenario=int(elements[1]),
                                      id_problem=int(elements[2]), connection=self.connection))

            # Insert description of the current scenario into visual component
            self.txt_scenario_desc['state'] = NORMAL
            self.txt_scenario_desc.delete('1.0', 'end-1c')
            # Create datetime objects for each time (a and b)
            dateTimeA = datetime.datetime.combine(datetime.date.today(), self.experimental_scenario.end_time )
            dateTimeB = datetime.datetime.combine(datetime.date.today(), self.experimental_scenario.start_time)
            # Get the difference between datetimes (as timedelta)
            dateTimeDifference = dateTimeA - dateTimeB
            # Divide difference in seconds by number of seconds in minutes (60)
            dateTimeDifferenceInHours = dateTimeDifference.total_seconds() / 60
            if len(self.scenario_components) == 1:
                text = 'The selected scenario has one design problem that you can solve within {} minutes and with supporting ' \
                       'tools, such as: design patterns, digrams and descriptions. Take the necessary time to solve it ' \
                       'in the most efficient way.'.format(int(dateTimeDifferenceInHours))
            else:
                text = 'The selected scenario has {} design problems that you can solve within {} minutes and with supporting ' \
                       'tools, such as: design patterns, digrams and descriptions. Take the necessary time to solve it ' \
                       'in the most efficient way.'.format(len(self.scenario_components), int(dateTimeDifferenceInHours))
            self.txt_scenario_desc.insert('1.0', wrap_text(text,95))
            self.txt_scenario_desc['state'] = DISABLED

    def click_enter_scenario(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.tlevel_auth_scenario.title('Need to authenticate')
            self.tlevel_auth_scenario.deiconify()
            self.tlevel_auth_scenario.grab_set()
            self.txt_auth_scenario.focus_set()

    def click_authenticate_scenario(self):
        if self.validate_access_code():
            self.txt_auth_scenario.delete('1.0', 'end-1c')
            self.tlevel_auth_scenario.grab_release()
            self.tlevel_auth_scenario.withdraw()
            self.frm_parent.grid_forget()
            self.frm_general.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)
            self.load_scenario_component(0)
        else:
            messagebox.showerror(parent=self.tlevel_auth_scenario, title='Wrong access code',
                                    message='The access code you provided is worng, retry')

    def click_authenticate_cancel(self):
        self.txt_auth_scenario.delete('1.0', 'end-1c')
        self.tlevel_auth_scenario.grab_release()
        self.tlevel_auth_scenario.withdraw()

    def validate_access_code(self):
        if len(self.txt_auth_scenario.get('1.0','end-1c')) != 0:
            if self.txt_auth_scenario.get('1.0','end-1c') == self.experimental_scenario.access_code:
                return True
        return False

    def click_next_scenario(self):
        pass

    def click_attach_file(self):
        pass

    def click_remove_file(self):
        pass

    def click_add_patt(self):
        element = self.lbx_av_patterns.curselection()
        if element is not None:   # Check if listbox is selected
            index = element[0]
            id_selected = self.av_patterns_ids[index]
            if not id_selected in self.sel_patterns_ids:    # Check if current patern_id is not in the 'selected patterns list'
                for item in self.available_patterns:
                    if item.id == id_selected:  # Find selected pattern in available patterns list
                        self.selected_pattern = item
                        break
                self.sel_patterns_ids.append(id_selected)   # Append pattern_id to selected patterns ids
                self.lbx_sel_paterns.insert(END, self.selected_pattern.get_content_name())  # Insert pattern name into selected listbox patters

    def click_remove_patt(self):
        element = self.lbx_sel_paterns.curselection()
        if element is not None:  # Check if listbox is selected
            if element:
                index = element[0]
                id_selected = self.sel_patterns_ids[index]
                self.lbx_sel_paterns.delete(element)  # Remove from listbox
                for item in reversed(self.sel_patterns_ids):
                    if item == id_selected:
                        self.sel_patterns_ids.remove(item)
                        break

    def expand_image(self, event):
        # Fill canvas with retrieved image
        load = Image.open(self.file_aux.filename)
        load = load.resize((500, 500), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(load)
        self.canvas_expanded.delete()
        self.file_aux.image = self.canvas_expanded.create_image(0, 0, anchor='nw',
                                                                image=self.render)  # and display new image
        self.tlevel_image_exp.deiconify()
        self.tlevel_image_exp.grab_set()

    def close_tlevel_image(self):
        self.tlevel_image_exp.grab_release()
        self.tlevel_image_exp.withdraw()
        self.select_pattern_section(None)

    def load_scenario_component(self, index):
        self.directive = Message(action=42, information=[self.id_designer, self.scenario_components[index].id_DB])
        self.connection = self.directive.send_directive(self.connection)
        self.available_patterns = Pattern.get_patterns(self.connection, self.connection.message.information)
        self.txt_hints['state'] = NORMAL
        self.txt_hints.delete('1.0', 'end-1c')
        self.txt_hints.insert('1.0', wrap_text('ESTAS SON INDICACIONES DE PRUEBA', 95))
        self.txt_hints['state'] = DISABLED
        self.lbl_problem_title['text'] = self.scenario_components[index].problem.name
        self.txt_problem_desc['state'] = NORMAL
        self.txt_problem_desc.delete('1.0', 'end-1c')
        self.txt_problem_desc.insert('1.0', wrap_text(self.scenario_components[index].problem.description, 95))
        self.txt_hints['state'] = DISABLED
        self.lbx_av_patterns.delete(0, END)  # clear
        self.av_patterns_ids = []
        self.sel_patterns_ids = []
        for item in self.available_patterns:
            self.av_patterns_ids.append(item.id)
            self.lbx_av_patterns.insert(END, item.get_content_name())
        self.lbx_av_patterns.select_set(0)
        self.select_available_pattern(None)

    def select_available_pattern(self, event):
        self.lbx_sections.delete(0, END)  # clear
        id_selected = self.av_patterns_ids[self.lbx_av_patterns.curselection()[0]]
        for item in self.available_patterns:
            if item.id == id_selected:
                self.selected_pattern = item
                break
        self.pattern_sections_ids = []
        for item in self.selected_pattern.sections:
            if item.name != 'Name':
                self.pattern_sections_ids.append(item.temp_section_id)
                self.lbx_sections.insert(END, item.name)
        self.lbx_sections.select_set(0)
        self.select_pattern_section(None)

    def select_pattern_section(self, event):
        id_selected = self.pattern_sections_ids[self.lbx_sections.curselection()[0]]
        for item in self.selected_pattern.sections:
            if item.temp_section_id == id_selected:
                self.show_section_content(item)
                break

    def show_section_content(self, section):
        self.txt_section_content['state'] = NORMAL
        self.txt_section_content.delete('1.0', 'end-1c')
        self.file_canvas.grid_forget()
        self.txt_section_content.grid_forget()
        if section.data_type == 'File': # The section content is a file (display in a canvas)
            self.directive = Message(action=65, information=[section.diagram_id])
            self.connection = self.directive.send_directive(self.connection)
            self.file_aux = File()
            self.file_aux.write_file(self.connection.message.information[0], self.connection.message.information[1])
            # Fill canvas with retrieved image
            load = Image.open(self.file_aux.filename)
            load = load.resize((150, 150), Image.ANTIALIAS)
            self.render = ImageTk.PhotoImage(load)
            self.file_canvas.delete()
            self.file_aux.image = self.file_canvas.create_image(0, 0, anchor='nw',
                                                              image=self.render)  # and display new image
            self.file_canvas.grid()
        else:   # The section content is text (Display in a textbox)
            self.txt_section_content.insert('1.0', wrap_text(section.content, 34))
            self.txt_section_content.grid()
        self.txt_section_content['state'] = DISABLED




