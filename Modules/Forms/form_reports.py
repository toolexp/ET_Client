from tkinter import Label, LabelFrame, Frame, Text, Button, messagebox, PhotoImage, Toplevel, Scrollbar, Canvas
from tkinter.constants import *
from tkinter.ttk import Treeview, Combobox, Separator
from Modules.Config.Data import Message, Experiment, CreateToolTip, Problem, Pattern, ExperimentalSC, File, \
    summarize_text, get_mean_value, Solution
from PIL import ImageTk, Image
from Modules.Config.Visual import *


class FormParentReport:
    def __init__(self, window, connection):
        self.frm_parent = Frame(window)
        self.initialize_components()
        self.frm_child = FormChildReport(self.frm_parent, connection)

    def initialize_components(self):
        lbl_report_title = Label(self.frm_parent, text='Experiment Report')
        lbl_report_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_report_title.grid(row=0, column=0, pady=20)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildReport:
    def __init__(self, frm_parent, connection):
        self.connection = connection
        self.id_selected = 0
        self.frm_child_report = LabelFrame(frm_parent)
        self.tlevel_comp_detail = Toplevel(frm_parent)
        self.tlevel_comp_detail.protocol("WM_DELETE_WINDOW", self.click_exit_component_det)
        self.tlevel_comp_detail.withdraw()
        self.tlevel_sol_detail = Toplevel(frm_parent)
        self.tlevel_sol_detail.protocol("WM_DELETE_WINDOW", self.click_exit_solution_det)
        self.tlevel_sol_detail.withdraw()
        self.tlevel_diagram = Toplevel(self.tlevel_sol_detail)
        self.tlevel_diagram.protocol("WM_DELETE_WINDOW", self.click_exit_diagram)
        self.tlevel_diagram.withdraw()
        self.initialize_components()

    def initialize_components(self):
        """
        Method that initialize the visual components for each form associated with the configuration of experiments
        """
        # Button icons used in the forms
        self.csv_icon = PhotoImage(file=r"./Resources/csv.png")
        self.info_icon = PhotoImage(file=r"./Resources/info.png")

        # Components for Report form (list of experiments)
        # General selection section
        lbl_sep1 = Label(self.frm_child_report)
        lbl_sep1.grid(row=0, column=0, padx=10, pady=10, rowspan=7)
        lbl_available_exp = Label(self.frm_child_report, text='Select an experiment', anchor=W)
        lbl_available_exp.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_available_exp.grid(row=0, column=1, pady=10, sticky=W)
        self.trv_available_exp = Treeview(self.frm_child_report, height=5, columns=('N', 'Experiment'))
        self.trv_available_exp.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_exp.heading('#1', text='N', anchor=CENTER)
        self.trv_available_exp.heading('#2', text='Experiment', anchor=CENTER)
        self.trv_available_exp.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_exp.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available_exp.column('#2', width=250, minwidth=250, stretch=NO)
        self.trv_available_exp.bind("<ButtonRelease-1>", self.select_experiment_general)
        self.trv_available_exp.grid(row=1, column=1, columnspan=3, sticky=W, pady=10)
        vsb_trv_avex = Scrollbar(self.frm_child_report, orient="vertical", command=self.trv_available_exp.yview)
        vsb_trv_avex.grid(row=1, column=4, pady=10, sticky=NS)
        self.trv_available_exp.configure(yscrollcommand=vsb_trv_avex.set)
        btn_detail_exp = Button(self.frm_child_report, image=self.info_icon, command=self.click_view_experiment)
        btn_detail_exp.grid(row=0, column=3, pady=10, padx=5, sticky=E)
        btn_detail_exp_ttp = CreateToolTip(btn_detail_exp, 'View experiment information')
        btn_csv = Button(self.frm_child_report, image=self.csv_icon, command=self.click_csv)
        btn_csv.grid(row=0, column=2, pady=10, sticky=E)
        btn_csv_ttp = CreateToolTip(btn_csv, 'Generate .csv file')
        lbl_available_sc = Label(self.frm_child_report, text='Select a scenario', anchor=W)
        lbl_available_sc.config(font=SUBTITLE2_FONT, fg=TEXT_COLOR)
        lbl_available_sc.grid(row=2, column=1, pady=10, columnspan=2, sticky=W)
        self.trv_available_sc = Treeview(self.frm_child_report, height=5, columns=('N', 'Experimental scenario'))
        self.trv_available_sc.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_sc.heading('#1', text='N', anchor=CENTER)
        self.trv_available_sc.heading('#2', text='Experimental scenario', anchor=CENTER)
        self.trv_available_sc.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_sc.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available_sc.column('#2', width=250, minwidth=250, stretch=NO)
        self.trv_available_sc.bind("<ButtonRelease-1>", self.select_scenario_general)
        self.trv_available_sc.grid(row=3, column=1, columnspan=3, sticky=W, pady=10)
        vsb_trv_avsc = Scrollbar(self.frm_child_report, orient="vertical", command=self.trv_available_sc.yview)
        vsb_trv_avsc.grid(row=3, column=4, pady=10, sticky=NS)
        self.trv_available_sc.configure(yscrollcommand=vsb_trv_avsc.set)
        btn_detail_sc = Button(self.frm_child_report, image=self.info_icon, command=self.click_view_scenario)
        btn_detail_sc.grid(row=2, column=3, pady=10, sticky=E)
        btn_detail_sc_ttp = CreateToolTip(btn_detail_sc, 'View scenario information')
        lbl_available_prob = Label(self.frm_child_report, text='Select a problem', anchor=W)
        lbl_available_prob.config(font=SUBTITLE2_FONT, fg=TEXT_COLOR)
        lbl_available_prob.grid(row=4, column=1, pady=10, columnspan=2, sticky=W)
        self.trv_available_prob = Treeview(self.frm_child_report, height=5, columns=('N', 'Design problem'))
        self.trv_available_prob.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_prob.heading('#1', text='N', anchor=CENTER)
        self.trv_available_prob.heading('#2', text='Design problem', anchor=CENTER)
        self.trv_available_prob.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_prob.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available_prob.column('#2', width=250, minwidth=250, stretch=NO)
        self.trv_available_prob.bind("<ButtonRelease-1>", self.select_problem_general)
        self.trv_available_prob.grid(row=5, column=1, columnspan=3, sticky=W, pady=10)
        vsb_trv_avprob = Scrollbar(self.frm_child_report, orient="vertical", command=self.trv_available_prob.yview)
        vsb_trv_avprob.grid(row=5, column=4, pady=10, sticky=NS)
        self.trv_available_prob.configure(yscrollcommand=vsb_trv_avprob.set)
        btn_detail_prob = Button(self.frm_child_report, image=self.info_icon, command=self.click_view_problem)
        btn_detail_prob.grid(row=4, column=3, pady=10, sticky=E)
        btn_detail_prob_ttp = CreateToolTip(btn_detail_prob, 'View problem report')
        sep_aux1 = Separator(self.frm_child_report, orient=VERTICAL)
        sep_aux1.grid(row=0, column=5, sticky=NS, rowspan=7, padx=30)
        # Detailed selection section
        self.trv_detail_sc = Treeview(self.frm_child_report, height=8,
                                      columns=('N', 'Scenario', 'M1', 'M2', 'M3', 'M4'))
        self.trv_detail_sc.heading('#0', text='ID', anchor=CENTER)
        self.trv_detail_sc.heading('#1', text='N', anchor=CENTER)
        self.trv_detail_sc.heading('#2', text='Scenario', anchor=CENTER)
        self.trv_detail_sc.heading('#3', text='M1', anchor=CENTER)
        self.trv_detail_sc.heading('#4', text='M2', anchor=CENTER)
        self.trv_detail_sc.heading('#5', text='M3', anchor=CENTER)
        self.trv_detail_sc.heading('#6', text='M4', anchor=CENTER)
        self.trv_detail_sc.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_detail_sc.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_detail_sc.column('#2', width=250, minwidth=250, stretch=NO)
        self.trv_detail_sc.column('#3', width=55, minwidth=55, stretch=NO)
        self.trv_detail_sc.column('#4', width=55, minwidth=55, stretch=NO)
        self.trv_detail_sc.column('#5', width=55, minwidth=55, stretch=NO)
        self.trv_detail_sc.column('#6', width=55, minwidth=55, stretch=NO)
        self.trv_detail_sc.grid(row=0, column=6, rowspan=2, sticky=W, pady=10)
        vsb_trv_detsc = Scrollbar(self.frm_child_report, orient="vertical", command=self.trv_detail_sc.yview)
        vsb_trv_detsc.grid(row=0, column=7, rowspan=2, pady=10, sticky=NS)
        self.trv_detail_sc.configure(yscrollcommand=vsb_trv_detsc.set)
        self.trv_detail_prob = Treeview(self.frm_child_report, height=8,
                                        columns=('N', 'Problem', 'M1', 'M2', 'M3', 'M4'))
        self.trv_detail_prob.heading('#0', text='ID', anchor=CENTER)
        self.trv_detail_prob.heading('#1', text='N', anchor=CENTER)
        self.trv_detail_prob.heading('#2', text='Problem', anchor=CENTER)
        self.trv_detail_prob.heading('#3', text='M1', anchor=CENTER)
        self.trv_detail_prob.heading('#4', text='M2', anchor=CENTER)
        self.trv_detail_prob.heading('#5', text='M3', anchor=CENTER)
        self.trv_detail_prob.heading('#6', text='M4', anchor=CENTER)
        self.trv_detail_prob.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_detail_prob.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_detail_prob.column('#2', width=250, minwidth=250, stretch=NO)
        self.trv_detail_prob.column('#3', width=55, minwidth=55, stretch=NO)
        self.trv_detail_prob.column('#4', width=55, minwidth=55, stretch=NO)
        self.trv_detail_prob.column('#5', width=55, minwidth=55, stretch=NO)
        self.trv_detail_prob.column('#6', width=55, minwidth=55, stretch=NO)
        self.trv_detail_prob.grid(row=2, column=6, rowspan=2, sticky=W, pady=10)
        vsb_trv_detprob = Scrollbar(self.frm_child_report, orient="vertical", command=self.trv_detail_prob.yview)
        vsb_trv_detprob.grid(row=2, column=7, rowspan=2, pady=10, sticky=NS)
        self.trv_detail_prob.configure(yscrollcommand=vsb_trv_detprob.set)
        self.trv_detail_designer = Treeview(self.frm_child_report, height=8, columns=('N', 'Designer', 'M1', 'M2',
                                                                                      'M3', 'M4'))
        self.trv_detail_designer.heading('#0', text='ID', anchor=CENTER)
        self.trv_detail_designer.heading('#1', text='N', anchor=CENTER)
        self.trv_detail_designer.heading('#2', text='Designer', anchor=CENTER)
        self.trv_detail_designer.heading('#3', text='M1', anchor=CENTER)
        self.trv_detail_designer.heading('#4', text='M2', anchor=CENTER)
        self.trv_detail_designer.heading('#5', text='M3', anchor=CENTER)
        self.trv_detail_designer.heading('#6', text='M4', anchor=CENTER)
        self.trv_detail_designer.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_detail_designer.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_detail_designer.column('#2', width=250, minwidth=250, stretch=NO)
        self.trv_detail_designer.column('#3', width=55, minwidth=55, stretch=NO)
        self.trv_detail_designer.column('#4', width=55, minwidth=55, stretch=NO)
        self.trv_detail_designer.column('#5', width=55, minwidth=55, stretch=NO)
        self.trv_detail_designer.column('#6', width=55, minwidth=55, stretch=NO)
        self.trv_detail_designer.bind("<Double-1>", self.view_detailed_solution)
        self.trv_detail_designer.grid(row=4, column=6, rowspan=2, sticky=W, pady=10)
        vsb_trv_detdesig = Scrollbar(self.frm_child_report, orient="vertical", command=self.trv_detail_designer.yview)
        vsb_trv_detdesig.grid(row=4, column=7, rowspan=2, pady=10, sticky=NS)
        self.trv_detail_designer.configure(yscrollcommand=vsb_trv_detdesig.set)
        lbl_notes = Label(self.frm_child_report, text='NOTE:\tDouble click on a designer to see\tLEGEND:\tM1=Solution '
                                                      'time | M3=Viewed patterns\n\this solution for a problem ^.\t\t\t'
                                                      'M2=Selection time | M4=Chosen patterns\n')
        lbl_notes.config(fg=TEXT_COLOR, font=NOTE_FONT, justify=LEFT)
        lbl_notes.grid(row=6, column=6, pady=10, sticky=W)
        lbl_sep2 = Label(self.frm_child_report)
        lbl_sep2.grid(row=0, column=8, padx=10, pady=10, rowspan=7)

        # Components for component (experiment, scenario or problem) details
        lbl_sep3 = Label(self.tlevel_comp_detail)
        lbl_sep3.grid(row=0, column=0, padx=10, pady=20)
        self.txt_detail_component = Text(self.tlevel_comp_detail, height=25, width=60)
        self.txt_detail_component.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_detail_component.grid(row=0, column=1, pady=20, sticky=W)
        vsb_txt_detcomp = Scrollbar(self.tlevel_comp_detail, orient="vertical", command=self.txt_detail_component.yview)
        vsb_txt_detcomp.grid(row=0, column=2, pady=20, sticky=NS)
        self.txt_detail_component.configure(yscrollcommand=vsb_txt_detcomp.set)
        lbl_sep4 = Label(self.tlevel_comp_detail)
        lbl_sep4.grid(row=0, column=3, padx=10, pady=20)

        # Components of expanded detailed sent solution
        lbl_sep5 = Label(self.tlevel_sol_detail)
        lbl_sep5.grid(row=0, column=0, padx=10, pady=20, rowspan=3)
        lbl_sep6 = Label(self.tlevel_sol_detail)
        lbl_sep6.grid(row=0, column=1, pady=10)
        self.btn_detail_sol = Button(self.tlevel_sol_detail, text='View diagram >>',
                                     command=self.click_view_diagram_sol)
        self.txt_detail_solution = Text(self.tlevel_sol_detail, height=25, width=60)
        self.txt_detail_solution.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_detail_solution.grid(row=1, column=1, sticky=W, columnspan=2)
        vsb_txt_detsol = Scrollbar(self.tlevel_sol_detail, orient="vertical", command=self.txt_detail_solution.yview)
        vsb_txt_detsol.grid(row=1, column=3, sticky=NS)
        self.txt_detail_solution.configure(yscrollcommand=vsb_txt_detsol.set)
        lbl_sep7 = Label(self.tlevel_sol_detail)
        lbl_sep7.grid(row=0, column=4, padx=10, pady=20, rowspan=3)
        lbl_sep8 = Label(self.tlevel_sol_detail)
        lbl_sep8.grid(row=2, column=1, pady=10, columnspan=2)

        # Components of expanded sent solution diagram
        self.canvas_expanded = Canvas(self.tlevel_diagram, width=500, height=500)
        self.canvas_expanded.config(background='white', borderwidth=1)
        self.canvas_expanded.grid()

    def show_frm(self):
        """
        Displays the home list of the 'Experiments' form
        """
        self.frm_child_report.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        self.retrieve_experiments()

    def hide_frm(self):
        """
        Hides all forms that are currently active
        """
        self.clear_components()
        self.frm_child_report.grid_forget()

    def retrieve_experiments(self):
        """
        This function shows the existing 'Experiments' in the home TreeView
        """
        # Remove existing elements in the list
        for item in self.trv_available_exp.get_children():
            self.trv_available_exp.delete(item)
        self.directive = Message(action=92, information=['finished'])
        self.connection = self.directive.send_directive(self.connection)
        if len(self.connection.message.information) != 0:
            for index, item in enumerate(self.connection.message.information):
                elements = item.split('¥')
                self.trv_available_exp.insert('', 'end', text=elements[0], values=(index + 1,
                                                                                   summarize_text(elements[1], 250)))
            self.available_patterns = Pattern.get_available_patterns(self.connection)
            '''if len(self.trv_available_exp.get_children()) != 0:
                self.trv_available_exp.selection_set(self.trv_available_exp.get_children()[0])
                self.select_experiment_general()'''
        else:
            messagebox.showwarning(parent=self.frm_child_report, title='No experiments',
                                   message='No experiments in finished state')

    def retrieve_scenarios(self, scenarios=None):
        """
        This function shows the existing Experimental scenarios in an 'Experiment'
        """
        # Remove existing elements in the list
        for item in self.trv_available_sc.get_children():
            self.trv_available_sc.delete(item)
        for index, item in enumerate(scenarios):
            elements = item.split('¥')
            self.trv_available_sc.insert('', 'end', text=elements[0], values=(index + 1,
                                                                              summarize_text(elements[1], 250)))
        '''if len(self.trv_available_sc.get_children()) != 0:
            self.trv_available_sc.selection_set(self.trv_available_sc.get_children()[0])
            self.select_scenario()'''

    def retrieve_problems(self, problems=None):
        """
        This function shows the existing Problems in an 'Experimental scenario'
        """
        # Remove existing elements in the list
        for item in self.trv_available_prob.get_children():
            self.trv_available_prob.delete(item)
        for index, item in enumerate(problems):
            elements = item.split('¥')
            self.trv_available_prob.insert('', 'end', text=elements[0], values=(index + 1,
                                                                                summarize_text(elements[1], 250)))
        '''if len(self.trv_available_prob.get_children()) != 0:
            self.trv_available_prob.selection_set(self.trv_available_prob.get_children()[0])
            self.select_problem()'''

    def select_experiment_general(self, event=None):
        """
        This function is activated when the 'Click Experiments TreeView' event ocurrs, it indicates than an experiments
        has been selected
        """
        if len(self.trv_available_exp.selection()) == 1:
            self.clear_components(3)
            id_selected_exp = int(self.trv_available_exp.item(self.trv_available_exp.selection())[
                                      'text'])  # Retrieve id of selected item from TreeView
            self.directive = Message(action=95, information=[id_selected_exp])
            self.connection = self.directive.send_directive(self.connection)
            self.experiment = Experiment(id=id_selected_exp, name=self.connection.message.information[0],
                                         description=self.connection.message.information[1],
                                         design_type=self.connection.message.information[2],
                                         state=self.connection.message.information[3],
                                         creation_date=self.connection.message.information[5],
                                         execution_date=self.connection.message.information[6],
                                         finished_date=self.connection.message.information[7])
            self.retrieve_scenarios(self.connection.message.information[4])
            # Ask to server for dataframe of the measurements for the scenarios of selected experiment
            self.directive = Message(action=107, information=[id_selected_exp, 'experiment'])
            self.connection = self.directive.send_directive(self.connection)
            final_df = get_mean_value(self.connection.message.information[0])
            for index, row in final_df.iterrows():
                self.trv_detail_sc.insert('', 'end', text=row.id, values=(index + 1, summarize_text(row.variable, 250),
                                                                          row.m1, row.m2, row.m3, row.m4))

    def select_scenario_general(self, event=None):
        """
        Function activated when a scenario is selecteded
        """
        if len(self.trv_available_sc.selection()) == 1:
            self.clear_components(2)
            id_selected_sc = int(self.trv_available_sc.item(self.trv_available_sc.selection())[
                                     'text'])  # Retrieve id of selected item from TreeView
            self.directive = Message(action=85, information=[id_selected_sc, 'report', 1])
            self.connection = self.directive.send_directive(self.connection)
            self.scenario = ExperimentalSC(id=id_selected_sc, title=self.connection.message.information[0],
                                           description=self.connection.message.information[1],
                                           id_description_diagram=self.connection.message.information[2],
                                           info_designers=self.connection.message.information[4])
            self.retrieve_problems(self.connection.message.information[3])
            # Ask to server for dataframe of the measurements for the problems of selected scenario
            self.directive = Message(action=107, information=[id_selected_sc, 'scenario'])
            self.connection = self.directive.send_directive(self.connection)
            final_df = get_mean_value(self.connection.message.information[0])
            for index, row in final_df.iterrows():
                self.trv_detail_prob.insert('', 'end', text=row.id, values=(index + 1,
                                                                            summarize_text(row.variable, 250), row.m1,
                                                                            row.m2, row.m3, row.m4))

    def select_problem_general(self, event=None):
        """
        Function activated when a scenario is selected
        """
        if len(self.trv_available_prob.selection()) == 1:
            self.clear_components(1)
            id_selected_prob = int(self.trv_available_prob.item(self.trv_available_prob.selection())[
                                       'text'])  # Retrieve id of selected item from TreeView
            self.directive = Message(action=55, information=[id_selected_prob])
            self.connection = self.directive.send_directive(self.connection)
            self.problem = Problem(id=id_selected_prob, brief_description=self.connection.message.information[0],
                                   description=self.connection.message.information[1],
                                   id_solution=self.connection.message.information[2],
                                   av_patterns=self.available_patterns, connection=self.connection)
            # Ask to server for dataframe of the measurements for the designers of selected problem
            self.directive = Message(action=107, information=[id_selected_prob, 'problem'])
            self.connection = self.directive.send_directive(self.connection)
            final_df = get_mean_value(self.connection.message.information[0])
            for index, row in final_df.iterrows():
                self.trv_detail_designer.insert('', 'end', text=row.id, values=(index + 1,
                                                                                summarize_text(row.variable, 250),
                                                                                row.m1, row.m2, row.m3, row.m4))

    def click_view_experiment(self):
        """
        Function activated when 'Experiment detail' button is pressed, it shows the tlevel_detail window showing
        main information of the selected experimentin trv_available_sc
        """
        if len(self.trv_available_exp.selection()) == 1:
            self.txt_detail_component['state'] = NORMAL
            self.txt_detail_component.delete('1.0', 'end-1c')
            self.txt_detail_component.insert('1.0', 'EXPERIMENT NAME\n{}\n\n'
                                                    'DESCRIPTION\n{}\n\n'
                                                    'DESIGN TYPE\n{}\n\n'
                                                    'CREATION DATETIME\n{}\n\n'
                                                    'EXECUTION DATETIME\n{}\n\n'
                                                    'FINISHED DATETIME\n{}'.
                                             format(self.experiment.name,
                                                    self.experiment.description,
                                                    'One group' if self.experiment.design_type == 1 else 'Two groups',
                                                    self.experiment.creation_date.strftime('%c'),
                                                    self.experiment.execution_date.strftime('%c'),
                                                    self.experiment.finished_date.strftime('%c')))
            self.txt_detail_component['state'] = DISABLED
            self.tlevel_comp_detail.deiconify()
            self.tlevel_comp_detail.grab_set()
        else:
            messagebox.showwarning(parent=self.frm_child_report, title='No selection',
                                   message='You must select one item')

    def click_view_scenario(self):
        """
        Function activated when 'Scenario detail' button is pressed, it shows the tlevel_detail window showing
        main information of the selected experimental scenario in trv_available_sc
        """
        if len(self.trv_available_sc.selection()) == 1:
            self.txt_detail_component['state'] = NORMAL
            self.txt_detail_component.delete('1.0', 'end-1c')
            self.txt_detail_component.insert('1.0', 'EXPERIMENTAL SCENARIO TITLE\n{}\n\n'
                                                    'DESCRIPTION\n{}\n\n'
                                                    'DESIGNERS SCENARIO ASSIGNED: {}\n\n'
                                                    'DESIGNERS COMPLETED SCENARIO: {}\n\n'
                                                    'DESIGNERS DID NOT COMPLETE SCENARIO: {}\n\n'
                                                    'DESIGNERS DID NOT RUN SCENARIO: {}'.
                                             format(self.scenario.title,
                                                    self.scenario.description,
                                                    self.scenario.info_designers[0],
                                                    self.scenario.info_designers[1],
                                                    self.scenario.info_designers[2],
                                                    self.scenario.info_designers[3]))
            self.txt_detail_component['state'] = DISABLED
            self.tlevel_comp_detail.deiconify()
            self.tlevel_comp_detail.grab_set()
        else:
            messagebox.showwarning(parent=self.frm_child_report, title='No selection',
                                   message='You must select one item')

    def click_view_problem(self):
        """
        Function activated when 'Problem detail' button is pressed, it shows the tlevel_detail window showing
        main information of the selected problem in trv_available_prob
        """
        if len(self.trv_available_prob.selection()) == 1:
            aux_patterns = ''
            for item in self.problem.solution.patterns:
                aux_patterns += '- {}\n'.format(item.get_joined_main_s())
            self.txt_detail_component['state'] = NORMAL
            self.txt_detail_component.delete('1.0', 'end-1c')
            self.txt_detail_component.insert('1.0', 'PROBLEM BRIEF DESCRIPTION\n{}\n\n'
                                                    'DESCRIPTION\n{}\n\n'
                                                    'EXPECTED SOLUTION NOTES\n{}\n\n'
                                                    'EXPECTED SOLUTION PATTERNS\n{}'.
                                             format(self.problem.brief_description,
                                                    self.problem.description,
                                                    self.problem.solution.annotations,
                                                    'No patterns configured' if aux_patterns == '' else aux_patterns))
            self.txt_detail_component['state'] = DISABLED
            self.tlevel_comp_detail.deiconify()
            self.tlevel_comp_detail.grab_set()
        else:
            messagebox.showwarning(parent=self.frm_child_report, title='No selection',
                                   message='You must select one item')

    def click_view_diagram_sol(self):
        # Fill summary problem canvas with retrieved image
        load = Image.open(self.solution.diagram.filename)
        load = load.resize((500, 500), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(load)
        self.canvas_expanded.delete()
        self.solution.diagram.image = self.canvas_expanded.create_image(0, 0, anchor='nw',
                                                                        image=self.render)  # and display new image
        self.tlevel_diagram.deiconify()
        self.tlevel_diagram.grab_set()

    def click_csv(self):
        if len(self.trv_available_exp.selection()) == 1:
            # Get report in .zip (temporarly)
            self.directive = Message(action=106, information=[self.experiment.id])
            self.connection = self.directive.send_directive(self.connection)
            report_file = File()
            path = report_file.write_permanent_file(self.connection.message.information[0],
                                                    self.connection.message.information[1])
            messagebox.showinfo(parent=self.frm_child_report, title='Report created',
                                message='Zipped report created in app main folder')
        else:
            messagebox.showwarning(parent=self.frm_child_report, title='No selection',
                                   message='You must select one item')

    def view_detailed_solution(self, event=None):
        if len(self.trv_detail_designer.selection()) == 1:
            id_selected_desig = self.trv_detail_designer.item(self.trv_detail_designer.selection())[
                'text']  # Retrieve id of selected item from TreeView
            if id_selected_desig != 'X':
                if self.trv_detail_designer.item(self.trv_detail_designer.selection())['values'][2] != 'X':
                    # Here asks for the sent solution of specific designer
                    self.directive = Message(action=105, information=[int(id_selected_desig), self.problem.id])
                    self.connection = self.directive.send_directive(self.connection)
                    # Getting assigned patterns in current experimental scenario
                    assigned_patterns = []
                    for item in self.connection.message.information[4]:
                        for pattern in self.available_patterns:
                            if item == pattern.id:
                                assigned_patterns.append(pattern)
                    chosen_patterns = []
                    # Getting patterns of sent solution
                    for item in self.connection.message.information[2]:
                        id_pattern = int(item.split('¥')[0])
                        for pattern in self.available_patterns:
                            if id_pattern == pattern.id:
                                chosen_patterns.append(pattern)
                    # Getting current group for the designer
                    current_group = self.connection.message.information[3]
                    # Creating the auxiliar solution
                    self.solution = Solution(annotations=self.connection.message.information[0],
                                             patterns=chosen_patterns,
                                             diagram_id=self.connection.message.information[1],
                                             connection=self.connection)
                    # Adjust visual components depending on the sent solution
                    self.btn_detail_sol.grid_forget()
                    if self.solution.diagram_id is not None:
                        self.btn_detail_sol.grid(row=0, column=2, pady=10, sticky=E)
                    aux_patterns_assign = ''
                    for item in assigned_patterns:
                        aux_patterns_assign += '- {}\n'.format(item.get_joined_main_s())
                    aux_patterns_sent_sol = ''
                    for item in self.solution.patterns:
                        aux_patterns_sent_sol += '- {}\n'.format(item.get_joined_main_s())
                    self.txt_detail_solution['state'] = NORMAL
                    self.txt_detail_solution.delete('1.0', 'end-1c')
                    self.txt_detail_solution.insert('1.0', 'CURRENT PROBLEM\n{}\n\n'
                                                           'CURRENT DESIGNER\n{}\n\n'
                                                           'ASSIGNED GROUP\n{}\n\n'
                                                           'SENT SOLUTION NOTES\n{}\n\n'
                                                           'SENT SOLUTION DIAGRAM\n{}\n\n'
                                                           'ASSIGNED PATTERNS\n{}\n\n'
                                                           'CHOSEN PATTERNS\n{}'.
                                                    format(self.problem.brief_description,
                                                           self.trv_detail_designer.item(
                                                               self.trv_detail_designer.selection())['values'][1],
                                                           'Control group' if current_group == 1 else 'Experimental group',
                                                           self.solution.annotations,
                                                           'No diagram in solution' if self.solution.diagram_id is None else 'Click up button to see diagram ^',
                                                           'No patterns configured' if aux_patterns_assign == '' else aux_patterns_assign,
                                                           'No patterns chosen' if aux_patterns_sent_sol == '' else aux_patterns_sent_sol))
                    self.txt_detail_solution['state'] = DISABLED
                    self.tlevel_sol_detail.deiconify()
                    self.tlevel_sol_detail.grab_set()
                else:
                    messagebox.showwarning(parent=self.frm_child_report, title='Wrong selection',
                                           message='The selected designer does not have a solution for the current '
                                                   'problem')

    def clear_components(self, decision=4):
        if decision > 0:  # When selecting an problem form general list
            for item in self.trv_detail_designer.get_children():
                self.trv_detail_designer.delete(item)
            if decision > 1:  # When selecting a scenario form general list
                for item in self.trv_available_prob.get_children():
                    self.trv_available_prob.delete(item)
                for item in self.trv_detail_prob.get_children():
                    self.trv_detail_prob.delete(item)
                if decision > 2:  # When selecting an experiment form general list
                    for item in self.trv_available_sc.get_children():
                        self.trv_available_sc.delete(item)
                    for item in self.trv_detail_sc.get_children():
                        self.trv_detail_sc.delete(item)
                    if decision > 3:  # Clearing information from all the treeviews
                        for item in self.trv_available_exp.get_children():
                            self.trv_available_exp.delete(item)

    def click_exit_component_det(self):
        self.tlevel_comp_detail.grab_release()
        self.tlevel_comp_detail.withdraw()

    def click_exit_diagram(self):
        self.tlevel_diagram.grab_release()
        self.tlevel_diagram.withdraw()

    def click_exit_solution_det(self):
        self.tlevel_sol_detail.grab_release()
        self.tlevel_sol_detail.withdraw()