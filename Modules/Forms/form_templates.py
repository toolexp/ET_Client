from tkinter import Label, LabelFrame, Frame, Text, Button, messagebox, PhotoImage, Scrollbar
from tkinter.constants import *
from tkinter.ttk import Treeview, Separator
from Modules.Config.Data import Message, CreateToolTip, wrap_text
from Modules.Config.Visual import *


class FormParentTemplate:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildTemplate(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Templates')
        lbl_experimenter_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_experimenter_title.grid(row=0, column=0, columnspan=9, pady=50)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)
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
        self.frm_child_section = LabelFrame(frm_parent)
        self.frm_child_section.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
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
        defaultbg = self.frm_child_list.cget('bg')

        # Components for List FRM
        lbl_sep1 = Label(self.frm_child_list)
        lbl_sep1.grid(row=0, column=0, padx=25, pady=25)
        self.trv_available = Treeview(self.frm_child_list, height=7, columns='Name')
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=300, minwidth=300, stretch=NO)
        self.trv_available.bind("<ButtonRelease-1>", self.select_template_summary)
        self.trv_available.grid(row=0, column=1, rowspan=2, sticky=W, pady=25)
        vsb_trv_av = Scrollbar(self.frm_child_list, orient="vertical", command=self.trv_available.yview)
        vsb_trv_av.grid(row=0, column=2, rowspan=2, pady=25, sticky=NS)
        self.trv_available.configure(yscrollcommand=vsb_trv_av.set)
        frm_aux4 = Frame(self.frm_child_list)
        btn_new = Button(frm_aux4, image=self.new_icon, command=self.click_new)
        btn_new.grid(row=0, column=0, pady=5, padx=5, sticky=E)
        btn_new_ttp = CreateToolTip(btn_new, 'New template')
        btn_edit = Button(frm_aux4, image=self.modify_icon, command=self.click_update)
        btn_edit.grid(row=1, column=0, pady=5, padx=5, sticky=E)
        btn_edit_ttp = CreateToolTip(btn_edit, 'Edit template')
        btn_delete = Button(frm_aux4, image=self.remove_icon, command=self.click_delete)
        btn_delete.grid(row=2, column=0, pady=5, padx=5, sticky=E)
        btn_delete_ttp = CreateToolTip(btn_delete, 'Delete template')
        frm_aux4.grid(row=0, column=4, pady=25, padx=25, rowspan=2, sticky=NW)
        sep_template = Separator(self.frm_child_list, orient=VERTICAL)
        sep_template.grid(row=0, column=5, sticky=NS, rowspan=2, padx=25)
        lbl_sep3 = Label(self.frm_child_list)
        lbl_sep3.grid(row=0, column=6, padx=15, pady=25)
        lbl_details = Label(self.frm_child_list, text='Details')
        lbl_details.config(fg=TEXT_COLOR, font=SUBTITLE_FONT)
        lbl_details.grid(row=0, column=7, sticky=W, pady=25)
        self.txt_summary = Text(self.frm_child_list, height=18, width=50)
        self.txt_summary.config(font=TEXT_FONT, bg=defaultbg)
        self.txt_summary.grid(row=1, column=7, pady=10, sticky=NW)
        vsb_txt_sum = Scrollbar(self.frm_child_list, orient="vertical", command=self.txt_summary.yview)
        vsb_txt_sum.grid(row=1, column=8, pady=1, sticky=NS)
        self.txt_summary.configure(yscrollcommand=vsb_txt_sum.set)
        lbl_sep4 = Label(self.frm_child_list)
        lbl_sep4.grid(row=0, column=9, padx=25, pady=25)

        # Components for CRUD FRM
        frm_aux1 = Frame(self.frm_child_crud)
        frm_aux2 = Frame(self.frm_child_crud)
        lbl_name = Label(frm_aux1, text='Name')
        lbl_name.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_description = Label(frm_aux1, text='Description')
        lbl_description.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_description.grid(pady=10, padx=50, sticky=NW)
        self.txt_name = Text(frm_aux1, height=1, width=60)
        self.txt_name.config(font=TEXT_FONT)
        self.txt_name.grid(row=0, column=1, padx=10)
        self.txt_description = Text(frm_aux1, height=3, width=60)
        self.txt_description.config(font=TEXT_FONT)
        self.txt_description.grid(row=1, column=1, padx=10, pady=10)
        btn_save = Button(frm_aux1, image=self.save_icon, command=self.click_save)
        btn_save.grid(row=0, column=2, padx=30, sticky=W)
        btn_save_ttp = CreateToolTip(btn_save, 'Save template')
        btn_cancel = Button(frm_aux1, image=self.cancel_icon, command=self.click_cancel)
        btn_cancel.grid(row=1, column=2, padx=30, sticky=NW)
        btn_cancel_ttp = CreateToolTip(btn_cancel, 'Cancel')
        lbl_available_d = Label(frm_aux2, text='Available sections')
        lbl_available_d.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_available_d.grid(row=0, column=0, pady=10, sticky=W)
        lbl_selected_d = Label(frm_aux2, text='Selected sections')
        lbl_selected_d.config(fg=TEXT_COLOR, font=LABEL_FONT)
        lbl_selected_d.grid(row=0, column=5, pady=10, sticky=W)
        self.trv_available_sections = Treeview(frm_aux2, height=5, columns=('Name', 'Data Type'))
        self.trv_available_sections.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_sections.heading('#1', text='Name', anchor=CENTER)
        self.trv_available_sections.heading('#2', text='Data Type', anchor=CENTER)
        self.trv_available_sections.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_available_sections.column('#1', width=150, minwidth=150, stretch=NO)
        self.trv_available_sections.column('#2', width=120, minwidth=120, stretch=NO)
        self.trv_available_sections.bind("<Button-1>", self.click_trv_asections)
        self.trv_available_sections.grid(row=1, column=0, rowspan=10, sticky=W, pady=10)
        vsb_trv_avs = Scrollbar(frm_aux2, orient="vertical", command=self.trv_available_sections.yview)
        vsb_trv_avs.grid(row=1, column=1, rowspan=10, pady=10, sticky=NS)
        self.trv_available_sections.configure(yscrollcommand=vsb_trv_avs.set)
        lbl_sep3 = Label(frm_aux2)
        lbl_sep3.grid(row=1, column=2, padx=10, pady=10)
        lbl_sep4 = Label(frm_aux2)
        lbl_sep4.grid(row=1, column=4, padx=10, pady=10)
        self.trv_selected_sections = Treeview(frm_aux2, height=5, columns=('Name', 'Data type', 'Mandatory'))
        self.trv_selected_sections.heading('#0', text='ID', anchor=CENTER)
        self.trv_selected_sections.heading('#1', text='Name', anchor=CENTER)
        self.trv_selected_sections.heading('#2', text='Data type', anchor=CENTER)
        self.trv_selected_sections.heading('#3', text='Mandatory', anchor=CENTER)
        self.trv_selected_sections.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_selected_sections.column('#1', width=150, minwidth=150, stretch=NO)
        self.trv_selected_sections.column('#2', width=120, minwidth=120, stretch=NO)
        self.trv_selected_sections.column('#3', width=80, minwidth=80, stretch=NO)
        self.trv_selected_sections.bind("<Button-1>", self.click_trv_ssections)
        self.trv_selected_sections.bind("<Double-1>", self.click_switch_mandatory)
        self.trv_selected_sections.grid(row=1, column=5, rowspan=10, sticky=W, pady=10)
        vsb_trv_ses = Scrollbar(frm_aux2, orient="vertical", command=self.trv_selected_sections.yview)
        vsb_trv_ses.grid(row=1, column=6, rowspan=10, pady=10, sticky=NS)
        self.trv_selected_sections.configure(yscrollcommand=vsb_trv_ses.set)
        lbl_note_optional = Label(frm_aux2, text='NOTE: To switch between optional and mandatory, double click on '
                                                 'selected section\n')
        lbl_note_optional.config(fg=TEXT_COLOR, font=NOTE_FONT)
        lbl_note_optional.grid(row=11, column=5, columnspan=3, sticky=W)
        btn_add = Button(frm_aux2, image=self.add_icon, command=self.click_add)
        btn_add.grid(row=4, column=3)
        btn_add_ttp = CreateToolTip(btn_add, 'Add section')
        btn_remove = Button(frm_aux2, image=self.delete_icon, command=self.click_remove)
        btn_remove.grid(row=5, column=3)
        btn_remove_ttp = CreateToolTip(btn_remove, 'Remove section')
        btn_up = Button(frm_aux2, image=self.up_arrow, command=self.click_up)
        btn_up.grid(row=4, column=7)
        btn_up_ttp = CreateToolTip(btn_up, 'Move up')
        btn_down = Button(frm_aux2, image=self.down_arrow, command=self.click_down)
        btn_down.grid(row=5, column=7)
        btn_down_ttp = CreateToolTip(btn_down, 'Move down')
        frm_aux1.grid(row=1, column=0, pady=20, padx=40, columnspan=5, rowspan=5)
        frm_aux2.grid(row=8, column=0, padx=40, columnspan=5, rowspan=10)

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        self.directive = Message(action=37, information=[])
        self.connection = self.directive.send_directive(self.connection)
        # Adding elements into the list
        for item in self.connection.message.information:
            elements = item.split('¥')
            self.trv_available.insert('', 'end', text=elements[0], values=(wrap_text(elements[1], 305), ))

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
                self.txt_summary.insert('end-1c', "{}) {}\t\t{}\n".format(index + 1, elements[3], 'optional' if elements[7] == '' else 'mandatory'))
                index += 1
            self.txt_summary['state'] = DISABLED


    def show_frm(self):
        self.retrieve_list()
        if len(self.trv_available.get_children()) != 0:
            self.trv_available.selection_set(self.trv_available.get_children()[0])
            self.select_template_summary()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        self.clear_fields()
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid_forget()

    def click_delete(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
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
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select an item')

    def click_new(self):
        self.decide_template = True
        self.frm_child_list.grid_forget()
        self.directive = Message(action=32, information=[])
        self.connection = self.directive.send_directive(self.connection)
        a_sections = self.connection.message.information
        self.retrieve_sections([], a_sections)
        self.txt_name.focus_set()
        self.frm_child_crud['text'] = 'New template'
        self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            self.decide_template = False
            self.directive = Message(action=40, information=[self.id_selected, 'validate'])
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.action == 5:  # An error ocurred while trying to update the item
                messagebox.showerror(parent=self.frm_child_list, title='Can not update the item',
                                     message=self.connection.message.information[0])
            else:
                self.txt_name.insert('1.0', self.connection.message.information[0])
                self.txt_description.insert('1.0', wrap_text(self.connection.message.information[1], 65))
                s_sections = self.connection.message.information[2]
                self.directive = Message(action=32, information=[])
                self.connection = self.directive.send_directive(self.connection)
                a_sections = self.connection.message.information
                self.retrieve_sections(s_sections, a_sections)
                self.txt_name.focus_set()
                self.frm_child_list.grid_forget()
                self.frm_child_crud['text'] = 'Update template'
                self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
        else:
            messagebox.showwarning(parent=self.frm_child_list, title='No selection', message='You must select an item')

    def retrieve_sections(self, s_sections, a_sections):
        for item in self.trv_available_sections.get_children():
            self.trv_available_sections.delete(item)
        for item in self.trv_selected_sections.get_children():
            self.trv_selected_sections.delete(item)
        for item in s_sections:
            item = item.split('¥')
            item.remove(item[0])
            item.remove(item[0])
            item.remove(item[-1])
            item.remove(item[-1])
            item.remove(item[-1])
            item = '¥'.join(item)
            if item in a_sections:
                a_sections.remove(item)
        for item in a_sections:
            elements = item.split('¥')
            self.trv_available_sections.insert('', 'end', text=elements[0], values=(elements[1], elements[3]))
        for item in s_sections:
            elements = item.split('¥')
            self.trv_selected_sections.insert('', 'end', text=elements[2], values=(elements[3], elements[5],
                                                                                   elements[7]))

    def click_add(self):
        if self.trv_available_sections.item(self.trv_available_sections.selection())['text'] != '' and \
                self.trv_selected_sections.item(self.trv_selected_sections.selection())['text'] == '':
            values = self.trv_available_sections.item(
                self.trv_available_sections.focus())['values']
            text = self.trv_available_sections.item(
                self.trv_available_sections.focus())['text']
            self.trv_selected_sections.insert('', 'end', text=text, values=(values[0], values[1], '✓'))
            self.trv_available_sections.delete(self.trv_available_sections.selection())

    def click_remove(self):
        if self.trv_selected_sections.item(self.trv_selected_sections.selection())['text'] != '' and \
                self.trv_available_sections.item(self.trv_available_sections.selection())['text'] == '':
            values = self.trv_selected_sections.item(
                self.trv_selected_sections.focus())['values']
            text = self.trv_selected_sections.item(
                self.trv_selected_sections.focus())['text']
            self.trv_available_sections.insert('', 'end', text=text, values=(values[0], values[1]))
            self.trv_selected_sections.delete(self.trv_selected_sections.selection())

    def click_up(self):
        if self.trv_selected_sections.item(self.trv_selected_sections.selection())['text'] != '' and \
                self.trv_available_sections.item(self.trv_available_sections.selection())['text'] == '':
            item = self.trv_selected_sections.selection()
            index = self.trv_selected_sections.index(item)
            self.trv_selected_sections.move(item, '', index - 1)

    def click_down(self):
        if self.trv_selected_sections.item(self.trv_selected_sections.selection())['text'] != '' and \
                self.trv_available_sections.item(self.trv_available_sections.selection())['text'] == '':
            item = self.trv_selected_sections.selection()
            index = self.trv_selected_sections.index(item)
            self.trv_selected_sections.move(item, '', index + 1)

    def click_trv_asections(self, event):
        self.trv_selected_sections.selection_remove(self.trv_selected_sections.selection())

    def click_trv_ssections(self, event):
        self.trv_available_sections.selection_remove(self.trv_available_sections.selection())

    def click_save(self):
        if self.validate_fields():
            name_aux = self.txt_name.get('1.0', 'end-1c')
            description_aux = self.txt_description.get('1.0', 'end-1c')
            if self.decide_template:
                self.directive = Message(action=36, information=[name_aux, description_aux, [], []])
                for item in self.trv_selected_sections.get_children():
                    self.directive.information[2].append(int(self.trv_selected_sections.item(item)['text']))
                    self.directive.information[3].append(self.trv_selected_sections.item(item)['values'][2])
            else:
                self.directive = Message(action=38,
                                         information=[self.id_selected, name_aux, description_aux, [], []])
                for item in self.trv_selected_sections.get_children():
                    self.directive.information[3].append(int(self.trv_selected_sections.item(item)['text']))
                    self.directive.information[4].append(self.trv_selected_sections.item(item)['values'][2])
            self.connection = self.directive.send_directive(self.connection)
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()
        else:
            messagebox.showwarning(parent=self.frm_child_crud, title='Missing information',
                                   message='There are mandatory fields that need to be filled!')

    def click_cancel(self):
        decision = messagebox.askyesno(parent=self.frm_child_crud, title='Cancel',
                                       message='Are you sure you want to cancel?')
        if decision:
            self.clear_fields()
            self.frm_child_crud.grid_forget()
            self.show_frm()

    def validate_fields(self):
        if len(self.txt_name.get('1.0', 'end-1c')) != 0 and len(self.txt_description.get('1.0', 'end-1c')) != 0:
            if len(self.trv_selected_sections.get_children()) != 0:
                return True
            else:
                return False
        else:
            return False

    def clear_fields(self):
        self.txt_name.delete('1.0', 'end-1c')
        self.txt_description.delete('1.0', 'end-1c')

    def click_switch_mandatory(self, event):
        if self.trv_selected_sections.item(self.trv_selected_sections.selection())['text'] != '':
            values = self.trv_selected_sections.item(
                self.trv_selected_sections.focus())['values']
            if values[2] == '':
                self.trv_selected_sections.item(self.trv_selected_sections.focus(), values=(values[0], values[1], '✓'))
            else:
                self.trv_selected_sections.item(self.trv_selected_sections.focus(), values=(values[0], values[1], ''))


