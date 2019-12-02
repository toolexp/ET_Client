from tkinter import Label, LabelFrame, Frame, Text, Button, messagebox, PhotoImage, Toplevel, Scrollbar
from tkinter.constants import *
from tkinter.ttk import Treeview, Combobox, Separator
from Modules.Config.Data import Message, ExperimentalSC, ScenarioComponent, CreateToolTip, Problem, Pattern, \
    DesignersGroup, wrap_text
from Modules.Config.Visual import *


class FormParentExConfig:
    def __init__(self, window, connection):
        self.frm_parent = Frame(window)
        self.initialize_components()
        self.frm_child = FormChildExConfig(self.frm_parent, self.lbl_experiment_title, connection)

    def initialize_components(self):
        self.lbl_experiment_title = Label(self.frm_parent, text='Experiment configuration')
        self.lbl_experiment_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        self.lbl_experiment_title.grid(row=0, column=0, pady=20)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildExConfig:
    def __init__(self, frm_parent, title_parent, connection):
        self.title_parent = title_parent
        self.connection = connection
        self.decide = True
        self.id_selected = 0
        self.frm_child_exp_list = LabelFrame(frm_parent)
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_general = LabelFrame(frm_parent)
        self.frm_child_general.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        self.tlevel_problem = Toplevel(frm_parent)
        self.tlevel_problem.protocol("WM_DELETE_WINDOW", self.click_cancel_sc_component)
        self.tlevel_problem.withdraw()
        self.initialize_components()

    def initialize_components(self):
        """
        Method that initialize the visual components for each form associated with the configuration of experiments
        """
        # Button icons used in the forms
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
        self.view_icon = PhotoImage(file=r"./Resources/view.png")
        defaultbg = self.frm_child_general.cget('bg')

        # Components for Experiments List form (list of experiments)
        lbl_sep1 = Label(self.frm_child_exp_list)
        lbl_sep1.grid(row=1, column=0, padx=25, pady=25)
        lbl_select_exp = Label(self.frm_child_exp_list, text=wrap_text('Here is a list of configurable experiments, '
                                                                       'select one to configure', 80), anchor=W)
        lbl_select_exp.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_select_exp.grid(row=0, column=1, pady=25, sticky=W)
        self.trv_available_exp = Treeview(self.frm_child_exp_list, height=15, columns=('Name', 'Description'))
        self.trv_available_exp.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_exp.heading('#1', text='Name', anchor=CENTER)
        self.trv_available_exp.heading('#2', text='Description', anchor=CENTER)
        self.trv_available_exp.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_exp.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available_exp.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available_exp.bind("<Double-1>", self.select_experiment)
        self.trv_available_exp.grid(row=1, column=1, rowspan=15, sticky=W, pady=25)
        vsb_trv_avex = Scrollbar(self.frm_child_exp_list, orient="vertical", command=self.trv_available_exp.yview)
        vsb_trv_avex.grid(row=1, column=2, rowspan=15, pady=25, sticky=NS)
        self.trv_available_exp.configure(yscrollcommand=vsb_trv_avex.set)
        btn_select = Button(self.frm_child_exp_list, image=self.next_icon, command=self.select_experiment)
        btn_select.grid(row=1, column=4, pady=25, padx=30, sticky=W)
        btn_select_ttp = CreateToolTip(btn_select, 'Access experiment')

        # Components for Experimental scenarios List form (list of experimental scenarios)
        lbl_sep3 = Label(self.frm_child_list)
        lbl_sep3.grid(row=1, column=0, padx=25, pady=25)
        lbl_scenario_desc = Label(self.frm_child_list, text=wrap_text('In this section you can configure the '
                                                                      'experimental scenarios associated with the '
                                                                      'experiment you have selected. Each scenario '
                                                                      'contains one or more design problems and extra '
                                                                      'information such as: designers groups and a '
                                                                      'description', 80), anchor=W)
        lbl_scenario_desc.config(font=SUBTITLE2_FONT, fg=TEXT_COLOR)
        lbl_scenario_desc.grid(row=0, column=1, pady=25)
        self.trv_available = Treeview(self.frm_child_list, height=15, columns=('Name', 'Description', 'Available?',
                                                                              'Locked?'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.heading('#3', text='Available?', anchor=CENTER)
        self.trv_available.heading('#4', text='Locked?', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.column('#3', width=75, minwidth=75, stretch=NO, anchor=CENTER)
        self.trv_available.column('#4', width=75, minwidth=75, stretch=NO, anchor=CENTER)
        self.trv_available.bind("<ButtonRelease-1>", self.refresh_crud_buttons)
        self.trv_available.bind("<Double-1>", self.switch_availability)
        self.trv_available.grid(row=1, column=1, rowspan=2, sticky=W, pady=25)
        vsb_trv_av = Scrollbar(self.frm_child_list, orient="vertical", command=self.trv_available.yview)
        vsb_trv_av.grid(row=1, column=2, rowspan=2, pady=25, sticky=NS)
        self.trv_available.configure(yscrollcommand=vsb_trv_av.set)
        lbl_note_available = Label(self.frm_child_list, text='NOTE: To switch between available and disabled '
                                                             '(for designers), double click on selected scenario\n')
        lbl_note_available.config(fg=TEXT_COLOR, font=NOTE_FONT)
        lbl_note_available.grid(row=3, column=1, columnspan=3, sticky=W)
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New experimental scenario')
        btn_view = Button(frm_aux4, image=self.view_icon, command=self.click_view)
        btn_view.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_view_ttp = CreateToolTip(btn_view, 'View experimental scenario')
        self.btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        self.btn_edit.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_edit_ttp = CreateToolTip(self.btn_edit, 'Edit experimental scenario')
        self.btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        self.btn_delete.grid(row=3, column=0, pady=5, padx=5, sticky=E)
        btn_delete_ttp = CreateToolTip(self.btn_delete, 'Delete experimental scenario')
        frm_aux5 = Frame(self.frm_child_list)
        btn_save_experiment = Button(frm_aux5, image=self.save_icon, command=self.click_save_experiment)
        btn_save_experiment.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_save_experiment_ttp = CreateToolTip(btn_save_experiment, 'Save experiment')
        btn_cancel_experiment = Button(frm_aux5, image=self.cancel_icon, command=self.click_cancel_experiment)
        btn_cancel_experiment.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_cancel_experiment_ttp = CreateToolTip(btn_cancel_experiment, 'Cancel')
        frm_aux4.grid(row=1, column=4, pady=25, padx=25, sticky=NW)
        frm_aux5.grid(row=2, column=4, pady=25, padx=25, sticky=SW)

        # Components for General info form, where each experimental scenario may be configured
        lbl_name = Label(self.frm_child_general, text='Name')
        lbl_name.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_description = Label(self.frm_child_general, text='Description')
        lbl_description.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_description.grid(pady=10, padx=50, sticky=NW)
        lbl_access = Label(self.frm_child_general, text='Access code')
        lbl_access.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_access.grid(row=6, column=0,pady=10, padx=50, sticky=W)
        lbl_cgroup = Label(self.frm_child_general, text='Control group')
        lbl_cgroup.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_cgroup.grid(row=7, column=0, pady=10, padx=50, sticky=W)
        lbl_egroup = Label(self.frm_child_general, text='Experimental group')
        lbl_egroup.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_egroup.grid(row=8, column=0, pady=10, padx=50, sticky=W)
        self.txt_name = Text(self.frm_child_general, height=1, width=80)
        self.txt_name.config(font=TEXT_FONT)
        self.txt_name.grid(row=0, column=1, padx=50, pady=10, columnspan=8)
        self.txt_description = Text(self.frm_child_general, height=5, width=80)
        self.txt_description.config(font=TEXT_FONT)
        self.txt_description.grid(row=1, column=1, padx=50, pady=10, columnspan=8, rowspan=5)
        self.txt_access_code = Text(self.frm_child_general, height=1, width=80)
        self.txt_access_code.config(font=TEXT_FONT)
        self.txt_access_code.grid(row=6, column=1, padx=50, pady=10, columnspan=8)
        self.cbx_cgroup = Combobox(self.frm_child_general, state="readonly", width=40)
        self.cbx_cgroup.config(font=TEXT_FONT)
        self.cbx_cgroup.grid(row=7, column=2, padx=50, pady=10, columnspan=8, sticky=W)
        self.cbx_egroup = Combobox(self.frm_child_general, state="readonly", width=40)
        self.cbx_egroup.config(font=TEXT_FONT)
        self.cbx_egroup.grid(row=8, column=2, padx=50, pady=10, columnspan=8, sticky=W)
        sep_general = Separator(self.frm_child_general, orient=HORIZONTAL)
        sep_general.grid(row=9, column=0, sticky=EW, columnspan=10, pady=10)
        lbl_general_components = Label(self.frm_child_general, text='Design problems')
        lbl_general_components.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_general_components.grid(row=12, column=0, pady=10, padx=50, sticky=W)
        lbl_sep5 = Label(self.frm_child_general)
        lbl_sep5.grid(row=12, column=1, padx=50, pady=10)
        self.trv_scenario_components = Treeview(self.frm_child_general, height=6, columns=('Problem',
                                                                                           'Control group patterns?',
                                                                                           'Expm. group patterns?'))
        self.trv_scenario_components.heading('#0', text='ID', anchor=CENTER)
        self.trv_scenario_components.heading('#1', text='Problem', anchor=CENTER)
        self.trv_scenario_components.heading('#2', text='Control group patterns?', anchor=CENTER)
        self.trv_scenario_components.heading('#3', text='Expm. group patterns?', anchor=CENTER)
        self.trv_scenario_components.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_scenario_components.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_scenario_components.column('#2', width=150, minwidth=150, stretch=NO, anchor=CENTER)
        self.trv_scenario_components.column('#3', width=150, minwidth=150, stretch=NO, anchor=CENTER)
        self.trv_scenario_components.grid(row=12, column=2, pady=10, rowspan=10, sticky=W)
        vsb_trv_sc = Scrollbar(self.frm_child_general, orient="vertical", command=self.trv_scenario_components.yview)
        vsb_trv_sc.grid(row=12, column=3, rowspan=10, pady=10, sticky=NS)
        self.trv_scenario_components.configure(yscrollcommand=vsb_trv_sc.set)
        lbl_sep6 = Label(self.frm_child_general)
        lbl_sep6.grid(row=12, column=4, padx=50, pady=10)
        self.btn_new_comp = Button(self.frm_child_general, image=self.new_icon, command=self.click_new_component)
        btn_new_comp_ttp = CreateToolTip(self.btn_new_comp, 'New component')
        self.btn_delete_comp = Button(self.frm_child_general, image=self.remove_icon, command=self.click_delete_component)
        btn_delete_comp_ttp = CreateToolTip(self.btn_delete_comp, 'Delete component')
        self.btn_view_comp = Button(self.frm_child_general, image=self.view_icon, command=self.click_view_component)
        btn_view_comp_ttp = CreateToolTip(self.btn_view_comp, 'View component')
        self.btn_save = Button(self.frm_child_general, image=self.save_icon, command=self.click_save_general)
        btn_save_ttp = CreateToolTip(self.btn_save, 'Save experimental scenario')
        self.btn_cancel = Button(self.frm_child_general, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel_ttp = CreateToolTip(self.btn_cancel, 'Cancel')
        self.btn_back_general = Button(self.frm_child_general, image=self.back_icon, command=self.click_back_general)
        btn_back_general_ttp = CreateToolTip(self.btn_back_general, 'Go back')

        # Components Problem configuration Top Level window (scenario components configuration)
        frm_aux2 = Frame(self.tlevel_problem)
        lbl_problem = Label(frm_aux2, text='Design Problem')
        lbl_problem.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_problem.grid(pady=10, padx=50, sticky=W)
        lbl_problem_desc = Label(frm_aux2, text='Description')
        lbl_problem_desc.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_problem_desc.grid(pady=10, padx=50, sticky=NW)
        self.cbx_problem = Combobox(frm_aux2, state="readonly", width=80)
        self.cbx_problem.config(font=TEXT_FONT)
        self.cbx_problem.bind("<<ComboboxSelected>>", self.cbx_problem_selected)
        self.cbx_problem.grid(row=0, column=1, padx=50, pady=10, sticky=W)
        self.txt_problem_desc = Text(frm_aux2, height=6, width=80)
        self.txt_problem_desc.config(font=TEXT_FONT, bg=defaultbg)
        self.txt_problem_desc.grid(row=1, column=1, padx=50, pady=10, rowspan=6)
        # Buttons of the Problem configuration Top Level window
        self.btn_save_scomp = Button(frm_aux2, image=self.save_icon, command=self.click_save_sc_component)
        btn_save_scomp_ttp = CreateToolTip(self.btn_save_scomp, 'Save')
        self.btn_cancel_scomp = Button(frm_aux2, image=self.cancel_icon, command=self.click_cancel_sc_component)
        btn_cancel_scomp_ttp = CreateToolTip(self.btn_cancel_scomp, 'Cancel')
        self.btn_back_scomp = Button(frm_aux2, image=self.back_icon, command=self.click_cancel_sc_component)
        btn_back_scomp_ttp = CreateToolTip(self.btn_back_scomp, 'Go back')
        frm_aux2.grid(row=0, column=0, pady=20, padx=10, columnspan=7, rowspan=5)
        # Components for adding patterns to the designers groups
        frm_aux3 = LabelFrame(self.tlevel_problem, text='Select available patterns for control group:')
        frm_aux3.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        frm_aux6 = LabelFrame(self.tlevel_problem, text='Select available patterns for experimental group:')
        frm_aux6.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_sep7 = Label(frm_aux3)
        lbl_sep7.grid(row=0, column=0, padx=10, pady=10)
        self.trv_available_patters_cgroup = Treeview(frm_aux3, height=10, columns='Patterns')
        self.trv_available_patters_cgroup.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_patters_cgroup.heading('#1', text='Patterns', anchor=CENTER)
        self.trv_available_patters_cgroup.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_available_patters_cgroup.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available_patters_cgroup.bind("<Button-1>", self.click_trv_apatters_cgroup)
        self.trv_available_patters_cgroup.grid(row=0, column=1, rowspan=10, pady=10, sticky=W)
        vsb_trv_avcg = Scrollbar(frm_aux3, orient="vertical", command=self.trv_available_patters_cgroup.yview)
        vsb_trv_avcg.grid(row=0, column=2, rowspan=10, pady=10, sticky=NS)
        self.trv_available_patters_cgroup.configure(yscrollcommand=vsb_trv_avcg.set)
        lbl_sep8 = Label(frm_aux3)
        lbl_sep8.grid(row=0, column=3, padx=10, pady=10)
        lbl_sep9 = Label(frm_aux3)
        lbl_sep9.grid(row=0, column=5, padx=10, pady=10)
        self.trv_selected_patterns_cgroup = Treeview(frm_aux3, height=10, columns=('Available patterns',))
        self.trv_selected_patterns_cgroup.heading('#0', text='ID', anchor=CENTER)
        self.trv_selected_patterns_cgroup.heading('#1', text='Available patterns', anchor=CENTER)
        self.trv_selected_patterns_cgroup.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_selected_patterns_cgroup.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_selected_patterns_cgroup.bind("<Button-1>", self.click_trv_spatters_cgroup)
        self.trv_selected_patterns_cgroup.grid(row=0, column=6, rowspan=10, pady=10, sticky=W)
        vsb_trv_selcg = Scrollbar(frm_aux3, orient="vertical", command=self.trv_selected_patterns_cgroup.yview)
        vsb_trv_selcg.grid(row=0, column=7, rowspan=10, pady=10, sticky=NS)
        self.trv_selected_patterns_cgroup.configure(yscrollcommand=vsb_trv_selcg.set)
        lbl_sep10 = Label(frm_aux3)
        lbl_sep10.grid(row=0, column=8, padx=10, pady=10)
        self.btn_add_cg = Button(frm_aux3, image=self.add_icon, command=self.click_add_cgroup)
        self.btn_add_cg.grid(row=3, column=4)
        btn_add_cg_ttp = CreateToolTip(self.btn_add_cg, 'Add pattern')
        self.btn_remove_cg = Button(frm_aux3, image=self.delete_icon, command=self.click_remove_cgroup)
        self.btn_remove_cg.grid(row=4, column=4)
        btn_remove_cg_ttp = CreateToolTip(self.btn_remove_cg, 'Remove pattern')
        frm_aux3.grid(row=5, column=0, pady=20, padx=10, rowspan=10)
        self.btn_copy_patterns = Button(self.tlevel_problem, image=self.copy_icon, command=self.click_copy_patterns)
        self.btn_copy_patterns.grid(row=10, column=1, padx=5)
        btn_copy_patterns_ttp = CreateToolTip(self.btn_copy_patterns, 'Copy patterns')
        lbl_sep11 = Label(frm_aux6)
        lbl_sep11.grid(row=0, column=0, padx=10, pady=10)
        self.trv_available_patters_egroup = Treeview(frm_aux6, height=10, columns='Patterns')
        self.trv_available_patters_egroup.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_patters_egroup.heading('#1', text='Patterns', anchor=CENTER)
        self.trv_available_patters_egroup.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_available_patters_egroup.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available_patters_egroup.bind("<Button-1>", self.click_trv_apatters_egroup)
        self.trv_available_patters_egroup.grid(row=0, column=1, rowspan=10, pady=10, sticky=W)
        vsb_trv_aveg = Scrollbar(frm_aux6, orient="vertical", command=self.trv_available_patters_egroup.yview)
        vsb_trv_aveg.grid(row=0, column=2, rowspan=10, pady=10, sticky=NS)
        self.trv_available_patters_egroup.configure(yscrollcommand=vsb_trv_aveg.set)
        lbl_sep12 = Label(frm_aux6)
        lbl_sep12.grid(row=0, column=3, padx=10, pady=10)
        lbl_sep13 = Label(frm_aux6)
        lbl_sep13.grid(row=0, column=5, padx=10, pady=10)
        self.trv_selected_patterns_egroup = Treeview(frm_aux6, height=10, columns=('Available patterns',))
        self.trv_selected_patterns_egroup.heading('#0', text='ID', anchor=CENTER)
        self.trv_selected_patterns_egroup.heading('#1', text='Available patterns', anchor=CENTER)
        self.trv_selected_patterns_egroup.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_selected_patterns_egroup.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_selected_patterns_egroup.bind("<Button-1>", self.click_trv_spatters_egroup)
        self.trv_selected_patterns_egroup.grid(row=0, column=6, rowspan=10, pady=10, sticky=W)
        vsb_trv_seleg = Scrollbar(frm_aux6, orient="vertical", command=self.trv_selected_patterns_egroup.yview)
        vsb_trv_seleg.grid(row=0, column=7, rowspan=10, pady=10, sticky=NS)
        self.trv_selected_patterns_egroup.configure(yscrollcommand=vsb_trv_seleg.set)
        lbl_sep14 = Label(frm_aux6)
        lbl_sep14.grid(row=0, column=8, padx=10, pady=10)
        self.btn_add_eg = Button(frm_aux6, image=self.add_icon, command=self.click_add_egroup)
        self.btn_add_eg.grid(row=3, column=4)
        btn_add_eg_ttp = CreateToolTip(self.btn_add_eg, 'Add pattern')
        self.btn_remove_eg = Button(frm_aux6, image=self.delete_icon, command=self.click_remove_egroup)
        self.btn_remove_eg.grid(row=4, column=4)
        btn_remove_eg_ttp = CreateToolTip(self.btn_remove_eg, 'Remove pattern')
        frm_aux6.grid(row=5, column=2, pady=20, padx=10, rowspan=10)

    def initialize_variables(self):
        """
        Method that set the local variables to its initial state (empty) and retrieve info from the database
        """
        # Retrieve available problems from the server
        self.problems = []
        self.directive = Message(action=52)
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.problems.append(Problem(id=int(elements[0]), name=elements[1], description=elements[2],
                                         id_solution=int(elements[3]), connection=self.connection))

        # Retrieve available patterns from the server
        self.patterns = Pattern.get_available_patterns(self.connection)
        # Retrieve available designers groups from the server
        self.designers_group = []
        self.directive = Message(action=27)
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.designers_group.append(DesignersGroup(id=int(elements[0]), name=elements[1], description=elements[2]))
        # Other important variables for internal use
        self.directive = Message()
        self.current_sc_comp = None
        self.scenario_components = []
        self.experimental_scenario = None

    def select_experiment(self, event=None):
        """
        This function is activated when the 'Click Experiments TreeView' event ocurrs, it indicates than an experiments
        has been selected
        """
        if self.trv_available_exp.item(self.trv_available_exp.selection())['text'] != '':
            self.id_selected_exp = int(self.trv_available_exp.item(self.trv_available_exp.selection())['text'])
            # Retrieve selected experiment and its 'Experimental scenarios'
            self.retrieve_list()
            self.frm_child_exp_list.grid_forget()
            if len(self.trv_available.get_children()) != 0:
                self.trv_available.selection_set(self.trv_available.get_children()[0])
                self.refresh_crud_buttons()
            self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_save_experiment(self):
        """
        Function activated when 'Save experiment' button is pressed, it saves availability of each exerimental scenario
        configured
        """
        index = 0
        for item in self.trv_available.get_children():
            aux_av = True if self.trv_available.item(item)['values'][2] == '✓' else False
            if self.current_availability[index] != aux_av:
                self.directive = Message(action=83, information=['change_availability',
                                                                 int(self.trv_available.item(item)['text']), aux_av])
                self.connection = self.directive.send_directive(self.connection)
            index += 1
        # Return to Experiments list home form
        self.click_cancel_experiment()

    def click_cancel_experiment(self):
        """
        Function activated when 'Cancel experiment' button is pressed, it hides the Experimental scenarios List form
        without saving any changes that may be done. It returns to Experiments list home form
        """
        self.frm_child_list.grid_forget()
        self.frm_child_exp_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def retrieve_experiments(self):
        """
        This function shows the existing 'Experiments' in the home TreeView
        """
        # Remove existing elements in the list
        for item in self.trv_available_exp.get_children():
            self.trv_available_exp.delete(item)
        self.directive = Message(action=92, information=[])
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available_exp.insert('', 'end', text=elements[0], values=(elements[1], wrap_text(elements[2], 72)))

    def retrieve_list(self):
        """
        This function shows the existing Experimental scenarios in an 'Experiment'
        """
        # Remove existing elements in the list
        self.current_availability = []  # Saves initial availability for experimental scenarios, so any change made later could be saved
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=82, information=[self.id_selected_exp])
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1], wrap_text(elements[2], 72),
                                                                           elements[3], elements[4]))
            aux = True if elements[3] == '✓' else False
            self.current_availability.append(aux)

    def show_frm(self):
        """
        Displays the home list of the 'Experiments' form
        """
        self.retrieve_experiments()
        if len(self.trv_available_exp.get_children()) != 0:
            self.trv_available_exp.selection_set(self.trv_available_exp.get_children()[0])
        self.frm_child_exp_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        """
        Hides all forms that are currently active
        """
        self.clear_fields()
        self.hide_buttons()
        self.frm_child_exp_list.grid_forget()
        self.frm_child_list.grid_forget()
        self.frm_child_general.grid_forget()

    def click_new(self):
        """
        Function activated when 'New' button is pressed, allows user to create a new experimetal scenario. Shows visual
        components for the creation of an experiment
        """
        self.decide = True
        self.initialize_variables()
        self.show_buttons_create_update()
        self.load_designers()
        self.frm_child_list.grid_forget()
        self.txt_name.focus_set()
        self.title_form = 'New'
        self.frm_child_general['text'] = self.title_form + ' experimental scenario'
        self.frm_child_general.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_view(self):
        """
        Function activated when 'View' experimental scenario button is pressed. It allows the user to view information
        of the selected experimental scenario, but can not make any changes. It also loads special buttons for this
        function (view button)
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.initialize_variables()  # Retrieve information to show in visual components
            #self.load_designers()
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            # Retrieve selected experimental scenario
            self.directive = Message(action=85, information=[self.id_selected])
            self.connection = self.directive.send_directive(self.connection)
            self.experimental_scenario = ExperimentalSC(id=self.id_selected,
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
            self.directive = Message(action=87, information=[self.id_selected, 1])
            self.connection = self.directive.send_directive(self.connection)
            for item in self.connection.message.information:
                elements = item.split('¥')
                self.scenario_components.append(
                    ScenarioComponent(id_DB=int(elements[0]), id_exp_scenario=int(elements[1]),
                                      id_problem=int(elements[2]), connection=self.connection))
            # Fill visual components with retrieved information
            self.txt_name.insert('1.0', self.experimental_scenario.name)
            self.txt_description.insert('1.0', wrap_text(self.experimental_scenario.description, 85))
            self.txt_access_code.insert('1.0', self.experimental_scenario.access_code)
            self.cbx_cgroup.set(self.experimental_scenario.control_group.name)
            self.cbx_egroup.set(self.experimental_scenario.experimental_group.name)
            for item in self.scenario_components:
                if len(item.id_patterns_cgroup) == 0 and len(item.id_patterns_egroup) == 0:
                    self.trv_scenario_components.insert('', 'end', text=item.id, values=(item.problem.name, '', ''))
                elif len(item.id_patterns_cgroup) != 0 and len(item.id_patterns_egroup) == 0:
                    self.trv_scenario_components.insert('', 'end', text=item.id, values=(item.problem.name, '✓', ''))
                elif len(item.id_patterns_cgroup) == 0 and len(item.id_patterns_egroup) != 0:
                    self.trv_scenario_components.insert('', 'end', text=item.id, values=(item.problem.name, '', '✓'))
                else:
                    self.trv_scenario_components.insert('', 'end', text=item.id, values=(item.problem.name, '✓', '✓'))
            self.frm_child_list.grid_forget()
            self.title_form = 'View'
            self.frm_child_general['text'] = self.title_form + ' experimental scenario'
            self.btn_view_comp.grid(row=12, column=5, padx=10)
            self.btn_back_general.grid(row=0, column=9, padx=20)
            self.btn_back_scomp.grid(row=0, column=9, padx=20)
            self.txt_name['state'] = DISABLED
            self.txt_description['state'] = DISABLED
            self.txt_access_code['state'] = DISABLED
            self.cbx_cgroup['state'] = DISABLED
            self.cbx_egroup['state'] = DISABLED
            self.btn_add_cg['state'] = DISABLED
            self.btn_add_eg['state'] = DISABLED
            self.btn_remove_cg['state'] = DISABLED
            self.btn_remove_eg['state'] = DISABLED
            self.btn_copy_patterns['state'] = DISABLED
            self.frm_child_general.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select an item')

    def click_update(self):
        """
        Function activated when 'Update' button is pressed, allows user to modify an existing experimental scenario.
        Shows visual components for the modification of an experimental scenario, fill visual components with current
        information
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.decide = False  # Important variable when saving, it indicates the 'Experimental scenario' is being modified
            self.initialize_variables()  # Retrieve information to show in visual components
            self.show_buttons_create_update()
            self.load_designers()
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            # Retrieve selected experimental scenario
            self.directive = Message(action=85, information=[self.id_selected])
            self.connection = self.directive.send_directive(self.connection)
            self.experimental_scenario = ExperimentalSC(id=self.id_selected, name=self.connection.message.information[0],
                                                        description=self.connection.message.information[1],
                                                        access_code=self.connection.message.information[2],
                                                        scenario_availability=self.connection.message.information[3],
                                                        scenario_lock=self.connection.message.information[4],
                                                        id_experiment=self.connection.message.information[5],
                                                        id_control_group=self.connection.message.information[6],
                                                        id_experimental_group=self.connection.message.information[7],
                                                        connection=self.connection)
            # Retrieve scenario components
            self.directive = Message(action=87, information=[self.id_selected, 1])
            self.connection = self.directive.send_directive(self.connection)
            for item in self.connection.message.information:
                elements = item.split('¥')
                self.scenario_components.append(ScenarioComponent(id_DB=int(elements[0]), id_exp_scenario=int(elements[1]),
                                                                  id_problem=int(elements[2]), connection=self.connection))
            # Fill visual components with retrieved information
            self.txt_name.insert('1.0', self.experimental_scenario.name)
            self.txt_description.insert('1.0', wrap_text(self.experimental_scenario.description, 85))
            self.txt_access_code.insert('1.0', self.experimental_scenario.access_code)
            self.cbx_cgroup.set(self.experimental_scenario.control_group.name)
            self.cbx_egroup.set(self.experimental_scenario.experimental_group.name)
            for item in self.scenario_components:
                if len(item.id_patterns_cgroup) == 0 and len(item.id_patterns_egroup) == 0:
                    self.trv_scenario_components.insert('', 'end', text=item.id, values=(item.problem.name, '', ''))
                elif len(item.id_patterns_cgroup) != 0 and len(item.id_patterns_egroup) == 0:
                    self.trv_scenario_components.insert('', 'end', text=item.id, values=(item.problem.name, '✓', ''))
                elif len(item.id_patterns_cgroup) == 0 and len(item.id_patterns_egroup) != 0:
                    self.trv_scenario_components.insert('', 'end', text=item.id, values=(item.problem.name, '', '✓'))
                else:
                    self.trv_scenario_components.insert('', 'end', text=item.id, values=(item.problem.name, '✓', '✓'))
            self.frm_child_list.grid_forget()
            self.txt_name.focus_set()
            self.title_form = 'Update'
            self.frm_child_general['text'] = self.title_form + ' experimental scenario'
            self.frm_child_general.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select an item')

    def click_delete(self):
        """
        Function activated when 'Delete' button is pressed, it removes an experimental scenario from the database
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            # MessageBox asking confirmation
            decision = messagebox.askyesno(parent=self.frm_child_list, title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
                self.directive = Message(action=84, information=[self.id_selected])
                self.connection = self.directive.send_directive(self.connection)
                self.retrieve_list()
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select an item')

    def show_buttons_create_update(self):
        """
        Shows button in forms when creating or updating an experimental scenario
        """
        self.btn_new_comp.grid(row=12, column=5, padx=10)
        self.btn_delete_comp.grid(row=13, column=5, padx=10)
        self.btn_save.grid(row=0, column=9, padx=20)
        self.btn_cancel.grid(row=1, column=9, padx=20)
        self.btn_save_scomp.grid(row=0, column=9, padx=20)
        self.btn_cancel_scomp.grid(row=1, column=9, padx=20)
        # Enable visual components
        self.trv_available_patters_cgroup.configure(selectmode='browse')
        self.trv_selected_patterns_cgroup.configure(selectmode='browse')
        self.trv_available_patters_egroup.configure(selectmode='browse')
        self.trv_selected_patterns_egroup.configure(selectmode='browse')

    def hide_buttons(self):
        """
        Hides all buttons in forms
        """
        self.btn_new_comp.grid_forget()
        self.btn_delete_comp.grid_forget()
        self.btn_view_comp.grid_forget()
        self.btn_save.grid_forget()
        self.btn_cancel.grid_forget()
        self.btn_back_general.grid_forget()
        self.btn_save_scomp.grid_forget()
        self.btn_cancel_scomp.grid_forget()
        self.btn_back_scomp.grid_forget()

    def click_back_general(self):
        """
        In 'General form' when user is viewing an experimental scenario, the back button returns GUI to 'List of
        experimental scenario form'. (Does not perform any change to info)
        """
        self.hide_frm()
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_view_component(self):
        """
        Function activated when 'View' scenario component button is pressed (Accesible in viewer role)
        """
        if self.trv_scenario_components.item(self.trv_scenario_components.selection())['text'] != '':
            id_selected = int(self.trv_scenario_components.item(self.trv_scenario_components.selection())['text'])
            for item in self.scenario_components:
                if item.id == id_selected:
                    self.current_sc_comp = item
                    break
            self.cbx_problem['state'] = NORMAL
            self.show_current_problem(self.current_sc_comp.problem)
            self.cbx_problem['state'] = DISABLED
            self.decide_component = False   # This variable indicates that the components is being viewed, so the patterns for scenario components are correctly loaded
            # Enable visual components to insert info
            self.load_patterns()
            # Disable visual components so the user cant make any change
            self.trv_available_patters_cgroup.configure(selectmode='none')
            self.trv_selected_patterns_cgroup.configure(selectmode='none')
            self.trv_available_patters_egroup.configure(selectmode='none')
            self.trv_selected_patterns_egroup.configure(selectmode='none')
            self.tlevel_problem.title(self.title_form + ' component')
            self.tlevel_problem.deiconify()
            self.tlevel_problem.grab_set()
        else:
            messagebox.showwarning(parent=self.frm_child_general, title='No selection',
                                   message='You must select an item')

    def click_save_general(self):
        validation_option = self.validate_general_frm() # Validate any problem with info inserted into visual components
        if validation_option == 0:
            exp_sc_aux = ExperimentalSC(name=self.txt_name.get('1.0', 'end-1c'),
                                        description=self.txt_description.get('1.0', 'end-1c'),
                                        access_code=self.txt_access_code.get('1.0', 'end-1c'),
                                        id_experiment=self.id_selected_exp,
                                        id_control_group=self.designers_group[int(self.cbx_cgroup.current())].id,
                                        id_experimental_group=self.designers_group[
                                            int(self.cbx_egroup.current())].id)
            if self.decide:
                # Create an experimental scenario
                self.directive = Message(action=81, information=[exp_sc_aux.name, exp_sc_aux.description,
                                                                 exp_sc_aux.access_code, exp_sc_aux.scenario_availability,
                                                                 exp_sc_aux.scenario_lock, exp_sc_aux.id_experiment,
                                                                 exp_sc_aux.id_control_group, exp_sc_aux.id_experimental_group])
                self.connection = self.directive.send_directive(self.connection)
                id_exp_sc = self.connection.message.information[0]
                # Create scenario components
                for item in self.scenario_components:
                    self.directive = Message(action=86, information=[id_exp_sc, item.id_problem, item.id_patterns_cgroup,
                                                                     item.id_patterns_egroup])
                    self.connection = self.directive.send_directive(self.connection)
            else:
                # Update selected experimental scenario
                self.directive = Message(action=83, information=[self.experimental_scenario.id,
                                                                 exp_sc_aux.name, exp_sc_aux.description,
                                                                 exp_sc_aux.access_code, exp_sc_aux.scenario_availability,
                                                                 exp_sc_aux.scenario_lock, exp_sc_aux.id_experiment,
                                                                 exp_sc_aux.id_control_group,
                                                                 exp_sc_aux.id_experimental_group])
                self.connection = self.directive.send_directive(self.connection)
                # Update existing scenario components and create new ones if added
                for item in self.scenario_components:
                    if item.id_DB == 0: # Create new scenario components
                        self.directive = Message(action=86,
                                                 information=[self.experimental_scenario.id, item.id_problem,
                                                              item.id_patterns_cgroup,
                                                              item.id_patterns_egroup])
                    elif item.id == 0:  # Delete scenario components
                        self.directive = Message(action=89, information=[item.id_DB])
                    else:   # Update existing scenario components
                        self.directive = Message(action=88,
                                                 information=[item.id_DB, item.id_problem,
                                                              item.id_patterns_cgroup,
                                                              item.id_patterns_egroup])
                    self.connection = self.directive.send_directive(self.connection)
            self.click_back_general()
        elif validation_option == 1:
            messagebox.showwarning(parent=self.frm_child_general, title='Missing information',
                                   message='There are mandatory fields that need to be filled!')
        elif validation_option == 2:
            messagebox.showwarning(parent=self.frm_child_general, title='Designers',
                                   message='Control group and experimental group cant be the same')
        elif validation_option == 3:
            messagebox.showwarning(parent=self.frm_child_general, title='Scenario components',
                                   message='You must insert at least one scenario component')
        else:
            messagebox.showwarning(parent=self.frm_child_general, title='Designers',
                                   message='At least one designer belongs to control and experimental group. Please '
                                           'check the selected groups')

    def click_cancel(self):
        """
        Function activated when 'Cancel' button is pressed in General form, it goes back to the 'Experimental scenarios'
        home page
        """
        decision = messagebox.askyesno(parent=self.frm_child_general, title='Cancel', message='Are you sure you want to cancel?')
        if decision:
            self.click_back_general()

    def click_new_component(self):
        if len(self.problems) > len(self.trv_scenario_components.get_children()):  # Validates if the design problems are all already configured or not
            self.decide_component = True
            self.load_problems()
            self.load_patterns()
            self.tlevel_problem.title(self.title_form + ' component')
            self.tlevel_problem.deiconify()
            self.tlevel_problem.grab_set()
        else:
            messagebox.showwarning(parent=self.frm_child_general, title='No design problems',
                                   message='All design problems are already configured within this scenario')

    def click_delete_component(self):
        if self.trv_scenario_components.item(self.trv_scenario_components.selection())['text'] != '':
            decision = messagebox.askyesno(parent=self.frm_child_general, title='Confirmation', message='Are you sure you want to delete the item?')
            if decision:
                id_selected = int(self.trv_scenario_components.item(self.trv_scenario_components.selection())['text'])
                for item in self.scenario_components:
                    if item.id == id_selected:
                        index = self.scenario_components.index(item)
                        break
                if not self.decide and item.id_DB != 0: # If editing an experimental scenario and removing existing sc comp
                    self.scenario_components[index].id = 0  # Mark scenario for removing from DB when when saving changes
                else:
                    self.scenario_components.remove(item)   # Remove sc component from local variable
                self.trv_scenario_components.delete(self.trv_scenario_components.selection())   # Remove sc component from TRV
        else:
            messagebox.showwarning(parent=self.frm_child_general, title='No selection', message='You must select an item')

    '''def click_edit_component(self):
        if self.trv_scenario_components.item(self.trv_scenario_components.selection())['text'] != '':
            id_selected = int(self.trv_scenario_components.item(self.trv_scenario_components.selection())['text'])
            for item in self.scenario_components:
                if item.id == id_selected:
                    self.current_sc_comp = item
                    break
            self.click_new_component('edit')
            self.show_current_problem(self.current_sc_comp.problem)
            self.cbx_problem['state'] = DISABLED
        else:
            messagebox.showwarning(parent=self.frm_child_general, title='No selection', message='You must select an item')'''

    def click_save_sc_component(self):
        validation_option = self.validate_problem_frm()  # Validate any issue associated with problem selection
        if validation_option == 0: # No issues
            if len(self.trv_selected_patterns_cgroup.get_children()) != 0 or len(
                    self.trv_selected_patterns_egroup.get_children()) != 0: # When at least one pattern is selected
                if self.decide_component:   # New component
                    scenario_component_aux = ScenarioComponent(id_problem=self.current_sc_comp.problem.id,
                                                               problem=self.current_sc_comp.problem)
                else:   # Edit component
                    scenario_component_aux = ScenarioComponent(id=self.current_sc_comp.id,
                                                               id_problem=self.current_sc_comp.problem.id,
                                                               id_DB=self.current_sc_comp.id_DB,
                                                               problem=self.current_sc_comp.problem)
                if len(self.trv_selected_patterns_cgroup.get_children()) != 0:  # If patterns selected for control group
                    for item in self.trv_selected_patterns_cgroup.get_children():
                        scenario_component_aux.id_patterns_cgroup.append(
                            self.trv_selected_patterns_cgroup.item(item)['text'])
                if len(self.trv_selected_patterns_egroup.get_children()) != 0:  # If patterns selected for experimental group
                    for item in self.trv_selected_patterns_egroup.get_children():
                        scenario_component_aux.id_patterns_egroup.append(
                            self.trv_selected_patterns_egroup.item(item)['text'])
                if self.decide_component:
                    self.scenario_components.append(scenario_component_aux)
                    if len(self.trv_selected_patterns_cgroup.get_children()) != 0 and len(
                    self.trv_selected_patterns_egroup.get_children()) != 0:
                        self.trv_scenario_components.insert('', 'end', text=scenario_component_aux.id,
                                                            values=(self.current_sc_comp.problem.name, '✓', '✓'))
                    elif len(self.trv_selected_patterns_cgroup.get_children()) != 0 and len(
                    self.trv_selected_patterns_egroup.get_children()) == 0:
                        self.trv_scenario_components.insert('', 'end', text=scenario_component_aux.id,
                                                            values=(self.current_sc_comp.problem.name, '✓', ''))
                    else:
                        self.trv_scenario_components.insert('', 'end', text=scenario_component_aux.id,
                                                            values=(self.current_sc_comp.problem.name, '', '✓'))
                else:
                    for item in self.scenario_components:
                        if item.id == self.current_sc_comp.id:
                            index = self.scenario_components.index(item)
                            break
                    self.scenario_components[index] = scenario_component_aux
                self.current_sc_comp = None
                self.tlevel_problem.grab_release()
                self.tlevel_problem.withdraw()
            else:
                decision = messagebox.askyesno(parent=self.tlevel_problem, title='No patterns',
                                               message='No patterns selected for any group. Do you want to continue?')
                # Saving an scenario component without associated patterns
                if decision:
                    if self.decide_component:
                        scenario_component_aux = ScenarioComponent(id_problem=self.current_sc_comp.problem.id,
                                                                   problem=self.current_sc_comp.problem)
                        self.trv_scenario_components.insert('', 'end', text=scenario_component_aux.id,
                                                            values=(self.current_sc_comp.problem.name, '', ''))
                        self.scenario_components.append(scenario_component_aux)
                    self.current_sc_comp = None
                    self.tlevel_problem.grab_release()
                    self.tlevel_problem.withdraw()
        elif validation_option == 1:
            messagebox.showwarning(parent=self.tlevel_problem, title='Missing information',
                                   message='You must select a problem!')
        else:
            messagebox.showwarning(parent=self.tlevel_problem, title='Repeated problem',
                                   message='The selected problem has been already chosen')

    def click_cancel_sc_component(self):
        self.current_sc_comp = None
        self.tlevel_problem.grab_release()
        self.tlevel_problem.withdraw()

    def click_trv_apatters_cgroup(self, event):
        self.trv_selected_patterns_cgroup.selection_remove(self.trv_selected_patterns_cgroup.selection())

    def click_trv_spatters_cgroup(self, event):
        self.trv_available_patters_cgroup.selection_remove(self.trv_available_patters_cgroup.selection())

    def click_add_cgroup(self):
        if self.trv_available_patters_cgroup.item(self.trv_available_patters_cgroup.selection())['text'] != '' and \
                self.trv_selected_patterns_cgroup.item(self.trv_selected_patterns_cgroup.selection())['text'] == '':
            self.trv_selected_patterns_cgroup.insert('', 'end', text=self.trv_available_patters_cgroup.item(
                self.trv_available_patters_cgroup.focus())['text'], values=self.trv_available_patters_cgroup.item(
                self.trv_available_patters_cgroup.focus())['values'])
            self.trv_available_patters_cgroup.delete(self.trv_available_patters_cgroup.selection())

    def click_remove_cgroup(self):
        if self.trv_selected_patterns_cgroup.item(self.trv_selected_patterns_cgroup.selection())['text'] != '' and \
                self.trv_available_patters_cgroup.item(self.trv_available_patters_cgroup.selection())['text'] == '':
            self.trv_available_patters_cgroup.insert('', 'end', text=self.trv_selected_patterns_cgroup.item(
                self.trv_selected_patterns_cgroup.focus())['text'], values=self.trv_selected_patterns_cgroup.item(
                self.trv_selected_patterns_cgroup.focus())['values'])
            self.trv_selected_patterns_cgroup.delete(self.trv_selected_patterns_cgroup.selection())

    def click_trv_apatters_egroup(self, event):
        self.trv_selected_patterns_egroup.selection_remove(self.trv_selected_patterns_egroup.selection())

    def click_trv_spatters_egroup(self, event):
        self.trv_available_patters_egroup.selection_remove(self.trv_available_patters_egroup.selection())

    def click_add_egroup(self):
        if self.trv_available_patters_egroup.item(self.trv_available_patters_egroup.selection())['text'] != '' and \
                self.trv_selected_patterns_egroup.item(self.trv_selected_patterns_egroup.selection())['text'] == '':
            self.trv_selected_patterns_egroup.insert('', 'end', text=self.trv_available_patters_egroup.item(
                self.trv_available_patters_egroup.focus())['text'], values=self.trv_available_patters_egroup.item(
                self.trv_available_patters_egroup.focus())['values'])
            self.trv_available_patters_egroup.delete(self.trv_available_patters_egroup.selection())

    def click_remove_egroup(self):
        if self.trv_selected_patterns_egroup.item(self.trv_selected_patterns_egroup.selection())['text'] != '' and \
                self.trv_available_patters_egroup.item(self.trv_available_patters_egroup.selection())['text'] == '':
            self.trv_available_patters_egroup.insert('', 'end', text=self.trv_selected_patterns_egroup.item(
                self.trv_selected_patterns_egroup.focus())['text'], values=self.trv_selected_patterns_egroup.item(
                self.trv_selected_patterns_egroup.focus())['values'])
            self.trv_selected_patterns_egroup.delete(self.trv_selected_patterns_egroup.selection())

    def validate_general_frm(self):
        if len(self.txt_name.get('1.0','end-1c')) !=0 and len(self.txt_description.get('1.0','end-1c')) !=0 and \
                len(self.txt_access_code.get('1.0','end-1c')) != 0 and len(self.cbx_cgroup.get()) != 0 and len(self.cbx_egroup.get()) != 0:
            if self.cbx_egroup.get() != self.cbx_cgroup.get():
                if len(self.trv_scenario_components.get_children()) != 0:
                    if self.validate_repeated_designers():
                        return 0
                    else:
                        return 4
                else:
                    return 3
            else:
                return 2
        else:
            return 1

    def validate_problem_frm(self):
        if self.decide_component:
            if len(self.cbx_problem.get()) == 0:
                return 1
            if self.current_sc_comp.problem is not None:
                repeated_problem = 0
                for item in self.scenario_components:
                    # Validate repetition of the problem in the sc components of the list
                    if item.id_problem == self.current_sc_comp.problem.id and item.id != 0:  # If sc comp existing in DB and was deleted
                        repeated_problem += 1
                if repeated_problem == 0:
                    return 0
                else:
                    return 2
            else:
                return 1
        else:
            return 0

    def validate_repeated_designers(self):
        self.directive = Message(action=30, information=[self.designers_group[int(self.cbx_cgroup.current())].id])
        self.connection = self.directive.send_directive(self.connection)
        control_group = self.connection.message.information[2]
        self.directive = Message(action=30, information=[self.designers_group[int(self.cbx_egroup.current())].id])
        self.connection = self.directive.send_directive(self.connection)
        experimental_group = self.connection.message.information[2]
        for item in control_group:
            if item in experimental_group:  # If designer (control group) belongs to experimental group
                return False
        return True     # Any designer belongs to both groups simultaneously

    def load_problems(self):
        # Clear fields associated with the 'problem'
        self.cbx_problem['state'] = NORMAL
        self.txt_problem_desc['state'] = NORMAL
        self.txt_problem_desc.delete('1.0', 'end-1c')
        self.txt_problem_desc['state'] = DISABLED
        self.cbx_problem['values'] = []
        self.cbx_problem.set('')
        # Load comboboxes with available problems
        for item in self.problems:
            self.cbx_problem['values'] += (item.name,)

    def load_designers(self):
        # Clear designers groups comboboxes
        self.cbx_cgroup['values'] = []
        self.cbx_egroup['values'] = []
        # Load comboboex with designers groups info
        for item in self.designers_group:
            self.cbx_cgroup['values'] += (item.name,)
            self.cbx_egroup['values'] += (item.name,)

    def load_patterns(self):
        # Remove existing elements (available patterns)
        for item in self.trv_available_patters_egroup.get_children():
            self.trv_available_patters_egroup.delete(item)
        for item in self.trv_available_patters_cgroup.get_children():
            self.trv_available_patters_cgroup.delete(item)
        # Remove existing elements (selected patterns)
        for item in self.trv_selected_patterns_egroup.get_children():
            self.trv_selected_patterns_egroup.delete(item)
        for item in self.trv_selected_patterns_cgroup.get_children():
            self.trv_selected_patterns_cgroup.delete(item)
        # Adding elements in the list depending if the component is new or being modified
        if not self.decide_component:   # This is executed when an scenario component is being edited
            a_patterns_cgroup = self.patterns[:]
            a_patterns_egroup = self.patterns[:]
            s_patterns_cgroup = self.current_sc_comp.id_patterns_cgroup
            selected_patterns_cg = []
            s_patterns_egroup = self.current_sc_comp.id_patterns_egroup
            selected_patterns_eg = []
            # Compare and distribute patterns correctly in control group
            for identity in s_patterns_cgroup:
                for item in a_patterns_cgroup:
                    if identity == item.id:
                        selected_patterns_cg.append(item)
                        a_patterns_cgroup.remove(item)
            # Compare and distribute patterns correctly in experimental group
            for identity in s_patterns_egroup:
                for item in a_patterns_egroup:
                    if identity == item.id:
                        selected_patterns_eg.append(item)
                        a_patterns_egroup.remove(item)
            # Fill TVs with the results from the comparation
            for item in a_patterns_cgroup:
                content = item.get_content_name()
                self.trv_available_patters_cgroup.insert('', 'end', text=item.id, values=(content,))
            for item in selected_patterns_cg:
                content = item.get_content_name()
                self.trv_selected_patterns_cgroup.insert('', 'end', text=item.id, values=(content,))
            for item in a_patterns_egroup:
                content = item.get_content_name()
                self.trv_available_patters_egroup.insert('', 'end', text=item.id, values=(content,))
            for item in selected_patterns_eg:
                content = item.get_content_name()
                self.trv_selected_patterns_egroup.insert('', 'end', text=item.id, values=(content,))
        else:
            for item in self.patterns:
                content = item.get_content_name()
                self.trv_available_patters_cgroup.insert('', 'end', text=item.id, values=(content,))
                self.trv_available_patters_egroup.insert('', 'end', text=item.id, values=(content,))

    def cbx_problem_selected(self, event):
        self.current_sc_comp = ScenarioComponent(id=100)
        self.current_sc_comp.problem = self.problems[int(self.cbx_problem.current())]
        self.show_current_problem(self.current_sc_comp.problem)

    def show_current_problem(self, problem):
        self.cbx_problem.set(problem.name)
        # Insert description of the current problem into visual component
        self.txt_problem_desc['state'] = NORMAL
        self.txt_problem_desc.delete('1.0', 'end-1c')
        self.txt_problem_desc.insert('1.0', wrap_text(problem.description, 85))
        self.txt_problem_desc['state'] = DISABLED

    def clear_fields(self):
        self.btn_add_cg['state'] = NORMAL
        self.btn_add_eg['state'] = NORMAL
        self.btn_remove_cg['state'] = NORMAL
        self.btn_remove_eg['state'] = NORMAL
        self.btn_copy_patterns['state'] = NORMAL
        self.txt_name['state'] = NORMAL
        self.txt_description['state'] = NORMAL
        self.txt_access_code['state'] = NORMAL
        self.cbx_cgroup['state'] = NORMAL
        self.cbx_egroup['state'] = NORMAL
        self.txt_name.delete('1.0', 'end-1c')
        self.txt_description.delete('1.0', 'end-1c')
        self.txt_access_code.delete('1.0', 'end-1c')
        self.cbx_cgroup.set('')
        self.cbx_egroup.set('')
        self.cbx_problem.set('')
        for item in self.trv_scenario_components.get_children():
            self.trv_scenario_components.delete(item)

    def click_copy_patterns(self):
        if len(self.trv_selected_patterns_cgroup.get_children()) != 0 and len(
                self.trv_selected_patterns_egroup.get_children()) == 0:
            for child in self.trv_selected_patterns_cgroup.get_children():
                self.trv_selected_patterns_egroup.insert('', 'end', text=self.trv_selected_patterns_cgroup.item(child)['text'], values=self.trv_selected_patterns_cgroup.item(child)['values'])
                for object in self.trv_available_patters_egroup.get_children():
                    if self.trv_selected_patterns_cgroup.item(child)['text'] == self.trv_available_patters_egroup.item(object)['text']:
                        self.trv_available_patters_egroup.delete(object)
                        break

    def refresh_crud_buttons(self, event=None):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            values = self.trv_available.item(
                self.trv_available.selection())['values']
            if values[3] == '':
                self.btn_edit['state'] = NORMAL
                self.btn_delete['state'] = NORMAL
            else:
                self.btn_edit['state'] = DISABLED
                self.btn_delete['state'] = DISABLED

    def switch_availability(self, event):
        """
        This function is activated when the 'Double click Experimental scenarios TreeView' event ocurrs, it switches the
        availability if an experimental scenario
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            values = self.trv_available.item(
                self.trv_available.focus())['values']
            if values[3] == '':
                if values[2] == '':
                    self.trv_available.item(self.trv_available.focus(), values=(values[0], values[1], '✓', values[3]))
                else:
                    self.trv_available.item(self.trv_available.focus(), values=(values[0], values[1], '', values[3]))
            else:
                messagebox.showwarning(parent=self.frm_child_list, title='Locked scenario',
                                       message='The selected scenario can not be disabled because it is locked')