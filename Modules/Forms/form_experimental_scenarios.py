from tkinter import Label, LabelFrame, Frame, Text, Button, filedialog, Canvas, messagebox, PhotoImage
from tkinter.constants import *
from tkinter.ttk import Treeview, Notebook, Combobox, Style
from Modules.Config.Data import *
from PIL import Image, ImageTk
import os
import shutil

from Modules.Config.Data import Message

TITLE_FONT = ("Arial", 18)
SUBTITLE_FONT = ("Arial", 14)
LABEL_FONT = ("Arial", 10)
TEXT_FONT = ("Arial", 10)


class FormParentExSC:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildExSC(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Experimental scenarios administration')
        lbl_experimenter_title.config(fg="#222cb3", font=TITLE_FONT)
        lbl_experimenter_title.grid(row=0, column=0, columnspan=9, pady=50)

    def show_frm(self):
        self.frm_parent.grid(row=0, column=0, columnspan=9, rowspan=9, pady=10, padx=10)
        self.frm_child.show_frm()

    def hide_frm(self):
        self.frm_parent.grid_forget()
        self.frm_child.hide_frm()


class FormChildExSC:
    def __init__(self, frm_parent, connection):
        self.connection = connection
        self.decide = True
        self.id_selected = 0
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_list.config(fg="#222cb3", font=SUBTITLE_FONT)
        self.frm_child_general = LabelFrame(frm_parent)
        self.frm_child_general.config(fg="#222cb3", font=SUBTITLE_FONT)
        self.frm_child_problem = LabelFrame(frm_parent)
        self.frm_child_problem.config(fg="#222cb3", font=SUBTITLE_FONT)
        self.frm_child_control_g = LabelFrame(frm_parent)
        self.frm_child_control_g.config(fg="#222cb3", font=SUBTITLE_FONT)
        self.frm_child_experimental_g = LabelFrame(frm_parent)
        self.frm_child_experimental_g.config(fg="#222cb3", font=SUBTITLE_FONT)
        self.frm_child_sc_component_summary = LabelFrame(frm_parent)
        self.frm_child_sc_component_summary.config(fg="#222cb3", font=SUBTITLE_FONT)
        self.frm_child_experimental_sc_summary = LabelFrame(frm_parent)
        self.frm_child_experimental_sc_summary.config(fg="#222cb3", font=SUBTITLE_FONT)
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
        self.trv_available = Treeview(self.frm_child_list, height=7, columns=('Name', 'Description', 'Active', 'Available'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.heading('#3', text='Active', anchor=CENTER)
        self.trv_available.heading('#4', text='Available', anchor=CENTER)
        self.trv_available.column('#0', width=0, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.column('#3', width=100, minwidth=100, stretch=NO)
        self.trv_available.column('#4', width=100, minwidth=100, stretch=NO)
        self.trv_available.grid(row=1, column=1, columnspan=5, rowspan=10, sticky=W, padx=50, pady=25)

        # Components for General info FRM
        lbl_name = Label(self.frm_child_general, text='Name')
        lbl_name.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=50, sticky=W)
        lbl_description = Label(self.frm_child_general, text='Description')
        lbl_description.config(fg="#222cb3", font=LABEL_FONT)
        lbl_description.grid(pady=10, padx=50, sticky=NW)
        lbl_access = Label(self.frm_child_general, text='Access code')
        lbl_access.config(fg="#222cb3", font=LABEL_FONT)
        lbl_access.grid(row=11, column=0,pady=10, padx=50, sticky=W)
        lbl_start = Label(self.frm_child_general, text='Start time')
        lbl_start.config(fg="#222cb3", font=LABEL_FONT)
        lbl_start.grid(row=12, column=0,pady=10, padx=50, sticky=W)
        lbl_end = Label(self.frm_child_general, text='End time')
        lbl_end.config(fg="#222cb3", font=LABEL_FONT)
        lbl_end.grid(row=13, column=0, pady=10, padx=50, sticky=W)
        self.txt_name = Text(self.frm_child_general, height=1, width=80)
        self.txt_name.config(font=TEXT_FONT)
        self.txt_name.grid(row=0, column=1, padx=50, pady=10, columnspan=8)
        self.txt_description = Text(self.frm_child_general, height=10, width=80)
        self.txt_description.config(font=TEXT_FONT)
        self.txt_description.grid(row=1, column=1, padx=50, pady=10, columnspan=8, rowspan=10)
        self.txt_access_code = Text(self.frm_child_general, height=1, width=80)
        self.txt_access_code.config(font=TEXT_FONT)
        self.txt_access_code.grid(row=11, column=1, padx=50, pady=10, columnspan=8)
        frm_aux1 = Frame(self.frm_child_general)
        self.cbx_start_hour = Combobox(frm_aux1, state="readonly", width=10)
        self.cbx_start_hour.config(font=TEXT_FONT)
        self.cbx_start_hour.grid(pady=10, padx=10, sticky=W)
        lbl_separator = Label(frm_aux1, text=':')
        lbl_separator.config(fg="#222cb3", font=TEXT_FONT)
        lbl_separator.grid(row=0, column=1, pady=10, padx=10, sticky=W)
        self.cbx_start_minute = Combobox(frm_aux1, state="readonly", width=10)
        self.cbx_start_minute.config(font=TEXT_FONT)
        self.cbx_start_minute.grid(row=0, column=2, pady=10, padx=10, sticky=W)
        self.cbx_end_hour = Combobox(frm_aux1, state="readonly", width=10)
        self.cbx_end_hour.config(font=TEXT_FONT)
        self.cbx_end_hour.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        lbl_separator2 = Label(frm_aux1, text=':')
        lbl_separator2.config(fg="#222cb3", font=TEXT_FONT)
        lbl_separator2.grid(row=1, column=1, pady=10, padx=10, sticky=W)
        self.cbx_end_minute = Combobox(frm_aux1, state="readonly", width=10)
        self.cbx_end_minute.config(font=TEXT_FONT)
        self.cbx_end_minute.grid(row=1, column=2, padx=10, pady=10, sticky=W)
        frm_aux1.grid(row=12, column=1, padx=50, rowspan=2, sticky=W)

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        msg = Message(action=27, information=[])
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.receive_message()
        for i in range(0, len(self.connection.message.information)):
            elements = self.connection.message.information[i].split('¥')
            self.trv_available.insert('','end',text=elements[0], values=(elements[1], elements[2]))

    def show_frm(self):
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        self.frm_child_list.grid_forget()
        self.frm_child_general.grid_forget()
        self.frm_child_problem.grid_forget()
        self.frm_child_control_g.grid_forget()
        self.frm_child_experimental_g.grid_forget()
        self.frm_child_sc_component_summary.grid_forget()
        self.frm_child_experimental_sc_summary.grid_forget()

    def click_delete(self):
        """if self.trv_available.selection() != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            msg = Message(action=29, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.lbl_mensaje['text'] = self.connection.message.comment
            self.retrieve_list()
        else:
            self.lbl_mensaje['text'] = 'No register selected'"""
        pass

    def click_new(self):
        self.decide = True
        self.frm_child_list.grid_forget()
        self.txt_name.focus_set()
        self.title_form = 'New Experimental Scenario'
        self.frm_child_general['text'] = self.title_form
        self.frm_child_general.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        """if self.trv_available.selection() != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            self.decide = False
            self.frm_child_list.grid_forget()
            self.frm_child_crud.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
            msg = Message(action=30, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.txt_name.delete(0, END)
            self.txt_name.insert(0, self.connection.message.information[0])
            self.txt_description.delete(0, END)
            self.txt_description.insert(0, self.connection.message.information[1])
            self.txt_members.delete(0, END)
            self.txt_members.insert(0, len(self.connection.message.information[2]))
            s_designers = self.connection.message.information[2]
            msg = Message(action=22, information=[])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            a_designers = self.connection.message.information
            self.retrieve_designers(s_designers, a_designers)
        else:
            self.lbl_mensaje['text'] = 'No register selected'"""

        pass

    """def retrieve_designers(self, s_designers, a_designers):
        for item in self.trv_available_designers.get_children():
            self.trv_available_designers.delete(item)
        for item in self.trv_selected_designers.get_children():
            self.trv_selected_designers.delete(item)
        for item in s_designers:
            if item in a_designers:
                a_designers.remove(item)
        for i in range(0, len(a_designers)):
            elements = a_designers[i].split('¥')
            self.trv_available_designers.insert('', 'end', text=elements[0], values=(elements[1], elements[2]))
        for i in range(0, len(s_designers)):
            elements = s_designers[i].split('¥')
            self.trv_selected_designers.insert('', 'end', text=elements[0], values=(elements[1], elements[2]))

    def click_add(self):
        if self.trv_available_designers.selection() != '' and self.trv_selected_designers.selection() == '':
            self.trv_selected_designers.insert('', 'end', text=self.trv_available_designers.item(
                self.trv_available_designers.focus())['text'], values=self.trv_available_designers.item(
                self.trv_available_designers.focus())['values'])
            self.trv_available_designers.delete(self.trv_available_designers.selection())

    def click_remove(self):
        if self.trv_selected_designers.selection() != '' and self.trv_available_designers.selection() == '':
            self.trv_available_designers.insert('', 'end', text=self.trv_selected_designers.item(
                self.trv_selected_designers.focus())['text'], values=self.trv_selected_designers.item(
                self.trv_selected_designers.focus())['values'])
            self.trv_selected_designers.delete(self.trv_selected_designers.selection())

    def click_trv_adesigners(self, event):
        self.trv_selected_designers.selection_remove(self.trv_selected_designers.selection())

    def click_trv_sdesigners(self, event):
        self.trv_available_designers.selection_remove(self.trv_available_designers.selection())

    def click_save(self):
        if self.validate_fields():
            name_aux = self.txt_name.get()
            description_aux = self.txt_description.get()
            if self.decide:
                msg = Message(action=26, information=[name_aux, description_aux, []])
                for item in self.trv_selected_designers.get_children():
                    msg.information[2].append(int(self.trv_selected_designers.item(item)['text']))
            else:
                msg = Message(action=28, information=[int(self.id_selected), name_aux, description_aux, []])
                for item in self.trv_selected_designers.get_children():
                    msg.information[3].append(int(self.trv_selected_designers.item(item)['text']))
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.frm_child_crud.grid_forget()
            self.show_frm()
            self.lbl_mensaje['text'] = self.connection.message.comment
        else:
            self.lbl_mensaje_crud['text'] = 'Fill all the fields'

    def click_cancel(self):
        self.txt_name.delete(0, END)
        self.txt_description.delete(0, END)
        self.txt_members.delete(0, END)
        '''for item in self.trv_available_designers.get_children():
            self.trv_available_designers.delete(item)
        for item in self.trv_selected_designers.get_children():
            self.trv_selected_designers.delete(item)'''
        self.frm_child_crud.grid_forget()
        self.show_frm()

    def validate_fields(self):
        if len(self.txt_name.get()) != 0 and len(self.txt_description.get()) != 0 and len(self.txt_members.get()) != 0:
            if len(self.trv_selected_designers.get_children()) != 0:
                if int(self.txt_members.get()) == len(self.trv_selected_designers.get_children()):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False"""
