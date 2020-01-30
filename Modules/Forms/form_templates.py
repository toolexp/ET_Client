from tkinter import Label, LabelFrame, Frame, Text, Button, messagebox, PhotoImage, Scrollbar, Toplevel
from tkinter.constants import *
from tkinter.ttk import Treeview, Separator
from Modules.Config.Data import Message, CreateToolTip, wrap_text, Template
from Modules.Config.Visual import *


class FormParentTemplate:
    def __init__(self, window, connection):
        self.frm_parent = Frame(window)
        self.initialize_components()
        self.frm_child = FormChildTemplate(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Templates')
        lbl_experimenter_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_experimenter_title.grid(row=0, column=0, pady=20)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildTemplate:
    def __init__(self, frm_parent, connection):
        self.connection = connection
        self.directive = Message()
        self.decide_template = True
        self.id_selected = 0
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_crud = LabelFrame(frm_parent)
        self.frm_child_crud.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
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
        self.add_icon = PhotoImage(file=r"./Resources/right.png")
        self.delete_icon = PhotoImage(file=r"./Resources/left.png")
        self.up_arrow = PhotoImage(file=r"./Resources/up_arrow.png")
        self.down_arrow = PhotoImage(file=r"./Resources/down_arrow.png")
        self.star_icon = PhotoImage(file=r"./Resources/star.png")
        self.back_icon = PhotoImage(file=r"./Resources/back.png")
        self.view_icon = PhotoImage(file=r"./Resources/view.png")
        self.disabled_color = self.frm_child_list.cget('bg')

        # Components for List FRM
        lbl_sep1 = Label(self.frm_child_list)
        lbl_sep1.grid(row=0, column=0, padx=10, pady=25)
        self.trv_available = Treeview(self.frm_child_list, height=20, columns=('N', 'Name'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='N', anchor=CENTER)
        self.trv_available.heading('#2', text='Name', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available.column('#2', width=375, minwidth=375, stretch=NO)
        self.trv_available.bind("<ButtonRelease-1>", self.select_template_summary)
        self.trv_available.grid(row=0, column=1, sticky=W, pady=25)
        vsb_trv_av = Scrollbar(self.frm_child_list, orient="vertical", command=self.trv_available.yview)
        vsb_trv_av.grid(row=0, column=2, pady=25, sticky=NS)
        self.trv_available.configure(yscrollcommand=vsb_trv_av.set)
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New template')
        btn_view = Button(frm_aux4, image=self.view_icon, command=self.click_view)
        btn_view.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_view_ttp = CreateToolTip(btn_new, 'View template')
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit template')
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=3, column=0, pady=5, padx=5, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete template')
        frm_aux4.grid(row=0, column=3, pady=25, padx=25, sticky=NW)
        sep_template = Separator(self.frm_child_list, orient=VERTICAL)
        sep_template.grid(row=0, column=4, sticky=NS, padx=25)
        frm_aux3 = Frame(self.frm_child_list)
        lbl_sep3 = Label(frm_aux3)
        lbl_sep3.grid(row=0, column=0, padx=10, pady=25, rowspan=3)
        lbl_details = Label(frm_aux3, text='Details')
        lbl_details.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_details.grid(row=0, column=1, sticky=W, pady=25, columnspan=2)
        self.txt_summary = Text(frm_aux3, height=22, width=50)
        self.txt_summary.config(font=TEXT_FONT, bg=self.disabled_color)
        self.txt_summary.grid(row=1, column=1)
        vsb_txt_sum = Scrollbar(frm_aux3, orient="vertical", command=self.txt_summary.yview)
        vsb_txt_sum.grid(row=1, column=2, sticky=NS)
        self.txt_summary.configure(yscrollcommand=vsb_txt_sum.set)
        lbl_sep4 = Label(frm_aux3)
        lbl_sep4.grid(row=0, column=3, padx=10, pady=25, rowspan=3)
        lbl_sep5 = Label(frm_aux3)
        lbl_sep5.grid(row=2, column=1, pady=5, columnspan=2)
        frm_aux3.grid(row=0, column=5)

        # Components for CRUD FRM
        lbl_sep6 = Label(self.frm_child_crud)
        lbl_sep6.grid(row=0, column=0, padx=10, pady=25, rowspan=10)
        lbl_name = Label(self.frm_child_crud, text='Name*')
        lbl_name.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name.grid(row=0, column=1, pady=25, sticky=NW)
        lbl_description = Label(self.frm_child_crud, text='Description*')
        lbl_description.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_description.grid(row=0, column=6, pady=25, sticky=NW)
        lbl_sep3 = Label(self.frm_child_crud)
        lbl_sep3.grid(row=0, column=2, padx=10, pady=25)
        self.txt_name = Text(self.frm_child_crud, height=1, width=30)
        self.txt_name.config(font=TEXT_FONT)
        self.txt_name.grid(row=0, column=3, pady=25, sticky=NW)
        lbl_sep4 = Label(self.frm_child_crud)
        lbl_sep4.grid(row=0, column=7, padx=10, pady=25)
        self.txt_description = Text(self.frm_child_crud, height=5, width=49)
        self.txt_description.config(font=TEXT_FONT)
        self.txt_description.grid(row=0, column=8, pady=25, sticky=W)
        vsb_txt_desc = Scrollbar(self.frm_child_crud, orient="vertical", command=self.txt_description.yview)
        vsb_txt_desc.grid(row=0, column=9, pady=25, sticky=NS)
        self.txt_description.configure(yscrollcommand=vsb_txt_desc.set)
        lbl_sep7 = Label(self.frm_child_crud)
        lbl_sep7.grid(row=0, column=5, padx=10, pady=25, rowspan=3)
        lbl_sep8 = Label(self.frm_child_crud)
        lbl_sep8.grid(row=0, column=10, padx=10, pady=25, rowspan=2)
        lbl_available_d = Label(self.frm_child_crud, text='Available sections')
        lbl_available_d.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_available_d.grid(row=1, column=1, pady=10, sticky=W, columnspan=4)
        lbl_selected_d = Label(self.frm_child_crud, text='Selected sections*')
        lbl_selected_d.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_selected_d.grid(row=1, column=6, pady=10, sticky=W, columnspan=4)
        self.trv_available_sections = Treeview(self.frm_child_crud, height=10, columns=('N', 'Name', 'Data Type'))
        self.trv_available_sections.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_sections.heading('#1', text='N', anchor=CENTER)
        self.trv_available_sections.heading('#2', text='Name', anchor=CENTER)
        self.trv_available_sections.heading('#3', text='Data Type', anchor=CENTER)
        self.trv_available_sections.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_available_sections.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_available_sections.column('#2', width=150, minwidth=150, stretch=NO)
        self.trv_available_sections.column('#3', width=120, minwidth=120, stretch=NO)
        self.trv_available_sections.bind("<Button-1>", self.click_trv_asections)
        self.trv_available_sections.grid(row=2, column=1, rowspan=7, columnspan=3,sticky=W, pady=10)
        vsb_trv_avs = Scrollbar(self.frm_child_crud, orient="vertical", command=self.trv_available_sections.yview)
        vsb_trv_avs.grid(row=2, column=4, rowspan=7, pady=10, sticky=NS)
        self.trv_available_sections.configure(yscrollcommand=vsb_trv_avs.set)
        self.trv_selected_sections = Treeview(self.frm_child_crud, height=10, columns=('N', 'Name', 'Data type', 'Mandatory', 'Main'))
        self.trv_selected_sections.heading('#0', text='ID', anchor=CENTER)
        self.trv_selected_sections.heading('#1', text='N', anchor=CENTER)
        self.trv_selected_sections.heading('#2', text='Name', anchor=CENTER)
        self.trv_selected_sections.heading('#3', text='Data type', anchor=CENTER)
        self.trv_selected_sections.heading('#4', text='Mandatory', anchor=CENTER)
        self.trv_selected_sections.heading('#5', text='Main', anchor=CENTER)
        self.trv_selected_sections.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_selected_sections.column('#1', width=20, minwidth=20, stretch=NO)
        self.trv_selected_sections.column('#2', width=150, minwidth=150, stretch=NO)
        self.trv_selected_sections.column('#3', width=120, minwidth=120, stretch=NO)
        self.trv_selected_sections.column('#4', width=80, minwidth=80, stretch=NO)
        self.trv_selected_sections.column('#5', width=80, minwidth=80, stretch=NO)
        self.trv_selected_sections.bind("<Button-1>", self.click_trv_ssections)
        self.trv_selected_sections.bind("<Double-1>", self.click_switch_mandatory)
        self.trv_selected_sections.grid(row=2, column=6, rowspan=7, columnspan=3, sticky=W, pady=10)
        vsb_trv_ses = Scrollbar(self.frm_child_crud, orient="vertical", command=self.trv_selected_sections.yview)
        vsb_trv_ses.grid(row=2, column=9, rowspan=7, pady=10, sticky=NS)
        self.trv_selected_sections.configure(yscrollcommand=vsb_trv_ses.set)
        self.lbl_note_optional = Label(self.frm_child_crud, text='NOTES:\tTo switch between optional and mandatory, double click '
                                                      'on selected section.\n\tChoose one or up to three main sections '
                                                      'by first selecting the target sections\n\tand then clicking the '
                                                      'star button.\n')
        self.lbl_note_optional.config(fg=TEXT_COLOR, font=NOTE_FONT, justify=LEFT)
        self.btn_add = Button(self.frm_child_crud, image=self.add_icon, command=self.click_add)
        btn_add_ttp = CreateToolTip(self.btn_add, 'Add section')
        self.btn_remove = Button(self.frm_child_crud, image=self.delete_icon, command=self.click_remove)
        btn_remove_ttp = CreateToolTip(self.btn_remove, 'Remove section')
        self.btn_main_section = Button(self.frm_child_crud, image=self.star_icon, command=self.click_main_section)
        btn_main_section_ttp = CreateToolTip(self.btn_main_section, 'Main section(s)')
        self.btn_up = Button(self.frm_child_crud, image=self.up_arrow, command=self.click_up)
        btn_up_ttp = CreateToolTip(self.btn_up, 'Move up')
        self.btn_down = Button(self.frm_child_crud, image=self.down_arrow, command=self.click_down)
        btn_down_ttp = CreateToolTip(self.btn_down, 'Move down')
        sep_aux1 = Separator(self.frm_child_crud, orient=VERTICAL)
        sep_aux1.grid(row=0, column=11, sticky=NS, rowspan=10)
        frm_aux1 = Frame(self.frm_child_crud)
        self.btn_save = Button(frm_aux1, image=self.save_icon, command=self.click_save)
        btn_save_ttp = CreateToolTip(self.btn_save, 'Save template')
        self.btn_back = Button(frm_aux1, image=self.back_icon, command=self.click_back)
        btn_back_ttp = CreateToolTip(self.btn_back, 'Go back')
        self.btn_cancel = Button(frm_aux1, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel_ttp = CreateToolTip(self.btn_cancel, 'Cancel')
        frm_aux1.grid(row=0, column=12, pady=10, padx=25, sticky=NW, rowspan=10)
        self.enabled_color = self.txt_name.cget('bg')

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=37)
        self.connection = self.directive.send_directive(self.connection)
        # Adding elements into the list
        for index, item in enumerate(self.connection.message.information):
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(index+1, elements[1]))
        if len(self.trv_available.get_children()) != 0:
            self.trv_available.selection_set(self.trv_available.get_children()[0])
            self.select_template_summary()

    def select_template_summary(self, event=None):
        """
        Function activated when the event of selecting an item in the available templates TV is generated. It fills the
        summary text box with information of the selected template
        :param event:
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            # Clear summary txt box
            self.txt_summary['state'] = NORMAL
            self.txt_summary.delete('1.0', 'end-1c')
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])  # Retrieve id of selected item from TreeView
            self.directive = Message(action=40, information=[self.id_selected]) # ask for the template
            self.connection = self.directive.send_directive(self.connection)
            # Insert template's name and description
            self.txt_summary.insert('end-1c', "Name:\n{}\n\n".format(wrap_text(self.connection.message.information[0], 55)))
            self.txt_summary.insert('end-1c', "Description:\n{}\n\nSections:\n".format(wrap_text(self.connection.message.information[1], 55)))
            self.directive = Message(action=77, information=[self.id_selected])  # ask for the sections of the selected template
            self.connection = self.directive.send_directive(self.connection)
            # Adding elements in the summary text box
            index = 0
            for item in self.connection.message.information:
                elements = item.split('¥')
                self.txt_summary.insert('end-1c', "{}) {}\t\t{}\t\t{}\n".format(index + 1, elements[3], 'optional' \
                    if elements[7] == '' else 'mandatory', '' if elements[8] == '' else '(MAIN)'))
                index += 1
            self.txt_summary['state'] = DISABLED


    def show_frm(self):
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        self.clear_fields()
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid_forget()

    def click_new(self):
        self.view_decision = False  # Decision when viewing a template
        self.template = Template()
        self.retrieve_sections()
        self.txt_name.focus_set()
        self.show_cu_buttons()
        self.frm_child_crud['text'] = 'New template'
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_view(self):
        if len(self.trv_available.selection()) == 1:
            self.view_decision = True  # Decision when viewing a template
            self.directive = Message(action=40, information=[self.id_selected])
            self.connection = self.directive.send_directive(self.connection)
            self.template = Template(id=self.id_selected, name=self.connection.message.information[0],
                                     description=self.connection.message.information[1],
                                     sections=self.connection.message.information[2])
            self.txt_name.insert('1.0', self.template.name)
            self.txt_description.insert('1.0', self.template.description)
            self.retrieve_sections(self.template.sections)
            self.txt_name.focus_set()
            self.disable_visual_components()
            self.btn_back.grid(row=0, column=0, padx=5, pady=5, sticky=W)
            self.frm_child_list.grid_forget()
            self.frm_child_crud['text'] = 'View template'
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_update(self):
        if len(self.trv_available.selection()) == 1:
            self.view_decision = False  # Decision when viewing a template
            self.directive = Message(action=40, information=[self.id_selected, 'validate'])
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.action == 5:  # An error ocurred while trying to update the item
                messagebox.showerror(parent=self.frm_child_list, title='Can not edit the template',
                                     message=self.connection.message.information[0])
            else:
                self.template = Template(id=self.id_selected, name=self.connection.message.information[0],
                                         description=self.connection.message.information[1],
                                         sections=self.connection.message.information[2])
                self.txt_name.insert('1.0', self.template.name)
                self.txt_description.insert('1.0', self.template.description)
                self.retrieve_sections(self.template.sections)
                self.txt_name.focus_set()
                self.show_cu_buttons()
                self.frm_child_crud['text'] = 'Update template'
                self.frm_child_list.grid_forget()
                self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def click_delete(self):
        if len(self.trv_available.selection()) == 1:
            decision = messagebox.askyesno(parent=self.frm_child_list, title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                self.directive = Message(action=39, information=[self.id_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:  # An error ocurred while deleting the item
                    messagebox.showerror(parent=self.frm_child_list, title='Can not delete the item',
                                         message=self.connection.message.information[0])
                else:
                    self.retrieve_list()
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select one item')

    def show_cu_buttons(self):
        self.btn_add.grid(row=5, column=5, padx=25)
        self.btn_remove.grid(row=6, column=5, padx=25)
        self.btn_main_section.grid(row=2, column=10, padx=25)
        self.btn_down.grid(row=6, column=10, padx=25)
        self.btn_up.grid(row=5, column=10, padx=25)
        self.btn_save.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.btn_cancel.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.lbl_note_optional.grid(row=9, column=6, columnspan=4, sticky=W)

    def disable_visual_components(self):
        self.txt_name['bg'] = self.disabled_color
        self.txt_description['bg'] = self.disabled_color
        self.txt_name['state'] = DISABLED
        self.txt_description['state'] = DISABLED
        self.btn_add.grid_forget()
        self.btn_remove.grid_forget()
        self.btn_main_section.grid_forget()
        self.btn_down.grid_forget()
        self.btn_up.grid_forget()

    def retrieve_sections(self, s_sections=None):
        if s_sections is None:
            s_sections = []
        self.directive = Message(action=32)
        self.connection = self.directive.send_directive(self.connection)
        a_sections = self.connection.message.information
        for item in self.trv_available_sections.get_children():
            self.trv_available_sections.delete(item)
        for item in self.trv_selected_sections.get_children():
            self.trv_selected_sections.delete(item)
        for item in s_sections:
            item_aux1 = item.split('¥')[2:6]
            item_aux2 = [item.split('¥')[-1]]
            item = item_aux1 + item_aux2
            item = '¥'.join(item)
            if item in a_sections:
                a_sections.remove(item)
        for index, item in enumerate(a_sections):
            elements = item.split('¥')
            self.trv_available_sections.insert('', 'end', text=elements[0], values=(index+1, elements[1], elements[3]))
        for index, item in enumerate(s_sections):
            elements = item.split('¥')
            self.trv_selected_sections.insert('', 'end', text=elements[2], values=(index+1, elements[3], elements[5],
                                                                                   elements[7], elements[8]))

    def click_add(self):
        """
        Function that moves a 'Section' from available tree view to selected tree view (in frm_child_crud)
        """
        if len(self.trv_available_sections.selection()) != 0 and len(self.trv_selected_sections.selection()) == 0:
            if len(self.trv_selected_sections.get_children()) != 0:
                index = self.trv_selected_sections.item(self.trv_selected_sections.get_children()[-1])['values'][0]
            else:
                index = 0
            for row in self.trv_available_sections.selection():
                index += 1
                values = self.trv_available_sections.item(row)['values']
                self.trv_selected_sections.insert('', 'end', text=self.trv_available_sections.item(row)['text'],
                                                  values=(index, values[1], values[2], '✓', ''))
                self.trv_available_sections.delete(row)

    def click_remove(self):
        """
        Function that moves a 'Section' from selected tree view to available tree view (in frm_child_crud)
        """
        if len(self.trv_selected_sections.selection()) != 0 and len(self.trv_available_sections.selection()) == 0:
            if len(self.trv_available_sections.get_children()) != 0:
                index = self.trv_available_sections.item(self.trv_available_sections.get_children()[-1])['values'][0]
            else:
                index = 0
            for row in self.trv_selected_sections.selection():
                index += 1
                values = self.trv_selected_sections.item(row)['values']
                self.trv_available_sections.insert('', 'end', text=self.trv_selected_sections.item(row)['text'],
                                                   values=(index, values[1], values[2]))
                self.trv_selected_sections.delete(row)

    def click_up(self):
        # Make sure only one item in 'selected sections' is selected
        if len(self.trv_selected_sections.selection()) == 1 and len(self.trv_available_sections.selection()) == 0:
            item = self.trv_selected_sections.selection()
            index = self.trv_selected_sections.index(item)
            self.trv_selected_sections.move(item, '', index - 1)

    def click_down(self):
        # Make sure only one item in 'selected sections' is selected
        if len(self.trv_selected_sections.selection()) == 1 and len(self.trv_available_sections.selection()) == 0:
            item = self.trv_selected_sections.selection()
            index = self.trv_selected_sections.index(item)
            self.trv_selected_sections.move(item, '', index + 1)

    def click_main_section(self):
        # Make sure a max of three items of 'selected sections' are selected
        if 4 > len(self.trv_selected_sections.selection()) > 0 and len(self.trv_available_sections.selection()) == 0:
            # First change all sections as normal (not main)
            for item in self.trv_selected_sections.get_children():
                if self.trv_selected_sections.item(item)['values'][3] != '':
                    values = self.trv_selected_sections.item(item)['values']
                    self.trv_selected_sections.item(item, values=(values[0], values[1], values[2], values[3], ''))
            # Set new main sections
            cont_error = False
            for row in self.trv_selected_sections.selection():
                values = self.trv_selected_sections.item(row)['values']
                if values[2] == 'Classification' or values[2] == 'Text':
                    self.trv_selected_sections.item(row, values=(values[0], values[1], values[2], values[3], '✓'))
                else:   # File sections can not be main
                    cont_error = True
            if cont_error:
                messagebox.showwarning(parent=self.frm_child_crud, title='Main section(s)',
                                       message="Main section(s) must be of 'Text' or 'Classification' data type")
        else:
            messagebox.showwarning(parent=self.frm_child_crud, title='Main section(s)',
                                   message='You must select a minimum of one and a maximum of three sections')

    def click_trv_asections(self, event):
        """
        Function that removes selection from 'available' tree view when 'selected' tree view is selected (in frm_child_crud)
        """
        self.trv_selected_sections.selection_remove(self.trv_selected_sections.selection())

    def click_trv_ssections(self, event):
        """
        Function that removes selection from 'selected' tree view when 'available' tree view is selected (in frm_child_crud)
        """
        self.trv_available_sections.selection_remove(self.trv_available_sections.selection())

    def click_save(self):
        if self.validate_fields():
            self.template.name = self.txt_name.get('1.0', 'end-1c')
            self.template.description = self.txt_description.get('1.0', 'end-1c')
            if self.template.id == 0:  # Creating a template
                self.directive = Message(action=36, information=[self.template.name, self.template.description, [], [],
                                                                 []])
                for item in self.trv_selected_sections.get_children():
                    values = self.trv_selected_sections.item(item)['values']
                    self.directive.information[2].append(int(self.trv_selected_sections.item(item)['text']))
                    self.directive.information[3].append(values[4])
                    if values[4] != '':
                        self.directive.information[4].append('✓')
                    else:
                        self.directive.information[4].append(values[3])
            else:   # Updating a template
                self.directive = Message(action=38, information=[self.template.id, self.template.name,
                                                                 self.template.description, [], [], []])
                for item in self.trv_selected_sections.get_children():
                    values = self.trv_selected_sections.item(item)['values']
                    self.directive.information[3].append(int(self.trv_selected_sections.item(item)['text']))
                    self.directive.information[4].append(values[4])
                    if values[4] != '':
                        self.directive.information[5].append('✓')
                    else:
                        self.directive.information[5].append(values[3])
            self.connection = self.directive.send_directive(self.connection)
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def click_cancel(self):
        decision = True
        if self.txt_name.get('1.0', 'end-1c') != self.template.name or \
                self.txt_description.get('1.0', 'end-1c') != self.template.description or \
                len(self.trv_selected_sections.get_children()) != len(self.template.sections):
            decision = messagebox.askyesno(parent=self.frm_child_crud, title='Cancel',
                                           message='Are you sure you want to cancel?')
        if decision:
            self.click_back()

    def click_back(self):
        self.clear_fields()
        self.frm_child_crud.grid_forget()
        self.show_frm()

    def validate_fields(self):
        text_section = False
        if len(self.txt_name.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='You must provide a name')
            return False
        if len(self.txt_description.get('1.0', 'end-1c')) == 0:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='You must provide a description')
            return False
        if len(self.trv_selected_sections.get_children()) == 0:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='You must select at least one section')
            return False
        for item in self.trv_selected_sections.get_children():
            values = self.trv_selected_sections.item(item)['values']
            if values[2] == 'Text' or values[2] == 'Classification':
                text_section = True
                break
        if not text_section:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='At least one section has to be of text type')
            return False
        for item in self.trv_selected_sections.get_children():
            values = self.trv_selected_sections.item(item)['values']
            if values[4] == '✓':
                if values[2] == 'Text' or values[2] == 'Classification':
                    return True
                else:
                    messagebox.showwarning(parent=self.frm_child_crud, title='Main section',
                                           message='The main section has to be of text or classification type')
                    return False
        messagebox.showwarning(parent=self.frm_child_crud, title='Main section',
                               message='You must set one of the selected section as main')
        return False

    def clear_fields(self):
        self.txt_name['state'] = NORMAL
        self.txt_description['state'] = NORMAL
        self.txt_name['bg'] = self.enabled_color
        self.txt_description['bg'] = self.enabled_color
        self.txt_name.delete('1.0', 'end-1c')
        self.txt_description.delete('1.0', 'end-1c')
        self.btn_save.grid_forget()
        self.btn_cancel.grid_forget()
        self.btn_back.grid_forget()
        self.lbl_note_optional.grid_forget()

    def click_switch_mandatory(self, event):
        if not self.view_decision:  # Only if not viewing a template
            # Make sure only one item in 'selected sections' is selected
            if len(self.trv_selected_sections.selection()) == 1 and len(self.trv_available_sections.selection()) == 0:
                values = self.trv_selected_sections.item(
                    self.trv_selected_sections.focus())['values']
                if values[3] == '':
                    self.trv_selected_sections.item(self.trv_selected_sections.focus(),
                                                    values=(values[0], values[1], values[2], '✓', values[4]))
                else:
                    self.trv_selected_sections.item(self.trv_selected_sections.focus(),
                                                    values=(values[0], values[1], values[2], '', values[4]))