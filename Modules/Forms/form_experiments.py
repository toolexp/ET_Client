from tkinter import Label, LabelFrame, Frame, Text, Button, messagebox, PhotoImage, Scrollbar, Toplevel, Listbox, \
    Canvas, StringVar, filedialog
from tkinter.constants import *
from tkinter.ttk import Treeview, Separator, Combobox, Notebook, Style
from Modules.Config.Data import Message, CreateToolTip, Experiment, Pattern, wrap_text, Designer, ExperimentalSC, \
    Problem, File, Solution, treeview_sort_column
from Modules.Config.Visual import *
from PIL import ImageTk, Image
import os


class FormParentExperiment:
    def __init__(self, window, connection):
        self.frm_parent = Frame(window)
        self.main_title = StringVar()
        self.initialize_components()
        self.frm_child = FormChildExperiment(self.frm_parent, connection, self.main_title)

    def initialize_components(self):
        lbl_experiment_title = Label(self.frm_parent, textvariable=self.main_title)
        lbl_experiment_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_experiment_title.grid(row=0, column=0, pady=20)
        self.main_title.set('Experiments')

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildExperiment:
    def __init__(self, frm_parent, connection, main_title):
        self.main_title = main_title
        self.connection = connection
        self.file_dd = None
        self.file_esol = None

        self.frm_child_exp_list = LabelFrame(frm_parent)
        self.frm_child_sc_list = LabelFrame(frm_parent)
        self.frm_child_general_sc = LabelFrame(frm_parent)
        self.frm_child_general_sc.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        self.tlevel_problem = Toplevel(self.frm_child_general_sc)
        self.tlevel_problem.protocol("WM_DELETE_WINDOW", self.click_cancel_problem)
        self.tlevel_problem.withdraw()
        self.tlevel_designers = Toplevel(self.frm_child_general_sc)
        self.tlevel_designers.title('Configure designers')
        self.tlevel_designers.protocol("WM_DELETE_WINDOW", self.click_cancel_designers)
        self.tlevel_designers.withdraw()
        self.tlevel_patterns = Toplevel(self.tlevel_problem)
        self.tlevel_patterns.title('Configure patterns')
        self.tlevel_patterns.protocol("WM_DELETE_WINDOW", self.click_cancel_patterns)
        self.tlevel_patterns.withdraw()
        self.tlevel_diagram = Toplevel(self.tlevel_problem)
        self.tlevel_diagram.title('Diagram')
        self.tlevel_diagram.protocol("WM_DELETE_WINDOW", self.click_cancel_diagram)
        self.tlevel_diagram.withdraw()
        self.initialize_components()

    def initialize_components(self):
        """
        Method that initialize the visual components for each form associated with the administration of experiments
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
        self.config_icon = PhotoImage(file=r"./Resources/config.png")
        self.exec_icon = PhotoImage(file=r"./Resources/exec.png")
        self.finish_icon = PhotoImage(file=r"./Resources/finish.png")
        self.open_icon = PhotoImage(file=r"./Resources/open.png")
        self.designers_icon = PhotoImage(file=r"./Resources/people.png")
        self.patterns_icon = PhotoImage(file=r"./Resources/pattern.png")
        self.check_icon = PhotoImage(file=r"./Resources/check.png")
        self.disabled_color = self.frm_child_exp_list.cget('bg')

        # Components for experiment list form (list of experiments)
        lbl_sep1 = Label(self.frm_child_exp_list)
        lbl_sep1.grid(row=0, column=0, padx=10, pady=25)
        self.trv_available_exp = Treeview(self.frm_child_exp_list, height=20, columns=('N', 'Name', 'Description',
                                                                                       'Design type', 'State'))
        self.trv_available_exp.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_exp.heading('#1', text='N', anchor=CENTER)
        self.trv_available_exp.heading('#2', text='Name', anchor=CENTER)
        self.trv_available_exp.heading('#3', text='Description', anchor=CENTER)
        self.trv_available_exp.heading('#4', text='Design type', anchor=CENTER)
        self.trv_available_exp.heading('#5', text='State', anchor=CENTER)
        self.trv_available_exp.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_exp.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available_exp.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_available_exp.column('#3', width=400, minwidth=400, stretch=NO)
        self.trv_available_exp.column('#4', width=100, minwidth=100, stretch=NO, anchor=CENTER)
        self.trv_available_exp.column('#5', width=100, minwidth=100, stretch=NO, anchor=CENTER)
        self.trv_available_exp.grid(row=0, column=1, sticky=W, pady=25, rowspan=2)
        vsb_trv_av_exp = Scrollbar(self.frm_child_exp_list, orient="vertical", command=self.trv_available_exp.yview)
        vsb_trv_av_exp.grid(row=0, column=2, pady=25, rowspan=2, sticky=NS)
        self.trv_available_exp.configure(yscrollcommand=vsb_trv_av_exp.set)
        frm_aux4 = Frame(self.frm_child_exp_list)
        btn_new_exp = Button(frm_aux4, image=self.new_icon, command=self.click_new_exp)
        btn_new_exp.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_new_exp_ttp = CreateToolTip(btn_new_exp, 'New experiment')
        btn_view_exp = Button(frm_aux4, image=self.view_icon, command=self.click_view_exp)
        btn_view_exp.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_view_exp_ttp = CreateToolTip(btn_view_exp, 'View experiment')
        btn_config_exp = Button(frm_aux4, image=self.config_icon, command=self.click_config_exp)
        btn_config_exp.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_config_exp_ttp = CreateToolTip(btn_config_exp, 'Configure experiment')
        btn_delete_exp = Button(frm_aux4, image=self.remove_icon, command=self.click_delete_exp)
        btn_delete_exp.grid(row=3, column=0, pady=5, padx=5, sticky=E)
        btn_delete_exp_ttp = CreateToolTip(btn_delete_exp, 'Delete experiment')

        frm_aux5 = Frame(self.frm_child_exp_list)
        btn_exec_exp = Button(frm_aux5, image=self.exec_icon, command=self.click_exec_exp)
        btn_exec_exp.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_exec_exp_exp_ttp = CreateToolTip(btn_exec_exp, 'Execute experiment')
        btn_finish_exp = Button(frm_aux5, image=self.finish_icon, command=self.click_finish_exp)
        btn_finish_exp.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_finish_exp_ttp = CreateToolTip(btn_finish_exp, 'Finish experiment and generate report')
        frm_aux4.grid(row=0, column=4, pady=25, padx=25, sticky=NW)
        frm_aux5.grid(row=1, column=4, pady=25, padx=25, sticky=SW)

        # Components for experimental scenarios List form (list of experimental scenarios and info of experiment)
        lbl_sep24 = Label(self.frm_child_sc_list)
        lbl_sep24.grid(row=0, column=0, padx=10, pady=10, rowspan=3)
        lbl_name_exp = Label(self.frm_child_sc_list, text='Name*')
        lbl_name_exp.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name_exp.grid(row=0, column=1, pady=10, sticky=W)
        lbl_description_exp = Label(self.frm_child_sc_list, text='Description*')
        lbl_description_exp.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_description_exp.grid(row=1, column=1, pady=10, sticky=NW)
        lbl_design_type = Label(self.frm_child_sc_list, text='Design type*')
        lbl_design_type.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_design_type.grid(row=2, column=1, pady=10, sticky=W)
        lbl_sep25 = Label(self.frm_child_sc_list)
        lbl_sep25.grid(row=0, column=2, padx=10, pady=10, rowspan=3)
        self.txt_name_exp = Text(self.frm_child_sc_list, height=1, width=79)
        self.txt_name_exp.config(font=TEXT_FONT)
        self.txt_name_exp.grid(row=0, column=3, pady=10, sticky=W)
        self.txt_description_exp = Text(self.frm_child_sc_list, height=4, width=79)
        self.txt_description_exp.config(font=TEXT_FONT)
        self.txt_description_exp.grid(row=1, column=3, pady=10, sticky=W)
        vsb_txt_desc_exp = Scrollbar(self.frm_child_sc_list, orient="vertical", command=self.txt_description_exp.yview)
        vsb_txt_desc_exp.grid(row=1, column=4, pady=10, sticky=NS)
        self.txt_description_exp.configure(yscrollcommand=vsb_txt_desc_exp.set)
        self.cbx_dt_exp = Combobox(self.frm_child_sc_list, state="readonly", width=80)
        self.cbx_dt_exp['values'] = ['One group', 'Two groups']
        self.cbx_dt_exp.grid(row=2, column=3, pady=25, columnspan=2, sticky=W)
        frm_aux14 = Frame(self.frm_child_sc_list)
        self.btn_save_exp = Button(frm_aux14, image=self.save_icon, command=self.click_save_exp)
        btn_save_exp_ttp = CreateToolTip(self.btn_save_exp, 'Save experiment')
        self.btn_back_exp = Button(frm_aux14, image=self.back_icon, command=self.click_back_exp)
        btn_back_exp_ttp = CreateToolTip(self.btn_back_exp, 'Go back')
        self.btn_cancel_exp = Button(frm_aux14, image=self.cancel_icon, command=self.click_cancel_exp)
        btn_cancel_exp_ttp = CreateToolTip(self.btn_cancel_exp, 'Cancel')
        frm_aux14.grid(row=0, column=5, pady=10, padx=25, sticky=NW, rowspan=3)
        self.enabled_color = self.txt_name_exp.cget('bg')
        sep_aux1 = Separator(self.frm_child_sc_list, orient=HORIZONTAL)
        sep_aux1.grid(row=3, column=0, sticky=EW, columnspan=6)
        lbl_sep2 = Label(self.frm_child_sc_list)
        lbl_sep2.grid(row=4, column=0, padx=10, pady=10, rowspan=3)
        lbl_scenario_desc = Label(self.frm_child_sc_list, text=wrap_text('In this section you can configure the '
                                                                         'experimental scenarios associated with the '
                                                                         'experiment you have selected.', 95))
        lbl_scenario_desc.config(font=SUBTITLE2_FONT, fg=TEXT_COLOR, justify=LEFT)
        lbl_scenario_desc.grid(row=4, column=1, pady=10, sticky=W, columnspan=4)
        self.trv_available_sc = Treeview(self.frm_child_sc_list, height=10, columns=('N', 'Name', 'Context', 'State',
                                                                                     'Available?'))
        self.trv_available_sc.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_sc.heading('#1', text='N', anchor=CENTER)
        self.trv_available_sc.heading('#2', text='Name', anchor=CENTER)
        self.trv_available_sc.heading('#3', text='Context', anchor=CENTER)
        self.trv_available_sc.heading('#4', text='State', anchor=CENTER)
        self.trv_available_sc.heading('#5', text='Available?', anchor=CENTER)
        self.trv_available_sc.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_sc.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available_sc.column('#2', width=180, minwidth=180, stretch=NO)
        self.trv_available_sc.column('#3', width=300, minwidth=300, stretch=NO)
        self.trv_available_sc.column('#4', width=80, minwidth=80, stretch=NO, anchor=CENTER)
        self.trv_available_sc.column('#5', width=80, minwidth=80, stretch=NO, anchor=CENTER)
        self.trv_available_sc.bind("<Double-1>", self.switch_availability)
        self.trv_available_sc.grid(row=5, column=1, columnspan=3, sticky=W, pady=10)
        vsb_trv_av_sc = Scrollbar(self.frm_child_sc_list, orient="vertical", command=self.trv_available_sc.yview)
        vsb_trv_av_sc.grid(row=5, column=4, pady=10, sticky=NS)
        self.trv_available_sc.configure(yscrollcommand=vsb_trv_av_sc.set)
        self.lbl_note_available = Label(self.frm_child_sc_list, text='NOTE: To switch between available and disabled '
                                                                     '(for designers), double click on selected scenario\n')
        self.lbl_note_available.config(fg=TEXT_COLOR, font=NOTE_FONT)
        frm_aux6 = Frame(self.frm_child_sc_list)
        self.btn_new_sc = Button(frm_aux6, image=self.new_icon, command=self.click_new_sc)
        btn_new_sc_ttp = CreateToolTip(self.btn_new_sc, 'New experimental scenario')
        self.btn_view_sc = Button(frm_aux6, image=self.view_icon, command=self.click_view_sc)
        btn_view_sc_ttp = CreateToolTip(self.btn_view_sc, 'View experimental scenario')
        self.btn_edit_sc = Button(frm_aux6, image=self.modify_icon, command=self.click_update_sc)
        btn_edit_sc_ttp = CreateToolTip(self.btn_edit_sc, 'Edit experimental scenario')
        self.btn_delete_sc = Button(frm_aux6, image=self.remove_icon, command=self.click_delete_sc)
        btn_delete_sc_ttp = CreateToolTip(self.btn_delete_sc, 'Delete experimental scenario')
        frm_aux6.grid(row=5, column=5, pady=10, padx=25, sticky=NW)

        # Components for general scenario config form, where each experimental scenario may be configured
        lbl_sep3 = Label(self.frm_child_general_sc)
        lbl_sep3.grid(row=0, column=0, padx=10, pady=10, rowspan=6)
        lbl_sep20 = Label(self.frm_child_general_sc)
        lbl_sep20.grid(row=0, column=2, padx=10, pady=10, rowspan=5)
        lbl_title_sc = Label(self.frm_child_general_sc, text='Title*')
        lbl_title_sc.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_title_sc.grid(row=0, column=1, pady=10, sticky=W)
        lbl_description_sc = Label(self.frm_child_general_sc, text='Description*\t')
        lbl_description_sc.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_description_sc.grid(row=1, column=1, pady=10, sticky=NW)
        lbl_dg_description_sc = Label(self.frm_child_general_sc, text='Desc. diagram')
        lbl_dg_description_sc.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_dg_description_sc.grid(row=2, column=1, pady=10, rowspan=2, sticky=NW)
        lbl_access_sc = Label(self.frm_child_general_sc, text='Access code*\t')
        lbl_access_sc.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_access_sc.grid(row=4, column=1, pady=10, sticky=W)
        self.txt_title_sc = Text(self.frm_child_general_sc, height=1, width=50)
        self.txt_title_sc.config(font=TEXT_FONT)
        self.txt_title_sc.grid(row=0, column=3, pady=10, columnspan=2, sticky=W)
        self.txt_description_sc = Text(self.frm_child_general_sc, height=6, width=50)
        self.txt_description_sc.config(font=TEXT_FONT)
        self.txt_description_sc.grid(row=1, column=3, pady=10, columnspan=2, sticky=W)
        vsb_txt_description = Scrollbar(self.frm_child_general_sc, orient="vertical",
                                        command=self.txt_description_sc.yview)
        vsb_txt_description.grid(row=1, column=5, pady=10, sticky=NS)
        self.txt_description_sc.configure(yscrollcommand=vsb_txt_description.set)
        self.canvas_dd = Canvas(self.frm_child_general_sc, width=110, height=110)
        self.canvas_dd.config(background='white', borderwidth=1)
        self.canvas_dd.grid(row=2, column=3, pady=10, rowspan=2, sticky=W)
        self.btn_open_dd = Button(self.frm_child_general_sc, image=self.open_icon, command=self.click_upload_dd)
        btn_open_dd_ttp = CreateToolTip(self.btn_open_dd, 'Open image')
        self.btn_quit_dd = Button(self.frm_child_general_sc, image=self.remove_icon, command=self.click_remove_dd)
        btn_quit_dd_ttp = CreateToolTip(self.btn_quit_dd, 'Remove image')
        self.btn_view_dd = Button(self.frm_child_general_sc, image=self.view_icon, command=self.click_view_dd)
        btn_view_dd_ttp = CreateToolTip(self.btn_view_dd, 'View image')
        self.txt_access_sc = Text(self.frm_child_general_sc, height=1, width=50)
        self.txt_access_sc.config(font=TEXT_FONT)
        self.txt_access_sc.grid(row=4, column=3, pady=10, columnspan=2, sticky=W)

        self.tab_control = Notebook(self.frm_child_general_sc)
        tab_problem = Frame(self.tab_control)
        self.tab_control.add(tab_problem, text="Problems", padding=10)
        lbl_problems = Label(tab_problem, text='Configured problems*')
        lbl_problems.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_problems.grid(row=0, column=0, pady=10, rowspan=5, sticky=NW)
        lbl_sep6 = Label(tab_problem)
        lbl_sep6.grid(row=0, column=1, padx=10, pady=10, rowspan=5)
        self.lbx_problems = Listbox(tab_problem, height=6, width=40, exportselection=0)
        self.lbx_problems.grid(row=0, column=2, sticky=W, rowspan=5, pady=10)
        vsb_lbx_problems = Scrollbar(tab_problem, orient="vertical", command=self.lbx_problems.yview)
        vsb_lbx_problems.grid(row=0, column=3, rowspan=5, pady=10, sticky=NS)
        self.lbx_problems.configure(yscrollcommand=vsb_lbx_problems.set)
        self.btn_new_prob = Button(tab_problem, image=self.new_icon, command=self.click_new_problem)
        btn_new_prob_ttp = CreateToolTip(self.btn_new_prob, 'New problem')
        self.btn_delete_prob = Button(tab_problem, image=self.remove_icon,
                                      command=self.click_delete_problem)
        btn_delete_prob_ttp = CreateToolTip(self.btn_delete_prob, 'Delete problem')
        self.btn_view_prob = Button(tab_problem, image=self.view_icon, command=self.click_view_problem)
        btn_view_prob_ttp = CreateToolTip(self.btn_view_prob, 'View problem')
        tab_designers = Frame(self.tab_control)
        self.tab_control.add(tab_designers, text="Designers", padding=10)
        frm_aux8 = Frame(tab_designers)
        lbl_egroup = Label(frm_aux8, text='Experimental group*')
        lbl_egroup.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_egroup.grid(row=0, column=0, sticky=NW, pady=10)
        lbl_sep4 = Label(frm_aux8)
        lbl_sep4.grid(row=0, column=1, padx=10, pady=10)
        self.lbx_egroup = Listbox(frm_aux8, height=6, width=40, exportselection=0)
        self.lbx_egroup.grid(row=0, column=2, sticky=W, pady=10)
        vsb_lbx_egroup = Scrollbar(frm_aux8, orient="vertical", command=self.lbx_egroup.yview)
        vsb_lbx_egroup.grid(row=0, column=3, sticky=NS, pady=10)
        self.lbx_egroup.configure(yscrollcommand=vsb_lbx_egroup.set)
        self.btn_egroup = Button(frm_aux8, image=self.designers_icon, command=self.click_egroup_sc)
        btn_egroup_ttp = CreateToolTip(self.btn_egroup, 'Configure experimental group')
        frm_aux8.grid(row=0, column=0, sticky=W)
        self.frm_aux9 = Frame(tab_designers)
        lbl_cgroup = Label(self.frm_aux9, text='Control group*  \t')
        lbl_cgroup.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_cgroup.grid(row=0, column=0, sticky=NW, pady=10)
        lbl_sep5 = Label(self.frm_aux9)
        lbl_sep5.grid(row=0, column=1, padx=10, pady=10)
        self.lbx_cgroup = Listbox(self.frm_aux9, height=6, width=40, exportselection=0)
        self.lbx_cgroup.grid(row=0, column=2, sticky=W, pady=10)
        vsb_lbx_cgroup = Scrollbar(self.frm_aux9, orient="vertical", command=self.lbx_cgroup.yview)
        vsb_lbx_cgroup.grid(row=0, column=3, pady=10, sticky=NS)
        self.lbx_cgroup.configure(yscrollcommand=vsb_lbx_cgroup.set)
        self.btn_cgroup = Button(self.frm_aux9, image=self.designers_icon, command=self.click_cgroup_sc)
        btn_cgroup_ttp = CreateToolTip(self.btn_cgroup, 'Configure control group')
        tab_designers_patterns = Frame(self.tab_control)
        self.tab_control.add(tab_designers_patterns, text="Designers\' available patterns", padding=10)
        frm_aux13 = Frame(tab_designers_patterns)
        lbl_egroup_pat = Label(frm_aux13, text='Experimental group')
        lbl_egroup_pat.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_egroup_pat.grid(row=0, column=0, pady=10, sticky=NW)
        lbl_sep13 = Label(frm_aux13)
        lbl_sep13.grid(row=0, column=1, padx=10, pady=10)
        self.lbx_egroup_pat = Listbox(frm_aux13, height=6, width=40, exportselection=0)
        self.lbx_egroup_pat.grid(row=0, column=2, pady=10, sticky=W)
        vsb_lbx_egroup_pat = Scrollbar(frm_aux13, orient="vertical", command=self.lbx_egroup_pat.yview)
        vsb_lbx_egroup_pat.grid(row=0, column=3, pady=10, sticky=NS)
        self.lbx_egroup_pat.configure(yscrollcommand=vsb_lbx_egroup_pat.set)
        self.btn_egroup_pat = Button(frm_aux13, image=self.patterns_icon, command=self.click_egroup_pat)
        btn_egroup_pat_ttp = CreateToolTip(self.btn_egroup_pat, 'Configure patterns')
        self.frm_aux11 = Frame(tab_designers_patterns)
        lbl_cgroup_pat = Label(self.frm_aux11, text='Control group\t')
        lbl_cgroup_pat.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_cgroup_pat.grid(row=0, column=0, pady=10, rowspan=5, sticky=NW)
        lbl_sep14 = Label(self.frm_aux11)
        lbl_sep14.grid(row=0, column=1, padx=10, pady=10, rowspan=5)
        self.lbx_cgroup_pat = Listbox(self.frm_aux11, height=6, width=40, exportselection=0)
        self.lbx_cgroup_pat.grid(row=0, column=2, sticky=W, pady=10, rowspan=5)
        vsb_lbx_cgroup_pat = Scrollbar(self.frm_aux11, orient="vertical", command=self.lbx_cgroup_pat.yview)
        vsb_lbx_cgroup_pat.grid(row=0, column=3, pady=10, rowspan=5, sticky=NS)
        self.lbx_cgroup_pat.configure(yscrollcommand=vsb_lbx_cgroup_pat.set)
        self.btn_cgroup_pat = Button(self.frm_aux11, image=self.patterns_icon, command=self.click_cgroup_pat)
        btn_cgroup_pat_ttp = CreateToolTip(self.btn_cgroup_pat, 'Configure patterns')
        self.btn_copy_pat = Button(self.frm_aux11, image=self.copy_icon, command=self.click_copy_pats)
        btn_copy_pat_ttp = CreateToolTip(self.btn_copy_pat, 'Copy patterns from experimental group')
        frm_aux13.grid(row=0, column=0)
        self.tab_control.grid(row=5, column=1, pady=10, sticky=W, columnspan=5)
        sep_general_sc = Separator(self.frm_child_general_sc, orient=VERTICAL)
        sep_general_sc.grid(row=0, column=6, sticky=NS, rowspan=6, padx=20)
        frm_aux12 = Frame(self.frm_child_general_sc)
        self.btn_save_sc = Button(frm_aux12, image=self.save_icon, command=self.click_save_sc)
        btn_save_sc_ttp = CreateToolTip(self.btn_save_sc, 'Save experimental scenario')
        self.btn_cancel_sc = Button(frm_aux12, image=self.cancel_icon, command=self.click_cancel_sc)
        btn_cancel_sc_ttp = CreateToolTip(self.btn_cancel_sc, 'Cancel')
        self.btn_back_sc = Button(frm_aux12, image=self.back_icon, command=self.click_back_sc)
        btn_back_sc_ttp = CreateToolTip(self.btn_back_sc, 'Go back')
        frm_aux12.grid(row=0, column=7, rowspan=6, sticky=N)

        # Components for selecting designers
        lbl_sep7 = Label(self.tlevel_designers)
        lbl_sep7.grid(row=0, column=0, rowspan=10, padx=25, pady=25)
        self.trv_available_designers = Treeview(self.tlevel_designers, height=10, columns=('N', 'Available designers'),
                                                show='headings')
        self.trv_available_designers.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_designers.heading('#1', text='N', anchor=CENTER)
        self.trv_available_designers.heading('#2', text='Available designers', anchor=CENTER)
        self.trv_available_designers.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_available_designers.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available_designers.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_available_designers.bind("<Button-1>", self.click_trv_adesigners)
        self.trv_available_designers.grid(row=0, column=1, rowspan=10, pady=25, sticky=W)
        vsb_trv_avdes = Scrollbar(self.tlevel_designers, orient="vertical", command=self.trv_available_designers.yview)
        vsb_trv_avdes.grid(row=0, column=2, rowspan=10, pady=25, sticky=NS)
        self.trv_available_designers.configure(yscrollcommand=vsb_trv_avdes.set)
        self.btn_add_designer = Button(self.tlevel_designers, image=self.add_icon, command=self.click_add_designer)
        self.btn_add_designer.grid(row=3, column=3, padx=25)
        btn_add_designer_ttp = CreateToolTip(self.btn_add_designer, 'Add designer')
        self.btn_remove_designer = Button(self.tlevel_designers, image=self.delete_icon, command=self.click_remove_designer)
        self.btn_remove_designer.grid(row=4, column=3, padx=25)
        btn_remove_designer_ttp = CreateToolTip(self.btn_remove_designer, 'Remove designer')
        self.trv_selected_designers = Treeview(self.tlevel_designers, height=10, columns=('N', 'Selected designers'),
                                                show='headings')
        self.trv_selected_designers.heading('#0', text='ID', anchor=CENTER)
        self.trv_selected_designers.heading('#1', text='N', anchor=CENTER)
        self.trv_selected_designers.heading('#2', text='Selected designers', anchor=CENTER)
        self.trv_selected_designers.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_selected_designers.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_selected_designers.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_selected_designers.bind("<Button-1>", self.click_trv_sdesigners)
        self.trv_selected_designers.grid(row=0, column=4, rowspan=10, pady=25, sticky=W)
        vsb_trv_seldes = Scrollbar(self.tlevel_designers, orient="vertical", command=self.trv_selected_designers.yview)
        vsb_trv_seldes.grid(row=0, column=5, rowspan=10, pady=25, sticky=NS)
        self.trv_selected_designers.configure(yscrollcommand=vsb_trv_seldes.set)
        sep_designers = Separator(self.tlevel_designers, orient=VERTICAL)
        sep_designers.grid(row=0, column=6, sticky=NS, padx=25, rowspan=10)
        btn_save_des = Button(self.tlevel_designers, image=self.check_icon, command=self.click_save_designers)
        btn_save_des.grid(row=0, column=7, padx=10, sticky=E)
        btn_save_des_ttp = CreateToolTip(btn_save_des, 'Save designers')
        btn_cancel_des = Button(self.tlevel_designers, image=self.cancel_icon, command=self.click_cancel_designers)
        btn_cancel_des.grid(row=1, column=7, padx=10, sticky=E)
        btn_cancel_des_ttp = CreateToolTip(btn_cancel_des, 'Cancel')

        # Components for administrating a problem
        frm_aux1 = Frame(self.tlevel_problem)
        frm_aux2 = LabelFrame(self.tlevel_problem, text='Expected solution')
        frm_aux2.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_sep9 = Label(frm_aux1)
        lbl_sep9.grid(row=0, column=0, padx=10, pady=10, rowspan=2)
        lbl_short_desc_prob = Label(frm_aux1, text='Short description*')
        lbl_short_desc_prob.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_short_desc_prob.grid(row=0, column=1, pady=10, sticky=W)
        lbl_description_prob = Label(frm_aux1, text='Description*')
        lbl_description_prob.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_description_prob.grid(row=1, column=1, pady=10, sticky=NW)
        lbl_sep10 = Label(frm_aux1)
        lbl_sep10.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        lbl_sep18 = Label(frm_aux1)
        lbl_sep18.grid(row=0, column=5, padx=10, pady=10, rowspan=2)
        self.txt_short_desc_prob = Text(frm_aux1, height=1, width=100)
        self.txt_short_desc_prob.config(font=TEXT_FONT)
        self.txt_short_desc_prob.grid(row=0, column=3, pady=10, sticky=W)
        self.txt_description_prob = Text(frm_aux1, height=10, width=100)
        self.txt_description_prob.config(font=TEXT_FONT)
        self.txt_description_prob.grid(row=1, column=3, pady=10, sticky=W)
        vsb_txt_desc_prob = Scrollbar(frm_aux1, orient="vertical", command=self.txt_description_prob.yview)
        vsb_txt_desc_prob.grid(row=1, column=4, pady=10, sticky=NS)
        self.txt_description_prob.configure(yscrollcommand=vsb_txt_desc_prob.set)
        self.btn_save_prob = Button(frm_aux1, image=self.check_icon, command=self.click_save_problem)
        btn_save_prob_ttp = CreateToolTip(self.btn_save_prob, 'Save problem')
        self.btn_cancel_prob = Button(frm_aux1, image=self.cancel_icon, command=self.click_cancel_problem)
        btn_cancel_prob_ttp = CreateToolTip(self.btn_cancel_prob, 'Cancel')
        self.btn_back_prob = Button(frm_aux1, image=self.back_icon, command=self.click_back_problem)
        btn_back_prob_ttp = CreateToolTip(self.btn_back_prob, 'Go back')
        frm_aux1.grid(row=0, column=0, padx=10, pady=10, sticky=EW)
        lbl_sep11 = Label(frm_aux2)
        lbl_sep11.grid(row=0, column=0, rowspan=6, padx=10, pady=10)
        lbl_sep12 = Label(frm_aux2)
        lbl_sep12.grid(row=0, column=2, rowspan=6, padx=10, pady=10)
        lbl_sep15 = Label(frm_aux2)
        lbl_sep15.grid(row=1, column=5, padx=20, pady=10, rowspan=5)
        lbl_sep16 = Label(frm_aux2)
        lbl_sep16.grid(row=1, column=7, padx=10, pady=10, rowspan=5)
        lbl_sep17 = Label(frm_aux2)
        lbl_sep17.grid(row=0, column=11, padx=10, pady=10, rowspan=6)
        lbl_annotations_esol = Label(frm_aux2, text='Notes\t\t')
        lbl_annotations_esol.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_annotations_esol.grid(row=0, column=1, pady=10, sticky=NW)
        self.txt_annotations_esol = Text(frm_aux2, height=10, width=97)
        self.txt_annotations_esol.config(font=TEXT_FONT)
        self.txt_annotations_esol.grid(row=0, column=3, pady=10, columnspan=6)
        vsb_txt_annot_iso = Scrollbar(frm_aux2, orient="vertical", command=self.txt_annotations_esol.yview)
        vsb_txt_annot_iso.grid(row=0, column=9, pady=10, sticky=NS)
        self.txt_annotations_esol.configure(yscrollcommand=vsb_txt_annot_iso.set)
        lbl_diagram_esol = Label(frm_aux2, text='Diagram')
        lbl_diagram_esol.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_diagram_esol.grid(row=1, column=1, pady=10, sticky=W)
        self.canvas_esol = Canvas(frm_aux2, width=110, height=110)
        self.canvas_esol.config(background='white', borderwidth=1)
        self.canvas_esol.grid(row=1, column=3, pady=10, rowspan=5, sticky=E)
        self.btn_open_esol = Button(frm_aux2, image=self.open_icon, command=self.click_upload_esol)
        btn_open_esol_ttp = CreateToolTip(self.btn_open_esol, 'Open image')
        self.btn_quit_esol = Button(frm_aux2, image=self.remove_icon, command=self.click_remove_esol)
        btn_quit_esol_ttp = CreateToolTip(self.btn_quit_esol, 'Remove image')
        self.btn_view_esol = Button(frm_aux2, image=self.view_icon, command=self.click_view_esol)
        btn_view_esol_ttp = CreateToolTip(self.btn_view_esol, 'View image')
        lbl_patterns = Label(frm_aux2, text='Patterns')
        lbl_patterns.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_patterns.grid(row=1, column=6, pady=10, sticky=W)
        self.lbx_patterns_esol = Listbox(frm_aux2, height=7, width=61, exportselection=0)
        self.lbx_patterns_esol.grid(row=1, column=8, pady=10, sticky=W, rowspan=5)
        vsb_lbx_pat_esol = Scrollbar(frm_aux2, orient="vertical", command=self.lbx_patterns_esol.yview)
        vsb_lbx_pat_esol.grid(row=1, column=9, pady=10, rowspan=5, sticky=NS)
        self.lbx_patterns_esol.configure(yscrollcommand=vsb_lbx_pat_esol.set)
        self.btn_pat_esol = Button(frm_aux2, image=self.patterns_icon, command=self.click_pat_esol)
        btn_pat_esol_ttp = CreateToolTip(self.btn_pat_esol, 'Configure patterns')
        frm_aux2.grid(row=1, column=0, padx=10, pady=10, sticky=EW)

        # Components for selecting patterns
        lbl_sep8 = Label(self.tlevel_patterns)
        lbl_sep8.grid(row=0, column=0, rowspan=10, padx=25, pady=25)
        self.trv_available_patterns = Treeview(self.tlevel_patterns, height=10, columns=('N', 'Available patterns'))
        self.trv_available_patterns.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_patterns.heading('#1', text='N', anchor=CENTER)
        self.trv_available_patterns.heading('#2', text='Available patterns', anchor=CENTER)
        self.trv_available_patterns.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_available_patterns.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available_patterns.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_available_patterns.bind("<Button-1>", self.click_trv_apatterns)
        self.trv_available_patterns.grid(row=0, column=1, rowspan=10, pady=25, sticky=W)
        vsb_trv_avpat = Scrollbar(self.tlevel_patterns, orient="vertical", command=self.trv_available_patterns.yview)
        vsb_trv_avpat.grid(row=0, column=2, rowspan=10, pady=25, sticky=NS)
        self.trv_available_patterns.configure(yscrollcommand=vsb_trv_avpat.set)
        self.btn_add_pattern = Button(self.tlevel_patterns, image=self.add_icon, command=self.click_add_pattern)
        self.btn_add_pattern.grid(row=3, column=3, padx=25)
        btn_add_pattern_ttp = CreateToolTip(self.btn_add_designer, 'Add pattern')
        self.btn_remove_pattern = Button(self.tlevel_patterns, image=self.delete_icon, command=self.click_remove_pattern)
        self.btn_remove_pattern.grid(row=4, column=3, padx=25)
        btn_remove_pattern_ttp = CreateToolTip(self.btn_remove_designer, 'Remove pattern')
        self.trv_selected_patterns = Treeview(self.tlevel_patterns, height=10, columns=('N', 'Selected patterns'))
        self.trv_selected_patterns.heading('#0', text='ID', anchor=CENTER)
        self.trv_selected_patterns.heading('#1', text='N', anchor=CENTER)
        self.trv_selected_patterns.heading('#2', text='Selected patterns', anchor=CENTER)
        self.trv_selected_patterns.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_selected_patterns.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_selected_patterns.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_selected_patterns.bind("<Button-1>", self.click_trv_spatterns)
        self.trv_selected_patterns.grid(row=0, column=4, rowspan=10, pady=25, sticky=W)
        vsb_trv_selpat = Scrollbar(self.tlevel_patterns, orient="vertical", command=self.trv_selected_patterns.yview)
        vsb_trv_selpat.grid(row=0, column=5, rowspan=10, pady=25, sticky=NS)
        self.trv_selected_patterns.configure(yscrollcommand=vsb_trv_selpat.set)
        sep_patterns = Separator(self.tlevel_patterns, orient=VERTICAL)
        sep_patterns.grid(row=0, column=6, sticky=NS, padx=25, rowspan=10)
        btn_save_pats = Button(self.tlevel_patterns, image=self.check_icon, command=self.click_save_patterns)
        btn_save_pats.grid(row=0, column=7, padx=10, sticky=E)
        btn_save_pats_ttp = CreateToolTip(btn_save_pats, 'Save patterns')
        btn_cancel_pats = Button(self.tlevel_patterns, image=self.cancel_icon, command=self.click_cancel_patterns)
        btn_cancel_pats.grid(row=1, column=7, padx=10, sticky=E)
        btn_cancel_pats_ttp = CreateToolTip(btn_cancel_pats, 'Cancel')

        # Components of expanded diagram
        self.canvas_expanded = Canvas(self.tlevel_diagram, width=500, height=500)
        self.canvas_expanded.config(background='white', borderwidth=1)
        self.canvas_expanded.grid()

    def retrieve_list_exp(self):
        """
        Function that shows the existing 'Experiments' in the home list (TreeView)
        """
        # Remove existing elements in the list
        for item in self.trv_available_exp.get_children():
            self.trv_available_exp.delete(item)
        self.directive = Message(action=92, information=[])
        self.connection = self.directive.send_directive(self.connection)
        for index, item in enumerate(self.connection.message.information):
            elements = item.split('¥')
            self.trv_available_exp.insert('', 'end', text=elements[0], values=(index+1, elements[1], elements[2],
                                                                               'One group' if elements[3] == '1' else
                                                                               'Two groups', elements[4]))
        if len(self.trv_available_exp.get_children()) != 0:
            self.trv_available_exp.selection_set(self.trv_available_exp.get_children()[0])

    def show_frm(self):
        """
        Displays the home list of the 'Experiments' form
        """
        self.style = Style()
        #self.style.layout('TNotebook')[("TNotebook.Tab", {"state": "normal"})]  # turn on tabs
        self.retrieve_list_exp()
        self.frm_child_exp_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        """
        Hides all forms that are currently active
        """
        self.hide_buttons()
        self.click_back_sc()
        self.clear_exp_fields()
        self.main_title.set('Experiments')
        self.frm_child_exp_list.grid_forget()
        self.frm_child_sc_list.grid_forget()
        self.frm_child_general_sc.grid_forget()

    def click_new_exp(self):
        """
        Function activated when 'New experiment' button is pressed, allows user to create a new experiment. Shows visual
        components for the creation of an experiment
        """
        self.view_decision = False  # Decision when viewing an experiment
        self.experiment = Experiment()
        self.load_available()
        self.show_cu_components()
        self.frm_child_exp_list.grid_forget()
        self.frm_child_sc_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_view_exp(self):
        """
        Function activated when 'View experiment' button is pressed, allows user to view info of an experiment
        """
        if len(self.trv_available_exp.selection()) == 1:
            id_exp_selected = int(self.trv_available_exp.item(self.trv_available_exp.selection())['text'])
            self.view_decision = True  # Decision when viewing an experiment
            # Retrieve selected experiment
            self.directive = Message(action=95, information=[id_exp_selected])
            self.connection = self.directive.send_directive(self.connection)
            self.experiment = Experiment(id=id_exp_selected, name=self.connection.message.information[0],
                                         description=self.connection.message.information[1],
                                         design_type=int(self.connection.message.information[2]),
                                         state=self.connection.message.information[3])
            # Fill visual components with retrieved information
            self.txt_name_exp.insert('1.0', self.experiment.name)
            self.txt_description_exp.insert('1.0', self.experiment.description)
            self.cbx_dt_exp.set('One group' if self.experiment.design_type == 1 else
                                'Two groups')
            self.txt_name_exp['bg'] = self.disabled_color
            self.txt_description_exp['bg'] = self.disabled_color
            self.txt_name_exp['state'] = DISABLED
            self.txt_description_exp['state'] = DISABLED
            self.cbx_dt_exp['state'] = DISABLED
            self.retrieve_list_sc()
            self.load_available()
            self.main_title.set('Experiment: ' + self.experiment.name)
            self.frm_child_exp_list.grid_forget()
            self.show_view_buttons()
            self.frm_child_sc_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_exp_list, title='No selection',
                                   message='You must select one item')

    def click_config_exp(self):
        """
        Function activated when 'Configure experiment' button is pressed, allows user to configure an existing experiment.
        When configuring an experiment, the user will be allowed to administrate experimental scenarios associated with
        the experiment
        """
        if len(self.trv_available_exp.selection()) == 1:
            id_exp_selected = int(self.trv_available_exp.item(self.trv_available_exp.selection())['text'])
            if self.trv_available_exp.item(self.trv_available_exp.selection())['values'][4] != 'finished':
                self.view_decision = False  # Decision when viewing an experiment
                self.directive = Message(action=95, information=[id_exp_selected])
                self.connection = self.directive.send_directive(self.connection)
                self.experiment = Experiment(id=id_exp_selected, name=self.connection.message.information[0],
                                             description=self.connection.message.information[1],
                                             design_type=int(self.connection.message.information[2]),
                                             state=self.connection.message.information[3])
                # Fill visual components with retrieved information
                self.txt_name_exp.insert('1.0', self.experiment.name)
                self.txt_description_exp.insert('1.0', self.experiment.description)
                self.cbx_dt_exp.set('One group' if self.experiment.design_type == 1 else
                                    'Two groups')
                if self.experiment.state == 'execution':
                    self.cbx_dt_exp['state'] = DISABLED

                # Retrieve selected experiment and its 'Experimental scenarios'
                self.retrieve_list_sc()
                self.load_available()
                self.main_title.set('Experiment: ' + self.experiment.name)
                self.show_cu_components()
                self.frm_child_exp_list.grid_forget()
                self.frm_child_sc_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
            else:
                messagebox.showwarning(parent=self.frm_child_exp_list, title='Blocked state',
                                       message='The experiment can not be configured because, it is finished')
        else:
            messagebox.showwarning(parent=self.frm_child_exp_list, title='No selection',
                                   message='You must select one item')

    def click_delete_exp(self):
        """
        Function activated when 'Delete' button is pressed, it removes an experiment from the database
        """
        if len(self.trv_available_exp.selection()) == 1:
            # MessageBox asking confirmation
            decision = messagebox.askyesno(parent=self.frm_child_exp_list, title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                id_exp_selected = int(self.trv_available_exp.item(self.trv_available_exp.selection())['text'])
                self.directive = Message(action=94, information=[id_exp_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:  # An error ocurred while deleting the item
                    messagebox.showerror(parent=self.frm_child_exp_list, title='Can not delete the item',
                                         message=self.connection.message.information[0])
                else:
                    self.retrieve_list_exp()
        else:
            messagebox.showwarning(parent=self.frm_child_exp_list, title='No selection', message='You must select one item')

    def click_exec_exp(self):
        """
        Execute an experiment and all it's configured experimental scenarios (change their states)
        """
        if len(self.trv_available_exp.selection()) == 1:
            id_exp_selected = int(self.trv_available_exp.item(self.trv_available_exp.selection())['text'])
            self.directive = Message(action=93, information=[id_exp_selected, 'execution'])
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.action == 5:  # An error ocurred while executing experiment
                messagebox.showerror(parent=self.frm_child_exp_list, title='Can not execute experiment',
                                     message=self.connection.message.information[0])
            self.retrieve_list_exp()
        else:
            messagebox.showwarning(parent=self.frm_child_exp_list, title='No selection',
                                   message='You must select one item')

    def click_finish_exp(self):
        """
        Function activated when 'Finish experiment' button is pressed. Finishes an experiment and generates a report
        for it. After finishing it, its structure wont be able to be modified, neither its information
        """
        if len(self.trv_available_exp.selection()) == 1:
            decision = messagebox.askyesno(parent=self.frm_child_exp_list, title='Confirmation',
                                           message='Are you sure you want to finish the experiment?')
            if decision:
                id_exp_selected = int(self.trv_available_exp.item(self.trv_available_exp.selection())['text'])
                self.directive = Message(action=93, information=[id_exp_selected, 'finished'])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:  # An error ocurred while finishing experiment
                    messagebox.showerror(parent=self.frm_child_exp_list, title='Can not finish experiment',
                                         message=self.connection.message.information[0])
                self.retrieve_list_exp()
        else:
            messagebox.showwarning(parent=self.frm_child_exp_list, title='No selection',
                                   message='You must select one item')

    def click_save_exp(self):
        """
        Function that saves all inserted information of a new experiment (if it is being created) or saves changes made
        to a selected experiment (updated)
        """
        if self.experiment.id == 0:  # Create an experiment
            validation_option = self.validate_exp_fields()
            if validation_option == 0:
                self.experiment.name = self.txt_name_exp.get('1.0', 'end-1c')
                self.experiment.description = self.txt_description_exp.get('1.0', 'end-1c')
                self.experiment.design_type = 1 if self.cbx_dt_exp.get() == 'One group' else 2
                self.directive = Message(action=91, information=[self.experiment.name, self.experiment.description,
                                                                 self.experiment.design_type])
                self.connection = self.directive.send_directive(self.connection)
                decision = messagebox.askyesno(parent=self.frm_child_sc_list, title='Keep configuring experiment',
                                               message='Do you want to continue configuring the scenarios associated with '
                                                       'the experiment?')
                if decision:
                    id_exp_selected = self.connection.message.information[0]
                    self.experiment.id = id_exp_selected
                    self.experiment.state = 'created'
                    self.main_title.set('Experiment: ' + self.experiment.name)
                else:
                    self.click_back_exp()
        else:   # Update selected experiment
            design_type_aux = 1 if self.cbx_dt_exp.get() == 'One group' else 2
            decision_aux = 1
            decision_remove_egroup = False
            # Section executed when an experiment is being updated (in warning state) and its design type is changed
            if design_type_aux != self.experiment.design_type and len(self.trv_available_sc.get_children()) != 0 and design_type_aux == 1:
                decision = messagebox.askyesno(parent=self.frm_child_sc_list, title='Warning!',
                                               message='You just changed the field \'design type\', this can cause LOSS '
                                                       'OF INFORMATION, are you sure you want to continue?')
                if decision:
                    decision_aux = 1
                    decision_remove_egroup = True
                else:
                    decision_aux = 0
            if decision_aux == 1:
                validation_option = self.validate_exp_fields()
                if validation_option == 0:
                    self.experiment.name = self.txt_name_exp.get('1.0', 'end-1c')
                    self.experiment.description = self.txt_description_exp.get('1.0', 'end-1c')
                    self.experiment.design_type = design_type_aux
                    self.directive = Message(action=93, information=[self.experiment.id, self.experiment.name,
                                                                     self.experiment.description,
                                                                     self.experiment.design_type])
                    self.connection = self.directive.send_directive(self.connection)
                    if decision_remove_egroup:
                        self.directive = Message(action=29, information=[self.experiment.id])
                        self.connection = self.directive.send_directive(self.connection)
                        self.directive = Message(action=89, information=[self.experiment.id])
                        self.connection = self.directive.send_directive(self.connection)
                    decision = messagebox.askyesno(parent=self.frm_child_sc_list, title='Keep configuring experiment',
                                                   message='Do you want to continue configuring the scenarios associated with '
                                                           'the experiment?')
                    if decision:
                        self.main_title.set('Experiment: ' + self.experiment.name)
                    else:
                        self.click_back_exp()

    def click_cancel_exp(self):
        """
        Function activated when 'Cancel experiment' button is pressed in general exp form, it goes back to the
        'Experiments' list home form (hides all active forms an show the list form)
        """
        decision = True
        if self.cbx_dt_exp.get() == 'One group':
            aux_d_type = 1
        elif self.cbx_dt_exp.get() == 'Two groups':
            aux_d_type = 2
        else:
            aux_d_type = 0
        if self.txt_name_exp.get('1.0', 'end-1c') != self.experiment.name or \
            self.txt_description_exp.get('1.0', 'end-1c') != self.experiment.description or \
                aux_d_type != self.experiment.design_type:
            decision = messagebox.askyesno(parent=self.frm_child_sc_list, title='Cancel',
                                           message='Are you sure you want to cancel?')
        if decision:
            self.click_back_exp()

    def click_back_exp(self):
        """
        Function activated when 'Back experiment' button is pressed in general exp form, it goes back to the
        'Experiments' list home form (hides all active forms an show the list form). It is only available in view
        experiment option
        """
        self.hide_frm()
        self.show_frm()

    def retrieve_list_sc(self):
        """
        This function displays the existing Experimental scenarios associated with an 'Experiment' into 'Expeimental
        scenarios list form'
        """
        # Remove existing elements in the list
        for item in self.trv_available_sc.get_children():
            self.trv_available_sc.delete(item)
        self.directive = Message(action=82, information=[self.experiment.id])
        self.connection = self.directive.send_directive(self.connection)
        for index, item in enumerate(self.connection.message.information):
            elements = item.split('¥')
            self.trv_available_sc.insert('', 'end', text=elements[0], values=(index+1, elements[1], elements[2],
                                                                              elements[3], elements[4]))
        if len(self.trv_available_sc.get_children()) != 0:
            self.trv_available_sc.selection_set(self.trv_available_sc.get_children()[0])

    def switch_availability(self, event):
        """
        This function is activated when the 'Double click Experimental scenarios TreeView' event ocurrs, it switches the
        availability if an experimental scenario for designers
        """
        if not self.view_decision:
            if self.trv_available_sc.item(self.trv_available_sc.selection())['text'] != '':
                values = self.trv_available_sc.item(self.trv_available_sc.focus())['values']
                if values[3] == 'created':
                    if values[4] == '':
                        self.trv_available_sc.item(self.trv_available_sc.focus(), values=(values[0], values[1], values[2],
                                                                                          values[3], '✓'))
                        aux_av = True
                    else:
                        self.trv_available_sc.item(self.trv_available_sc.focus(), values=(values[0], values[1], values[2],
                                                                                          values[3], ''))
                        aux_av = False
                    # Change availability in databse
                    self.directive = Message(action=83, information=['change_availability',
                                                                     int(self.trv_available_sc.item(self.trv_available_sc.focus())['text']), aux_av])
                    self.connection = self.directive.send_directive(self.connection)
                else:
                    messagebox.showwarning(parent=self.frm_child_sc_list, title='Locked scenario',
                                           message='The selected scenario can not be disabled because its state does not'
                                                   ' allows it')

    def click_new_sc(self):
        """
        Function activated when 'New' experimental scenario button is pressed, allows user to create a new experimental
        scenario. Shows visual components for the creation of an experimental scenario
        """
        if self.experiment.design_type != 0:  # Scenarios can be created only when an experiment is already created
            self.experimental_scenario = ExperimentalSC()
            self.cancel_sc_decision = False  # Decision changes when any changes in general sc configuration form is done
            self.reload_available()
            self.visual_problems = []
            self.txt_title_sc.focus_set()
            self.frm_child_general_sc['text'] = 'New experimental scenario'
            self.frm_child_sc_list.grid_forget()
            self.frm_child_general_sc.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
            if self.experiment.design_type == 2:
                self.frm_aux9.grid(row=1, column=0, sticky=W)
                self.frm_aux11.grid(row=1, column=0, sticky=W)
        else:
            messagebox.showerror(parent=self.frm_child_sc_list, title='No experiment',
                                 message='First configure and save a new experiment')

    def click_view_sc(self):
        """
        Function activated when 'View' experimental scenario button is pressed. It allows the user to view information
        of the selected experimental scenario, but can not make any changes.
        """
        if len(self.trv_available_sc.selection()) == 1:
            id_sc_selected = int(self.trv_available_sc.item(self.trv_available_sc.selection())['text'])
            # Retrieve selected Experimental scenario and its components
            self.directive = Message(action=85, information=[id_sc_selected])
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.information[5] is None:
                id_diagram = None
            else:
                id_diagram = int(self.connection.message.information[5])
            self.experimental_scenario = ExperimentalSC(id=id_sc_selected, title=self.connection.message.information[0],
                                                        description=self.connection.message.information[1],
                                                        access_code=self.connection.message.information[2],
                                                        id_experiment=int(self.connection.message.information[6]),
                                                        id_description_diagram=id_diagram,
                                                        connection=self.connection)
            self.experimental_scenario.retrieve_designers_groups()
            self.experimental_scenario.retrieve_patterns_groups(self.av_patterns)
            self.experimental_scenario.retrieve_problems(self.av_patterns)
            # Fill visual components
            self.txt_title_sc.insert('1.0', self.experimental_scenario.title)
            self.txt_description_sc.insert('1.0', self.experimental_scenario.description)
            self.file_dd = self.experimental_scenario.description_diagram
            if self.file_dd is not None:
                self.show_dd_file()
            self.txt_access_sc.insert('1.0', self.experimental_scenario.access_code)
            for index, item in enumerate(self.experimental_scenario.experimental_group):
                self.lbx_egroup.insert(END, '{}) {} {}'.format(index + 1, item.surname, item.name))
            for index, item in enumerate(self.experimental_scenario.control_group):
                self.lbx_cgroup.insert(END, '{}) {} {}'.format(index + 1, item.surname, item.name))
            self.visual_problems = []
            for index, item in enumerate(self.experimental_scenario.problems):
                self.visual_problems.append(item.id_visual)
                self.lbx_problems.insert(END, '{}) {}'.format(index + 1, item.brief_description))
            for index, item in enumerate(self.experimental_scenario.egroup_patterns):
                self.lbx_egroup_pat.insert(END, '{}) {}'.format(index + 1, item.get_main_section()))
            for index, item in enumerate(self.experimental_scenario.cgroup_patterns):
                self.lbx_cgroup_pat.insert(END, '{}) {}'.format(index + 1, item.get_main_section()))
            self.txt_title_sc['bg'] = self.disabled_color
            self.txt_description_sc['bg'] = self.disabled_color
            self.txt_access_sc['bg'] = self.disabled_color
            self.lbx_egroup['bg'] = self.disabled_color
            self.lbx_cgroup['bg'] = self.disabled_color
            self.lbx_egroup_pat['bg'] = self.disabled_color
            self.lbx_cgroup_pat['bg'] = self.disabled_color
            self.txt_title_sc['state'] = DISABLED
            self.txt_description_sc['state'] = DISABLED
            self.txt_access_sc['state'] = DISABLED
            self.lbx_egroup['state'] = DISABLED
            self.lbx_cgroup['state'] = DISABLED
            self.lbx_egroup_pat['state'] = DISABLED
            self.lbx_cgroup_pat['state'] = DISABLED
            self.frm_child_general_sc['text'] = 'View experimental scenario'
            if self.experiment.design_type == 2:
                self.frm_aux9.grid(row=1, column=0, sticky=W)
                self.frm_aux11.grid(row=1, column=0, sticky=W)
            self.frm_child_sc_list.grid_forget()
            self.frm_child_general_sc.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_sc_list, title='No selection', message='You must select one '
                                                                                                'item')

    def click_update_sc(self):
        """
        Function activated when 'Update' experimental scenario button is pressed, allows user to modify information of a
        selected scenario. Shows visual components for the modification of an experimental scenario.
        """
        if len(self.trv_available_sc.selection()) == 1:
            values = self.trv_available_sc.item(self.trv_available_sc.selection())['values']
            if values[3] == 'created':  # Scenario can be modified only when it is in creation process
                id_sc_selected = int(self.trv_available_sc.item(self.trv_available_sc.selection())['text'])
                # Retrieve selected Experimental scenario and its components
                self.directive = Message(action=85, information=[id_sc_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.information[5] is None:
                    id_diagram = None
                else:
                    id_diagram = int(self.connection.message.information[5])
                self.experimental_scenario = ExperimentalSC(id=id_sc_selected,
                                                            title=self.connection.message.information[0],
                                                            description=self.connection.message.information[1],
                                                            access_code=self.connection.message.information[2],
                                                            id_experiment=int(self.connection.message.information[6]),
                                                            id_description_diagram=id_diagram,
                                                            connection=self.connection)
                self.experimental_scenario.retrieve_designers_groups()
                self.experimental_scenario.retrieve_patterns_groups(self.av_patterns)
                self.experimental_scenario.retrieve_problems(self.av_patterns)
                self.reload_available()
                self.cancel_sc_decision = False  # Decision changes when any changes in general sc configuration form is done
                # Fill visual components
                self.txt_title_sc.insert('1.0', self.experimental_scenario.title)
                self.txt_description_sc.insert('1.0', self.experimental_scenario.description)
                self.file_dd = self.experimental_scenario.description_diagram
                if self.file_dd is not None:
                    self.show_dd_file()
                self.txt_access_sc.insert('1.0', self.experimental_scenario.access_code)
                for index, item in enumerate(self.experimental_scenario.experimental_group):
                    self.lbx_egroup.insert(END, '{}) {} {}'.format(index + 1, item.surname, item.name))
                for index, item in enumerate(self.experimental_scenario.control_group):
                    self.lbx_cgroup.insert(END, '{}) {} {}'.format(index + 1, item.surname, item.name))
                self.visual_problems = []
                for index, item in enumerate(self.experimental_scenario.problems):
                    self.visual_problems.append(item.id_visual)
                    self.lbx_problems.insert(END, '{}) {}'.format(index + 1, item.brief_description))
                for index, item in enumerate(self.experimental_scenario.egroup_patterns):
                    self.lbx_egroup_pat.insert(END, '{}) {}'.format(index + 1, item.get_main_section()))
                for index, item in enumerate(self.experimental_scenario.cgroup_patterns):
                    self.lbx_cgroup_pat.insert(END, '{}) {}'.format(index + 1, item.get_main_section()))
                self.frm_child_general_sc['text'] = 'Update experimental scenario'
                if self.experiment.design_type == 2:
                    self.frm_aux9.grid(row=1, column=0, sticky=W)
                    self.frm_aux11.grid(row=1, column=0, sticky=W)
                self.frm_child_sc_list.grid_forget()
                self.frm_child_general_sc.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
            else:
                messagebox.showerror(parent=self.frm_child_sc_list, title='Scenario locked',
                                     message='You are not allowed to modify the selected scenario, because '
                                             'it has finished or it is in execution')
        else:
            messagebox.showwarning(parent=self.frm_child_sc_list, title='No selection', message='You must select one '
                                                                                                'item')

    def click_delete_sc(self):
        """
        Function activated when 'Delete' experiment sc button is pressed, it removes an experimental scenario from the
        database
        """
        if len(self.trv_available_sc.selection()) == 1:
            values = self.trv_available_sc.item(self.trv_available_sc.selection())['values']
            if values[3] == 'created':  # Scenario can be deleted only when it is in creation process
                decision = messagebox.askyesno(parent=self.frm_child_general_sc, title='Confirmation',
                                               message='Are you sure you want to delete the item?')
                if decision:  # Confirm decision
                    id_sc_selected = int(self.trv_available_sc.item(self.trv_available_sc.selection())['text'])
                    # Retrieve selected Experimental scenario and its components
                    self.directive = Message(action=84, information=[id_sc_selected])
                    self.connection = self.directive.send_directive(self.connection)
                    self.retrieve_list_sc()
            else:
                messagebox.showerror(parent=self.frm_child_sc_list, title='Scenario locked',
                                     message='You are not allowed to delete the selected scenario, because '
                                             'it has finished or it is in execution')
        else:
            messagebox.showwarning(parent=self.frm_child_sc_list, title='No selection', message='You must select one '
                                                                                                'item')

    def click_save_sc(self):
        """
        Function that saves all inserted information of a new scenario component into the database
        """
        validation_option = self.validate_sc_fields()
        if validation_option == 0:
            patterns_decision = True
            if self.lbx_egroup_pat.size() == 0:
                patterns_decision = False
                # MessageBox asking confirmation not saving patterns for exp. group
                decision = messagebox.askyesno(parent=self.frm_child_general_sc, title='Confirmation',
                                               message='Are you sure you don\'t want to configure patterns for '
                                                       'experimental group?')
                if decision:    # Confirm saving without patterns for experimental group
                    patterns_decision = True
            if self.experiment.design_type == 2:
                if self.lbx_cgroup_pat.size() == 0:
                    patterns_decision = False
                    # MessageBox asking confirmation not saving patterns for ctrl. group
                    decision = messagebox.askyesno(parent=self.frm_child_general_sc, title='Confirmation',
                                                   message='Are you sure you don\'t want to configure patterns for '
                                                           'control group?')
                    if decision:  # Cancel
                        patterns_decision = True
            if patterns_decision:
                self.experimental_scenario.title = self.txt_title_sc.get('1.0', 'end-1c')
                self.experimental_scenario.description = self.txt_description_sc.get('1.0', 'end-1c')
                self.experimental_scenario.access_code = self.txt_access_sc.get('1.0', 'end-1c')
                if self.experimental_scenario.id == 0:  # New experimental scenario
                    # Ask if the new scenario turn into execution after creation
                    estado_inicial = 'created'
                    decision = messagebox.askyesno(parent=self.frm_child_general_sc, title='Execute scenario',
                                                   message='Do you want to execute the newly configured scenario?')
                    if decision:
                        estado_inicial = 'execution'
                    # Create context diagram in DB (if exist)
                    id_diagram = None
                    if self.file_dd is not None:
                        self.directive = Message(action=61,
                                                 information=[self.file_dd.file_bytes, self.file_dd.name, 'scen context'])
                        self.connection = self.directive.send_directive(self.connection)
                        id_diagram = self.connection.message.information[0]
                    # Create scenario in DB
                    self.directive = Message(action=81,
                                             information=[self.experimental_scenario.title,
                                                          self.experimental_scenario.description,
                                                          self.experimental_scenario.access_code, estado_inicial,
                                                          id_diagram, self.experiment.id, [], [], [], []])
                    for item in self.experimental_scenario.experimental_group:
                        self.directive.information[6].append(item.id)
                    for item in self.experimental_scenario.egroup_patterns:
                        self.directive.information[8].append(item.id)
                    if self.experiment.design_type == 2:
                        for item in self.experimental_scenario.control_group:
                            self.directive.information[7].append(item.id)
                        for item in self.experimental_scenario.cgroup_patterns:
                            self.directive.information[9].append(item.id)
                    self.connection = self.directive.send_directive(self.connection)
                    id_exp_scenario = self.connection.message.information[0]
                    # Create problems and its associated objects
                    for item in self.experimental_scenario.problems:
                        # Create expected solution diagram in DB
                        id_diagram = None
                        if item.solution.diagram is not None:
                            self.directive = Message(action=61,
                                                     information=[item.solution.diagram.file_bytes, item.solution.diagram.name,
                                                                  'exp sol'])
                            self.connection = self.directive.send_directive(self.connection)
                            id_diagram = self.connection.message.information[0]
                        # Create the expected solution in DB
                        self.directive = Message(action=56, information=[item.solution.annotations, id_diagram])
                        if item.solution.patterns:
                            self.directive.information.append([])
                            for item2 in item.solution.patterns:
                                self.directive.information[2].append(item2.id)
                        self.connection = self.directive.send_directive(self.connection)
                        id_solution = self.connection.message.information[0]
                        # Create the problem in DB
                        self.directive = Message(action=51,
                                                 information=[item.brief_description, item.description, id_solution,
                                                              id_exp_scenario])
                        self.connection = self.directive.send_directive(self.connection)
                else:   # Updating experimental scenario
                    # Update context diagram in DB (optional field)
                    id_diagram = None
                    delete_diagram = False
                    if self.file_dd is not None:    # A diagram is uploaded
                        if self.experimental_scenario.id_description_diagram is not None:
                            if self.experimental_scenario.description_diagram.file_bytes != self.file_dd.file_bytes: # Update diagram
                                self.directive = Message(action=63, information=[self.experimental_scenario.id_description_diagram,
                                                                                 self.file_dd.file_bytes, self.file_dd.name,
                                                                                 'scen context'])
                                self.connection = self.directive.send_directive(self.connection)
                            id_diagram = self.experimental_scenario.id_description_diagram
                        else:   # Create diagram
                            self.directive = Message(action=61,
                                                     information=[self.file_dd.file_bytes, self.file_dd.name,
                                                                  'scen context'])
                            self.connection = self.directive.send_directive(self.connection)
                            id_diagram = self.connection.message.information[0]
                    else:   # No diagram uploaded
                        if self.experimental_scenario.id_description_diagram is not None:   # Must delete existing diagram
                            id_diagram = self.experimental_scenario.id_description_diagram
                            delete_diagram = True
                    # Update scenario in DB
                    self.directive = Message(action=83,
                                             information=[self.experimental_scenario.id, self.experimental_scenario.title,
                                                          self.experimental_scenario.description,
                                                          self.experimental_scenario.access_code, id_diagram,
                                                          self.experiment.id, [], [], [], []])
                    for item in self.experimental_scenario.experimental_group:
                        self.directive.information[6].append(item.id)
                    for item in self.experimental_scenario.egroup_patterns:
                        self.directive.information[8].append(item.id)
                    if self.experiment.design_type == 2:
                        for item in self.experimental_scenario.control_group:
                            self.directive.information[7].append(item.id)
                        for item in self.experimental_scenario.cgroup_patterns:
                            self.directive.information[9].append(item.id)
                    self.connection = self.directive.send_directive(self.connection)
                    id_exp_scenario = self.experimental_scenario.id
                    if delete_diagram:  # Deleting diagram if necessary
                        self.directive = Message(action=64, information=[id_diagram])
                        self.connection = self.directive.send_directive(self.connection)
                    # Create problems and its associated objects (if neccesary)
                    for item in self.experimental_scenario.problems:
                        if item.id == 0:
                            # Create expected solution diagram in DB
                            self.directive = Message(action=61,
                                                     information=[item.solution.diagram.file_bytes,
                                                                  item.solution.diagram.name,
                                                                  'exp sol'])
                            self.connection = self.directive.send_directive(self.connection)
                            id_diagram = self.connection.message.information[0]
                            # Create the expected solution in DB
                            self.directive = Message(action=56, information=[item.solution.annotations, id_diagram])
                            if item.solution.patterns:
                                self.directive.information.append([])
                                for item2 in item.solution.patterns:
                                    self.directive.information[2].append(item2.id)
                            self.connection = self.directive.send_directive(self.connection)
                            id_solution = self.connection.message.information[0]
                            # Create the problem in DB
                            self.directive = Message(action=51,
                                                     information=[item.brief_description, item.description, id_solution,
                                                                  id_exp_scenario])
                            self.connection = self.directive.send_directive(self.connection)
                self.clear_sc_fields()
                self.frm_child_general_sc.grid_forget()
                self.retrieve_list_sc()
                self.frm_child_sc_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_cancel_sc(self):
        """
        Function activated when 'Cancel' button is pressed in 'Experimental scenario configuration form', it goes back
        to the 'Experimental scenarios list form'
        """
        decision = True
        if self.txt_title_sc.get('1.0', 'end-1c') != self.experimental_scenario.title or \
                self.txt_description_sc.get('1.0', 'end-1c') != self.experimental_scenario.description or \
                self.txt_access_sc.get('1.0', 'end-1c') != self.experimental_scenario.access_code or \
                self.file_dd != self.experimental_scenario.description_diagram or self.cancel_sc_decision:
            decision = messagebox.askyesno(parent=self.tlevel_problem, title='Cancel',
                                           message='Are you sure you want to cancel?')
        if decision:
            self.click_back_sc()

    def click_back_sc(self):
        """
        Function activated when 'Back' button is presed in 'Experimental scenario configuration form'. It returns the
        user to the 'Experimental scenarios list form'. (Does not perform any change with inserted info)
        """
        self.clear_sc_fields()
        # Change color to enabled (only when viewing option)
        self.txt_title_sc['bg'] = self.enabled_color
        self.txt_description_sc['bg'] = self.enabled_color
        self.txt_access_sc['bg'] = self.enabled_color
        self.lbx_egroup['bg'] = self.enabled_color
        self.lbx_cgroup['bg'] = self.enabled_color
        self.lbx_egroup_pat['bg'] = self.enabled_color
        self.lbx_cgroup_pat['bg'] = self.enabled_color
        self.frm_child_general_sc.grid_forget()
        self.frm_aux9.grid_forget() # Hide experimental group configuration
        self.frm_child_sc_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_cancel_problem(self):
        """
        Function activated when 'Cancel' button is pressed in 'Problem configuration tlevel', it goes back
        to the 'Experimental scenario configuration form'
        """
        decision = True
        if self.txt_short_desc_prob.get('1.0', 'end-1c') != self.problem.brief_description or \
                self.txt_description_prob.get('1.0', 'end-1c') != self.problem.description or \
                self.txt_annotations_esol.get('1.0', 'end-1c') != self.problem.solution.annotations or \
                self.lbx_patterns_esol.size() != len(self.problem.solution.patterns_id):
            decision = messagebox.askyesno(parent=self.tlevel_problem, title='Cancel',
                                           message='Are you sure you want to cancel?')
        if decision:
            self.click_back_problem()

    def click_cancel_designers(self):
        self.tlevel_designers.grab_release()
        self.tlevel_designers.withdraw()
        self.tlevel_designers_type = 0

    def click_cancel_patterns(self):
        self.tlevel_patterns.grab_release()
        self.tlevel_patterns.withdraw()
        self.tlevel_patterns_type = 0

    def click_cancel_diagram(self):
        self.tlevel_diagram.grab_release()
        self.tlevel_diagram.withdraw()

    def click_cgroup_sc(self):
        # Clear treeviews
        for item in self.trv_available_designers.get_children():
            self.trv_available_designers.delete(item)
        for item in self.trv_selected_designers.get_children():
            self.trv_selected_designers.delete(item)
        # Fill available designers treeview
        for index, item in enumerate(self.av_designers_cgroup):
            self.trv_available_designers.insert('', 'end', text=item.id,
                                                values=(index+1, '{} {}'.format(item.name, item.surname)))
        # Fill selected designers treeview
        for index, item in enumerate(self.experimental_scenario.control_group):
            self.trv_selected_designers.insert('', 'end', text=item.id,
                                               values=(index+1, '{} {}'.format(item.name, item.surname)))
        self.tlevel_designers.deiconify()
        self.tlevel_designers.grab_set()
        self.tlevel_designers_type = 2

    def click_egroup_sc(self):
        # Clear treeviews
        for item in self.trv_available_designers.get_children():
            self.trv_available_designers.delete(item)
        for item in self.trv_selected_designers.get_children():
            self.trv_selected_designers.delete(item)
        # Fill available designers treeview
        for index, item in enumerate(self.av_designers_egroup):
            self.trv_available_designers.insert('', 'end', text=item.id,
                                                values=(index+1, '{} {}'.format(item.name, item.surname)))
        # Fill selected designers treeview
        for index, item in enumerate(self.experimental_scenario.experimental_group):
            self.trv_selected_designers.insert('', 'end', text=item.id,
                                               values=(index+1, '{} {}'.format(item.name, item.surname)))
        '''
        for col in self.trv_available_designers['columns']:
            self.trv_available_designers.heading(col, text=col, command=lambda:
            treeview_sort_column(self.trv_available_designers, col, False))
        for col in self.trv_selected_designers['columns']:
            self.trv_selected_designers.heading(col, text=col, command=lambda:
                treeview_sort_column(self.trv_selected_designers, col, False))'''
        self.tlevel_designers.deiconify()
        self.tlevel_designers.grab_set()
        self.tlevel_designers_type = 1

    def click_upload_dd(self):
        """
        Create a File object that is uploaded by the user, validating that there is not a file uploaded already.
        """
        if self.file_dd is None:
            filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select image file",
                                                  filetypes=[("Diagrams", ".jpg .png .tiff")])
            if not filename:
                return  # user cancelled; stop this method
            self.file_dd = File()
            self.file_dd.read_file(filename)
            self.show_dd_file()

    def click_remove_dd(self):
        """
        Remove an uploaded file from the system validating it is already uploaded. This method also delete
        any image in the canvas that may be fulfilled with an image.
        """
        if self.file_dd is not None:  # if an image was already loaded
            self.canvas_dd.delete(self.file_dd.image)  # clear canvas
            self.render_dd = None
            self.file_dd = None

    def click_view_dd(self):
        # Fill summary problem canvas with retrieved image
        if self.file_dd is not None:
            load = Image.open(self.file_dd.filename)
            load = load.resize((500, 500), Image.ANTIALIAS)
            self.render_dd_exp = ImageTk.PhotoImage(load)
            self.canvas_expanded.delete()
            self.file_dd.image = self.canvas_expanded.create_image(0, 0, anchor='nw', image=self.render_dd_exp)  # and display new image
            self.tlevel_diagram.deiconify()
            self.tlevel_diagram.grab_set()
        else:
            messagebox.showwarning(parent=self.frm_child_general_sc, title='No diagram',
                                   message='No diagram uploaded in this section')

    def click_new_problem(self):
        self.problem = Problem()
        self.av_patterns_esol = self.av_patterns[:]
        self.txt_title_sc.focus_set()
        self.tlevel_problem.title('New problem')
        self.txt_short_desc_prob.focus_set()
        self.tlevel_problem.deiconify()
        self.tlevel_problem.grab_set()

    def click_delete_problem(self):
        element = self.lbx_problems.curselection()
        if element is not None:  # Check if listbox is selected
            if element:
                decision = messagebox.askyesno(parent=self.frm_child_general_sc, title='Confirmation',
                                               message='Are you sure you want to delete the item?')
                if decision:    # Confirm decision
                    index = element[0]
                    id_selected = self.visual_problems[index]
                    self.lbx_problems.delete(element)  # Remove from listbox
                    for item in reversed(self.experimental_scenario.problems):  # Remove from object
                        if item.id_visual == id_selected:
                            if self.experimental_scenario.id != 0:  # When updating an experimental scenario must remove from db
                                self.directive = Message(action=54, information=[item.id])
                                self.connection = self.directive.send_directive(self.connection)
                            self.experimental_scenario.problems.remove(item)
                            break
            else:
                messagebox.showwarning(parent=self.frm_child_general_sc, title='No selection',
                                       message='You must select one item')

    def click_view_problem(self):
        element = self.lbx_problems.curselection()
        if element is not None:  # Check if listbox is selected
            if element:
                index = element[0]
                id_selected = self.visual_problems[index]
                for item in self.experimental_scenario.problems:  # Find selected problem
                    if item.id_visual == id_selected:
                        self.problem = item
                        break
                self.txt_short_desc_prob['bg'] = self.disabled_color
                self.txt_description_prob['bg'] = self.disabled_color
                self.txt_annotations_esol['bg'] = self.disabled_color
                self.lbx_patterns_esol['bg'] = self.disabled_color
                self.txt_short_desc_prob.insert('1.0', self.problem.brief_description)
                self.txt_description_prob.insert('1.0', wrap_text(self.problem.description, 40))
                self.txt_annotations_esol.insert('1.0', wrap_text(self.problem.solution.annotations, 50))
                for item in self.problem.solution.patterns:
                    self.lbx_patterns_esol.insert(END, item.get_main_section())
                self.txt_short_desc_prob['state'] = DISABLED
                self.txt_description_prob['state'] = DISABLED
                self.txt_annotations_esol['state'] = DISABLED
                self.lbx_patterns_esol['state'] = DISABLED
                self.file_esol = self.problem.solution.diagram
                if self.file_esol is not None:
                    self.show_esol_file()
                self.tlevel_problem.title('View problem')
                self.tlevel_problem.deiconify()
                self.tlevel_problem.grab_set()
            else:
                messagebox.showwarning(parent=self.frm_child_general_sc, title='No selection',
                                       message='You must select one item')

    def click_save_problem(self):
        """
        Function that saves all inserted information when creating or updating a problem
        """
        validation_option = self.validate_problem_fields()
        if validation_option == 0:
            patterns_decision = True
            if self.lbx_patterns_esol.size() == 0:
                patterns_decision = False
                # MessageBox asking confirmation not saving patterns for exp. group
                decision = messagebox.askyesno(parent=self.tlevel_problem, title='Confirmation',
                                               message='Are you sure you don\'t want to configure patterns for '
                                                       'the expected solution?')
                if decision:
                    patterns_decision = True
            if patterns_decision:
                self.problem.brief_description = self.txt_short_desc_prob.get('1.0', 'end-1c')
                self.problem.description = self.txt_description_prob.get('1.0', 'end-1c')
                self.problem.solution.annotations = self.txt_description_prob.get('1.0', 'end-1c')
                self.problem.solution.diagram = self.file_esol
                self.experimental_scenario.problems.append(self.problem)
                self.visual_problems.append(self.problem.id_visual)
                self.lbx_problems.insert(END, '{}) {}'.format(self.lbx_problems.size() + 1, self.problem.brief_description))
                self.cancel_sc_decision = True  # Decision changes when any changes in general sc configuration form is done
                self.click_back_problem()

    def click_back_problem(self):
        """
        Function activated when 'Back' button is presed in 'Problem configuration tlevel'. It returns the
        user to the 'Experimental scenario configuration form'.
        """
        self.clear_problem_fields()
        self.tlevel_problem.grab_release()
        self.tlevel_problem.withdraw()

    def click_trv_adesigners(self, event):
        """
        Function that removes selection from 'available' tree view when 'selected' tree view is selected (in tlevel_designer)
        """
        self.trv_selected_designers.selection_remove(self.trv_selected_designers.selection())

    def click_add_designer(self):
        """
        Function that moves a 'Designer' from available tree view to selected tree view (in tlevel_designer)
        """
        if len(self.trv_available_designers.selection()) != 0 and len(self.trv_selected_designers.selection()) == 0:
            if len(self.trv_selected_designers.get_children()) != 0:
                index = self.trv_selected_designers.item(self.trv_selected_designers.get_children()[-1])['values'][0]
            else:
                index = 0
            for row in self.trv_available_designers.selection():
                index += 1
                values = self.trv_available_designers.item(row)['values']
                self.trv_selected_designers.insert('', 'end', text=self.trv_available_designers.item(row)['text'],
                                                   values=(index, values[1]))
                self.trv_available_designers.delete(row)

    def click_remove_designer(self):
        """
        Function that moves a 'Designer' from selected tree view to available tree view (in tlevel_designer)
        """
        if len(self.trv_selected_designers.selection()) != 0 and len(self.trv_available_designers.selection()) == 0:
            if len(self.trv_available_designers.get_children()) != 0:
                index = self.trv_available_designers.item(self.trv_available_designers.get_children()[-1])['values'][0]
            else:
                index = 0
            for row in self.trv_selected_designers.selection():
                index += 1
                values = self.trv_selected_designers.item(row)['values']
                self.trv_available_designers.insert('', 'end', text=self.trv_selected_designers.item(row)['text'],
                                                    values=(index, values[1]))
                self.trv_selected_designers.delete(row)

    def click_trv_sdesigners(self, event):
        """
        Function that removes selection from 'selected' tree view when 'available' tree view is selected (in tlevel_designer)
        """
        self.trv_available_designers.selection_remove(self.trv_available_designers.selection())

    def click_save_designers(self):
        aux_designers_av = []
        aux_designers_sel = []
        if self.tlevel_designers_type == 1: # Current view is for experimental group
            # Compare current available designers in treeview with available designers in object
            for item1 in reversed(self.av_designers_egroup):
                found = False
                for item2 in self.trv_available_designers.get_children():
                    if self.trv_available_designers.item(item2)['text'] == item1.id:
                        found = True
                        break
                if not found:   # Append designer to aux (added to selected ones) variable if designer not found and delete
                    # from current list
                    aux_designers_sel.append(item1)
                    self.av_designers_egroup.remove(item1)
            # Compare current selected designers in treeview with selected designers in object
            for item1 in reversed(self.experimental_scenario.experimental_group):
                found = False
                for item2 in self.trv_selected_designers.get_children():
                    if self.trv_selected_designers.item(item2)['text'] == item1.id:
                        found = True
                        break
                if not found:  # Append designer to aux (added to available ones) variable if designer not found and delete
                    # from current list
                    aux_designers_av.append(item1)
                    self.experimental_scenario.experimental_group.remove(item1)
            # Add object to respective objects
            for item in reversed(aux_designers_sel):
                self.experimental_scenario.experimental_group.append(item)
            for item in reversed(aux_designers_av):
                self.av_designers_egroup.append(item)
            # Clear patterns from listbox and insert new ones
            self.lbx_egroup.delete(0, END)
            for index, item in enumerate(self.experimental_scenario.experimental_group):
                self.lbx_egroup.insert(END, '{}) {} {}'.format(index+1, item.surname, item.name))
            self.cancel_sc_decision = True  # Decision changes when any changes in general sc configuration form is done
        elif self.tlevel_designers_type == 2:   # Current view is for control group
            # Compare current available designers in treeview with available designers in object
            for item1 in reversed(self.av_designers_cgroup):
                found = False
                for item2 in self.trv_available_designers.get_children():
                    if self.trv_available_designers.item(item2)['text'] == item1.id:
                        found = True
                        break
                if not found:  # Append designer to aux (added to selected ones) variable if designer not found and delete
                    # from current list
                    aux_designers_sel.append(item1)
                    self.av_designers_cgroup.remove(item1)
            # Compare current selected designers in treeview with selected designers in object
            for item1 in reversed(self.experimental_scenario.control_group):
                found = False
                for item2 in self.trv_selected_designers.get_children():
                    if self.trv_selected_designers.item(item2)['text'] == item1.id:
                        found = True
                        break
                if not found:  # Append designer to aux (added to available ones) variable if designer not found and delete
                    # from current list
                    aux_designers_av.append(item1)
                    self.experimental_scenario.control_group.remove(item1)
            # Add object to respective objects
            for item in reversed(aux_designers_sel):
                self.experimental_scenario.control_group.append(item)
            for item in reversed(aux_designers_av):
                self.av_designers_cgroup.append(item)
            # Clear patterns from listbox and insert new ones
            self.lbx_cgroup.delete(0, END)
            for index, item in enumerate(self.experimental_scenario.control_group):
                self.lbx_cgroup.insert(END, '{}) {} {}'.format(index + 1, item.surname, item.name))
            self.cancel_sc_decision = True  # Decision changes when any changes in general sc configuration form is done
        else:
            raise Exception('Tipo de grupo de disenadores es incongruente')
        self.tlevel_designers.grab_release()
        self.tlevel_designers.withdraw()
        self.tlevel_designers_type = 0

    def click_trv_apatterns(self, event):
        """
        Function that removes selection from 'available' tree view when 'selected' tree view is selected (in tlevel_patterns)
        """
        self.trv_selected_patterns.selection_remove(self.trv_selected_patterns.selection())

    def click_add_pattern(self):
        """
        Function that moves a 'Pattern' from available tree view to selected tree view (in tlevel_patterns)
        """
        if len(self.trv_available_patterns.selection()) != 0 and len(self.trv_selected_patterns.selection()) == 0:
            if len(self.trv_selected_patterns.get_children()) != 0:
                index = self.trv_selected_patterns.item(self.trv_selected_patterns.get_children()[-1])['values'][0]
            else:
                index = 0
            for row in self.trv_available_patterns.selection():
                index += 1
                values = self.trv_available_patterns.item(row)['values']
                self.trv_selected_patterns.insert('', 'end', text=self.trv_available_patterns.item(row)['text'],
                                                  values=(index, values[1]))
                self.trv_available_patterns.delete(row)

    def click_remove_pattern(self):
        """
        Function that moves a 'Pattern' from selected tree view to available tree view (in tlevel_patterns)
        """
        if len(self.trv_selected_patterns.selection()) != 0 and len(self.trv_available_patterns.selection()) == 0:
            if len(self.trv_available_patterns.get_children()) != 0:
                index = self.trv_available_patterns.item(self.trv_available_patterns.get_children()[-1])['values'][0]
            else:
                index = 0
            for row in self.trv_selected_patterns.selection():
                index += 1
                values = self.trv_selected_patterns.item(row)['values']
                self.trv_available_patterns.insert('', 'end', text=self.trv_selected_patterns.item(row)['text'],
                                                   values=(index, values[1]))
                self.trv_selected_patterns.delete(row)

    def click_trv_spatterns(self, event):
        """
        Function that removes selection from 'selected' tree view when 'available' tree view is selected (in tlevel_patterns)
        """
        self.trv_available_patterns.selection_remove(self.trv_available_patterns.selection())

    def click_save_patterns(self):
        aux_patterns_av = []
        aux_patterns_sel = []
        if self.tlevel_patterns_type == 1:  # Current view is for patterns of experimental group
            for item1 in reversed(self.av_patterns_egroup):
                found = False
                for item2 in self.trv_available_patterns.get_children():
                    if self.trv_available_patterns.item(item2)['text'] == item1.id:
                        found = True
                        break
                if not found:  # Append pattern to aux (added to selected ones) variable if designer not found and delete
                    # from current list
                    aux_patterns_sel.append(item1)
                    self.av_patterns_egroup.remove(item1)
            # Compare current selected patterns in treeview with selected patterns in object
            for item1 in reversed(self.experimental_scenario.egroup_patterns):
                found = False
                for item2 in self.trv_selected_patterns.get_children():
                    if self.trv_selected_patterns.item(item2)['text'] == item1.id:
                        found = True
                        break
                if not found:  # Append pattern to aux (added to available ones) variable if designer not found and delete
                    # from current list
                    aux_patterns_av.append(item1)
                    self.experimental_scenario.egroup_patterns.remove(item1)
            # Add object to respective objects
            for item in reversed(aux_patterns_sel):
                self.experimental_scenario.egroup_patterns.append(item)
            for item in reversed(aux_patterns_av):
                self.av_patterns_egroup.append(item)
            # Clear patterns from listbox and insert new ones
            self.lbx_egroup_pat.delete(0, END)
            for index, item in enumerate(self.experimental_scenario.egroup_patterns):
                self.lbx_egroup_pat.insert(END, '{}) {}'.format(index + 1, item.get_main_section()))
            self.cancel_sc_decision = True  # Decision changes when any changes in general sc configuration form is done
        elif self.tlevel_patterns_type == 2:     # Current view is for patterns of control group
            for item1 in reversed(self.av_patterns_cgroup):
                found = False
                for item2 in self.trv_available_patterns.get_children():
                    if self.trv_available_patterns.item(item2)['text'] == item1.id:
                        found = True
                        break
                if not found:  # Append pattern to aux (added to selected ones) variable if designer not found and delete
                    # from current list
                    aux_patterns_sel.append(item1)
                    self.av_patterns_cgroup.remove(item1)
            # Compare current selected patterns in treeview with selected patterns in object
            for item1 in reversed(self.experimental_scenario.cgroup_patterns):
                found = False
                for item2 in self.trv_selected_patterns.get_children():
                    if self.trv_selected_patterns.item(item2)['text'] == item1.id:
                        found = True
                        break
                if not found:  # Append pattern to aux (added to available ones) variable if designer not found and delete
                    # from current list
                    aux_patterns_av.append(item1)
                    self.experimental_scenario.cgroup_patterns.remove(item1)
            # Add object to respective objects
            for item in reversed(aux_patterns_sel):
                self.experimental_scenario.cgroup_patterns.append(item)
            for item in reversed(aux_patterns_av):
                self.av_patterns_cgroup.append(item)
            # Clear patterns from listbox and insert new ones
            self.lbx_cgroup_pat.delete(0, END)
            for index, item in enumerate(self.experimental_scenario.cgroup_patterns):
                self.lbx_cgroup_pat.insert(END, '{}) {}'.format(index + 1, item.get_main_section()))
            self.cancel_sc_decision = True  # Decision changes when any changes in general sc configuration form is done
        elif self.tlevel_patterns_type == 3:     # Current view is for patterns of expected solution
            for item1 in reversed(self.av_patterns_esol):
                found = False
                for item2 in self.trv_available_patterns.get_children():
                    if self.trv_available_patterns.item(item2)['text'] == item1.id:
                        found = True
                        break
                if not found:  # Append pattern to aux (added to selected ones) variable if designer not found and delete
                    # from current list
                    aux_patterns_sel.append(item1)
                    self.av_patterns_esol.remove(item1)
            # Compare current selected patterns in treeview with selected patterns in object
            for item1 in reversed(self.problem.solution.patterns):
                found = False
                for item2 in self.trv_selected_patterns.get_children():
                    if self.trv_selected_patterns.item(item2)['text'] == item1.id:
                        found = True
                        break
                if not found:  # Append pattern to aux (added to available ones) variable if designer not found and delete
                    # from current list
                    aux_patterns_av.append(item1)
                    self.problem.solution.patterns.remove(item1)
            # Add object to respective objects
            for item in reversed(aux_patterns_sel):
                self.problem.solution.patterns.append(item)
            for item in reversed(aux_patterns_av):
                self.av_patterns_esol.append(item)
            # Clear patterns from listbox and insert new ones
            self.lbx_patterns_esol.delete(0, END)
            for item in self.problem.solution.patterns:
                self.lbx_patterns_esol.insert(END, item.get_main_section())
        else:
            raise Exception('Tipo de grupo de patrones es incongruente')
        self.tlevel_patterns.grab_release()
        self.tlevel_patterns.withdraw()
        self.tlevel_patterns_type = 0

    def click_upload_esol(self):
        """
        Create a File object that is uploaded by the user, validating that there is not a file uploaded already.
        """
        if self.file_esol is None:
            filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select image file",
                                                  filetypes=[("Diagrams", ".jpg .png .tiff")])
            if not filename:
                return  # user cancelled; stop this method
            self.file_esol = File()
            self.file_esol.read_file(filename)
            self.show_esol_file()

    def click_remove_esol(self):
        """
        Remove an uploaded file from the system validating it is already uploaded. This method also delete
        any image in the canvas that may be fulfilled with an image.
        """
        if self.file_esol is not None:  # if an image was already loaded
            self.canvas_esol.delete(self.file_esol.image)  # clear canvas
            self.render_sol = None
            self.file_esol = None

    def click_view_esol(self):
        # Fill summary problem canvas with retrieved image
        if self.file_esol is not None:
            load = Image.open(self.file_esol.filename)
            load = load.resize((500, 500), Image.ANTIALIAS)
            self.render_sol = ImageTk.PhotoImage(load)
            self.canvas_expanded.delete()
            self.file_esol.image = self.canvas_expanded.create_image(0, 0, anchor='nw', image=self.render_sol)  # and display new image
            self.tlevel_diagram.deiconify()
            self.tlevel_diagram.grab_set()
        else:
            messagebox.showwarning(parent=self.tlevel_problem, title='No diagram',
                                   message='No diagram uploaded for the solution')

    def click_pat_esol(self):
        # Clear treeviews
        for item in self.trv_available_patterns.get_children():
            self.trv_available_patterns.delete(item)
        for item in self.trv_selected_patterns.get_children():
            self.trv_selected_patterns.delete(item)
        # Fill available patterns treeview
        for index, item in enumerate(self.av_patterns_esol):
            self.trv_available_patterns.insert('', 'end', text=item.id, values=(index+1, item.get_main_section()))
        # Fill selected patterns treeview
        for index, item in enumerate(self.problem.solution.patterns):
            self.trv_selected_patterns.insert('', 'end', text=item.id, values=(index+1, item.get_main_section()))
        self.tlevel_patterns.deiconify()
        self.tlevel_patterns.grab_set()
        self.tlevel_patterns_type = 3

    def click_cgroup_pat(self):
        # Clear treeviews
        for item in self.trv_available_patterns.get_children():
            self.trv_available_patterns.delete(item)
        for item in self.trv_selected_patterns.get_children():
            self.trv_selected_patterns.delete(item)
        # Fill available patterns treeview
        for index, item in enumerate(self.av_patterns_cgroup):
            self.trv_available_patterns.insert('', 'end', text=item.id, values=(index+1, item.get_main_section()))
        # Fill selected patterns treeview
        for index, item in enumerate(self.experimental_scenario.cgroup_patterns):
            self.trv_selected_patterns.insert('', 'end', text=item.id, values=(index+1, item.get_main_section()))
        self.tlevel_patterns.deiconify()
        self.tlevel_patterns.grab_set()
        self.tlevel_patterns_type = 2

    def click_egroup_pat(self):
        # Clear treeviews
        for item in self.trv_available_patterns.get_children():
            self.trv_available_patterns.delete(item)
        for item in self.trv_selected_patterns.get_children():
            self.trv_selected_patterns.delete(item)
        # Fill available patterns treeview
        for index, item in enumerate(self.av_patterns_egroup):
            self.trv_available_patterns.insert('', 'end', text=item.id, values=(index+1, item.get_main_section()))
        # Fill selected patterns treeview
        for index, item in enumerate(self.experimental_scenario.egroup_patterns):
            self.trv_selected_patterns.insert('', 'end', text=item.id, values=(index+1, item.get_main_section()))
        self.tlevel_patterns.deiconify()
        self.tlevel_patterns.grab_set()
        self.tlevel_patterns_type = 1

    def click_copy_pats(self):
        """
        When creating or updating an experimental scenario, copy assigned patterns from the experimental group to the
        control group
        :return:
        """
        if self.lbx_egroup_pat.size() != 0: # Chech experimental group has at least one pattern
            for item in reversed(self.av_patterns_cgroup):
                self.av_patterns_cgroup.remove(item)
            for item in reversed(self.experimental_scenario.cgroup_patterns): # Remove selected patterns in control group if inserted
                self.experimental_scenario.cgroup_patterns.remove(item)
            self.lbx_cgroup_pat.delete(0, END)
            for item in self.av_patterns_egroup:
                self.av_patterns_cgroup.append(item)
            for index, item in enumerate(self.experimental_scenario.egroup_patterns):  # Copy patterns from exp. group to control group
                self.experimental_scenario.cgroup_patterns.append(item)
                self.lbx_cgroup_pat.insert(END, '{}) {}'.format(index + 1, item.get_main_section()))
        else:
            messagebox.showwarning(parent=self.frm_child_general_sc, title='No patterns',
                                   message='You must insert at least one pattern to experimental group patterns\' list')

    def show_cu_components(self):
        """
        Shows buttons that are used when creating or updating an experimental scenario
        :return:
        """
        # Components frm_sc_list
        self.lbl_note_available.grid(row=6, column=1, columnspan=4, sticky=W)
        self.btn_new_sc.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        self.btn_edit_sc.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        self.btn_delete_sc.grid(row=3, column=0, pady=5, padx=5, sticky=E)
        self.btn_save_exp.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        self.btn_cancel_exp.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        self.btn_new_prob.grid(row=1, column=4, padx=20, pady=10, sticky=W)
        self.btn_delete_prob.grid(row=4, column=4, padx=20, pady=10, sticky=W)
        self.btn_save_sc.grid(row=0, column=0, padx=20, pady=10, sticky=W)
        self.btn_cancel_sc.grid(row=1, column=0, padx=20, pady=10, sticky=W)
        self.btn_save_prob.grid(row=0, column=6, padx=25, pady=5, sticky=W)
        self.btn_cancel_prob.grid(row=1, column=6, padx=25, pady=5, sticky=NW)
        self.btn_open_dd.grid(row=2, column=4, padx=10, pady=10, sticky=W)
        self.btn_quit_dd.grid(row=3, column=4, padx=10, pady=10, sticky=W)
        self.btn_egroup.grid(row=0, column=4, padx=20, pady=10, sticky=N)
        self.btn_cgroup.grid(row=0, column=4, padx=20, pady=10, sticky=N)
        self.btn_egroup_pat.grid(row=0, column=4, padx=20, pady=10, sticky=N)
        self.btn_cgroup_pat.grid(row=1, column=4, padx=20, pady=10, sticky=N)
        self.btn_copy_pat.grid(row=4, column=4, padx=20, pady=10, sticky=N)
        self.btn_pat_esol.grid(row=1, column=10, pady=10, padx=5, sticky=W)
        self.btn_open_esol.grid(row=1, column=4, padx=10, pady=5, sticky=W)
        self.btn_quit_esol.grid(row=2, column=4, padx=10, pady=5, sticky=W)
        self.txt_name_exp.focus_set()

    def show_view_buttons(self):
        """
        Shows buttons that are used when viewing an experimental scenario
        :return:
        """
        self.btn_view_sc.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        self.btn_back_exp.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        self.btn_view_prob.grid(row=1, column=4, padx=20, pady=10, sticky=NW)
        self.btn_back_sc.grid(row=0, column=0, padx=20, pady=5, sticky=NW)
        self.btn_back_prob.grid(row=0, column=6, padx=25, pady=5, sticky=NW)
        self.btn_view_dd.grid(row=2, column=4, padx=10, pady=10, sticky=NW)
        self.btn_view_esol.grid(row=1, column=4, padx=10, pady=10, sticky=NE)

    def hide_buttons(self):
        """
        Hides all buttons in forms associated with 'Experimental scenario administration' (frm_child_general_sc and
        tlevel_problem)
        """
        self.lbl_note_available.grid_forget()
        self.btn_new_sc.grid_forget()
        self.btn_edit_sc.grid_forget()
        self.btn_view_sc.grid_forget()
        self.btn_delete_sc.grid_forget()
        self.btn_save_exp.grid_forget()
        self.btn_cancel_exp.grid_forget()
        self.btn_back_exp.grid_forget()
        self.btn_save_sc.grid_forget()
        self.btn_cancel_sc.grid_forget()
        self.btn_back_sc.grid_forget()
        self.btn_save_prob.grid_forget()
        self.btn_cancel_prob.grid_forget()
        self.btn_back_prob.grid_forget()
        self.btn_new_prob.grid_forget()
        self.btn_delete_prob.grid_forget()
        self.btn_view_prob.grid_forget()
        self.btn_open_dd.grid_forget()
        self.btn_quit_dd.grid_forget()
        self.btn_view_dd.grid_forget()
        self.btn_egroup.grid_forget()
        self.btn_cgroup.grid_forget()
        self.btn_egroup_pat.grid_forget()
        self.btn_cgroup_pat.grid_forget()
        self.btn_copy_pat.grid_forget()
        self.btn_pat_esol.grid_forget()
        self.btn_open_esol.grid_forget()
        self.btn_quit_esol.grid_forget()
        self.btn_view_esol.grid_forget()

    def load_available(self):
        """
        Retrieve available objects from the server: Designers and Patterns
        :return:
        """
        self.directive = Message(action=22)
        self.connection = self.directive.send_directive(self.connection)
        self.av_designers = []
        # Create designers list as objects
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.av_designers.append(Designer(id=int(elements[0]), name=elements[1], surname=elements[2],
                                              user=elements[3]))
        self.av_patterns = Pattern.get_available_patterns(self.connection)

    def reload_available(self):
        """
        Restart available objects for administrating an object and compare them with existing objects if updating
        experimental scenario
        """
        self.av_designers_egroup = self.av_designers[:]
        self.av_designers_cgroup = self.av_designers[:]
        self.av_patterns_egroup = self.av_patterns[:]
        self.av_patterns_cgroup = self.av_patterns[:]
        if self.experimental_scenario.id != 0:  # If updating an experimental scenario
            # Remove existing designers of designers groups from available objects
            for item in self.experimental_scenario.experimental_group:
                for item2 in reversed(self.av_designers_egroup):
                    if item.id == item2.id:
                        self.av_designers_egroup.remove(item2)
            for item in self.experimental_scenario.control_group:
                for item2 in reversed(self.av_designers_cgroup):
                    if item.id == item2.id:
                        self.av_designers_cgroup.remove(item2)
            # Remove existing patterns of designers groups patterns from available objects
            for item in self.experimental_scenario.egroup_patterns:
                for item2 in reversed(self.av_patterns_egroup):
                    if item.id == item2.id:
                        self.av_patterns_egroup.remove(item2)
            for item in self.experimental_scenario.cgroup_patterns:
                for item2 in reversed(self.av_patterns_cgroup):
                    if item.id == item2.id:
                        self.av_patterns_cgroup.remove(item2)

    def clear_exp_fields(self):
        """
        Function that clear visual components tat may be fulfilled by the user when adding/editing information in
        'Experiment administration'
        """
        self.txt_name_exp['state'] = NORMAL
        self.txt_description_exp['state'] = NORMAL
        self.cbx_dt_exp['state'] = NORMAL
        self.txt_name_exp.delete('1.0', 'end-1c')
        self.txt_description_exp.delete('1.0', 'end-1c')
        self.txt_name_exp['bg'] = self.enabled_color
        self.txt_description_exp['bg'] = self.enabled_color
        # Remove existing elements in the list
        for item in self.trv_available_sc.get_children():
            self.trv_available_sc.delete(item)
        self.cbx_dt_exp.set('')

    def clear_sc_fields(self):
        """
        Function that clear visual components tat may be fulfilled by the user when adding/editing information in
        'Experimental scenario administration' (frm_child_general_sc)
        """
        self.btn_egroup['state'] = NORMAL
        self.btn_cgroup['state'] = NORMAL
        self.txt_title_sc['state'] = NORMAL
        self.txt_description_sc['state'] = NORMAL
        self.txt_access_sc['state'] = NORMAL
        self.lbx_egroup['state'] = NORMAL
        self.lbx_cgroup['state'] = NORMAL
        self.lbx_egroup_pat['state'] = NORMAL
        self.lbx_cgroup_pat['state'] = NORMAL
        self.txt_title_sc.delete('1.0', 'end-1c')
        self.txt_description_sc.delete('1.0', 'end-1c')
        self.txt_access_sc.delete('1.0', 'end-1c')
        self.lbx_problems.delete(0, END)
        self.lbx_egroup.delete(0, END)
        self.lbx_cgroup.delete(0, END)
        self.lbx_egroup_pat.delete(0, END)
        self.lbx_cgroup_pat.delete(0, END)
        if self.file_dd is not None:  # if an image was already loaded
            self.canvas_dd.delete(self.file_dd.image)  # clear canvas
            self.render_dd = None
            self.file_dd = None  # set file NULL
        self.tab_control.select(0)
        self.experimental_scenario = None
        self.frm_aux9.grid_forget()
        self.frm_aux11.grid_forget()

    def clear_problem_fields(self):
        """
        Function that clear visual components tat may be fulfilled by the user when adding/editing information in
        'Problem administration' (tlevel_problem)
        """
        self.txt_short_desc_prob['state'] = NORMAL
        self.txt_description_prob['state'] = NORMAL
        self.txt_annotations_esol['state'] = NORMAL
        self.lbx_patterns_esol['state'] = NORMAL
        self.txt_short_desc_prob['bg'] = self.enabled_color
        self.txt_description_prob['bg'] = self.enabled_color
        self.txt_annotations_esol['bg'] = self.enabled_color
        self.lbx_patterns_esol['bg'] = self.enabled_color
        self.txt_short_desc_prob.delete('1.0', 'end-1c')
        self.txt_description_prob.delete('1.0', 'end-1c')
        self.txt_annotations_esol.delete('1.0', 'end-1c')
        self.lbx_patterns_esol.delete(0, END)
        if self.file_esol is not None:  # if an image was already loaded
            self.canvas_esol.delete(self.file_esol.image)  # clear canvas
            self.file_esol = None  # set file NULL
            self.render_sol = None
        self.problem = None

    def validate_exp_fields(self):
        """
        Validation of fullfilled mandatory visual visual components when creating or updating an experiment
        :return:
        """
        if len(self.txt_name_exp.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.frm_child_sc_list, title='Missing information',
                                   message='You must insert a name for the experiment')
            return 1
        if len(self.txt_description_exp.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.frm_child_sc_list, title='Missing information',
                                   message='You must insert a description for the experiment')
            return 1
        if self.cbx_dt_exp.get() == 0:
            messagebox.showwarning(parent=self.frm_child_sc_list, title='Missing information',
                                   message='You must select a design type for the experiment')
            return 1
        return 0

    def validate_problem_fields(self):
        """
        Validation of fullfilled mandatory visual visual components when creating or updating a design problem
        :return:
        """
        if len(self.txt_short_desc_prob.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.tlevel_problem, title='Missing information',
                                   message='You must insert a brief description for the problem')
            return 1
        if len(self.txt_description_prob.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.tlevel_problem, title='Missing information',
                                   message='You must insert a full description for the problem')
            return 1
        return 0

    def validate_sc_fields(self):
        """
        Validation of fullfilled mandatory visual visual components when creating or updating an experimental scenario
        :return:
        """
        if len(self.txt_title_sc.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.frm_child_general_sc, title='Missing information',
                                   message='You must insert a title for the scenario')
            return 1
        if len(self.txt_description_sc.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.frm_child_general_sc, title='Missing information',
                                   message='You must insert a description for the scenario')
            return 1
        if len(self.txt_access_sc.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.frm_child_general_sc, title='Missing information',
                                   message='You must insert an access code for the scenario')
            return 1
        if self.experiment.design_type == 2:
            for item1 in self.experimental_scenario.experimental_group:
                for item2 in self.experimental_scenario.control_group:
                    if item1.id == item2.id:
                        messagebox.showwarning(parent=self.frm_child_general_sc, title='Missing information',
                                               message='At least one designer is in both, experimental and control group')
                        return 1
        if self.lbx_egroup.size() == 0:
            messagebox.showwarning(parent=self.frm_child_general_sc, title='Missing information',
                                   message='Experimental group can not be empty')
            return 1
        if self.experiment.design_type == 2 and self.lbx_cgroup.size() == 0:
            messagebox.showwarning(parent=self.frm_child_general_sc, title='Missing information',
                                   message='Control group can not be empty')
            return 1
        if self.lbx_problems.size() == 0:
            messagebox.showwarning(parent=self.frm_child_general_sc, title='Missing information',
                                   message='You must configure at least one problem')
            return 1
        return 0

    def show_dd_file(self):
        """
        Show the image in the visual canvas of a form only if it is empty, this function is called after uploading
        a diagram and depends of the file and the canvas where it has to be displayed, both given as parameters
        """
        load = Image.open(self.file_dd.filename)
        load = load.resize((110, 110), Image.ANTIALIAS)
        self.render_dd = ImageTk.PhotoImage(load)
        if self.file_dd.image is not None:  # if an image was already loaded
            self.canvas_dd.delete(self.file_dd.image)  # remove the previous image
        self.file_dd.image = self.canvas_dd.create_image(0, 0, anchor='nw', image=self.render_dd)  # and display new image

    def show_esol_file(self):
        """
        Show the image in the visual canvas of a form only if it is empty, this function is called after uploading
        a diagram and depends of the file and the canvas where it has to be displayed, both given as parameters
        """
        load = Image.open(self.file_esol.filename)
        load = load.resize((110, 110), Image.ANTIALIAS)
        self.render_sol = ImageTk.PhotoImage(load)
        if self.file_esol.image is not None:  # if an image was already loaded
            self.canvas_esol.delete(self.file_esol.image)  # remove the previous image
        self.file_esol.image = self.canvas_esol.create_image(0, 0, anchor='nw', image=self.render_sol)  # and display new image