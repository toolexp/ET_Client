import os
from tkinter import Label, LabelFrame, Frame, Text, Button, messagebox, PhotoImage
from tkinter.constants import *
from tkinter.ttk import Treeview
from Modules.Config.Data import Message

TITLE_FONT = ("Arial", 18)
SUBTITLE_FONT = ("Arial", 14)
LABEL_FONT = ("Arial", 10)
TEXT_FONT = ("Arial", 10)


class FormParentTemplate:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildTemplate(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Templates administration')
        lbl_experimenter_title.config(fg="#222cb3", font=TITLE_FONT)
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
        self.frm_child_crud.config(fg="#222cb3", font=SUBTITLE_FONT)
        self.frm_child_section = LabelFrame(frm_parent)
        self.frm_child_section.config(fg="#222cb3", font=SUBTITLE_FONT)
        self.initialize_components()

    def initialize_components(self):
        # Components for List FRM
        self.new_icon = PhotoImage(file=r"./Resources/create.png").subsample(2, 2)
        self.modify_icon = PhotoImage(file=r"./Resources/modify.png").subsample(2, 2)
        self.remove_icon = PhotoImage(file=r"./Resources/delete.png").subsample(2, 2)
        frm_aux4 = Frame(self.frm_child_list)
        Button(frm_aux4, image=self.new_icon, command=self.click_new).grid(row=0, column=0, pady=10, padx=10, sticky=E)
        Button(frm_aux4, image=self.remove_icon, command=self.click_delete).grid(row=1, column=0, pady=10, padx=10,
                                                                                 sticky=E)
        Button(frm_aux4, image=self.modify_icon, command=self.click_update).grid(row=2, column=0, pady=10, padx=10,
                                                                                 sticky=E)
        frm_aux4.grid(row=1, column=0, pady=35, padx=20, sticky=NW)
        self.trv_available = Treeview(self.frm_child_list, height=7, columns=('Name', 'Description'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=100, minwidth=100, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.bind("<ButtonRelease-1>", self.select_template_summary)
        self.trv_available.grid(row=1, column=1, columnspan=10, rowspan=20, sticky=W, padx=50, pady=25)
        self.trv_list_summary = Treeview(self.frm_child_list, height=5, columns=('Section', 'Data type', 'Mandatory'),
                                         selectmode='none')
        self.trv_list_summary.heading('#0', text='ID', anchor=CENTER)
        self.trv_list_summary.heading('#1', text='Section', anchor=CENTER)
        self.trv_list_summary.heading('#2', text='Data type', anchor=CENTER)
        self.trv_list_summary.heading('#3', text='Mandatory', anchor=CENTER)
        self.trv_list_summary.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_list_summary.column('#1', width=100, minwidth=100, stretch=NO)
        self.trv_list_summary.column('#2', width=200, minwidth=200, stretch=NO)
        self.trv_list_summary.column('#3', width=100, minwidth=100, stretch=NO)
        self.trv_list_summary.grid(row=1, column=11, columnspan=5, rowspan=20, sticky=W, padx=50, pady=100)

        # Components for CRUD FRM
        frm_aux1 = Frame(self.frm_child_crud)
        frm_aux2 = Frame(self.frm_child_crud)
        lbl_name = Label(frm_aux1, text='Name')
        lbl_name.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_description = Label(frm_aux1, text='Description')
        lbl_description.config(fg="#222cb3", font=LABEL_FONT)
        lbl_description.grid(pady=10, padx=50, sticky=NW)
        self.txt_name = Text(frm_aux1, height=1, width=60)
        self.txt_name.config(font=TEXT_FONT)
        self.txt_name.grid(row=0, column=1, padx=10)
        self.txt_description = Text(frm_aux1, height=6, width=60)
        self.txt_description.config(font=TEXT_FONT)
        self.txt_description.grid(row=1, column=1, padx=10, pady=10)
        Button(frm_aux1, text='Save', command=self.click_save).grid(row=0, column=2, padx=30, sticky=W)
        Button(frm_aux1, text='Cancel', command=self.click_cancel).grid(row=1, column=2, padx=30, sticky=NW)
        lbl_available_d = Label(frm_aux2, text='Available sections')
        lbl_available_d.config(fg="#222cb3", font=LABEL_FONT)
        lbl_available_d.grid(row=0, column=0, pady=10, sticky=W)
        lbl_selected_d = Label(frm_aux2, text='Selected sections')
        lbl_selected_d.config(fg="#222cb3", font=LABEL_FONT)
        lbl_selected_d.grid(row=0, column=2, pady=10, sticky=W)
        self.trv_available_sections = Treeview(frm_aux2, height=5, columns=('Name', 'Data Type'))
        self.trv_available_sections.heading('#0', text='ID', anchor=CENTER)
        self.trv_available_sections.heading('#1', text='Name', anchor=CENTER)
        self.trv_available_sections.heading('#2', text='Data Type', anchor=CENTER)
        self.trv_available_sections.column('#0', width=0, minwidth=20, stretch=NO)
        self.trv_available_sections.column('#1', width=150, minwidth=150, stretch=NO)
        self.trv_available_sections.column('#2', width=120, minwidth=120, stretch=NO)
        self.trv_available_sections.bind("<Button-1>", self.click_trv_asections)
        self.trv_available_sections.grid(row=1, column=0, rowspan=10, sticky=W, padx=10, pady=20)
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
        self.trv_selected_sections.grid(row=1, column=2, rowspan=10, sticky=W, padx=10, pady=20)
        Button(frm_aux2, text='Add', command=self.click_add).grid(row=4, column=1)
        Button(frm_aux2, text='Remove', command=self.click_remove).grid(row=5, column=1)
        self.up_arrow = PhotoImage(file=r"./Resources/up_arrow.png")
        self.up_arrow = self.up_arrow.subsample(2, 2)
        self.down_arrow = PhotoImage(file=r"./Resources/down_arrow.png")
        self.down_arrow = self.down_arrow.subsample(2, 2)
        Button(frm_aux2, image=self.up_arrow, command=self.click_up).grid(row=4, column=3)
        Button(frm_aux2, image=self.down_arrow, command=self.click_down).grid(row=5, column=3)
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
            self.trv_available.insert('', 'end', text=elements[0], values=(elements[1], elements[2]))

    def select_template_summary(self, event):
        """
        Function activated when the event of selecting an item in the available templates TV is generated. It fills the
        summary TV with information of the selected template
        :param event:
        """
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])  # Retrieve id of selected item from TreeView
            self.directive = Message(action=77, information=[id_selected])  # ask for the sections of the selected template
            self.connection = self.directive.send_directive(self.connection)
            # Remove existing elements in the list
            for item in self.trv_list_summary.get_children():
                self.trv_list_summary.delete(item)
            # Adding elements in the list
            for item in self.connection.message.information:
                elements = item.split('¥')
                self.trv_list_summary.insert('', 'end', text='', values=(elements[3], elements[5], elements[7]))


    def show_frm(self):
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        self.clear_fields()
        self.frm_child_list.grid_forget()
        self.frm_child_crud.grid_forget()

    def click_delete(self):
        if self.trv_available.item(self.trv_available.selection())['text'] != '':
            decision = messagebox.askyesno(title='Confirmation',
                                           message='Are you sure you want to delete the item?')
            if decision:
                self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
                self.directive = Message(action=39, information=[self.id_selected])
                self.connection = self.directive.send_directive(self.connection)
                if self.connection.message.action == 5:
                    messagebox.showwarning(title='Fail deleting',
                                           message='The template cant be deleted, it may be used in a pattern')
                self.retrieve_list()
        else:
            messagebox.showwarning(title='No selection', message='You must select an item')

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
            self.id_selected = int(self.trv_available.item(self.trv_available.selection())['text'])
            self.directive = Message(action=40, information=[self.id_selected])
            self.connection = self.directive.send_directive(self.connection)
            self.txt_name.insert('1.0', self.connection.message.information[0])
            self.txt_description.insert('1.0', self.connection.message.information[1])
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
            messagebox.showwarning(title='No selection', message='You must select an item')

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
            decision = messagebox.askyesnocancel(title='Add section', message='Is the selected section mandatory?')
            if decision:
                values = self.trv_available_sections.item(
                    self.trv_available_sections.focus())['values']
                text = self.trv_available_sections.item(
                    self.trv_available_sections.focus())['text']
                self.trv_selected_sections.insert('', 'end', text=text, values=(values[0], values[1], '✓'))
                self.trv_available_sections.delete(self.trv_available_sections.selection())
            elif decision == False:
                values = self.trv_available_sections.item(
                    self.trv_available_sections.focus())['values']
                text = self.trv_available_sections.item(
                    self.trv_available_sections.focus())['text']
                self.trv_selected_sections.insert('', 'end', text=text, values=(values[0], values[1], ''))
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
            decision = messagebox.askyesno(title='Confirmation', message='Are you sure you want to save the changes?')
            if decision:
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
            messagebox.showwarning(title='Missing information',
                                   message='There are mandatory fields that need to be filled!')

    def click_cancel(self):
        decision = messagebox.askyesno(title='Cancel', message='Are you sure you want to cancel?')
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
