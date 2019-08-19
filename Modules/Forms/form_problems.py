from tkinter import ttk
from tkinter import *
from Modules.Config.Message import Message

TITLE_FONT = ("Arial", 14, "bold")
SUBTITLE_FONT = ("Arial", 12, "bold")
ERROR_FONT = ("Arial", 10, "italic")
LABEL_FONT = ("Arial", 10)


class FormParentProblem:
    def __init__(self, window, connection):
        self.frm_parent = LabelFrame(window)
        self.initialize_components()
        self.frm_child = FormChildProblem(self.frm_parent, connection)

    def initialize_components(self):
        lbl_experimenter_title = Label(self.frm_parent, text='Problems administration')
        lbl_experimenter_title.config(fg="#222cb3", font=TITLE_FONT)
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
        self.id_selected = 0
        self.frm_child_list = LabelFrame(frm_parent)
        self.frm_child_crud_sol = LabelFrame(frm_parent)
        self.frm_child_patterns = LabelFrame(frm_parent)
        self.frm_child_diagram = LabelFrame(frm_parent)
        self.initialize_components()

    def initialize_components(self):
        # Components for List FRM
        lbl_available = Label(self.frm_child_list, text='Available problems')
        lbl_available.config(fg="#222cb3", font=SUBTITLE_FONT)
        lbl_available.grid(row=0, column=1, columnspan=4, rowspan=2, sticky=NW+SW, pady=50, padx=100)
        self.trv_available = ttk.Treeview(self.frm_child_list, height=20, columns=('Name', 'Description'))
        self.trv_available.heading('#0', text='ID', anchor=CENTER)
        self.trv_available.heading('#1', text='Name', anchor=CENTER)
        self.trv_available.heading('#2', text='Description', anchor=CENTER)
        self.trv_available.column('#0', width=50, minwidth=50, stretch=NO)
        self.trv_available.column('#1', width=200, minwidth=200, stretch=NO)
        self.trv_available.column('#2', width=400, minwidth=400, stretch=NO)
        self.trv_available.grid(row=2, column=1, columnspan=5, rowspan=10, sticky=W, padx=100)
        Button(self.frm_child_list, text='New', command=self.click_new).grid(row=2, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Delete', command=self.click_delete).grid(row=3, column=7, columnspan=2, padx=25, sticky=W)
        Button(self.frm_child_list, text='Update', command=self.click_update).grid(row=4, column=7, columnspan=2, padx=25, sticky=W)
        self.lbl_mensaje = Label(self.frm_child_list, text='')
        self.lbl_mensaje.config(fg="red", font=ERROR_FONT)
        self.lbl_mensaje.grid(row=0, column=5, columnspan=4, rowspan=2)

        # Components for CRUD_SOL FRM
        frm_aux1 = LabelFrame(self.frm_child_crud_sol, text='Problem')
        frm_aux2 = LabelFrame(self.frm_child_crud_sol, text='Ideal solution')
        lbl_name = Label(frm_aux1, text='Problem name')
        lbl_name.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name.grid(pady=10, padx=100, sticky=NW)
        lbl_description = Label(frm_aux1, text='Problem description')
        lbl_description.config(fg="#222cb3", font=LABEL_FONT)
        lbl_description.grid(padx=100, sticky=NW)
        self.txt_name_prob = Text(frm_aux1, height=1, width=60)
        self.txt_name_prob.grid(row=0, column=1, padx=10)
        self.txt_description_prob = Text(frm_aux1, height=6, width=60)
        self.txt_description_prob.grid(row=1, column=1, padx=10, pady=10)
        lbl_name_sol = Label(frm_aux2, text='Solution name')
        lbl_name_sol.config(fg="#222cb3", font=LABEL_FONT)
        lbl_name_sol.grid(pady=10, padx=100, sticky=NW)
        lbl_descr_sol = Label(frm_aux2, text='Solution description')
        lbl_descr_sol.config(fg="#222cb3", font=LABEL_FONT)
        lbl_descr_sol.grid(padx=100, sticky=NW)
        self.txt_name_sol = Text(frm_aux2, height=1, width=60)
        self.txt_name_sol.grid(row=0, column=1, padx=10)
        self.txt_description_sol = Text(frm_aux2, height=6, width=60)
        self.txt_description_sol.grid(row=1, column=1, padx=10, pady=10)
        var1 = IntVar()
        self.check_patterns = Checkbutton(frm_aux2, text="The solution includes patterns",variable=var1)
        self.check_patterns.grid(sticky=W)
        var2 = IntVar()
        self.check_diagram = Checkbutton(frm_aux2, text="The solution includes a diagram",variable=var2)
        self.check_diagram.grid(sticky=W)
        Button(self.frm_child_crud_sol, text='Next', command=self.click_next1).grid(row=4, column=5, padx=35)
        Button(self.frm_child_crud_sol, text='Cancel', command=self.click_cancel).grid(row=5, column=5, padx=35)
        self.lbl_mensaje_crud_sol = Label(self.frm_child_crud_sol, text='')
        self.lbl_mensaje_crud_sol.config(fg="red", font=ERROR_FONT)
        self.lbl_mensaje_crud_sol.grid(row=0, column=0, pady=5, sticky=W)
        frm_aux1.grid(row=1, column=0, pady=10, padx=10, columnspan=5,rowspan=5)
        frm_aux2.grid(row=8, column=0, pady=10, columnspan=5, rowspan=10)

    def retrieve_list(self):
        # Remove existing elements in the list
        for item in self.trv_available.get_children():
            self.trv_available.delete(item)
        msg = Message(action=52, information=[])
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.receive_message()
        for i in range(0, len(self.connection.message.information)):
            elements = self.connection.message.information[i].split(':')
            self.trv_available.insert('','end',text=elements[0], values=(elements[1], elements[2]))

    def show_frm(self):
        self.retrieve_list()
        self.frm_child_list.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def hide_frm(self):
        self.frm_child_list.grid_forget()
        self.frm_child_crud_sol.grid_forget()
        self.frm_child_patterns.grid_forget()
        self.frm_child_diagram.grid_forget()

    def click_delete(self):
        if self.trv_available.selection() != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            msg = Message(action=54, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.lbl_mensaje['text'] = self.connection.message.comment
            self.retrieve_list()
        else:
            self.lbl_mensaje['text'] = 'No register selected'

    def click_new(self):
        self.decide = True
        self.frm_child_list.grid_forget()
        self.txt_name_prob.delete(1.0, END)
        self.txt_description_prob.delete(1.0, END)
        self.txt_name_sol.delete(1.0, END)
        self.txt_description_sol.delete(1.0, END)
        self.frm_child_crud_sol.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)

    def click_update(self):
        '''if self.trv_available.selection() != '':
            item = self.trv_available.item(self.trv_available.selection())
            self.id_selected = item['text']
            self.decide = False
            self.frm_child_list.grid_forget()
            self.frm_child_crud_sol.grid(row=1, column=0, columnspan=9, rowspan=8, pady=10, padx=10)
            msg = Message(action=45, information=[int(self.id_selected)])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            self.txt_name_prob.delete(0, END)
            self.txt_name_prob.insert(0, self.connection.message.information[0])
            self.txt_description_prob.delete(0, END)
            self.txt_description_prob.insert(0, self.connection.message.information[1])

            s_designers = self.connection.message.information[2]
            msg = Message(action=22, information=[])
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.receive_message()
            a_designers = self.connection.message.information
            self.retrieve_designers(s_designers, a_designers)
        else:
            self.lbl_mensaje['text'] = 'No register selected'''
        pass

    '''def retrieve_designers(self, s_designers, a_designers):
        for item in self.trv_available_designers.get_children():
            self.trv_available_designers.delete(item)
        for item in self.trv_selected_designers.get_children():
            self.trv_selected_designers.delete(item)
        for item in s_designers:
            if item in a_designers:
                a_designers.remove(item)
        for i in range(0, len(a_designers)):
            elements = a_designers[i].split(':')
            self.trv_available_designers.insert('', 'end', text=elements[0], values=(elements[1], elements[2]))
        for i in range(0, len(s_designers)):
            elements = s_designers[i].split(':')
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
        self.trv_available_designers.selection_remove(self.trv_available_designers.selection())'''

    def click_next1(self):
        '''if self.validate_fields():
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
            self.lbl_mensaje_crud['text'] = 'Fill all the fields'''
        pass

    def click_cancel(self):
        '''self.txt_name.delete(0, END)
        self.txt_description.delete(0, END)
        self.txt_members.delete(0, END)
        self.frm_child_crud.grid_forget()
        self.show_frm()'''
        pass

    '''def validate_fields(self):
        if len(self.txt_name.get()) != 0 and len(self.txt_description.get()) != 0 and len(self.txt_members.get()) != 0:
            if len(self.trv_selected_designers.get_children()) != 0:
                if int(self.txt_members.get()) == len(self.trv_selected_designers.get_children()):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False'''
