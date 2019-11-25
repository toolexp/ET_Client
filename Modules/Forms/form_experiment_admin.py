from tkinter import Label, LabelFrame, Frame, Text, Button, messagebox, PhotoImage, Scrollbar
from tkinter.constants import *
from tkinter.ttk import Treeview
from Modules.Config.Data import Message, CreateToolTip, Experiment, wrap_text
from Modules.Config.Visual import *


class FormParentExAdmin:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildExAdmin(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experiment_title = Label(self.frm_parent, text='Experiments')
        lbl_experiment_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_experiment_title.grid(row=0, column=0, pady=30)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0, pady=10, padx=10)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildExAdmin:
    def __init__(self, frm_parent, connection):
        self.connection = connection
        self.decide = True
        self.id_selected = 0
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_general = LabelFrame(frm_parent)
        self.frm_child_general.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        self.initialize_components()

    def initialize_components(self):
        """
        Method that initialize the visual components for each form associated with the local administration
        """
        # Resources for the Forms
        self.new_icon = PhotoImage(file=r"./Resources/create.png")
        self.modify_icon = PhotoImage(file=r"./Resources/modify.png")
        self.remove_icon = PhotoImage(file=r"./Resources/delete.png")
        self.save_icon = PhotoImage(file=r"./Resources/save.png")
        self.cancel_icon = PhotoImage(file=r"./Resources/cancel.png")
        self.finish_icon = PhotoImage(file=r"./Resources/finish.png")

        # Components for List FRM
        lbl_sep1 = Label(self.frm_child_list)
        lbl_sep1.grid(row=0, column=0, padx=25, pady=25)
        self.trv_available = Treeview(self.frm_child_list, height=7, columns=('Name', 'Description', 'Configured?',
                                                                              'Finished?'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.heading('#3', text='Configured?', anchor=CENTER)
        self.trv_available.heading('#4', text='Finished?', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.column('#3', width=75, minwidth=75, stretch=NO, anchor=CENTER)
        self.trv_available.column('#4', width=75, minwidth=75, stretch=NO, anchor=CENTER)
        self.trv_available.grid(row=0, column=1, sticky=W, pady=25, rowspan=2)
        vsb_trv_av = Scrollbar(self.frm_child_list, orient="vertical", command=self.trv_available.yview)
        vsb_trv_av.grid(row=0, column=2, pady=25, rowspan=2, sticky=NS)
        self.trv_available.configure(yscrollcommand=vsb_trv_av.set)
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New experiment')
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit experiment')
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete experiment')
        frm_aux5 = Frame(self.frm_child_list)
        btn_finish_experiment = Button(frm_aux5, image=self.finish_icon, command=self.click_finish_experiment)
        btn_finish_experiment.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_finish_experiment_ttp = CreateToolTip(btn_finish_experiment, 'Finish experiment and generate report')
        frm_aux4.grid(row=0, column=4, pady=25, padx=25, sticky=NW)
        frm_aux5.grid(row=1, column=4, pady=25, padx=25, sticky=SW)

        # Components for General info FRM
        lbl_name = Label(self.frm_child_general, text='Name')
        lbl_name.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_description = Label(self.frm_child_general, text='Description')
        lbl_description.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_description.grid(pady=10, padx=50, sticky=NW)
        self.txt_name = Text(self.frm_child_general, height=1, width=80)
        self.txt_name.config(font=TEXT_FONT)
        self.txt_name.grid(row=0, column=1, padx=50, pady=10)
        self.txt_description = Text(self.frm_child_general, height=8, width=80)
        self.txt_description.config(font=TEXT_FONT)
        self.txt_description.grid(row=1, column=1, padx=50, pady=10, rowspan=8)
        btn_save = Button(self.frm_child_general, image=self.save_icon, command=self.click_save)
        btn_save.grid(row=0, column=2, padx=20)
        btn_save_ttp = CreateToolTip(btn_save, 'Save experiment')
        btn_cancel = Button(self.frm_child_general, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel.grid(row=1, column=2, padx=20)
        btn_cancel_ttp = CreateToolTip(btn_cancel, 'Cancel')

    def initialize_variables(self):
        """
        Method that set the local variables to its initial state (empty)
        """
        self.directive = Message()
        self.experiment = None

    def retrieve_list(self):
        """
        This function shows the existing 'Experiments' in the home TreeView
        """
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=92, information=[])
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.directive = Message(action=82, information=[int(elements[0])])
            self.connection = self.directive.send_directive(self.connection)
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1], wrap_text(elements[2], 72),
                                                                           '✓' if len(self.connection.message.information) != 0 else '',
                                                                           elements[3]))

    def show_frm(self):
        """
        Displays the home page of the 'Experiments'
        """
        self.retrieve_list()
        if len(self.trv_available.get_children()) != 0:
            self.trv_available.selection_set(self.trv_available.get_children()[0])
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        """
        Hides all forms that ar curently active
        """
        self.clear_fields()
        self.frm_child_list.grid_forget()
        self.frm_child_general.grid_forget()

    def click_delete(self):
        """
        Function activated when 'Delete' button is pressed
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            # MessageBox asking confirmation
            decision = messagebox.askyesno(parent=self.frm_child_list, title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
                self.directive = Message(action=94, information=[self.id_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:  # An error ocurred while deleting the item
                    messagebox.showerror(parent=self.frm_child_list, title='Can not delete the item',
                                         message=self.connection.message.information[0])
                else:
                    self.retrieve_list()
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select an item')

    def click_new(self):
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
        Function activated when 'Update' button is pressed
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
        if len(self.txt_name.get('1.0','end-1c')) != 0 and len(self.txt_description.get('1.0','end-1c')) != 0:
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
        Function activated when 'Cancel' button is pressed in General form, it goes back to the 'Experimental scenarios'
         home page
        """
        decision = messagebox.askyesno(parent=self.frm_child_general, title='Cancel',
                                       message='Are you sure you want to cancel?')
        if decision:
            self.clear_fields()
            self.hide_frm()
            self.show_frm()

    def clear_fields(self):
        self.txt_name.delete('1.0', 'end-1c')
        self.txt_description.delete('1.0', 'end-1c')

    def click_finish_experiment(self):
        """
        Finish an experiment and generates a report for it. After finishing it, its structure wont be able to be modified,
        neither its information
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
                    # Here generate the report
                    self.retrieve_list()
            else:
                messagebox.showwarning(parent=self.frm_child_list, title='Experiment finished',
                                       message='The selected experiment is already finished')
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select an item')