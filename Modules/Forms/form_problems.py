import os
from tkinter import Label, LabelFrame, Text, Button, Canvas, messagebox, Frame, filedialog, PhotoImage, Toplevel, \
    Scrollbar
from tkinter.constants import *
from Modules.Config.Data import Message, Problem, Solution, File, Pattern, wrap_text, CreateToolTip
from tkinter.ttk import Treeview, Separator
from PIL import ImageTk, Image
from Modules.Config.Visual import *


class FormParentProblem:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildProblem(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Problems')
        lbl_experimenter_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_experimenter_title.grid(row=0, column=0, columnspan=9, pady=50)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildProblem:
    def __init__(self, frm_parent, connection):
        self.connection = connection
        self.decide = True
        self.file = None
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_crud = LabelFrame(frm_parent)
        self.frm_child_crud.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        self.tlevel_diagram_summary = Toplevel(frm_parent)
        self.tlevel_diagram_summary.title('Diagram')
        self.tlevel_diagram_summary.protocol("WM_DELETE_WINDOW", self.close_tlevel_diagram)
        self.tlevel_diagram_summary.withdraw()
        self.tlevel_patterns_solution = Toplevel(frm_parent)
        self.tlevel_patterns_solution.title('Set patterns for the ideal solution')
        self.tlevel_patterns_solution.protocol("WM_DELETE_WINDOW", self.click_cancel_pat)
        self.tlevel_patterns_solution.withdraw()
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
        self.open_icon = PhotoImage(file=r"./Resources/open.png")
        self.add_icon = PhotoImage(file=r"./Resources/right.png")
        self.delete_icon = PhotoImage(file=r"./Resources/left.png")
        self.back_icon = PhotoImage(file=r"./Resources/back.png")
        self.next_icon = PhotoImage(file=r"./Resources/next.png")
        defaultbg = self.frm_child_crud.cget('bg')

        # Components for List FRM
        lbl_sep1 = Label(self.frm_child_list)
        lbl_sep1.grid(row=0, column=0, padx=25, pady=25)
        self.trv_available = Treeview(self.frm_child_list, height=7, columns='Name')
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=400, minwidth=400, stretch=NO)
        self.trv_available.grid(row=0, column=1, rowspan=2, sticky=W, pady=25)
        self.trv_available.bind("<ButtonRelease-1>", self.select_problem_summary)
        vsb_trv_av = Scrollbar(self.frm_child_list, orient="vertical", command=self.trv_available.yview)
        vsb_trv_av.grid(row=0, column=2, rowspan=2, pady=25, sticky=NS)
        self.trv_available.configure(yscrollcommand=vsb_trv_av.set)
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New problem')
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit problem')
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete problem')
        frm_aux4.grid(row=0, column=4, rowspan=2, pady=25, padx=25, sticky=NW)
        sep_problem = Separator(self.frm_child_list, orient=VERTICAL)
        sep_problem.grid(row=0, column=5, sticky=NS, rowspan=2, padx=25)
        lbl_sep3 = Label(self.frm_child_list)
        lbl_sep3.grid(row=0, column=6, padx=15, pady=25)
        lbl_details = Label(self.frm_child_list, text='Details')
        lbl_details.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_details.grid(row=0, column=7, sticky=W, pady=25)
        self.txt_summary = Text(self.frm_child_list, height=18, width=50)
        self.txt_summary.config(font=TEXT_FONT, bg=defaultbg)
        self.txt_summary.grid(row=1, column=7, pady=10, sticky=NW)
        vsb_txt_sum = Scrollbar(self.frm_child_list, orient="vertical", command=self.txt_summary.yview)
        vsb_txt_sum.grid(row=1, column=8, pady=10, sticky=NS)
        self.txt_summary.configure(yscrollcommand=vsb_txt_sum.set)
        self.btn_view_diagram = Button(self.frm_child_list, text='View >>\ndiagram', command=self.click_expand_diagram)
        self.btn_view_diagram.grid(row=1, column=9, padx=25, sticky=NW)
        lbl_sep4 = Label(self.frm_child_list)
        lbl_sep4.grid(row=0, column=10, padx=15, pady=25)

        self.canvas_summary = Canvas(self.tlevel_diagram_summary, width=500, height=500)
        self.canvas_summary.config(background='white', borderwidth=1)
        self.canvas_summary.grid()

        # Components for CRUD FRM
        frm_aux1 = Frame(self.frm_child_crud)
        frm_aux2 = LabelFrame(self.frm_child_crud, text='Ideal solution')
        frm_aux2.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_name = Label(frm_aux1, text='Name')
        lbl_name.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=NW)
        lbl_description = Label(frm_aux1, text='Description')
        lbl_description.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_description.grid(pady=10, padx=50, sticky=NW)
        self.txt_name_prob = Text(frm_aux1, height=1, width=60)
        self.txt_name_prob.config(font=TEXT_FONT)
        self.txt_name_prob.grid(row=0, column=1, pady=10, padx=50,)
        self.txt_description_prob = Text(frm_aux1, height=6, width=60)
        self.txt_description_prob.config(font=TEXT_FONT)
        self.txt_description_prob.grid(row=1, column=1, pady=10, padx=50,)
        lbl_annotations = Label(frm_aux2, text='Notes \n(optional)')
        lbl_annotations.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_annotations.grid(pady=10, padx=50, sticky=NW)
        self.txt_annotations = Text(frm_aux2, height=6, width=60)
        self.txt_annotations.config(font=TEXT_FONT)
        self.txt_annotations.grid(row=0, column=1, pady=10, padx=50, columnspan=3)
        lbl_diagram = Label(frm_aux2, text='File')
        lbl_diagram.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_diagram.grid(row=1, column=0, pady=10, padx=50, sticky=NW)
        btn_open = Button(frm_aux2, image=self.open_icon, command=self.click_upload_file)
        btn_open.grid(row=1, column=2, padx=50, pady=10, sticky=W)
        btn_open_ttp = CreateToolTip(btn_open, 'Open file')
        btn_quit = Button(frm_aux2, image=self.remove_icon, command=self.click_remove_file)
        btn_quit.grid(row=2, column=2, padx=50, pady=10, sticky=W)
        btn_quit_ttp = CreateToolTip(btn_quit, 'Remove file')
        self.canvas = Canvas(frm_aux2, width=160, height=160)
        self.canvas.config(background='white', borderwidth=1)
        self.canvas.grid(row=1, column=1, padx=50, pady=10, rowspan=5, sticky=W)
        btn_patterns = Button(frm_aux2, text='Patterns of the solution >>', command=self.click_associate_patterns)
        btn_patterns.grid(row=6, column=1, padx=50, pady=10, sticky=W)

        btn_save = Button(self.frm_child_crud, image=self.save_icon, command=self.click_save)
        btn_save.grid(row=1, column=5, padx=35)
        btn_save_ttp = CreateToolTip(btn_save, 'Save')
        btn_cancel = Button(self.frm_child_crud, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel.grid(row=2, column=5, padx=35)
        btn_cancel_ttp = CreateToolTip(btn_cancel, 'Cancel')
        frm_aux1.grid(row=1, column=0, pady=10, padx=10, columnspan=5, rowspan=5)
        frm_aux2.grid(row=8, column=0, pady=10, padx=10, columnspan=5, rowspan=10)

        # Components for patterns selection
        lbl_sep3 = Label(self.tlevel_patterns_solution)
        lbl_sep3.grid(row=0, column=0, padx=25, pady=25)
        self.trv_available_patterns = Treeview(self.tlevel_patterns_solution, height=5, columns=('Available patterns',))
        self.trv_available_patterns.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_patterns.heading('#1', text='Available patterns', anchor=CENTER)
        self.trv_available_patterns.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_available_patterns.column('#1', width=300, minwidth=200, stretch=NO)
        self.trv_available_patterns.bind("<Button-1>", self.click_trv_aptterns)
        self.trv_available_patterns.grid(row=0, column=1, rowspan=10, sticky=NW, pady=25)
        vsb_trv_avp = Scrollbar(self.tlevel_patterns_solution, orient="vertical", command=self.trv_available_patterns.yview)
        vsb_trv_avp.grid(row=0, column=2, rowspan=10, pady=25, sticky=NS)
        self.trv_available_patterns.configure(yscrollcommand=vsb_trv_avp.set)
        lbl_sep4 = Label(self.tlevel_patterns_solution)
        lbl_sep4.grid(row=0, column=3, padx=25, pady=25)
        lbl_sep5 = Label(self.tlevel_patterns_solution)
        lbl_sep5.grid(row=0, column=5, padx=25, pady=25)
        self.trv_selected_patterns = Treeview(self.tlevel_patterns_solution, height=5, columns=('Selected patterns',))
        self.trv_selected_patterns.heading('#0', text='ID', anchor=CENTER)
        self.trv_selected_patterns.heading('#1', text='Selected patterns', anchor=CENTER)
        self.trv_selected_patterns.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_selected_patterns.column('#1', width=300, minwidth=300, stretch=NO)
        self.trv_selected_patterns.bind("<Button-1>", self.click_trv_spatterns)
        self.trv_selected_patterns.grid(row=0, column=6, rowspan=10, sticky=NW, pady=25)
        vsb_trv_sep = Scrollbar(self.tlevel_patterns_solution, orient="vertical", command=self.trv_selected_patterns.yview)
        vsb_trv_sep.grid(row=0, column=7, rowspan=10, pady=25, sticky=NS)
        self.trv_selected_patterns.configure(yscrollcommand=vsb_trv_sep.set)
        lbl_sep6 = Label(self.tlevel_patterns_solution)
        lbl_sep6.grid(row=0, column=8, padx=25, pady=25)
        btn_add = Button(self.tlevel_patterns_solution, image=self.add_icon, command=self.click_add)
        btn_add.grid(row=1, column=4)
        btn_add_ttp = CreateToolTip(btn_add, 'Add pattern')
        btn_remove = Button(self.tlevel_patterns_solution, image=self.delete_icon, command=self.click_remove)
        btn_remove.grid(row=2, column=4)
        btn_remove_ttp = CreateToolTip(btn_remove, 'Remove pattern')
        sep_patterns = Separator(self.tlevel_patterns_solution, orient=VERTICAL)
        sep_patterns.grid(row=0, column=9, sticky=NS, rowspan=10, padx=5)
        btn_save_pat = Button(self.tlevel_patterns_solution, image=self.save_icon, command=self.click_save_pat)
        btn_save_pat.grid(row=0, column=10, padx=25, pady=10, sticky=SW)
        btn_save_pat_ttp = CreateToolTip(btn_save_pat, 'Save patterns')
        btn_cancel_pat = Button(self.tlevel_patterns_solution, image=self.cancel_icon, command=self.click_cancel_pat)
        btn_cancel_pat.grid(row=1, column=10, padx=25, pady=10, sticky=SW)
        btn_cancel_pat_ttp = CreateToolTip(btn_cancel_pat, 'Cancel')

    def retrieve_list(self):
        """
        This function shows the existing 'Problems' in the home TreeView
        """
        # Retrieve available patterns
        self.patterns = Pattern.get_available_patterns(self.connection)
        # Remove existing elements in the TreeView
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        # Retrieve 'Problems' from the DB
        msg = Message(action=52, information=[])
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.receive_message()
        # Fills the TreeView with the existing 'Problems', the id is stored in the 'text' field of the TV
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1],))

    def select_problem_summary(self, event):
        """
        Function activated when the event of selecting an item in the available problems TV is generated. It fills the
        summary textbox with information of the selected problem
        :param event:
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])  # Retrieve id of selected item from TreeView
            self.directive = Message(action=55, information=[self.id_selected])  # ask for the content of the selected problem
            self.connection = self.directive.send_directive(self.connection)
            problem_aux = Problem(id=self.id_selected, name=self.connection.message.information[0],
                                  description=self.connection.message.information[1],
                                  id_solution=self.connection.message.information[2], connection=self.connection)
            self.directive = Message(action=65, information=[problem_aux.solution.diagram_id])
            self.connection = self.directive.send_directive(self.connection)
            self.file_aux = File()
            self.file_aux.write_file(self.connection.message.information[0], self.connection.message.information[1])
            # Clear summary txt box
            self.txt_summary['state'] = NORMAL
            self.txt_summary.delete('1.0', 'end-1c')
            # Adding elements in the list
            self.txt_summary.insert('end-1c', "Name:\n{}\n\n".format(wrap_text(problem_aux.name, 50)))
            self.txt_summary.insert('end-1c', "Description:\n{}\n\nIdeal Solution:\n".format(wrap_text(problem_aux.description, 50)))
            self.txt_summary.insert('end-1c', "-Diagram:\tClick right button to see diagram >>\n\n")
            if len(problem_aux.solution.patterns_id) == 0:
                self.txt_summary.insert('end-1c', "-The ideal solution does not have associated patterns\n")
            else:
                self.txt_summary.insert('end-1c', "-Associated patterns:\n")
                index = 0
                for item in problem_aux.solution.patterns_id:
                    for item2 in self.patterns:
                        if item2.id == item:
                            break
                    self.txt_summary.insert('end-1c', "{}) {}\n".format(index + 1, item2.get_content_name()))
                    index += 1
            self.txt_summary['state'] = DISABLED

    def show_frm(self):
        """
        Displays the home page of the 'Problems'
        """
        # Variable to avoid consulting to the DB information of patterns associated with a 'Problem'
        # more than once when switching between CRUD form and patterns selection form
        self.back_window = True
        self.retrieve_list()
        self.trv_available.selection_set(self.trv_available.get_children()[0])
        self.select_problem_summary(None)
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        """
        Hides all forms that ar curently active
        """
        self.clear_fields()
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid_forget()

    def click_delete(self):
        """
        Function activated when 'Delete' button is pressed
        """
        if self.trv_available.selection() != '':
            # MessageBox asking confirmation
            decision = messagebox.askyesno(title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                self.directive = Message(action=54, information=[self.id_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:  # An error ocurred while deleting the item
                    messagebox.showerror(title='Can not delete the item', message=self.connection.message.information[0])
                else:
                    self.retrieve_list()
                    self.trv_available.selection_set(self.trv_available.get_children()[0])
        else:
            messagebox.showwarning(title='No selection', message='You must select an item')

    def click_new(self):
        """
        Function activated when 'New' button is pressed
        """
        self.decide = True  # Important variable when saving, it indicates the 'Problem' is new
        self.new_problem = Problem()
        self.frm_child_list.grid_forget()
        self.txt_name_prob.focus_set()
        self.title_form = 'New Problem'
        self.frm_child_crud['text'] = self.title_form
        self.txt_name_prob.focus_set()
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        """
        Function activated when 'Update' button is pressed
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.decide = False # Important variable when saving, it indicates the 'Problem' is being modified
            # Retrieve selected problem
            self.directive = Message(action=55, information=[self.id_selected, 'validate'])
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.action == 5:  # An error ocurred while trying to update the item
                messagebox.showerror(title='Can not update the item', message=self.connection.message.information[0])
            else:
                self.new_problem = Problem(id=self.id_selected, name=self.connection.message.information[0],
                                           description=self.connection.message.information[1])
                id_sol = self.connection.message.information[2]
                # Retrieve associated solution
                self.directive = Message(action=60, information=[id_sol])
                self.connection = self.directive.send_directive(self.connection)
                solution_aux = Solution(id=id_sol, annotations=self.connection.message.information[0],
                                        diagram_id=self.connection.message.information[1])
                for item in self.connection.message.information[2]:
                    elements = item.split('¥')
                    solution_aux.patterns_id.append(int(elements[0]))
                self.new_problem.solution = solution_aux
                # Retrieve associated diagram
                self.directive = Message(action=65, information=[solution_aux.diagram_id])
                self.connection = self.directive.send_directive(self.connection)
                self.file = File()
                self.file.write_file(self.connection.message.information[0], self.connection.message.information[1])
                # Fill visual components with retrieved information
                self.txt_name_prob.insert('1.0', self.new_problem.name)
                self.txt_description_prob.insert('1.0', self.new_problem.description)
                self.txt_annotations.insert('1.0', self.new_problem.solution.annotations)
                self.show_file()
                self.frm_child_list.grid_forget()
                self.txt_name_prob.focus_set()
                self.title_form = 'Update Problem'
                self.frm_child_crud['text'] = self.title_form
                self.txt_name_prob.focus_set()
                self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(title='No selection', message='You must select an item')

    def click_save(self):
        """
        Function activated when 'Save' button  is pressed. A new problem is created or updated, depending on the decision.
        In first case the solution does not have associated patterns, in that case, the user is prompted to confirm that
        decision. In the second case the solution has associated patterns, where the problem and the solution will be
        saved immediately
        """
        if self.validate_fields():
            if len(self.trv_selected_patterns.get_children()) == 0: # If no selected patterns for the solution
                # MessageBox asking confirmation
                decision = messagebox.askyesno(title='Confirmation',
                                               message='Are you sure you don\'t want to add patterns to the solution?')
                # Save problem and solution without patterns
                if decision:
                    if self.decide:  # New Problem
                        # Create diagram in DB
                        self.directive = Message(action=61, information=[self.file.file_bytes, self.file.name, 'ideal sol'])
                        self.connection = self.directive.send_directive(self.connection)
                        id_diagram = self.connection.message.information[0]
                        # Create object for the solution and the problem
                        solution_aux = Solution(annotations=self.txt_annotations.get('1.0', 'end-1c'),
                                                diagram_id=id_diagram)
                        self.new_problem = Problem(name=self.txt_name_prob.get('1.0', 'end-1c'),
                                                   description=self.txt_description_prob.get('1.0', 'end-1c'))
                        # Create the ideal solution in DB
                        self.directive = Message(action=56, information=[solution_aux.annotations,
                                                                         solution_aux.diagram_id])
                        self.connection = self.directive.send_directive(self.connection)
                        id_solution = self.connection.message.information[0]
                        # Create the problem in DB
                        self.directive = Message(action=51, information=[self.new_problem.name,self.new_problem.description,
                                                                         id_solution])
                        self.connection = self.directive.send_directive(self.connection)
                    else:   # Modifying problem
                        # Updating problem and solution object
                        self.new_problem.name = self.txt_name_prob.get('1.0', 'end-1c')
                        self.new_problem.description = self.txt_description_prob.get('1.0', 'end-1c')
                        self.new_problem.solution.annotations = self.txt_annotations.get('1.0', 'end-1c')
                        # Update current diagram in DB
                        self.directive = Message(action=63, information=[self.new_problem.solution.diagram_id,
                                                                         self.file.file_bytes, self.file.name, 'ideal sol'])
                        self.connection = self.directive.send_directive(self.connection)
                        # Update the ideal solution in DB
                        self.directive = Message(action=58, information=[self.new_problem.solution.id,
                                                                         self.new_problem.solution.annotations,
                                                                         self.new_problem.solution.diagram_id])
                        self.connection = self.directive.send_directive(self.connection)
                        # Update the problem in DB
                        self.directive = Message(action=53, information=[self.new_problem.id, self.new_problem.name,
                                                                         self.new_problem.description,
                                                                         self.new_problem.solution.id])
                        self.connection = self.directive.send_directive(self.connection)
                    self.clear_fields()
                    self.frm_child_crud.grid_forget()
                    self.show_frm()
            # Save problem and solution with patterns
            else:
                if self.decide:  # New problem
                    # Create diagram in DB
                    self.directive = Message(action=61, information=[self.file.file_bytes, self.file.name, 'ideal sol'])
                    self.connection = self.directive.send_directive(self.connection)
                    id_diagram = self.connection.message.information[0]
                    # Create object for the solution and the problem
                    solution_aux = Solution(annotations=self.txt_annotations.get('1.0', 'end-1c'),
                                            diagram_id=id_diagram)
                    for item in self.trv_selected_patterns.get_children():
                        solution_aux.patterns_id.append(int(self.trv_selected_patterns.item(item)['text']))
                    self.new_problem = Problem(name=self.txt_name_prob.get('1.0', 'end-1c'),
                                               description=self.txt_description_prob.get('1.0', 'end-1c'))
                    # Create the ideal solution in DB
                    self.directive = Message(action=56, information=[solution_aux.annotations, solution_aux.diagram_id,
                                                                     solution_aux.patterns_id])
                    self.connection = self.directive.send_directive(self.connection)
                    id_solution = self.connection.message.information[0]
                    # Create the problem in DB
                    self.directive = Message(action=51,
                                             information=[self.new_problem.name, self.new_problem.description,
                                                          id_solution])
                    self.connection = self.directive.send_directive(self.connection)
                else:  # Update problem
                    # Updating problem and solution object
                    self.new_problem.name = self.txt_name_prob.get('1.0', 'end-1c')
                    self.new_problem.description = self.txt_description_prob.get('1.0', 'end-1c')
                    self.new_problem.solution.annotations = self.txt_annotations.get('1.0', 'end-1c')
                    self.new_problem.solution.patterns_id = []
                    for item in self.trv_selected_patterns.get_children():
                        self.new_problem.solution.patterns_id.append(int(self.trv_selected_patterns.item(item)['text']))
                    # Update current diagram in DB
                    self.directive = Message(action=63, information=[self.new_problem.solution.diagram_id,
                                                                     self.file.file_bytes, self.file.name, 'ideal sol'])
                    self.connection = self.directive.send_directive(self.connection)
                    # Update the ideal solution in DB
                    self.directive = Message(action=58, information=[self.new_problem.solution.id,
                                                                     self.new_problem.solution.annotations,
                                                                     self.new_problem.solution.diagram_id,
                                                                     self.new_problem.solution.patterns_id])
                    self.connection = self.directive.send_directive(self.connection)
                    # Update the problem in DB
                    self.directive = Message(action=53, information=[self.new_problem.id, self.new_problem.name,
                                                                     self.new_problem.description,
                                                                     self.new_problem.solution.id])
                    self.connection = self.directive.send_directive(self.connection)
                self.clear_fields()
                self.frm_child_crud.grid_forget()
                self.show_frm()
        else:
            messagebox.showwarning(title='Missing information', message='Some fields are empty')

    def click_associate_patterns(self):
        """
        This method is executed when the 'Patterns of the solution' button is pressed. It shows the pop up window of
        patterns of the ideal solution. It also avoids to reload pattern when they were loaded previously (when the
        button was pressed for the first time).
        """
        if self.back_window:
            self.back_window = False
            if self.decide:
                self.retrieve_patterns([], self.patterns[:])
            else:
                self.retrieve_patterns(self.new_problem.solution.patterns_id, self.patterns[:])
        self.tlevel_patterns_solution.deiconify()
        self.tlevel_patterns_solution.grab_set()

    def retrieve_patterns(self, s_patterns, a_patterns):
        """
        Remove patterns from the available and selected patterns TV, compare selected patterns (if updating problem) and
        adjust correct distribution between both TVs, and fill the TVs with the content
        :param s_patterns: Selected patterns, this exist when modifying a problem
        :param a_patterns: Available patterns in the DB
        """
        # Remove existing elements from the TVs
        for item in self.trv_available_patterns.get_children():
            self.trv_available_patterns.delete(item)
        for item in self.trv_selected_patterns.get_children():
            self.trv_selected_patterns.delete(item)
        selected_patterns = []
        # Compare and distribute patterns correctly
        for id in s_patterns:
            for item in a_patterns:
                if id == item.id:
                    a_patterns.remove(item)
                    selected_patterns.append(item)
        # Fill TVs with the results from the comparation
        for item in a_patterns:
            content = item.get_content_name()
            self.trv_available_patterns.insert('', 'end', text=item.id, values=(content,))
        for item in selected_patterns:
            content = item.get_content_name()
            self.trv_selected_patterns.insert('', 'end', text=item.id, values=(content,))

    def click_cancel(self):
        """
        Function activated when 'Cancel' button is pressed in CRUD form, it goes back to the 'Problems' home page
        """
        # MessageBox asking confirmation
        decision = messagebox.askyesno(title='Cancel', message='Are you sure you want to cancel?')
        if decision:
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def validate_fields(self):
        """
        Function that validates empty mandatory visual fields and the diagram
        """
        if len(self.txt_name_prob.get('1.0','end-1c')) != 0 and len(self.txt_description_prob.get('1.0','end-1c')) != 0\
                and self.file is not None:
            return True
        else:
            return False

    def click_trv_aptterns(self, event):
        """
        Function activated when the event of selecting an item in the available patterns TV is generated. It deselect
        the selection that may be activated in the selected patterns TV
        """
        self.trv_selected_patterns.selection_remove(self.trv_selected_patterns.selection())

    def click_trv_spatterns(self, event):
        """
        Function activated when the event of selecting an item in the selected patterns TV is generated. It deselect
        the selection that may be activated in the available patterns TV
        """
        self.trv_available_patterns.selection_remove(self.trv_available_patterns.selection())

    def click_add(self):
        """
        Function activated when the 'Add' button is pressed in the patterns form. It inserts a selected item in
        the available patterns TV into the selected patterns TV and removes it from the available patterns TV
        """
        if self.trv_available_patterns.item(self.trv_available_patterns.selection())['text'] != '' and \
                self.trv_selected_patterns.item(self.trv_selected_patterns.selection())['text'] == '':
            self.trv_selected_patterns.insert('', 'end', text=self.trv_available_patterns.item(
                self.trv_available_patterns.focus())['text'], values=self.trv_available_patterns.item(
                self.trv_available_patterns.focus())['values'])
            self.trv_available_patterns.delete(self.trv_available_patterns.selection())

    def click_remove(self):
        """
        Function activated when the 'Add' button is pressed in the patterns form. It inserts a selected item in
        the selected patterns TV into the available patterns TV and removes it from the selected patterns TV
        """
        if self.trv_selected_patterns.item(self.trv_selected_patterns.selection())['text'] != '' and \
                self.trv_available_patterns.item(self.trv_available_patterns.selection())['text'] == '':
            self.trv_available_patterns.insert('', 'end', text=self.trv_selected_patterns.item(
                self.trv_selected_patterns.focus())['text'], values=self.trv_selected_patterns.item(
                self.trv_selected_patterns.focus())['values'])
            self.trv_selected_patterns.delete(self.trv_selected_patterns.selection())

    def click_cancel_pat(self):
        """
        Function activated when 'Cancel' button in Patterns form is pressed, it closes 'Patterns' selection pop-up window
        """
        self.back_window = True
        self.close_tlevel_patterns()

    def click_save_pat(self):
        """
        Function activated when 'Save' button in Patterns form is pressed, it closes 'Patterns' selection pop-up window
        and saves current selection
        """
        self.close_tlevel_patterns()

    def click_upload_file(self):
        """
        Create a File object that is uploaded by the user, validating that there is not a file uploaded already.
        """
        if self.file is None:
            filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select JPEG file",
                                                  filetypes=[("jpeg", "*.jpg")])
            if not filename:
                return  # user cancelled; stop this method
            self.file = File()
            self.file.read_file(filename)
            self.show_file()

    def click_remove_file(self):
        """
        Remove an uploaded file from the system validating it is already uploaded. This method also delete
        any image in the canvas that may be fulfilled with an image.
        """
        if self.file is not None:  # if an image was already loaded
            self.canvas.delete(self.file.image)  # clear canvas
            self.file = None

    def clear_fields(self):
        """
        Restart visual components to theirs initial state (cleared)
        """
        self.txt_name_prob.delete('1.0', 'end-1c')
        self.txt_description_prob.delete('1.0', 'end-1c')
        self.txt_annotations.delete('1.0', 'end-1c')
        if self.file is not None:  # if an image was already loaded
            self.canvas.delete(self.file.image)  # clear canvas
            self.file = None    # set file NULL

    def show_file(self):
        """
        Show the image in the visual canvas of the form only if it is empty, this function is called after uploading
        a diagram
        """
        load = Image.open(self.file.filename)
        load = load.resize((160, 160), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(load)
        if self.file.image is not None:  # if an image was already loaded
            self.canvas.delete(self.file.image)  # remove the previous image
        self.file.image = self.canvas.create_image(0, 0, anchor='nw', image=self.render)    # and display new image

    def click_expand_diagram(self):
        # Fill summary problem canvas with retrieved image
        load = Image.open(self.file_aux.filename)
        load = load.resize((500, 500), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(load)
        self.canvas_summary.delete()
        self.file_aux.image = self.canvas_summary.create_image(0, 0, anchor='nw',
                                                                image=self.render)  # and display new image
        self.tlevel_diagram_summary.deiconify()
        self.tlevel_diagram_summary.grab_set()

    def close_tlevel_diagram(self):
        self.tlevel_diagram_summary.grab_release()
        self.tlevel_diagram_summary.withdraw()

    def close_tlevel_patterns(self):
        self.tlevel_patterns_solution.grab_release()
        self.tlevel_patterns_solution.withdraw()