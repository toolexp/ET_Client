from tkinter import Label, LabelFrame, Frame, Text, Button, messagebox, PhotoImage, Toplevel, Scrollbar
from tkinter.constants import *
from tkinter.ttk import Treeview, Combobox, Separator
from Modules.Config.Data import Message, ExperimentalSC, ScenarioComponent, CreateToolTip, Problem, Pattern, \
    wrap_text
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
        self.frm_child_exp_list = LabelFrame(frm_parent)
        self.frm_child_sc_list = LabelFrame(frm_parent)
        self.frm_child_component = LabelFrame(frm_parent)
        self.tlevel_designer = Toplevel(frm_parent)
        self.tlevel_designer.protocol("WM_DELETE_WINDOW", self.click_exit_designer)
        self.tlevel_designer.withdraw()
        self.initialize_components()

    def initialize_components(self):
        """
        Method that initialize the visual components for each form associated with the configuration of experiments
        """
        # Button icons used in the forms
        self.csv_icon = PhotoImage(file=r"./Resources/csv.png")
        self.next_icon = PhotoImage(file=r"./Resources/next.png")
        self.back_icon = PhotoImage(file=r"./Resources/back.png")
        self.view_icon = PhotoImage(file=r"./Resources/view.png")
        defaultbg = self.frm_child_exp_list.cget('bg')

        # Components for Experiments List form (list of experiments)
        lbl_sep1 = Label(self.frm_child_exp_list)
        lbl_sep1.grid(row=0, column=0, padx=25, pady=25, rowspan=16)
        lbl_available_rep = Label(self.frm_child_exp_list, text='Experiments with available reports', anchor=W)
        lbl_available_rep.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_available_rep.grid(row=0, column=1, pady=25, sticky=W)
        self.trv_available_exp = Treeview(self.frm_child_exp_list, height=15, columns=('Name', 'Description'))
        self.trv_available_exp.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_exp.heading('#1', text='Name', anchor=CENTER)
        self.trv_available_exp.heading('#2', text='Description', anchor=CENTER)
        self.trv_available_exp.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_exp.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available_exp.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available_exp.bind("<Double-1>", self.click_select_experiment)
        self.trv_available_exp.grid(row=1, column=1, rowspan=15, sticky=W, pady=25)
        vsb_trv_avex = Scrollbar(self.frm_child_exp_list, orient="vertical", command=self.trv_available_exp.yview)
        vsb_trv_avex.grid(row=1, column=2, rowspan=15, pady=25, sticky=NS)
        self.trv_available_exp.configure(yscrollcommand=vsb_trv_avex.set)
        btn_select_exp = Button(self.frm_child_exp_list, image=self.view_icon, command=self.click_select_experiment)
        btn_select_exp.grid(row=1, column=3, pady=25, padx=30, sticky=W)
        btn_select_exp_ttp = CreateToolTip(btn_select_exp, 'View experiment report')

        # Components for Experimental scenarios List form (list of experimental scenarios)
        lbl_sep2 = Label(self.frm_child_sc_list)
        lbl_sep2.grid(row=0, column=0, padx=25, pady=25, rowspan=16)
        lbl_available_sc_list = Label(self.frm_child_sc_list, anchor=W)
        lbl_available_sc_list.config(font=SUBTITLE2_FONT, fg=TEXT_COLOR)
        lbl_available_sc_list.grid(row=0, column=1, pady=25)
        self.trv_available_sc = Treeview(self.frm_child_sc_list, height=15, columns=('Experimental scenarios',))
        self.trv_available_sc.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_sc.heading('#1', text='Experimental scenarios', anchor=CENTER)
        self.trv_available_sc.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_sc.column('#1', width=400, minwidth=400, stretch=NO)
        self.trv_available_sc.bind("<ButtonRelease-1>", self.click_select_scenario)
        self.trv_available_sc.grid(row=1, column=1, rowspan=15, sticky=W, pady=25)
        vsb_trv_avsc = Scrollbar(self.frm_child_sc_list, orient="vertical", command=self.trv_available_sc.yview)
        vsb_trv_avsc.grid(row=1, column=2, rowspan=15, pady=25, sticky=NS)
        self.trv_available_sc.configure(yscrollcommand=vsb_trv_avsc.set)
        lbl_sep3 = Label(self.frm_child_sc_list)
        lbl_sep3.grid(row=1, column=3, padx=25, pady=25, rowspan=15)
        self.trv_available_comp = Treeview(self.frm_child_sc_list, height=15, columns='Components')
        self.trv_available_comp.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_comp.heading('#1', text='Components', anchor=CENTER)
        self.trv_available_comp.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_comp.column('#1', width=400, minwidth=400, stretch=NO)
        self.trv_available_comp.bind("<Double-1>", self.click_select_component)
        self.trv_available_comp.grid(row=1, column=4, rowspan=15, sticky=W, pady=25)
        vsb_trv_avcomp = Scrollbar(self.frm_child_sc_list, orient="vertical", command=self.trv_available_comp.yview)
        vsb_trv_avcomp.grid(row=1, column=5, rowspan=15, pady=25, sticky=NS)
        self.trv_available_comp.configure(yscrollcommand=vsb_trv_avcomp.set)
        btn_select_comp = Button(self.frm_child_sc_list, image=self.view_icon, command=self.click_select_component)
        btn_select_comp.grid(row=1, column=6, pady=25, padx=30, sticky=W)
        btn_select_comp_ttp = CreateToolTip(btn_select_comp, 'View component report')
        btn_back_sc = Button(self.frm_child_sc_list, image=self.back_icon, command=self.click_back_scenario)
        btn_back_sc.grid(row=2, column=6, pady=5, padx=30, sticky=W)
        btn_back_sc_ttp = CreateToolTip(btn_back_sc, 'Go back')

        # Components for Component form (summary and details)
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
        self.txt_problem_desc.config(font=TEXT_FONT, bg=defaultbg)
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
        btn_back_component_ttp = CreateToolTip(btn_back_component, 'Generate .csv file')
        btn_csv = Button(self.frm_child_component, image=self.csv_icon, command=self.click_csv)
        btn_csv.grid(row=1, column=5, padx=30, pady=5)
        btn_csv_ttp = CreateToolTip(btn_csv, 'Generate .csv file')

        # Components for Designer detail TopLevel window

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
        #self.clear_fields()
        self.frm_child_exp_list.grid_forget()
        self.frm_child_sc_list.grid_forget()
        self.frm_child_component.grid_forget()

    def retrieve_experiments(self):
        """
        This function shows the existing 'Experiments' in the home TreeView
        """
        pass
        # Remove existing elements in the list
        '''for item in self.trv_available_exp.get_children():
            self.trv_available_exp.delete(item)
        self.directive = Message(action=92, information=[])
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available_exp.insert('', 'end', text=elements[0], values=(elements[1], wrap_text(elements[2], 72)))'''

    def retrieve_list(self):
        """
        This function shows the existing Experimental scenarios in an 'Experiment'
        """
        pass
        # Remove existing elements in the list
        '''self.current_availability = []  # Saves initial availability for experimental scenarios, so any change made later could be saved
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=82, information=[self.id_selected_exp])
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1], wrap_text(elements[2], 72),
                                                                           elements[3], elements[4]))
            aux = True if elements[3] == '✓' else False
            self.current_availability.append(aux)'''

    def click_select_experiment(self, event=None):
        """
        This function is activated when the 'Click Experiments TreeView' event ocurrs, it indicates than an experiments
        has been selected
        """
        self.frm_child_exp_list.grid_forget()
        self.frm_child_sc_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        '''if self.trv_available_exp.item(self.trv_available_exp.selection())['text'] != '':
            self.id_selected_exp = int(self.trv_available_exp.item(self.trv_available_exp.selection())['text'])
            # Retrieve selected experiment and its 'Experimental scenarios'
            self.retrieve_list()
            self.frm_child_exp_list.grid_forget()
            if len(self.trv_available.get_children()) != 0:
                self.trv_available.selection_set(self.trv_available.get_children()[0])
                self.refresh_crud_buttons()
            self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)'''

    def click_select_scenario(self, event=None):
        pass

    def click_back_scenario(self):
        """
        Function activated when 'Cancel scenario' button is pressed, it hides the Experimental scenarios List form.
        It returns to Experiments list home form
        """
        self.frm_child_sc_list.grid_forget()
        self.frm_child_exp_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_select_component(self):
        """
        Function activated when a scenario component is selected
        """
        self.frm_child_sc_list.grid_forget()
        self.frm_child_component.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_csv(self):
        pass

    def click_back_component(self):
        self.frm_child_component.grid_forget()
        self.frm_child_sc_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_exit_designer(self):
        pass