from tkinter import Label, LabelFrame, Frame, Text, Button, filedialog, Canvas, messagebox, PhotoImage, Toplevel, \
    Listbox, Entry
from tkinter.constants import *
from tkinter.ttk import Treeview, Notebook, Separator
from Modules.Config.Data import CreateToolTip, Message, Template, Pattern, Category, File, wrap_text, Section, \
    ExperimentalSC, ScenarioComponent, Measurement, Solution, TimerClass
from PIL import Image, ImageTk
import os
import shutil

TITLE_FONT = ("Arial", 18)
SUBTITLE_FONT = ("Arial", 14)
LABEL_FONT = ("Arial", 11)
TEXT_FONT = ("Arial", 10)
BOLD_FONT = ("Arial", 10, 'bold')

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
        lbl_title.grid(row=0, column=0, columnspan=2, pady=50, sticky=EW)
        lbl_experimental_trv = Label(self.frm_parent, text='Select a scenario')
        lbl_experimental_trv.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_experimental_trv.grid(row=1, column=0, pady=5, padx=50, sticky=NW)
        lbl_problem_desc = Label(self.frm_parent, text='Annotations')
        lbl_problem_desc.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_problem_desc.grid(row=3, column=0, pady=5, padx=50, sticky=NW)
        self.trv_available = Treeview(self.frm_parent, height=4, columns=('Scenario', 'Description'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Scenario', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=300, minwidth=300, stretch=NO)
        self.trv_available.column('#2', width=500, minwidth=500, stretch=NO)
        self.trv_available.bind("<ButtonRelease-1>", self.select_experimental_scenario)
        self.trv_available.grid(row=2, column=0, sticky=W, padx=50, pady=25)
        self.txt_scenario_desc = Text(self.frm_parent, height=6, width=70)
        self.txt_scenario_desc.config(font=SUBTITLE_FONT, bg=defaultbg)
        self.txt_scenario_desc.grid(row=4, column=0, padx=50, pady=25, sticky=NW)
        btn_access = Button(self.frm_parent, image=self.next_icon, command=self.click_enter_scenario)
        btn_access.grid(row=1, column=1, padx=50, pady=5, sticky=N)
        btn_access_ttp = CreateToolTip(btn_access, 'Go')

        # Window dialog to authenticate the selected experimental scenario
        lbl_access_auth = Label(self.tlevel_auth_scenario, text='Insert access code: ')
        lbl_access_auth.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_access_auth.grid(pady=10, padx=20, sticky=W)
        self.txt_auth_scenario = Entry(self.tlevel_auth_scenario, width=50)
        self.txt_auth_scenario.config(font=SUBTITLE_FONT, show="*")
        self.txt_auth_scenario.grid(row=0, column=1, padx=20, pady=10, sticky=W)
        btn_access_auth = Button(self.tlevel_auth_scenario, image=self.next_icon, command=self.click_authenticate_scenario)
        btn_access_auth.grid(row=0, column=2, padx=20, pady=10, sticky=W)
        btn_access_auth_ttp = CreateToolTip(btn_access_auth, 'Go')
        btn_cancel_auth = Button(self.tlevel_auth_scenario, image=self.cancel_icon, command=self.click_authenticate_cancel)
        btn_cancel_auth.grid(row=1, column=2, padx=20, pady=10, sticky=W)
        btn_cancel_auth_ttp = CreateToolTip(btn_cancel_auth, 'Cancel')

        # Experiment form
        frm_aux1 = Frame(self.frm_general)
        self.lbl_component_title = Label(frm_aux1, text='Component {} of {}')
        self.lbl_component_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        self.lbl_component_title.grid(row=0, column=0, columnspan=7, pady=15, sticky=EW)
        sep_aux1 = Separator(frm_aux1, orient=HORIZONTAL)
        sep_aux1.grid(row=1, column=0, sticky=EW, columnspan=7)
        self.txt_hints = Text(frm_aux1, height=8, width=80)
        self.txt_hints.config(font=TEXT_FONT, bg=defaultbg)
        self.txt_hints.grid(row=2, column=0, padx=20, pady=25, rowspan=2, sticky=NW)
        sep_aux2 = Separator(frm_aux1, orient=VERTICAL)
        sep_aux2.grid(row=1, column=1, sticky=NS, rowspan=3)
        lbl_problem = Label(frm_aux1, text='Design problem: ')
        lbl_problem.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_problem.grid(row=2, column=2, pady=25, padx=10, sticky=NW)
        self.lbl_problem_title = Label(frm_aux1)
        self.lbl_problem_title.config(font=TEXT_FONT)
        self.lbl_problem_title.grid(row=2, column=3, pady=25, padx=5, sticky=NW)
        self.txt_problem_desc = Text(frm_aux1, height=4, width=75)
        self.txt_problem_desc.config(font=TEXT_FONT, bg=defaultbg)
        self.txt_problem_desc.grid(row=3, column=2, padx=10, pady=10, columnspan=2, sticky=NW)
        sep_aux3 = Separator(frm_aux1, orient=HORIZONTAL)
        sep_aux3.grid(row=4, column=0, sticky=EW, columnspan=4)
        sep_aux4 = Separator(frm_aux1, orient=VERTICAL)
        sep_aux4.grid(row=2, column=4, sticky=NS, rowspan=6)

        self.btn_next_scenario = Button(frm_aux1, image=self.next_icon, command=self.click_next_scenario)
        self.btn_next_scenario.grid(row=2, column=6, padx=20, pady=10, sticky=W)
        btn_next_scenario_ttp = CreateToolTip(self.btn_next_scenario, 'Next problem')
        frm_aux1.grid(row=2, column=0, pady=20, padx=10, columnspan=4, rowspan=3, sticky=E)

        #frm_aux2 = Frame(self.frm_general)
        lbl_solution = Label(frm_aux1, text='Design a solution')
        lbl_solution.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_solution.grid(row=5, column=0, padx=20, pady=10, sticky=W)
        self.tab_control = Notebook(frm_aux1)

        tab_patterns = Frame(self.tab_control)
        self.tab_control.add(tab_patterns, text="Design patterns", padding=10)
        lbl_av_patterns = Label(tab_patterns, text='Patterns browser')
        lbl_av_patterns.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_av_patterns.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        lbl_sel_patterns = Label(tab_patterns, text='Selected patterns')
        lbl_sel_patterns.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_sel_patterns.grid(row=0, column=2, pady=10, padx=10, sticky=W)
        lbl_content = Label(tab_patterns, text='Pattern content')
        lbl_content.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_content.grid(row=0, column=3, pady=10, padx=10, sticky=W)
        self.lbx_av_patterns = Listbox(tab_patterns, height=16, width=40, exportselection=0)
        self.lbx_av_patterns.grid(row=1, column=0, padx=10, pady=10, sticky=W, rowspan=7)
        self.lbx_av_patterns.bind('<<ListboxSelect>>', self.select_available_pattern)
        self.lbx_sel_paterns = Listbox(tab_patterns, height=16, width=40, exportselection=0)
        self.lbx_sel_paterns.grid(row=1, column=2, padx=10, pady=10, sticky=W, rowspan=7)
        btn_add = Button(tab_patterns, image=self.add_icon, command=self.click_add_patt)
        btn_add.grid(row=2, column=1)
        btn_add_ttp = CreateToolTip(btn_add, 'Add pattern')
        btn_remove = Button(tab_patterns, image=self.delete_icon, command=self.click_remove_patt)
        btn_remove.grid(row=4, column=1)
        btn_remove_ttp = CreateToolTip(btn_remove, 'Remove pattern')
        self.txt_pattern_content = Text(tab_patterns, height=16, width=70)
        self.txt_pattern_content.config(font=TEXT_FONT)
        self.txt_pattern_content.grid(row=1, column=3, padx=10, pady=10, sticky=W, rowspan=7)
        self.btn_view_diagram = Button(tab_patterns, text='View >>\ndiagram', command=self.click_expand_diagram)
        self.btn_view_diagram.grid(row=1, column=4, padx=10, pady=10, sticky=W)

        tab_file = Frame(self.tab_control)
        self.tab_control.add(tab_file, text="File", padding=10)
        lbl_upload = Label(tab_file, text='Attach a file to the solution: ')
        lbl_upload.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_upload.grid(row=0, column=0, padx=20, pady=20, sticky=W)
        btn_open = Button(tab_file, image=self.open_icon, command=self.click_attach_file)
        btn_open.grid(row=1, column=0, padx=20, pady=10, sticky=E)
        btn_open_ttp = CreateToolTip(btn_open, 'Attach file')
        btn_quit = Button(tab_file, image=self.remove_icon, command=self.click_remove_file)
        btn_quit.grid(row=2, column=0, padx=20, pady=10, sticky=E)
        btn_quit_ttp = CreateToolTip(btn_quit, 'Remove file')
        self.canvas_solution = Canvas(tab_file, width=300, height=300)
        self.canvas_solution.config(background='white', borderwidth=1)
        self.canvas_solution.grid(row=0, column=1, padx=10, pady=10, rowspan=10, sticky=NS)

        tab_desc = Frame(self.tab_control)
        self.tab_control.add(tab_desc, text="Description", padding=10)
        self.txt_solution_desc = Text(tab_desc, height=10, width=160)
        self.txt_solution_desc.config(font=TEXT_FONT)
        self.txt_solution_desc.grid(row=0, column=0, padx=20, pady=20, sticky=W)

        self.tab_control.grid(row=6, column=0, padx=20, pady=10, sticky=W, columnspan=4)

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
        shutil.rmtree('./Resources/temp/')
        os.mkdir('./Resources/temp/')

    def retrieve_list(self):
        """
        This function shows the existing 'Experimental scenarios for the specified designer' in the home TreeView
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
                                                        scenario_availability=self.connection.message.information[3],
                                                        scenario_lock=self.connection.message.information[4],
                                                        id_experiment=self.connection.message.information[5],
                                                        id_control_group=self.connection.message.information[6],
                                                        id_experimental_group=self.connection.message.information[7],
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
            if len(self.scenario_components) == 1:
                text = 'The selected scenario has one design problem that you can solve with supporting ' \
                       'tools, such as: design patterns, digrams and descriptions. Take the necessary time to solve it ' \
                       'in the most efficient way.'
            else:
                text = 'The selected scenario has {} design problems that you can solve with supporting ' \
                       'tools, such as: design patterns, digrams and descriptions. Take the necessary time to solve it ' \
                       'in the most efficient way.'.format(len(self.scenario_components))
            self.txt_scenario_desc.insert('1.0', wrap_text(text,85))
            self.txt_scenario_desc['state'] = DISABLED

    def click_enter_scenario(self):
        """
        Shows pop-up window that allows validation of access code for the experimental scenario (necessary before showing
        the problems of the experimental scenario)
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.tlevel_auth_scenario.title('Need to authenticate')
            self.tlevel_auth_scenario.deiconify()
            self.tlevel_auth_scenario.grab_set()
            self.txt_auth_scenario.focus_set()

    def click_authenticate_scenario(self):
        """
        Shows the component form with information of first component loaded. This happens if the validation process is
        correct
        """
        if self.validate_access_code():
            self.txt_auth_scenario.delete(0, END)
            self.tlevel_auth_scenario.grab_release()
            self.tlevel_auth_scenario.withdraw()
            self.frm_parent.grid_forget()
            self.frm_general.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)
            self.initialize_component_variables()
            self.current_scenarios_counter = 0
            self.clear_visual_components()
            self.load_scenario_component(self.current_scenarios_counter)
        else:
            messagebox.showerror(parent=self.tlevel_auth_scenario, title='Wrong access code',
                                 message='The access code you provided is wrong, retry')

    def initialize_component_variables(self):
        self.attached_file = None
        self.av_patterns_seen = []
        self.solution_time = 0
        self.selection_time = 0
        self.first_pattern_sol = False # Indicates that any pattern solution has been selected yet

    def click_authenticate_cancel(self):
        """
        Cancel validation of access code for an experimental scenario, it hides the validation pop-up window
        """
        self.txt_auth_scenario.delete(0, END)
        self.tlevel_auth_scenario.grab_release()
        self.tlevel_auth_scenario.withdraw()

    def validate_access_code(self):
        """
        Verifies that the provided code matches the stored access code for the selected experimental scenario
        """
        if len(self.txt_auth_scenario.get()) != 0:
            if self.txt_auth_scenario.get() == self.experimental_scenario.access_code:
                return True
        return False

    def click_next_scenario(self):
        """
        After clicking next scenario component. This method prompts the user to confirm his decision. After confirming
        the system saves the important information (solutions and measurements) and then continue to the next scenario
        component if available, otherwise the experiment will be closed
        """
        decision = messagebox.askyesno(title='Confirmation',
                                       message="Are you sure you want to continue? Yo won't be able to make any change later")
        if decision: # Confirmation of action
            if self.save_changes():
                self.current_scenarios_counter += 1
                if self.current_scenarios_counter == len(self.scenario_components): # If no more scenario components available
                    messagebox.showinfo(title='Experimental scenario finished',
                                           message="This concludes the execution of the experimental scenario. Thank you!")
                    self.clear_visual_components()
                    self.finish_experiment()
                    self.hide_frm()
                    self.show_frm()
                else: # If another scenario component available
                    messagebox.showinfo(title='Next component',
                                        message="You are about to start a new component, press Ok when you are ready.")
                    self.clear_visual_components()
                    self.initialize_component_variables()
                    self.load_scenario_component(self.current_scenarios_counter)

    def save_changes(self):
        validation_option = self.validate_component_frm()  # Validate any problem with info inserted into visual components
        if validation_option == 0:  # No problem, proceed to save info
            self.solution_time += self.time_thread.seconds
            self.time_thread.stop() # Stop thread timer
            # Get measurements of important metrics for the current component
            scenario_comp_id = self.scenario_components[self.current_scenarios_counter].id_DB
            current_measurements = []
            # Solution time
            measurement_1 = Measurement(value=str(self.solution_time), id_metric=1, id_designer=self.id_designer,
                                        id_scenario_comp=scenario_comp_id)
            current_measurements.append(measurement_1)
            # Selection time
            measurement_2 = Measurement(value=str(self.selection_time), id_metric=2, id_designer=self.id_designer,
                                        id_scenario_comp=scenario_comp_id)
            current_measurements.append(measurement_2)
            # Viewed patterns
            measurement_3 = Measurement(value=str(len(self.av_patterns_seen)), id_metric=3,
                                        id_designer=self.id_designer, id_scenario_comp=scenario_comp_id)
            current_measurements.append(measurement_3)
            # Chosen patterns
            measurement_4 = Measurement(value=str(self.lbx_sel_paterns.size()), id_metric=4,
                                        id_designer=self.id_designer, id_scenario_comp=scenario_comp_id)
            current_measurements.append(measurement_4)
            for item in current_measurements:
                self.directive = Message(action=96, information=[item.value, item.date, item.id_metric, item.id_designer,
                                                                 item.id_scenario_comp])
                self.connection = self.directive.send_directive(self.connection)
            # Get info and build the solution to send to the server
            # Create diagram in DB
            self.directive = Message(action=61, information=[self.attached_file.file_bytes, self.attached_file.name])
            self.connection = self.directive.send_directive(self.connection)
            id_diagram = self.connection.message.information[0]
            # Create object for the solution
            solution_aux = Solution(annotations=self.txt_solution_desc.get('1.0', 'end-1c'), diagram_id=id_diagram,
                                    patterns_id=self.sel_patterns_ids)
            # Create the solution in DB
            self.directive = Message(action=101, information=[solution_aux.annotations, solution_aux.diagram_id,
                                                              self.id_designer, scenario_comp_id, solution_aux.patterns_id])
            self.connection = self.directive.send_directive(self.connection)
            return True
        elif validation_option == 1:
            messagebox.showwarning(title='Missing information',
                                   message="You haven't selected any pattern")
        elif validation_option == 2:
            messagebox.showwarning(title='Missing information',
                                   message="You haven't attached any file")
        else:
            messagebox.showwarning(title='Missing information',
                                   message='You must add annotations to your solution')
        return False

    def validate_component_frm(self):
        if len(self.txt_solution_desc.get('1.0','end-1c')) != 0:
            if self.attached_file is not None:
                if self.lbx_sel_paterns.size() != 0:
                    return 0
                return 1
            return 2
        return 3

    def finish_experiment(self):
        pass

    def click_attach_file(self):
        """
        Create a File object that is uploaded by the user, validating that there is not a file uploaded already.
        """
        if self.attached_file is None:
            filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select JPEG file",
                                                  filetypes=[("jpeg", "*.jpg")])
            if not filename:
                return  # user cancelled; stop this method
            self.attached_file = File()
            self.attached_file.read_file(filename)
            # Display image into canvas
            load = Image.open(self.attached_file.filename)
            load = load.resize((300, 300), Image.ANTIALIAS)
            self.render = ImageTk.PhotoImage(load)
            if self.attached_file.image is not None:  # if an image was already loaded
                self.canvas_solution.delete(self.attached_file.image)  # remove the previous image
            self.attached_file.image = self.canvas_solution.create_image(0, 0, anchor='nw', image=self.render)

    def click_remove_file(self):
        """
        Remove an uploaded file from the system validating it is already uploaded. This method also delete
        any image in the canvas that may be fulfilled with an image.
        """
        if self.attached_file is not None:  # if an image was already loaded
            self.canvas_solution.delete(self.attached_file.image)
            self.attached_file = None

    def click_add_patt(self):
        element = self.lbx_av_patterns.curselection()
        if element is not None:   # Check if listbox is selected
            index = element[0]
            id_selected = self.av_patterns_ids[index]
            if not id_selected in self.sel_patterns_ids:    # Check if current patern_id is not in the 'selected patterns list'
                if id_selected in self.current_ideal_patterns and not self.first_pattern_sol:  # Check if selected pattern matches ideal patterns and for the first time
                    self.first_pattern_sol = True
                    self.selection_time = self.time_thread.seconds
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
                if id_selected in self.current_ideal_patterns and self.first_pattern_sol:  # Check if selected pattern matches ideal patterns
                    self.first_pattern_sol = False
                    self.selection_time = 0 # Discard saved time
                for item in reversed(self.sel_patterns_ids):
                    if item == id_selected:
                        self.sel_patterns_ids.remove(item)
                        break

    def click_expand_diagram(self):
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

    def clear_visual_components(self):
        self.txt_hints['state'] = NORMAL
        self.txt_hints.delete('1.0', 'end-1c')
        self.txt_problem_desc['state'] = NORMAL
        self.txt_problem_desc.delete('1.0', 'end-1c')
        self.lbx_av_patterns.delete(0, END)
        self.lbx_sel_paterns.delete(0, END)
        self.txt_pattern_content['state'] = NORMAL
        self.txt_pattern_content.delete('1.0', 'end-1c')
        self.txt_pattern_content['state'] = DISABLED
        self.txt_solution_desc.delete('1.0', 'end-1c')
        if self.attached_file is not None:  # if an image was already loaded
            self.canvas_solution.delete(self.attached_file.image)
            self.attached_file = None

    def load_scenario_component(self, index):
        self.directive = Message(action=42, information=[self.id_designer, self.scenario_components[index].id_DB])
        self.connection = self.directive.send_directive(self.connection)
        self.available_patterns = Pattern.get_patterns(self.connection, self.connection.message.information)
        self.lbl_component_title['text'] = 'Component {} of {}'.format(self.current_scenarios_counter + 1,
                                                                       len(self.scenario_components))
        self.txt_hints.insert('1.0', wrap_text('ESTAS SON INDICACIONES DE PRUEBA', 90))
        self.txt_hints['state'] = DISABLED
        self.lbl_problem_title['text'] = self.scenario_components[index].problem.name
        self.txt_problem_desc.insert('1.0', wrap_text(self.scenario_components[index].problem.description, 80))
        self.txt_problem_desc['state'] = DISABLED
        self.tab_control.select(0)
        self.av_patterns_ids = []
        self.sel_patterns_ids = []
        for item in self.available_patterns:
            self.av_patterns_ids.append(item.id)
            self.lbx_av_patterns.insert(END, item.get_content_name())
        #self.lbx_av_patterns.select_set(0)
        #self.select_available_pattern(None)
        self.current_ideal_patterns = self.scenario_components[index].problem.solution.patterns_id  # Get the patterns of the ideal solution for current problem
        self.time_thread = TimerClass()
        self.time_thread.begin()

    def select_available_pattern(self, event):
        id_selected = self.av_patterns_ids[self.lbx_av_patterns.curselection()[0]]
        # Add selected pattern to the seen pattern (metric)
        if not id_selected in self.av_patterns_seen:
            self.av_patterns_seen.append(id_selected)
        # Retrieve info of the selected pattern (in available patterns list)
        for item in self.available_patterns:
            if item.id == id_selected:
                self.selected_pattern = item
                break
        # Set visual components depending on the selected pattern and its info
        self.btn_view_diagram['state'] = DISABLED
        self.txt_pattern_content['state'] = NORMAL
        self.txt_pattern_content.delete('1.0', 'end-1c')
        for item in self.selected_pattern.sections:
            self.txt_pattern_content.insert('end-1c', item.name + ": ")
            if item.data_type == 'File': # The section content is a file
                self.directive = Message(action=65, information=[item.diagram_id])
                self.connection = self.directive.send_directive(self.connection)
                self.file_aux = File()
                self.file_aux.write_file(self.connection.message.information[0], self.connection.message.information[1])
                self.btn_view_diagram['state'] = NORMAL
                self.txt_pattern_content.insert('end-1c', "\n" + wrap_text('Click right button to see diagram >>', 80) + "\n\n")
            else:
                self.txt_pattern_content.insert('end-1c', "\n" + wrap_text(item.content, 80) + "\n\n")
        self.txt_pattern_content['state'] = DISABLED




