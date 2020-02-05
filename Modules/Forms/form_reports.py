from tkinter import Label, LabelFrame, Frame, Text, Button, messagebox, PhotoImage, Toplevel, Scrollbar, Canvas
from tkinter.constants import *
from tkinter.ttk import Treeview, Combobox, Separator
from Modules.Config.Data import Message, Experiment, CreateToolTip, Problem, Pattern, ExperimentalSC, File, \
    summarize_text
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
        self.trv_detail_sc = Treeview(self.frm_child_report, height=8, columns=('N', 'Scenario', 'M1', 'M2', 'M3', 'M4'))
        self.trv_detail_sc.heading('#0', text='ID', anchor=CENTER)
        self.trv_detail_sc.heading('#1', text='N', anchor=CENTER)
        self.trv_detail_sc.heading('#2', text='Scenario', anchor=CENTER)
        self.trv_detail_sc.heading('#3', text='M1', anchor=CENTER)
        self.trv_detail_sc.heading('#4', text='M2', anchor=CENTER)
        self.trv_detail_sc.heading('#5', text='M3', anchor=CENTER)
        self.trv_detail_sc.heading('#6', text='M4', anchor=CENTER)
        self.trv_detail_sc.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_detail_sc.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_detail_sc.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_detail_sc.column('#3', width=40, minwidth=40, stretch=NO)
        self.trv_detail_sc.column('#4', width=40, minwidth=40, stretch=NO)
        self.trv_detail_sc.column('#5', width=40, minwidth=40, stretch=NO)
        self.trv_detail_sc.column('#6', width=40, minwidth=40, stretch=NO)
        self.trv_detail_sc.grid(row=0, column=6, rowspan=2, sticky=W, pady=10)
        vsb_trv_detsc = Scrollbar(self.frm_child_report, orient="vertical", command=self.trv_detail_sc.yview)
        vsb_trv_detsc.grid(row=0, column=7, rowspan=2, pady=10, sticky=NS)
        self.trv_detail_sc.configure(yscrollcommand=vsb_trv_detsc.set)
        self.trv_detail_prob = Treeview(self.frm_child_report, height=8, columns=('N', 'Problem', 'M1', 'M2', 'M3', 'M4'))
        self.trv_detail_prob.heading('#0', text='ID', anchor=CENTER)
        self.trv_detail_prob.heading('#1', text='N', anchor=CENTER)
        self.trv_detail_prob.heading('#2', text='Problem', anchor=CENTER)
        self.trv_detail_prob.heading('#3', text='M1', anchor=CENTER)
        self.trv_detail_prob.heading('#4', text='M2', anchor=CENTER)
        self.trv_detail_prob.heading('#5', text='M3', anchor=CENTER)
        self.trv_detail_prob.heading('#6', text='M4', anchor=CENTER)
        self.trv_detail_prob.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_detail_prob.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_detail_prob.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_detail_prob.column('#3', width=40, minwidth=40, stretch=NO)
        self.trv_detail_prob.column('#4', width=40, minwidth=40, stretch=NO)
        self.trv_detail_prob.column('#5', width=40, minwidth=40, stretch=NO)
        self.trv_detail_prob.column('#6', width=40, minwidth=40, stretch=NO)
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
        self.trv_detail_designer.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_detail_designer.column('#3', width=40, minwidth=40, stretch=NO)
        self.trv_detail_designer.column('#4', width=40, minwidth=40, stretch=NO)
        self.trv_detail_designer.column('#5', width=40, minwidth=40, stretch=NO)
        self.trv_detail_designer.column('#6', width=40, minwidth=40, stretch=NO)
        self.trv_detail_designer.bind("<Double-1>", self.view_detailed_solution)
        self.trv_detail_designer.grid(row=4, column=6, rowspan=2, sticky=W, pady=10)
        vsb_trv_detdesig = Scrollbar(self.frm_child_report, orient="vertical", command=self.trv_detail_designer.yview)
        vsb_trv_detdesig.grid(row=4, column=7, rowspan=2, pady=10, sticky=NS)
        self.trv_detail_designer.configure(yscrollcommand=vsb_trv_detdesig.set)
        lbl_notes = Label(self.frm_child_report, text='NOTE:\tDouble click on a designer to see\n\this solution for a '
                                                      'problem.\n')
        lbl_notes.config(fg=TEXT_COLOR, font=LABEL_FONT, justify=LEFT)
        lbl_notes.grid(row=6, column=6, pady=10, sticky=W)
        lbl_sep2 = Label(self.frm_child_report)
        lbl_sep2.grid(row=0, column=8, padx=10, pady=10, rowspan=7)

        '''lbl_details_exp = Label(self.frm_child_exp_list, text='Details', anchor=W)
        lbl_details_exp.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_details_exp.grid(row=0, column=6, pady=10, columnspan=4, sticky=W)
        lbl_name_exp = Label(self.frm_child_exp_list, text='Name', anchor=W)
        lbl_name_exp.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name_exp.grid(row=1, column=6, pady=10, sticky=W)
        lbl_desc_exp = Label(self.frm_child_exp_list, text='Description', anchor=W)
        lbl_desc_exp.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_desc_exp.grid(row=2, column=6, pady=10, sticky=NW)
        lbl_dtype_exp = Label(self.frm_child_exp_list, text='Design type', anchor=W)
        lbl_dtype_exp.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_dtype_exp.grid(row=3, column=6, pady=10, sticky=W)
        lbl_creation_date_exp = Label(self.frm_child_exp_list, text='Creation date', anchor=W)
        lbl_creation_date_exp.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_creation_date_exp.grid(row=4, column=6, pady=10, sticky=W)
        lbl_exec_date_exp = Label(self.frm_child_exp_list, text='Execution date', anchor=W)
        lbl_exec_date_exp.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_exec_date_exp.grid(row=5, column=6, pady=10, sticky=W)
        lbl_finish_date_exp = Label(self.frm_child_exp_list, text='Finish date', anchor=W)
        lbl_finish_date_exp.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_finish_date_exp.grid(row=6, column=6, pady=10, sticky=W)
        lbl_sep3 = Label(self.frm_child_exp_list)
        lbl_sep3.grid(row=1, column=7, padx=10, pady=10, rowspan=6)
        self.txt_name_exp = Text(self.frm_child_exp_list, height=1, width=30)
        self.txt_name_exp.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_name_exp.grid(row=1, column=8, pady=10, sticky=W)
        self.txt_desc_exp = Text(self.frm_child_exp_list, height=5, width=30)
        self.txt_desc_exp.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_desc_exp.grid(row=2, column=8, pady=10, sticky=W)
        vsb_txt_desc_exp = Scrollbar(self.frm_child_exp_list, orient="vertical", command=self.txt_desc_exp.yview)
        vsb_txt_desc_exp.grid(row=2, column=9, pady=10, sticky=NS)
        self.txt_desc_exp.configure(yscrollcommand=vsb_txt_desc_exp.set)
        self.txt_dtype_exp = Text(self.frm_child_exp_list, height=1, width=30)
        self.txt_dtype_exp.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_dtype_exp.grid(row=3, column=8, pady=10, sticky=W)
        self.txt_creation_date_exp = Text(self.frm_child_exp_list, height=1, width=30)
        self.txt_creation_date_exp.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_creation_date_exp.grid(row=4, column=8, pady=10, sticky=W)
        self.txt_exec_date_exp = Text(self.frm_child_exp_list, height=1, width=30)
        self.txt_exec_date_exp.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_exec_date_exp.grid(row=5, column=8, pady=10, sticky=W)
        self.txt_finish_date_exp = Text(self.frm_child_exp_list, height=1, width=30)
        self.txt_finish_date_exp.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_finish_date_exp.grid(row=6, column=8, pady=10, sticky=W)
        lbl_sep4 = Label(self.frm_child_exp_list)
        lbl_sep4.grid(row=0, column=10, padx=10, pady=10, rowspan=7)
        lbl_sep5 = Label(self.frm_child_exp_list)
        lbl_sep5.grid(row=7, column=0, padx=10, pady=10, columnspan=4)

        # Components for Experimental scenarios List form (list of experimental scenarios)
        lbl_sep6 = Label(self.frm_child_sc_list)
        lbl_sep6.grid(row=0, column=0, padx=10, pady=10, rowspan=4)
        lbl_available_sc_list = Label(self.frm_child_sc_list, text='Experimental scenarios', anchor=W)
        lbl_available_sc_list.config(font=SUBTITLE2_FONT, fg=TEXT_COLOR)
        lbl_available_sc_list.grid(row=0, column=1, pady=10, columnspan=2, sticky=W)
        self.trv_available_sc = Treeview(self.frm_child_sc_list, height=14, columns='Title')
        self.trv_available_sc.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_sc.heading('#1', text='Title', anchor=CENTER)
        self.trv_available_sc.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_sc.column('#1', width=400, minwidth=400, stretch=NO)
        self.trv_available_sc.bind("<ButtonRelease-1>", self.select_scenario)
        self.trv_available_sc.grid(row=1, column=1, rowspan=4, sticky=W, pady=10)
        vsb_trv_avsc = Scrollbar(self.frm_child_sc_list, orient="vertical", command=self.trv_available_sc.yview)
        vsb_trv_avsc.grid(row=1, column=2, rowspan=4, pady=10, sticky=NS)
        self.trv_available_sc.configure(yscrollcommand=vsb_trv_avsc.set)
        btn_select_sc = Button(self.frm_child_sc_list, image=self.view_icon, command=self.click_view_scenario)
        btn_select_sc.grid(row=1, column=3, pady=10, padx=30, sticky=W)
        btn_select_sc_ttp = CreateToolTip(btn_select_sc, 'View scenario report')
        btn_back_sc = Button(self.frm_child_sc_list, image=self.back_icon, command=self.click_back_scenario)
        btn_back_sc.grid(row=2, column=3, padx=30, sticky=NW)
        btn_back_sc_ttp = CreateToolTip(btn_back_sc, 'Go back')
        sep_aux2 = Separator(self.frm_child_sc_list, orient=VERTICAL)
        sep_aux2.grid(row=0, column=4, sticky=NS, rowspan=6)
        lbl_sep7 = Label(self.frm_child_sc_list)
        lbl_sep7.grid(row=0, column=5, padx=10, pady=10, rowspan=5)
        lbl_details_sc = Label(self.frm_child_sc_list, text='Details', anchor=W)
        lbl_details_sc.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_details_sc.grid(row=0, column=6, pady=10, columnspan=5, sticky=W)
        lbl_name_sc = Label(self.frm_child_sc_list, text='Title', anchor=W)
        lbl_name_sc.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name_sc.grid(row=1, column=6, pady=10, sticky=W)
        lbl_desc_sc = Label(self.frm_child_sc_list, text='Description', anchor=W)
        lbl_desc_sc.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_desc_sc.grid(row=2, column=6, pady=10, sticky=NW)
        lbl_sep8 = Label(self.frm_child_sc_list)
        lbl_sep8.grid(row=1, column=7, padx=10, pady=10, rowspan=2)
        self.txt_name_sc = Text(self.frm_child_sc_list, height=1, width=45)
        self.txt_name_sc.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_name_sc.grid(row=1, column=8, pady=10, sticky=W)
        self.txt_desc_sc = Text(self.frm_child_sc_list, height=5, width=45)
        self.txt_desc_sc.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_desc_sc.grid(row=2, column=8, pady=10, sticky=W)
        vsb_txt_desc_sc = Scrollbar(self.frm_child_sc_list, orient="vertical", command=self.txt_desc_sc.yview)
        vsb_txt_desc_sc.grid(row=2, column=9, pady=10, sticky=NS)
        self.txt_desc_sc.configure(yscrollcommand=vsb_txt_desc_sc.set)
        lbl_sep16 = Label(self.frm_child_sc_list)
        lbl_sep16.grid(row=1, column=10, pady=10, padx=45, sticky=NW)
        self.btn_view_dsc_diagram = Button(self.frm_child_sc_list, image=self.view_icon, command=self.click_view_desc_diagram)
        btn_view_dsc_diagram_ttp = CreateToolTip(self.btn_view_dsc_diagram, 'View description diagram')
        frm_aux1 = LabelFrame(self.frm_child_sc_list, text='Experimental group')
        frm_aux1.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_sep9 = Label(frm_aux1)
        lbl_sep9.grid(row=0, column=0, padx=10, pady=10, rowspan=3)
        lbl_design_exec_sc_egroup = Label(frm_aux1, text='Designers executed scenario', anchor=W)
        lbl_design_exec_sc_egroup.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_design_exec_sc_egroup.grid(row=0, column=1, pady=10, sticky=W)
        lbl_design_no_exec_sc_egroup = Label(frm_aux1, text='Designers did not execute scenario', anchor=W)
        lbl_design_no_exec_sc_egroup.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_design_no_exec_sc_egroup.grid(row=1, column=1, pady=10, sticky=W)
        lbl_given_patt_sc_egroup = Label(frm_aux1, text='Given patterns', anchor=W)
        lbl_given_patt_sc_egroup.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_given_patt_sc_egroup.grid(row=2, column=1, pady=10, sticky=W)
        lbl_sep10 = Label(frm_aux1)
        lbl_sep10.grid(row=0, column=2, padx=10, pady=10, rowspan=3)
        self.txt_design_exec_sc_egroup = Text(frm_aux1, height=1, width=15)
        self.txt_design_exec_sc_egroup.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_design_exec_sc_egroup.grid(row=0, column=3, pady=10, sticky=W)
        self.txt_design_no_exec_sc_egroup = Text(frm_aux1, height=1, width=15)
        self.txt_design_no_exec_sc_egroup.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_design_no_exec_sc_egroup.grid(row=1, column=3, pady=10, sticky=W)
        self.txt_given_patt_sc_egroup = Text(frm_aux1, height=1, width=15)
        self.txt_given_patt_sc_egroup.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_given_patt_sc_egroup.grid(row=2, column=3, pady=10, sticky=W)
        lbl_sep11 = Label(frm_aux1)
        lbl_sep11.grid(row=0, column=4, padx=10, pady=10, rowspan=3)
        btn_det_egroup_sc = Button(frm_aux1, text='View >>\ndetails', command=self.click_details_egroup)
        btn_det_egroup_sc.grid(row=0, column=5, padx=30, pady=10, rowspan=3)
        frm_aux1.grid(row=3, column=6, columnspan=5)
        self.frm_aux2 = LabelFrame(self.frm_child_sc_list, text='Control group')
        self.frm_aux2.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_sep12 = Label(self.frm_aux2)
        lbl_sep12.grid(row=0, column=0, padx=10, pady=10, rowspan=3)
        lbl_design_exec_sc_cgroup = Label(self.frm_aux2, text='Designers executed scenario', anchor=W)
        lbl_design_exec_sc_cgroup.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_design_exec_sc_cgroup.grid(row=0, column=1, pady=10, sticky=W)
        lbl_design_no_exec_sc_cgroup = Label(self.frm_aux2, text='Designers did not execute scenario', anchor=W)
        lbl_design_no_exec_sc_cgroup.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_design_no_exec_sc_cgroup.grid(row=1, column=1, pady=10, sticky=W)
        lbl_given_patt_sc_cgroup = Label(self.frm_aux2, text='Given patterns', anchor=W)
        lbl_given_patt_sc_cgroup.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_given_patt_sc_cgroup.grid(row=2, column=1, pady=10, sticky=W)
        lbl_sep13 = Label(self.frm_aux2)
        lbl_sep13.grid(row=0, column=2, padx=10, pady=10, rowspan=3)
        self.txt_design_exec_sc_cgroup = Text(self.frm_aux2, height=1, width=15)
        self.txt_design_exec_sc_cgroup.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_design_exec_sc_cgroup.grid(row=0, column=3, pady=10, sticky=W)
        self.txt_design_no_exec_sc_cgroup = Text(self.frm_aux2, height=1, width=15)
        self.txt_design_no_exec_sc_cgroup.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_design_no_exec_sc_cgroup.grid(row=1, column=3, pady=10, sticky=W)
        self.txt_given_patt_sc_cgroup = Text(self.frm_aux2, height=1, width=15)
        self.txt_given_patt_sc_cgroup.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_given_patt_sc_cgroup.grid(row=2, column=3, pady=10, sticky=W)
        lbl_sep13 = Label(self.frm_aux2)
        lbl_sep13.grid(row=0, column=4, padx=10, pady=10, rowspan=3)
        btn_det_cgroup_sc = Button(self.frm_aux2, text='View >>\ndetails', command=self.click_details_cgroup)
        btn_det_cgroup_sc.grid(row=0, column=5, padx=30, pady=10, rowspan=3)
        lbl_sep14 = Label(self.frm_child_sc_list)
        lbl_sep14.grid(row=0, column=11, padx=10, pady=10, rowspan=5)
        lbl_sep15 = Label(self.frm_child_sc_list)
        lbl_sep15.grid(row=5, column=0, padx=10, pady=10, columnspan=4)

        # Components for Problems List form (list of experimental scenarios)
        lbl_sep17 = Label(self.frm_child_problem_list)
        lbl_sep17.grid(row=0, column=0, padx=10, pady=10, rowspan=4)
        lbl_available_prob_list = Label(self.frm_child_problem_list, text='Problems', anchor=W)
        lbl_available_prob_list.config(font=SUBTITLE2_FONT, fg=TEXT_COLOR)
        lbl_available_prob_list.grid(row=0, column=1, pady=10, columnspan=2, sticky=W)
        self.trv_available_prob = Treeview(self.frm_child_problem_list, height=13, columns=('Brief description',))
        self.trv_available_prob.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_prob.heading('#1', text='Brief description', anchor=CENTER)
        self.trv_available_prob.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_prob.column('#1', width=400, minwidth=400, stretch=NO)
        self.trv_available_prob.bind("<ButtonRelease-1>", self.select_problem)
        self.trv_available_prob.grid(row=1, column=1, rowspan=3, sticky=W, pady=10)
        vsb_trv_avprob = Scrollbar(self.frm_child_problem_list, orient="vertical", command=self.trv_available_prob.yview)
        vsb_trv_avprob.grid(row=1, column=2, rowspan=3, pady=10, sticky=NS)
        self.trv_available_prob.configure(yscrollcommand=vsb_trv_avprob.set)
        frm_aux6 = Frame(self.frm_child_problem_list)
        btn_select_prob = Button(frm_aux6, image=self.view_icon, command=self.click_view_problem)
        btn_select_prob.grid(row=0, column=0, padx=30, pady=10, sticky=W)
        btn_select_prob_ttp = CreateToolTip(btn_select_prob, 'View problem report')
        btn_back_prob = Button(frm_aux6, image=self.back_icon, command=self.click_back_problem)
        btn_back_prob.grid(row=1, column=0, padx=30, pady=10, sticky=NW)
        btn_back_prob_ttp = CreateToolTip(btn_back_prob, 'Go back')
        frm_aux6.grid(row=1, column=3, rowspan=3, sticky=NW)
        sep_aux3 = Separator(self.frm_child_problem_list, orient=VERTICAL)
        sep_aux3.grid(row=0, column=4, sticky=NS, rowspan=5)
        lbl_sep18 = Label(self.frm_child_problem_list)
        lbl_sep18.grid(row=0, column=5, padx=10, pady=10, rowspan=4)
        lbl_details_prob = Label(self.frm_child_problem_list, text='Details', anchor=W)
        lbl_details_prob.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_details_prob.grid(row=0, column=6, pady=10, columnspan=4, sticky=W)
        lbl_desc_prob = Label(self.frm_child_problem_list, text='Description', anchor=W)
        lbl_desc_prob.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_desc_prob.grid(row=1, column=6, pady=10, sticky=NW, rowspan=2)
        lbl_sep19 = Label(self.frm_child_problem_list)
        lbl_sep19.grid(row=1, column=7, padx=10, pady=10)
        self.txt_desc_prob = Text(self.frm_child_problem_list, height=5, width=60)
        self.txt_desc_prob.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_desc_prob.grid(row=1, column=8, pady=10, sticky=W, rowspan=2)
        vsb_txt_desc_prob = Scrollbar(self.frm_child_problem_list, orient="vertical", command=self.txt_desc_prob.yview)
        vsb_txt_desc_prob.grid(row=1, column=9, pady=10, sticky=NS, rowspan=2)
        self.txt_desc_prob.configure(yscrollcommand=vsb_txt_desc_prob.set)
        lbl_sep20 = Label(self.frm_child_problem_list)
        lbl_sep20.grid(row=0, column=10, pady=10, padx=10, sticky=NW, rowspan=4)
        frm_aux3 = LabelFrame(self.frm_child_problem_list, text='Summary of measures')
        frm_aux3.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        frm_aux4 = Frame(frm_aux3)
        lbl_title_egroup_prob = Label(frm_aux4, text='Experimental\ngroup\t')
        lbl_title_egroup_prob.config(fg=TEXT_COLOR, font=LABEL_FONT, justify=LEFT)
        lbl_title_egroup_prob.grid(row=0, column=0, pady=10, padx=10, sticky=NW)
        self.trv_mean_egroup_prob = Treeview(frm_aux4, height=5, columns=('Variable', 'M1', 'M2', 'M3', 'M4'))
        self.trv_mean_egroup_prob.heading('#0', text='ID', anchor=CENTER)
        self.trv_mean_egroup_prob.heading('#1', text='Variable', anchor=CENTER)
        self.trv_mean_egroup_prob.heading('#2', text='M1', anchor=CENTER)
        self.trv_mean_egroup_prob.heading('#3', text='M2', anchor=CENTER)
        self.trv_mean_egroup_prob.heading('#4', text='M3', anchor=CENTER)
        self.trv_mean_egroup_prob.heading('#5', text='M4', anchor=CENTER)
        self.trv_mean_egroup_prob.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_mean_egroup_prob.column('#1', width=130, minwidth=130, stretch=NO)
        self.trv_mean_egroup_prob.column('#2', width=30, minwidth=30, stretch=NO)
        self.trv_mean_egroup_prob.column('#3', width=30, minwidth=30, stretch=NO)
        self.trv_mean_egroup_prob.column('#4', width=30, minwidth=30, stretch=NO)
        self.trv_mean_egroup_prob.column('#5', width=30, minwidth=30, stretch=NO)
        self.trv_mean_egroup_prob.grid(row=0, column=1, sticky=W, pady=10, padx=10)
        frm_aux4.grid(row=0, column=0, sticky=W)
        self.frm_aux5 = Frame(frm_aux3)
        lbl_title_cgroup_prob = Label(self.frm_aux5, text='Control\ngroup\t    ')
        lbl_title_cgroup_prob.config(fg=TEXT_COLOR, font=LABEL_FONT, justify=LEFT)
        lbl_title_cgroup_prob.grid(row=0, column=0, pady=10, padx=10, sticky=NW)
        self.trv_mean_cgroup_prob = Treeview(self.frm_aux5, height=5, columns=('Variable', 'M1', 'M2', 'M3', 'M4'))
        self.trv_mean_cgroup_prob.heading('#0', text='ID', anchor=CENTER)
        self.trv_mean_cgroup_prob.heading('#1', text='Variable', anchor=CENTER)
        self.trv_mean_cgroup_prob.heading('#2', text='M1', anchor=CENTER)
        self.trv_mean_cgroup_prob.heading('#3', text='M2', anchor=CENTER)
        self.trv_mean_cgroup_prob.heading('#4', text='M3', anchor=CENTER)
        self.trv_mean_cgroup_prob.heading('#5', text='M4', anchor=CENTER)
        self.trv_mean_cgroup_prob.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_mean_cgroup_prob.column('#1', width=130, minwidth=130, stretch=NO)
        self.trv_mean_cgroup_prob.column('#2', width=30, minwidth=30, stretch=NO)
        self.trv_mean_cgroup_prob.column('#3', width=30, minwidth=30, stretch=NO)
        self.trv_mean_cgroup_prob.column('#4', width=30, minwidth=30, stretch=NO)
        self.trv_mean_cgroup_prob.column('#5', width=30, minwidth=30, stretch=NO)
        self.trv_mean_cgroup_prob.grid(row=0, column=1, sticky=W, pady=10, padx=10)
        lbl_legend = Label(frm_aux3, text='Legend:\n\nM1 > Solution time\nM2 > Selection time\nM3 > '
                                          'Viewed patterns\nM4 > Chosen patterns')
        lbl_legend.config(fg=TEXT_COLOR, font=LABEL_FONT, justify=LEFT)
        lbl_legend.grid(row=0, column=1, pady=10, padx=10, sticky=W, rowspan=2)
        frm_aux3.grid(row=3, column=6, columnspan=4)
        lbl_sep21 = Label(self.frm_child_problem_list)
        lbl_sep21.grid(row=4, column=0, padx=10, pady=10, columnspan=4)


        # Components for Problem form (summary and details)
        frm_aux1 = Frame(self.frm_child_component)
        lbl_problem = Label(frm_aux1, text='Design Problem')
        lbl_problem.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_problem.grid(row=0, column=0, pady=25, padx=25, sticky=W)
        lbl_problem_desc = Label(frm_aux1, text='Description')
        lbl_problem_desc.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_problem_desc.grid(row=1, column=0, pady=25, padx=25, sticky=NW)
        self.lbl_problem_cont = Label(frm_aux1)
        self.lbl_problem_cont.config(fg=TEXT_COLOR, font=LABEL_FONT)
        self.lbl_problem_cont.grid(row=0, column=1, pady=25, padx=25, sticky=W)
        self.txt_problem_desc = Text(frm_aux1, height=5, width=60)
        self.txt_problem_desc.config(font=TEXT_FONT, bg=DISABLED_COLOR)
        self.txt_problem_desc.grid(row=1, column=1, padx=25, pady=25, rowspan=6, sticky=W)
        lbl_legend = Label(frm_aux1, text='Legend:\n\nM1 > Solution time\nM2 > Selection time\nM3 > '
                                          'Viewed patterns\nM4 > Chosen patterns')
        lbl_legend.config(fg=TEXT_COLOR, font=LABEL_FONT, justify=LEFT)
        lbl_legend.grid(row=0, column=2, pady=25, padx=25, sticky=W, rowspan=6, columnspan=2)
        frm_aux2 = LabelFrame(self.frm_child_component, text='Control group')
        frm_aux2.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_sep4 = Label(frm_aux2)
        lbl_sep4.grid(row=0, column=0, padx=25, pady=10, rowspan=12)
        lbl_summary_cg = Label(frm_aux2, text='Summary', anchor=W)
        lbl_summary_cg.config(font=LABEL_FONT, fg=TEXT_COLOR)
        lbl_summary_cg.grid(row=0, column=1, pady=10, columnspan=2, sticky=W)
        self.trv_summary_cg = Treeview(frm_aux2, height=5, columns=('Variable', 'M1', 'M2', 'M3', 'M4'))
        self.trv_summary_cg.heading('#0', text='ID', anchor=CENTER)
        self.trv_summary_cg.heading('#1', text='Variable', anchor=CENTER)
        self.trv_summary_cg.heading('#2', text='M1', anchor=CENTER)
        self.trv_summary_cg.heading('#3', text='M2', anchor=CENTER)
        self.trv_summary_cg.heading('#4', text='M3', anchor=CENTER)
        self.trv_summary_cg.heading('#5', text='M4', anchor=CENTER)
        self.trv_summary_cg.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_summary_cg.column('#1', width=130, minwidth=130, stretch=NO)
        self.trv_summary_cg.column('#2', width=30, minwidth=30, stretch=NO)
        self.trv_summary_cg.column('#3', width=30, minwidth=30, stretch=NO)
        self.trv_summary_cg.column('#4', width=30, minwidth=30, stretch=NO)
        self.trv_summary_cg.column('#5', width=30, minwidth=30, stretch=NO)
        self.trv_summary_cg.grid(row=1, column=1, rowspan=5, sticky=W, pady=10)
        vsb_trv_sumcg = Scrollbar(frm_aux2, orient="vertical", command=self.trv_summary_cg.yview)
        vsb_trv_sumcg.grid(row=1, column=2, rowspan=5, pady=10, sticky=NS)
        self.trv_summary_cg.configure(yscrollcommand=vsb_trv_sumcg.set)
        lbl_details_cg = Label(frm_aux2, text='Details', anchor=W)
        lbl_details_cg.config(font=LABEL_FONT, fg=TEXT_COLOR)
        lbl_details_cg.grid(row=6, column=1, pady=10, columnspan=2, sticky=W)
        self.trv_details_cg = Treeview(frm_aux2, height=5, columns=('Designer', 'M1', 'M2', 'M3', 'M4'))
        self.trv_details_cg.heading('#0', text='ID', anchor=CENTER)
        self.trv_details_cg.heading('#1', text='Designer', anchor=CENTER)
        self.trv_details_cg.heading('#2', text='M1', anchor=CENTER)
        self.trv_details_cg.heading('#3', text='M2', anchor=CENTER)
        self.trv_details_cg.heading('#4', text='M3', anchor=CENTER)
        self.trv_details_cg.heading('#5', text='M4', anchor=CENTER)
        self.trv_details_cg.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_details_cg.column('#1', width=130, minwidth=130, stretch=NO)
        self.trv_details_cg.column('#2', width=30, minwidth=30, stretch=NO)
        self.trv_details_cg.column('#3', width=30, minwidth=30, stretch=NO)
        self.trv_details_cg.column('#4', width=30, minwidth=30, stretch=NO)
        self.trv_details_cg.column('#5', width=30, minwidth=30, stretch=NO)
        self.trv_details_cg.grid(row=7, column=1, rowspan=5, sticky=W, pady=10)
        vsb_trv_detcg = Scrollbar(frm_aux2, orient="vertical", command=self.trv_details_cg.yview)
        vsb_trv_detcg.grid(row=7, column=2, rowspan=5, pady=10, sticky=NS)
        self.trv_details_cg.configure(yscrollcommand=vsb_trv_detcg.set)
        lbl_sep5 = Label(frm_aux2)
        lbl_sep5.grid(row=0, column=3, padx=25, pady=10, rowspan=12)

        frm_aux3 = LabelFrame(self.frm_child_component, text='Experimental group')
        frm_aux3.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_sep4 = Label(frm_aux3)
        lbl_sep4.grid(row=0, column=0, padx=25, pady=10, rowspan=12)
        lbl_summary_eg = Label(frm_aux3, text='Summary', anchor=W)
        lbl_summary_eg.config(font=LABEL_FONT, fg=TEXT_COLOR)
        lbl_summary_eg.grid(row=0, column=1, pady=10, columnspan=2, sticky=W)
        self.trv_summary_eg = Treeview(frm_aux3, height=5, columns=('Variable', 'M1', 'M2', 'M3', 'M4'))
        self.trv_summary_eg.heading('#0', text='ID', anchor=CENTER)
        self.trv_summary_eg.heading('#1', text='Variable', anchor=CENTER)
        self.trv_summary_eg.heading('#2', text='M1', anchor=CENTER)
        self.trv_summary_eg.heading('#3', text='M2', anchor=CENTER)
        self.trv_summary_eg.heading('#4', text='M3', anchor=CENTER)
        self.trv_summary_eg.heading('#5', text='M4', anchor=CENTER)
        self.trv_summary_eg.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_summary_eg.column('#1', width=130, minwidth=130, stretch=NO)
        self.trv_summary_eg.column('#2', width=30, minwidth=30, stretch=NO)
        self.trv_summary_eg.column('#3', width=30, minwidth=30, stretch=NO)
        self.trv_summary_eg.column('#4', width=30, minwidth=30, stretch=NO)
        self.trv_summary_eg.column('#5', width=30, minwidth=30, stretch=NO)
        self.trv_summary_eg.grid(row=1, column=1, rowspan=5, sticky=W, pady=10)
        vsb_trv_sumeg = Scrollbar(frm_aux3, orient="vertical", command=self.trv_summary_eg.yview)
        vsb_trv_sumeg.grid(row=1, column=2, rowspan=5, pady=10, sticky=NS)
        self.trv_summary_eg.configure(yscrollcommand=vsb_trv_sumeg.set)
        lbl_details_eg = Label(frm_aux3, text='Details', anchor=W)
        lbl_details_eg.config(font=LABEL_FONT, fg=TEXT_COLOR)
        lbl_details_eg.grid(row=6, column=1, pady=10, columnspan=2, sticky=W)
        self.trv_details_eg = Treeview(frm_aux3, height=5, columns=('Designer', 'M1', 'M2', 'M3', 'M4'))
        self.trv_details_eg.heading('#0', text='ID', anchor=CENTER)
        self.trv_details_eg.heading('#1', text='Designer', anchor=CENTER)
        self.trv_details_eg.heading('#2', text='M1', anchor=CENTER)
        self.trv_details_eg.heading('#3', text='M2', anchor=CENTER)
        self.trv_details_eg.heading('#4', text='M3', anchor=CENTER)
        self.trv_details_eg.heading('#5', text='M4', anchor=CENTER)
        self.trv_details_eg.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_details_eg.column('#1', width=130, minwidth=130, stretch=NO)
        self.trv_details_eg.column('#2', width=30, minwidth=30, stretch=NO)
        self.trv_details_eg.column('#3', width=30, minwidth=30, stretch=NO)
        self.trv_details_eg.column('#4', width=30, minwidth=30, stretch=NO)
        self.trv_details_eg.column('#5', width=30, minwidth=30, stretch=NO)
        self.trv_details_eg.grid(row=7, column=1, rowspan=5, sticky=W, pady=10)
        vsb_trv_deteg = Scrollbar(frm_aux3, orient="vertical", command=self.trv_details_eg.yview)
        vsb_trv_deteg.grid(row=7, column=2, rowspan=5, pady=10, sticky=NS)
        self.trv_details_eg.configure(yscrollcommand=vsb_trv_deteg.set)
        lbl_sep5 = Label(frm_aux3)
        lbl_sep5.grid(row=0, column=3, padx=25, pady=10, rowspan=12)
        frm_aux1.grid(rowspan=6, columnspan=4)
        frm_aux2.grid(row=6, column=0, rowspan=12, columnspan=2, padx=10, pady=10, sticky=W)
        frm_aux3.grid(row=6, column=2, rowspan=12, columnspan=2, padx=10, pady=10, sticky=E)
        lbl_notes = Label(self.frm_child_component, text='NOTE: To see details of measurements and solution of a '
                                                         'designer, double click a designer (details)\n')
        lbl_notes.config(fg=TEXT_COLOR, font=NOTE_FONT)
        lbl_notes.grid(row=18, column=0, padx=25, sticky=W, columnspan=4)
        sep_component = Separator(self.frm_child_component, orient=VERTICAL)
        sep_component.grid(row=0, column=4, sticky=NS, rowspan=19)
        btn_back_component = Button(self.frm_child_component, image=self.back_icon, command=self.click_back_component)
        btn_back_component.grid(row=0, column=5, padx=30, pady=25)
        btn_back_component_ttp = CreateToolTip(btn_back_component, 'Generate .csv file')'''

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

        # Components of expanded sent solution diagram
        self.canvas_expanded = Canvas(self.tlevel_diagram, width=500, height=500)
        self.canvas_expanded.config(background='white', borderwidth=1)
        self.canvas_expanded.grid()

    def show_frm(self):
        """
        Displays the home list of the 'Experiments' form
        """
        self.retrieve_experiments()
        self.frm_child_report.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

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
                self.trv_available_exp.insert('', 'end', text=elements[0], values=(index+1, elements[1]))
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
            self.trv_available_sc.insert('', 'end', text=elements[0], values=(index+1, elements[1]))
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
            self.trv_available_prob.insert('', 'end', text=elements[0], values=(index+1, elements[1]))
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
            id_selected_exp = int(self.trv_available_exp.item(self.trv_available_exp.selection())['text'])  # Retrieve id of selected item from TreeView
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

    def select_scenario_general(self, event=None):
        """
        Function activated when a scenario is selecteded
        """
        if len(self.trv_available_sc.selection()) == 1:
            self.clear_components(2)
            id_selected_sc = int(self.trv_available_sc.item(self.trv_available_sc.selection())['text'])  # Retrieve id of selected item from TreeView
            self.directive = Message(action=85, information=[id_selected_sc, 'report', 1])
            self.connection = self.directive.send_directive(self.connection)
            self.scenario = ExperimentalSC(id=id_selected_sc, title=self.connection.message.information[0],
                                           description=self.connection.message.information[1],
                                           id_description_diagram=self.connection.message.information[2],
                                           info_designers=self.connection.message.information[4])
            self.retrieve_problems(self.connection.message.information[3])
            # Ask to server for dataframe of the measurements for the problems of selected scenario

    def select_problem_general(self, event=None):
        """
        Function activated when a scenario is selecteded
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
                                                    self.problem.solution.annotations, aux_patterns))
            self.txt_detail_component['state'] = DISABLED
            self.tlevel_comp_detail.deiconify()
            self.tlevel_comp_detail.grab_set()
        else:
            messagebox.showwarning(parent=self.frm_child_report, title='No selection',
                                   message='You must select one item')

    def click_view_desc_diagram(self):
        # Fill summary problem canvas with retrieved image
        load = Image.open(self.scenario.description_diagram.filename)
        load = load.resize((500, 500), Image.ANTIALIAS)
        self.render_dd_exp = ImageTk.PhotoImage(load)
        self.canvas_expanded.delete()
        self.scenario.description_diagram.image = self.canvas_expanded.create_image(0, 0, anchor='nw',
                                                                                    image=self.render_dd_exp)  # and display new image
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

    def view_detailed_solution(self):
        pass

    def clear_components(self, decision=4):
        if decision > 0:    # When selecting an problem form general list
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
                    if decision > 3:    # Clearing information from all the treeviews
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
