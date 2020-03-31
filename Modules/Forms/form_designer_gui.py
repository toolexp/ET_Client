from tkinter import Label, LabelFrame, Frame, Text, Button, filedialog, Canvas, messagebox, PhotoImage, Toplevel, \
    Listbox, Entry, Scrollbar
from tkinter.constants import *
from tkinter.ttk import Treeview, Notebook, Separator
from Modules.Config.Data import CreateToolTip, Message, Pattern, File, ExperimentalSC, \
    Measurement, Solution, TimerClass, summarize_text
from PIL import Image, ImageTk
import os
from Modules.Config.Visual import *
from datetime import datetime


class FormParentDesigner:
    def __init__(self, window, connection, current_designer):
        self.connection = connection
        self.current_designer = current_designer
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
        self.add_icon = PhotoImage(file=r"./Resources/down_arrow.png")
        self.delete_icon = PhotoImage(file=r"./Resources/up_arrow.png")
        self.next_icon = PhotoImage(file=r"./Resources/next.png")
        self.back_icon = PhotoImage(file=r"./Resources/back.png")
        self.copy_icon = PhotoImage(file=r"./Resources/copy.png")
        self.open_icon = PhotoImage(file=r"./Resources/open.png")
        self.complete_icon = PhotoImage(file=r"./Resources/complete.png")
        self.incomplete_icon = PhotoImage(file=r"./Resources/incomplete.png")
        self.optional_icon = PhotoImage(file=r"./Resources/optional.png")
        self.refresh_icon = PhotoImage(file=r"./Resources/refresh.png")

        # Initialize visual components for displaying available experiment scenarios
        lbl_title = Label(self.frm_parent, text='Experiments')
        lbl_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_title.grid(row=0, column=0, columnspan=9, pady=20, sticky=EW)
        sep_aux5 = Separator(self.frm_parent, orient=HORIZONTAL)
        sep_aux5.grid(row=1, column=0, sticky=EW, columnspan=9)
        lbl_sep1 = Label(self.frm_parent)
        lbl_sep1.grid(row=2, column=0, padx=10, pady=20, rowspan=2)
        lbl_experimental_trv = Label(self.frm_parent, text='Select an experiment')
        lbl_experimental_trv.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_experimental_trv.grid(row=2, column=1, pady=20, sticky=W)
        lbl_sep2 = Label(self.frm_parent)
        lbl_sep2.grid(row=2, column=3, padx=10, pady=20, rowspan=2)
        lbl_problem_desc = Label(self.frm_parent, text='Information')
        lbl_problem_desc.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_problem_desc.grid(row=2, column=4, pady=20, sticky=W)
        lbl_sep3 = Label(self.frm_parent)
        lbl_sep3.grid(row=2, column=6, padx=10, pady=20, rowspan=2)
        self.trv_available = Treeview(self.frm_parent, height=11, columns='Title')
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Title', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=400, minwidth=400, stretch=NO)
        self.trv_available.bind("<ButtonRelease-1>", self.select_experimental_scenario)
        self.trv_available.grid(row=3, column=1, sticky=W, pady=20)
        vsb_trv_av = Scrollbar(self.frm_parent, orient="vertical", command=self.trv_available.yview)
        vsb_trv_av.grid(row=3, column=2, pady=20, sticky=NS)
        self.trv_available.configure(yscrollcommand=vsb_trv_av.set)
        self.txt_scenario_desc = Text(self.frm_parent, height=15, width=40)
        self.txt_scenario_desc.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_scenario_desc.grid(row=3, column=4, pady=20, sticky=W)
        vsb_txt_sc = Scrollbar(self.frm_parent, orient="vertical", command=self.txt_scenario_desc.yview)
        vsb_txt_sc.grid(row=3, column=5, pady=20, sticky=NS)
        self.txt_scenario_desc.configure(yscrollcommand=vsb_txt_sc.set)
        sep_aux1 = Separator(self.frm_parent, orient=VERTICAL)
        sep_aux1.grid(row=2, column=7, sticky=NS, rowspan=2)
        btn_access = Button(self.frm_parent, image=self.next_icon, command=self.click_enter_scenario)
        btn_access.grid(row=2, column=8, padx=30, pady=5)
        btn_access_ttp = CreateToolTip(btn_access, 'Go')
        btn_refresh = Button(self.frm_parent, image=self.refresh_icon, command=self.retrieve_list)
        btn_refresh.grid(row=3, column=8, padx=30, pady=5, sticky=N)
        btn_refresh_ttp = CreateToolTip(btn_refresh, 'Refresh list')

        # Window dialog to authenticate the selected experimental scenario
        lbl_access_auth = Label(self.tlevel_auth_scenario, text='Insert access code: ')
        lbl_access_auth.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_access_auth.grid(pady=10, padx=20, sticky=W)
        self.txt_auth_scenario = Entry(self.tlevel_auth_scenario, width=50)
        self.txt_auth_scenario.config(font=SUBTITLE2_FONT, show="*")
        self.txt_auth_scenario.grid(row=0, column=1, padx=20, pady=10, sticky=W)
        btn_access_auth = Button(self.tlevel_auth_scenario, image=self.next_icon, command=self.click_authenticate_scenario)
        btn_access_auth.grid(row=0, column=2, padx=20, pady=10, sticky=W)
        btn_access_auth_ttp = CreateToolTip(btn_access_auth, 'Go')
        btn_cancel_auth = Button(self.tlevel_auth_scenario, image=self.cancel_icon, command=self.click_authenticate_cancel)
        btn_cancel_auth.grid(row=1, column=2, padx=20, pady=10, sticky=W)
        btn_cancel_auth_ttp = CreateToolTip(btn_cancel_auth, 'Cancel')

        # Experiment form
        lbl_sep4 = Label(self.frm_general)
        lbl_sep4.grid(row=0, column=0, padx=10, pady=5, rowspan=2)
        self.lbl_exp_title = Label(self.frm_general, text='Experiment: {}')
        self.lbl_exp_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        self.lbl_exp_title.grid(row=0, column=1, columnspan=5, pady=5, sticky=EW)
        self.txt_exp_desc = Text(self.frm_general, height=4, width=157)
        self.txt_exp_desc.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_exp_desc.grid(row=1, column=1, pady=5, sticky=W)
        vsb_txt_expd = Scrollbar(self.frm_general, orient="vertical", command=self.txt_exp_desc.yview)
        vsb_txt_expd.grid(row=1, column=2, pady=5, sticky=NS)
        self.txt_exp_desc.configure(yscrollcommand=vsb_txt_expd.set)
        lbl_sep11 = Label(self.frm_general)
        lbl_sep11.grid(row=1, column=3, padx=10, pady=5)
        self.btn_view_dd = Button(self.frm_general, text='View >>\ndiagram', command=self.click_expand_dd)
        btn_view_dd_ttp = CreateToolTip(self.btn_view_dd, 'Experiment description diagram')
        sep_aux3 = Separator(self.frm_general, orient=HORIZONTAL)
        sep_aux3.grid(row=2, column=0, sticky=EW, columnspan=6)

        lbl_sep5 = Label(self.frm_general)
        lbl_sep5.grid(row=3, column=0, padx=10, pady=5, rowspan=2)
        self.lbl_prob_title = Label(self.frm_general, text='Problem {} of {}: {}')
        self.lbl_prob_title.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        self.lbl_prob_title.grid(row=3, column=1, columnspan=2, pady=5, sticky=W)
        self.txt_prob_desc = Text(self.frm_general, height=7, width=157)
        self.txt_prob_desc.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_prob_desc.grid(row=4, column=1, pady=5, sticky=W)
        vsb_txt_probd = Scrollbar(self.frm_general, orient="vertical", command=self.txt_prob_desc.yview)
        vsb_txt_probd.grid(row=4, column=2, pady=5, sticky=NS)
        self.txt_prob_desc.configure(yscrollcommand=vsb_txt_probd.set)
        lbl_sep12 = Label(self.frm_general)
        lbl_sep12.grid(row=3, column=3, padx=10, pady=5, rowspan=2)
        sep_aux2 = Separator(self.frm_general, orient=HORIZONTAL)
        sep_aux2.grid(row=5, column=0, sticky=EW, columnspan=4)
        lbl_sep6 = Label(self.frm_general)
        lbl_sep6.grid(row=6, column=0, padx=10, pady=5, rowspan=2)
        lbl_solution_title = Label(self.frm_general, text='Your solution')
        lbl_solution_title.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_solution_title.grid(row=6, column=1, pady=5, columnspan=2, sticky=W)
        self.btn_next_scenario = Button(self.frm_general, image=self.next_icon, command=self.click_next_scenario)
        self.btn_next_scenario.grid(row=3, column=5, padx=30, pady=5, sticky=W)
        btn_next_scenario_ttp = CreateToolTip(self.btn_next_scenario, 'Next component')
        sep_aux4 = Separator(self.frm_general, orient=VERTICAL)
        sep_aux4.grid(row=3, column=4, sticky=NS, rowspan=5)

        self.tab_control = Notebook(self.frm_general)
        self.tab_patterns = Frame(self.tab_control)
        self.tab_control.add(self.tab_patterns, text="Design patterns", padding=10, image=self.incomplete_icon, compound=RIGHT)
        lbl_av_patterns = Label(self.tab_patterns, text='Patterns browser')
        lbl_av_patterns.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_av_patterns.grid(row=0, column=1, pady=10, columnspan=6, sticky=W)
        lbl_content = Label(self.tab_patterns, text='Pattern content')
        lbl_content.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_content.grid(row=0, column=8, pady=10, sticky=W)
        lbl_sel_patterns = Label(self.tab_patterns, text='Selected patterns')
        lbl_sel_patterns.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_sel_patterns.grid(row=3, column=1, pady=10, columnspan=6, sticky=W)
        lbl_sep7 = Label(self.tab_patterns)
        lbl_sep7.grid(row=0, column=0, padx=10, pady=10, rowspan=5)
        self.lbx_av_patterns = Listbox(self.tab_patterns, height=6, width=60, exportselection=0)
        self.lbx_av_patterns.grid(row=1, column=1, sticky=W, columnspan=5)
        self.lbx_av_patterns.bind('<<ListboxSelect>>', self.select_available_pattern)
        vsb_trv_avpat = Scrollbar(self.tab_patterns, orient="vertical", command=self.lbx_av_patterns.yview)
        vsb_trv_avpat.grid(row=1, column=6, pady=10, sticky=NS)
        self.lbx_av_patterns.configure(yscrollcommand=vsb_trv_avpat.set)
        lbl_sep8 = Label(self.tab_patterns)
        lbl_sep8.grid(row=0, column=7, padx=10, pady=10, rowspan=5)
        self.btn_view_pd = Button(self.tab_patterns, text='View diagram >>', command=self.click_expand_pd)
        btn_view_pd_ttp = CreateToolTip(self.btn_view_pd, 'Pattern section diagram')
        self.txt_pattern_content = Text(self.tab_patterns, height=18, width=85)
        self.txt_pattern_content.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_pattern_content.tag_configure("center", justify='center')
        self.txt_pattern_content.tag_add("center", 1.0, "end")
        self.txt_pattern_content.grid(row=1, column=8, sticky=W, columnspan=2, rowspan=4)
        vsb_txt_content = Scrollbar(self.tab_patterns, orient="vertical", command=self.txt_pattern_content.yview)
        vsb_txt_content.grid(row=1, column=10, rowspan=4, pady=10, sticky=NS)
        self.txt_pattern_content.configure(yscrollcommand=vsb_txt_content.set)
        btn_add = Button(self.tab_patterns, image=self.add_icon, command=self.click_add_patt)
        btn_add.grid(row=2, column=3, pady=10, sticky=E)
        btn_add_ttp = CreateToolTip(btn_add, 'Add pattern')
        btn_remove = Button(self.tab_patterns, image=self.delete_icon, command=self.click_remove_patt)
        btn_remove.grid(row=2, column=4, pady=10)
        btn_remove_ttp = CreateToolTip(btn_remove, 'Remove pattern')
        self.lbx_sel_patterns = Listbox(self.tab_patterns, height=6, width=60, exportselection=0)
        self.lbx_sel_patterns.grid(row=4, column=1, sticky=W, columnspan=5)
        vsb_trv_selpat = Scrollbar(self.tab_patterns, orient="vertical", command=self.lbx_sel_patterns.yview)
        vsb_trv_selpat.grid(row=4, column=6, pady=10, sticky=NS)
        self.lbx_sel_patterns.configure(yscrollcommand=vsb_trv_selpat.set)
        lbl_sep9 = Label(self.tab_patterns)
        lbl_sep9.grid(row=0, column=11, padx=10, pady=10, rowspan=5)

        self.tab_desc = Frame(self.tab_control)
        self.tab_control.add(self.tab_desc, text="Notes", padding=10, image=self.incomplete_icon, compound=RIGHT)
        lbl_sep10 = Label(self.tab_desc)
        lbl_sep10.grid(row=0, column=0, padx=10, pady=20)
        self.txt_solution_desc = Text(self.tab_desc, height=20, width=145)
        self.txt_solution_desc.config(font=TEXT_FONT)
        self.txt_solution_desc.bind("<Key>", self.txt_notes_modified)
        self.txt_solution_desc.grid(row=0, column=1, pady=20, sticky=W)
        vsb_txt_solution_desc = Scrollbar(self.tab_desc, orient="vertical", command=self.txt_solution_desc.yview)
        vsb_txt_solution_desc.grid(row=0, column=2, pady=20, sticky=NS)
        self.txt_solution_desc.configure(yscrollcommand=vsb_txt_solution_desc.set)
        lbl_sep14 = Label(self.tab_desc)
        lbl_sep14.grid(row=0, column=3, padx=10, pady=20)

        self.tab_file = Frame(self.tab_control)
        self.tab_control.add(self.tab_file, text="File", padding=1, image=self.optional_icon, compound=RIGHT)
        lbl_upload = Label(self.tab_file, text='Attach a file to the solution: ')
        lbl_upload.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_upload.grid(row=0, column=0, padx=20, pady=20, sticky=W)
        btn_open = Button(self.tab_file, image=self.open_icon, command=self.click_attach_file)
        btn_open.grid(row=1, column=0, padx=20, pady=10, sticky=E)
        btn_open_ttp = CreateToolTip(btn_open, 'Attach file')
        btn_quit = Button(self.tab_file, image=self.remove_icon, command=self.click_remove_file)
        btn_quit.grid(row=2, column=0, padx=20, pady=10, sticky=E)
        btn_quit_ttp = CreateToolTip(btn_quit, 'Remove file')
        self.canvas_solution = Canvas(self.tab_file, width=350, height=350)
        self.canvas_solution.config(background='white', borderwidth=1)
        self.canvas_solution.grid(row=0, column=1, padx=10, pady=10, rowspan=10, sticky=NS)
        self.tab_control.grid(row=7, column=1, pady=10, sticky=W, columnspan=2)

        self.canvas_expanded = Canvas(self.tlevel_image_exp, width=500, height=500)
        self.canvas_expanded.config(background='white', borderwidth=1)
        self.canvas_expanded.grid()

    def show_frm(self):
        self.retrieve_list()
        self.frm_parent.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_general.grid_forget()

    def retrieve_list(self):
        """
        This function shows the existing 'Experimental scenarios for the specified designer' in the home TreeView, if
        not 'Experimental scenario' then an information box is showed
        """
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        # Retrieve scenario for current designer
        self.directive = Message(action=82, information=['my scenarios', self.current_designer.id])
        self.connection = self.directive.send_directive(self.connection)
        # Set visual components with retrieved scenarios
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(summarize_text(elements[1], 400),))
        if len(self.trv_available.get_children()) != 0:
            self.trv_available.selection_set(self.trv_available.get_children()[0])
            self.select_experimental_scenario()
        else:
            self.txt_scenario_desc['state'] = NORMAL
            self.txt_scenario_desc.delete('1.0', 'end-1c')
            self.txt_scenario_desc.insert('1.0', 'No experiments available for you')
            self.txt_scenario_desc['state'] = DISABLED

    def select_experimental_scenario(self, event=None):
        """
        Retrieves information of the selected experimental scenario form the server and saves in a local variable for
        future usage, also shows the description of the selected experimental scenario in a textbox
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            id_selected_ex_scenario = int(self.trv_available.item(self.trv_available.selection())['text'])  # Retrieve id of selected item from TreeView
            self.directive = Message(action=85, information=[id_selected_ex_scenario])
            self.connection = self.directive.send_directive(self.connection)
            self.experimental_scenario = ExperimentalSC(id=id_selected_ex_scenario,
                                                        title=self.connection.message.information[0],
                                                        description=self.connection.message.information[1],
                                                        access_code=self.connection.message.information[2],
                                                        state=self.connection.message.information[3],
                                                        availability=self.connection.message.information[4],
                                                        id_experiment=self.connection.message.information[6],
                                                        id_description_diagram=self.connection.message.information[5],
                                                        connection=self.connection)
            if self.experimental_scenario.description_diagram is not None:
                self.file_dd = self.experimental_scenario.description_diagram
            else:
                self.file_dd = None
            # Insert description of the current scenario into visual component
            self.txt_scenario_desc['state'] = NORMAL
            self.txt_scenario_desc.delete('1.0', 'end-1c')
            self.txt_scenario_desc.insert('1.0', self.experimental_scenario.description)
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
        If validation process is correct the the experimental scenario and it's problems are loaded into the visual
        components
        """
        if self.validate_access_code():
            self.load_experiment()
            self.txt_auth_scenario.delete(0, END)
            self.tlevel_auth_scenario.grab_release()
            self.tlevel_auth_scenario.withdraw()
            self.frm_parent.grid_forget()
            self.frm_general.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)
        else:
            messagebox.showerror(parent=self.tlevel_auth_scenario, title='Wrong access code',
                                 message='The access code you provided is wrong, retry')

    def initialize_component_variables(self):
        """
        Initialize to zero or empty state all variables associated with the resolution of a problem for the designers
        (solutions and measurements)
        """
        self.attached_file = None
        self.av_patterns_seen = []
        self.solution_time = 0
        self.selection_time = []    # Time for selecting solution patterns (may be more than one solution pattern)
        self.selected_pattern_sol = []  # Indicates that any pattern solution has been selected yet

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
        decision = messagebox.askyesno(parent=self.frm_general, title='Confirmation',
                                       message="Are you sure you want to continue? Yo won't be able to make any change "
                                               "later")
        if decision: # Confirmation of action
            if self.save_changes():
                self.problems_counter += 1
                if self.problems_counter == len(self.experimental_scenario.problems): # If no more problems available
                    messagebox.showinfo(parent=self.frm_general, title='Experiment',
                                        message="This concludes the execution of the experiment. Thank you!")
                    self.finish_experiment()
                    self.clear_visual_components()
                    self.hide_frm()
                    self.show_frm()
                else: # If another scenario component available
                    messagebox.showinfo(parent=self.frm_general, title='Next problem',
                                        message="You are about to start a new problem, press Ok when you are ready.")
                    self.clear_visual_components()
                    self.initialize_component_variables()
                    self.load_problem()

    def save_changes(self):
        # Validate any problem with info inserted into visual components
        if self.validate_component_frm():  # No problem, proceed to save info
            self.solution_time += self.time_thread.seconds
            self.time_thread.stop() # Stop thread timer
            acquisition_end_date = datetime.now()
            # Get measurements of important metrics for the current component
            problem_id = self.experimental_scenario.problems[self.problems_counter].id
            current_measurements = []
            # Solution time
            measurement_1 = Measurement(value=float(self.solution_time), acquisition_start_date=self.acquisition_start_date,
                                        acquisition_end_date=acquisition_end_date, id_metric=1,
                                        id_designer=self.current_designer.id, id_problem=problem_id)
            current_measurements.append(measurement_1)
            # Save measurements associated with patterns only when these are available for designer
            if self.pattern_decision:
                # Selection time
                # Getting average if more than one value for this metric
                selection_time = 0 if len(self.selection_time) == 0 else sum(self.selection_time) / len(self.selection_time)
                measurement_2 = Measurement(value=float(selection_time), acquisition_start_date=self.acquisition_start_date,
                                            acquisition_end_date=acquisition_end_date, id_metric=2,
                                            id_designer=self.current_designer.id, id_problem=problem_id)
                current_measurements.append(measurement_2)
                # Viewed patterns
                measurement_3 = Measurement(value=float(len(self.av_patterns_seen)),
                                            acquisition_start_date=self.acquisition_start_date,
                                            acquisition_end_date=acquisition_end_date, id_metric=3,
                                            id_designer=self.current_designer.id, id_problem=problem_id)
                current_measurements.append(measurement_3)
                # Chosen patterns
                measurement_4 = Measurement(value=float(self.lbx_sel_patterns.size()),
                                            acquisition_start_date=self.acquisition_start_date,
                                            acquisition_end_date=acquisition_end_date, id_metric=4,
                                            id_designer=self.current_designer.id, id_problem=problem_id)
                current_measurements.append(measurement_4)
            for item in current_measurements:
                self.directive = Message(action=96, information=[item.value, item.acquisition_start_date,
                                                                 item.acquisition_end_date, item.id_metric,
                                                                 item.id_designer, item.id_problem])
                self.connection = self.directive.send_directive(self.connection)
            # Get info and build the solution to send to the server
            # Create diagram in DB
            id_diagram = None
            if self.attached_file is not None:
                self.directive = Message(action=61, information=[self.attached_file.file_bytes, self.attached_file.name,
                                                                 'sent sol'])
                self.connection = self.directive.send_directive(self.connection)
                id_diagram = self.connection.message.information[0]
            # Create object for the solution
            solution_aux = Solution(annotations=self.txt_solution_desc.get('1.0', 'end-1c'), diagram_id=id_diagram,
                                    patterns_id=self.sel_patterns_ids)
            # Create the solution in DB
            self.directive = Message(action=101, information=[solution_aux.annotations, solution_aux.diagram_id,
                                                              self.current_designer.id, problem_id,
                                                              solution_aux.patterns_id])
            self.connection = self.directive.send_directive(self.connection)
            return True
        return False

    def finish_experiment(self):
        """
        This section checks in the server if current designer is the last of the current experimental scenario, and if
        True changes it's state to finished, otherwise the state remains in executed
        """
        self.directive = Message(action=83, information=['finished', self.experimental_scenario.id])
        self.connection = self.directive.send_directive(self.connection)

    def validate_component_frm(self):
        if self.pattern_decision:
            if self.lbx_sel_patterns.size() == 0:
                messagebox.showwarning(parent=self.frm_general, title='Missing information',
                                       message="You haven't selected any pattern")
                return False
        if len(self.txt_solution_desc.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.frm_general, title='Missing information',
                                   message='You must add notes to your solution')
            return False
        return True

    def click_attach_file(self):
        """
        Create a File object that is uploaded by the user, validating that there is not a file uploaded already.
        """
        if self.attached_file is None:
            filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select image file",
                                                  filetypes=[("Diagrams", ".jpg .png .tiff")])
            if not filename:
                return  # user cancelled; stop this method
            self.attached_file = File()
            self.attached_file.read_file(filename)
            # Display image into canvas
            load = Image.open(self.attached_file.filename)
            load = load.resize((350, 350), Image.ANTIALIAS)
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
        """
        Adds a pattern to the selected pattern listbox (when available to the designer).
        """
        element = self.lbx_av_patterns.curselection()
        if element is not None:   # Check if listbox is selected
            index = element[0]
            id_selected = self.av_patterns_ids[index]
            if not id_selected in self.sel_patterns_ids:    # Check if current pattern_id is not in the 'selected patterns list'
                if id_selected in self.current_ideal_patterns and not id_selected in self.selected_pattern_sol:  # Check if selected pattern matches ideal patterns and for the first time
                    self.selected_pattern_sol.append(id_selected)
                    self.selection_time.append(self.time_thread.seconds)
                for item in self.available_patterns:
                    if item.id == id_selected:  # Find selected pattern in available patterns list
                        self.selected_pattern = item
                        break
                self.sel_patterns_ids.append(id_selected)   # Append pattern_id to selected patterns ids
                self.lbx_sel_patterns.insert(END, self.selected_pattern.get_joined_main_s())  # Insert pattern name into selected listbox patters
                self.check_selected_patterns()

    def click_remove_patt(self):
        """
        Removes a pattern from the selected pattern listbox (when available to the designer).
        """
        element = self.lbx_sel_patterns.curselection()
        if element is not None:  # Check if listbox is selected
            if element:
                index = element[0]
                id_selected = self.sel_patterns_ids[index]
                self.lbx_sel_patterns.delete(element)  # Remove from listbox
                if id_selected in self.current_ideal_patterns and id_selected in self.selected_pattern_sol:  # Check if selected pattern matches ideal patterns and if the the selected pattern correspond to the one selected previously as the pattern solution
                    del self.selection_time[self.selected_pattern_sol.index(id_selected)]
                    self.selected_pattern_sol.remove(id_selected)
                for item in reversed(self.sel_patterns_ids):
                    if item == id_selected:
                        self.sel_patterns_ids.remove(item)
                        break
                self.check_selected_patterns()

    def click_expand_pd(self):
        # Fill canvas with retrieved image
        load = Image.open(self.file_pd.filename)
        load = load.resize((500, 500), Image.ANTIALIAS)
        self.render_pd = ImageTk.PhotoImage(load)
        self.canvas_expanded.delete()
        self.file_pd.image = self.canvas_expanded.create_image(0, 0, anchor='nw', image=self.render_pd)  # and display new image
        self.tlevel_image_exp.deiconify()
        self.tlevel_image_exp.grab_set()

    def click_expand_dd(self):
        # Fill canvas with retrieved image
        load = Image.open(self.file_dd.filename)
        load = load.resize((500, 500), Image.ANTIALIAS)
        self.render_dd = ImageTk.PhotoImage(load)
        self.canvas_expanded.delete()
        self.file_dd.image = self.canvas_expanded.create_image(0, 0, anchor='nw', image=self.render_dd)  # and display new image
        self.tlevel_image_exp.deiconify()
        self.tlevel_image_exp.grab_set()

    def close_tlevel_image(self):
        self.tlevel_image_exp.grab_release()
        self.tlevel_image_exp.withdraw()

    def clear_visual_components(self):
        self.txt_prob_desc['state'] = NORMAL
        self.txt_prob_desc.delete('1.0', 'end-1c')
        self.lbx_av_patterns.delete(0, END)
        self.lbx_sel_patterns.delete(0, END)
        self.txt_pattern_content['state'] = NORMAL
        self.txt_pattern_content.delete('1.0', 'end-1c')
        self.txt_pattern_content['state'] = DISABLED
        self.txt_solution_desc.delete('1.0', 'end-1c')
        if self.attached_file is not None:  # if an image was already loaded
            self.canvas_solution.delete(self.attached_file.image)
            self.attached_file = None
        self.tab_control.tab(0, image=self.incomplete_icon)
        self.tab_control.tab(1, image=self.incomplete_icon)

    def load_experiment(self):
        # Retrieve all information of problems of current scenario
        self.experimental_scenario.retrieve_problems(Pattern.get_available_patterns(self.connection))
        self.initialize_component_variables()
        self.problems_counter = 0
        self.current_designer.get_current_role(
            self.experimental_scenario.id)  # Get role for current experimental scenario
        # Retrieve patterns for designer in current experimental scenario
        self.directive = Message(action=42, information=[self.experimental_scenario.id,
                                                         1 if self.current_designer.current_group == 'experimental' else 2])
        self.connection = self.directive.send_directive(self.connection)
        self.available_patterns = Pattern.get_patterns(self.connection, self.connection.message.information)
        # Make patterns visible if the patterns are available for current designer in current experimental scenario
        if self.available_patterns:
            self.tab_control.tab(0, state='normal')
            self.tab_control.select(0)
            self.pattern_decision = True
        else:
            self.tab_control.tab(0, state='hidden')
            self.tab_control.select(1)
            self.pattern_decision = False
        self.btn_view_dd.grid_forget()
        if self.experimental_scenario.description_diagram is not None:
            self.btn_view_dd.grid(row=1, column=5, padx=10, pady=10, sticky=N)
        self.lbl_exp_title['text'] = 'Experiment: {}'.format(self.experimental_scenario.title)
        self.txt_exp_desc['state'] = NORMAL
        self.txt_exp_desc.delete('1.0', 'end-1c')
        self.txt_exp_desc.insert('1.0', self.experimental_scenario.description)
        self.txt_exp_desc['state'] = DISABLED
        self.load_problem()

    def load_problem(self):
        # Ask for available patterns in current problem for the current designer, depending of the role
        self.lbl_prob_title['text'] = 'Problem {} of {}: {}'.format(self.problems_counter + 1,
                                                                    len(self.experimental_scenario.problems),
                                                                    self.experimental_scenario.problems[self.problems_counter].brief_description)
        self.txt_prob_desc['state'] = NORMAL
        self.txt_prob_desc.delete('1.0', 'end-1c')
        self.txt_prob_desc.insert('1.0', self.experimental_scenario.problems[self.problems_counter].description)
        self.txt_prob_desc['state'] = DISABLED
        self.av_patterns_ids = []
        self.sel_patterns_ids = []
        for item in self.available_patterns:
            self.av_patterns_ids.append(item.id)
            self.lbx_av_patterns.insert(END, item.get_joined_main_s())
        self.current_ideal_patterns = self.experimental_scenario.problems[self.problems_counter].solution.patterns_id  # Get the patterns of the ideal solution for current problem
        # Make patterns visible if the patterns are available for current designer in current experimental scenario
        if self.pattern_decision:
            self.tab_control.select(0)
        else:
            self.tab_control.select(1)
        self.btn_view_pd.grid_forget()
        self.time_thread = TimerClass()
        self.time_thread.begin()
        self.acquisition_start_date = datetime.now()

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
        self.btn_view_pd.grid_forget()
        self.txt_pattern_content['state'] = NORMAL
        self.txt_pattern_content.delete('1.0', 'end-1c')
        for item in self.selected_pattern.sections:
            self.txt_pattern_content.insert('end-1c', item.name + ": ")
            if item.data_type == 'File': # The section content is a file
                if item.diagram_id != 0:
                    self.directive = Message(action=65, information=[item.diagram_id])
                    self.connection = self.directive.send_directive(self.connection)
                    self.file_pd = File()
                    self.file_pd.write_file(self.connection.message.information[0], self.connection.message.information[1])
                    self.btn_view_pd.grid(row=0, column=9, sticky=E)
                    self.txt_pattern_content.insert('end-1c', "\nClick up button to see diagram ^\n\n")

                else:
                    self.file_pd = None
                    self.txt_pattern_content.insert('end-1c', "\nNo diagram loaded for this section\n\n")

            else:
                self.txt_pattern_content.insert('end-1c', "\n" + item.content + "\n\n")
        self.txt_pattern_content['state'] = DISABLED

    def txt_notes_modified(self, event):
        """
        Method that checks if text box of additional notes (solution) is filled or not, so tab image is selected
        """
        if self.txt_solution_desc.get('1.0', 'end-1c') != '':
            self.tab_control.tab(1, image=self.complete_icon)
        else:
            self.tab_control.tab(1, image=self.incomplete_icon)

    def check_selected_patterns(self):
        """
        Method that checks if list box of selected patterns (solution) is filled or not, so tab image is selected
        """
        if self.lbx_sel_patterns.size() != 0:
            self.tab_control.tab(0, image=self.complete_icon)
        else:
            self.tab_control.tab(0, image=self.incomplete_icon)
