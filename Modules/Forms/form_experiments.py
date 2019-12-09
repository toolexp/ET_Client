from tkinter import Label, LabelFrame, Frame, Text, Button, messagebox, PhotoImage, Scrollbar, Toplevel
from tkinter.constants import *
from tkinter.ttk import Treeview, Separator, Combobox
from Modules.Config.Data import Message, CreateToolTip, Experiment, wrap_text
from Modules.Config.Visual import *


class FormParentExperiment:
    def __init__(self, window, connection):
        self.frm_parent = Frame(window)
        self.initialize_components()
        self.frm_child = FormChildExperiment(self.frm_parent, connection, self.title)

    def initialize_components(self):
        lbl_experiment_title = Label(self.frm_parent, text='Experiments')
        self.title = lbl_experiment_title['text']
        lbl_experiment_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_experiment_title.grid(row=0, column=0, pady=20)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildExperiment:
    def __init__(self, frm_parent, connection, title):
        self.title = title
        self.connection = connection
        self.decide = True
        self.id_selected = 0
        self.frm_child_exp_list = LabelFrame(frm_parent)
        self.frm_child_sc_list = LabelFrame(frm_parent)
        self.frm_child_general_exp = LabelFrame(frm_parent)
        self.frm_child_general_exp.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        self.frm_child_general_sc = LabelFrame(frm_parent)
        self.frm_child_general_sc.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        self.tlevel_problem = Toplevel(self.frm_child_general_sc)
        self.tlevel_problem.protocol("WM_DELETE_WINDOW", self.click_cancel_problem)
        self.tlevel_problem.withdraw()
        self.tlevel_patterns = Toplevel(self.tlevel_problem)
        self.tlevel_patterns.protocol("WM_DELETE_WINDOW", self.click_cancel_patterns)
        self.tlevel_patterns.withdraw()
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
        defaultbg = self.frm_child_exp_list.cget('bg')

        # Components for experiment list form (list of experiments)
        lbl_sep1 = Label(self.frm_child_exp_list)
        lbl_sep1.grid(row=0, column=0, padx=25, pady=25)
        self.trv_available_exp = Treeview(self.frm_child_exp_list, height=20, columns=('Name', 'Description',
                                                                                       'Design type', 'State'))
        self.trv_available_exp.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_exp.heading('#1', text='Name', anchor=CENTER)
        self.trv_available_exp.heading('#2', text='Description', anchor=CENTER)
        self.trv_available_exp.heading('#3', text='Design type', anchor=CENTER)
        self.trv_available_exp.heading('#4', text='State', anchor=CENTER)
        self.trv_available_exp.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available_exp.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available_exp.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available_exp.column('#3', width=100, minwidth=100, stretch=NO, anchor=CENTER)
        self.trv_available_exp.column('#4', width=100, minwidth=100, stretch=NO, anchor=CENTER)
        self.trv_available_exp.grid(row=0, column=1, sticky=W, pady=25, rowspan=2)
        vsb_trv_av = Scrollbar(self.frm_child_exp_list, orient="vertical", command=self.trv_available_exp.yview)
        vsb_trv_av.grid(row=0, column=2, pady=25, rowspan=2, sticky=NS)
        self.trv_available_exp.configure(yscrollcommand=vsb_trv_av.set)
        frm_aux4 = Frame(self.frm_child_exp_list)
        btn_new_exp = Button(frm_aux4, image=self.new_icon, command=self.click_new_exp)
        btn_new_exp.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_new_exp_ttp = CreateToolTip(btn_new_exp, 'New experiment')
        btn_view_exp = Button(frm_aux4, image=self.view_icon, command=self.click_view_exp)
        btn_view_exp.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_view_exp_ttp = CreateToolTip(btn_view_exp, 'View experiment')
        btn_edit_exp = Button(frm_aux4, image=self.modify_icon, command=self.click_update_exp)
        btn_edit_exp.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_edit_exp_ttp = CreateToolTip(btn_edit_exp, 'Edit experiment')
        btn_delete_exp = Button(frm_aux4, image=self.remove_icon, command=self.click_delete_exp)
        btn_delete_exp.grid(row=3, column=0, pady=5, padx=5, sticky=E)
        btn_delete_exp_ttp = CreateToolTip(btn_delete_exp, 'Delete experiment')
        frm_aux5 = Frame(self.frm_child_exp_list)
        btn_config_exp = Button(frm_aux5, image=self.config_icon, command=self.click_config_exp)
        btn_config_exp.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_config_exp_ttp = CreateToolTip(btn_config_exp, 'Configure experiment')
        btn_exec_exp = Button(frm_aux5, image=self.exec_icon, command=self.click_exec_exp)
        btn_exec_exp.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_exec_exp_exp_ttp = CreateToolTip(btn_exec_exp, 'Execute experiment')
        btn_finish_exp = Button(frm_aux5, image=self.finish_icon, command=self.click_finish_exp)
        btn_finish_exp.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_finish_exp_ttp = CreateToolTip(btn_finish_exp, 'Finish experiment and generate report')
        frm_aux4.grid(row=0, column=4, pady=25, padx=25, sticky=NW)
        frm_aux5.grid(row=1, column=4, pady=25, padx=25, sticky=SW)

        # Components for general experiment form, where each experiment may be administrated
        lbl_name_exp = Label(self.frm_child_general_exp, text='Name')
        lbl_name_exp.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name_exp.grid(pady=10, padx=50, sticky=W)
        lbl_description_exp = Label(self.frm_child_general_exp, text='Description')
        lbl_description_exp.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_description_exp.grid(pady=10, padx=50, sticky=NW)
        lbl_design_type = Label(self.frm_child_general_exp, text='Design type')
        lbl_design_type.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_design_type.grid(pady=10, padx=50, sticky=NW)
        self.txt_name_exp = Text(self.frm_child_general_exp, height=1, width=80)
        self.txt_name_exp.config(font=TEXT_FONT)
        self.txt_name_exp.grid(row=0, column=1, padx=50, pady=10)
        self.txt_description_exp = Text(self.frm_child_general_exp, height=8, width=80)
        self.txt_description_exp.config(font=TEXT_FONT)
        self.txt_description_exp.grid(row=1, column=1, padx=50, pady=10, rowspan=8)
        self.cbx_dt_exp = Combobox(self.frm_child_general_exp, state="readonly")
        self.cbx_dt_exp['values'] = ['One experimental group', 'Two groups(control and exp.)']
        self.cbx_dt_exp.grid(row=9, column=1, padx=50, pady=10)
        sep_aux1 = Separator(self.frm_child_general_exp, orient=VERTICAL)
        sep_aux1.grid(row=0, column=2, sticky=NS, rowspan=10)
        btn_save = Button(self.frm_child_general_exp, image=self.save_icon, command=self.click_save_exp)
        btn_save.grid(row=0, column=3, padx=20)
        btn_save_ttp = CreateToolTip(btn_save, 'Save experiment')
        btn_cancel = Button(self.frm_child_general_exp, image=self.cancel_icon, command=self.click_cancel_exp)
        btn_cancel.grid(row=1, column=3, padx=20)
        btn_cancel_ttp = CreateToolTip(btn_cancel, 'Cancel')

    def initialize_variables(self):
        """
        Method that set the local variables to its initial state (empty)
        """
        self.directive = Message()
        self.experiment = None

    def retrieve_list(self):
        """
        Function that shows the existing 'Experiments' in the home list (TreeView)
        """
        # Remove existing elements in the list
        for item in self.trv_available_exp.get_children():
            self.trv_available_exp.delete(item)
        self.directive = Message(action=92, information=[])
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available_exp.insert('', 'end', text=elements[0], values=(elements[1], elements[2], elements[3],
                                                                               elements[4].capitalize()))

    def show_frm(self):
        """
        Displays the home list of the 'Experiments' form
        """
        self.retrieve_list()
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
        self.frm_child_general_exp.grid_forget()
        self.frm_child_general_sc.grid_forget()

    def click_delete_exp(self):
        """
        Function activated when 'Delete' button is pressed, it removes an experiment from the database
        """
        if self.trv_available_exp.item(self.trv_available_exp.selection())['text'] != '':
            # MessageBox asking confirmation
            decision = messagebox.askyesno(parent=self.frm_child_exp_list, title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                self.id_selected = int(self.trv_available_exp.item(self.trv_available_exp.selection())['text'])
                self.directive = Message(action=94, information=[self.id_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:  # An error ocurred while deleting the item
                    messagebox.showerror(parent=self.frm_child_exp_list, title='Can not delete the item',
                                         message=self.connection.message.information[0])
                else:
                    self.retrieve_list()
        else:
            messagebox.showwarning(parent=self.frm_child_exp_list, title='No selection', message='You must select an item')

    '''def click_new(self):
        """
        Function activated when 'New' button is pressed, allows user to create a new experiment. Shows visual components
        for the creation of an experiment
        """
        self.decide = True
        self.initialize_variables()
        self.experiment = Experiment()
        self.txt_name.focus_set()
        self.title_form = 'New'
        self.frm_child_list.grid_forget()
        self.frm_child_general['text'] = self.title_form + ' experiment'
        self.frm_child_general.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        """
        Function activated when 'Update' button is pressed, allows user to modify an existing experiment. Shows visual
        components for the modification of an experiment, fill visual components with current information
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            # Retrieve selected experiment
            self.directive = Message(action=95, information=[self.id_selected, 'validate'])
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.action == 5:  # An error ocurred while trying to update the item
                messagebox.showerror(parent=self.frm_child_list, title='Can not update the item',
                                     message=self.connection.message.information[0])
            else:
                self.decide = False  # Important variable when saving, it indicates the 'Experimental scenario' is being modified
                self.initialize_variables()
                self.experiment = Experiment(id=self.id_selected, name=self.connection.message.information[0],
                                             description=self.connection.message.information[1])
                # Fill visual components with retrieved information
                self.txt_name.insert('1.0', self.experiment.name)
                self.txt_description.insert('1.0', wrap_text(self.experiment.description, 85))
                self.frm_child_list.grid_forget()
                self.txt_name.focus_set()
                self.title_form = 'Update'
                self.frm_child_general['text'] = self.title_form + ' experiment'
                self.frm_child_general.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select an item')

    def click_save(self):
        """
        Function that saves all inserted information of a new experiment (if it is being created) or saves changes made
        to a selected experiment (updated)
        """
        if len(self.txt_name.get('1.0', 'end-1c')) != 0 and len(self.txt_description.get('1.0', 'end-1c')) != 0:
            self.experiment.name = self.txt_name.get('1.0', 'end-1c')
            self.experiment.description = self.txt_description.get('1.0', 'end-1c')
            if self.decide:
                # Create an experiment
                self.directive = Message(action=91, information=[self.experiment.name, self.experiment.description])
            else:
                # Update selected experiment
                self.directive = Message(action=93, information=[self.experiment.id, self.experiment.name,
                                                                 self.experiment.description])
            self.connection = self.directive.send_directive(self.connection)
            self.clear_fields()
            self.frm_child_general.grid_forget()
            self.show_frm()
        else:
            messagebox.showwarning(parent=self.frm_child_general, title='Missing information',
                                   message='There are mandatory fields that need to be filled!')

    def click_cancel(self):
        """
        Function activated when 'Cancel' button is pressed in General form, it goes back to the 'Experiments' list home
        form (hides all active forms an show the list form)
        """
        decision = messagebox.askyesno(parent=self.frm_child_general, title='Cancel',
                                       message='Are you sure you want to cancel?')
        if decision:
            self.clear_fields()
            self.hide_frm()
            self.show_frm()

    def clear_fields(self):
        """
        Function that clear visual components tat may be fulfilled by the user when adding/editing information
        """
        self.txt_name.delete('1.0', 'end-1c')
        self.txt_description.delete('1.0', 'end-1c')'''

    def click_new_exp(self):
        pass

    def click_view_exp(self):
        pass

    def click_update_exp(self):
        pass

    def click_save_exp(self):
        pass

    def click_cancel_exp(self):
        pass

    def click_exec_exp(self):
        pass

    def click_config_exp(self):
        pass

    def click_finish_exp(self):
        """
        Function activated when 'Finish experiment' button is pressed. Finishes an experiment and generates a report
        for it. After finishing it, its structure wont be able to be modified, neither its information
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            values = self.trv_available.item(
                self.trv_available.focus())['values']
            if values[3] == '':
                # MessageBox asking confirmation
                decision = messagebox.askyesno(parent=self.frm_child_list, title='Confirmation',
                                               message='Are you sure you want to finish the experiment?')
                if decision:
                    self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
                    self.directive = Message(action=93, information=[self.id_selected, 'finish'])
                    self.connection = self.directive.send_directive(self.connection)
                    ################
                    # Here generate the report
                    ################
                    self.retrieve_list()
            else:
                messagebox.showwarning(parent=self.frm_child_list, title='Experiment finished',
                                       message='The selected experiment is already finished')
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select an item')

    def click_cancel_problem(self):
        pass

    def click_cancel_patterns(self):
        pass