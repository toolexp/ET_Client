import os
import shutil
import hashlib
from tkinter import Tk, Menu, Toplevel, LabelFrame, Label, Entry, Button, messagebox
from tkinter.ttk import Combobox
from tkinter.constants import *
from Modules.Config.Connection import Connection
from Modules.Config.Data import Message, Designer
from Modules.Config.Visual import *

from Modules.Forms.form_AED import FormParentAED
from Modules.Forms.form_designers_groups import FormParentDG
from Modules.Forms.form_experiment_config import FormParentExConfig
from Modules.Forms.form_problems import FormParentProblem
from Modules.Forms.form_templates import FormParentTemplate
from Modules.Forms.form_sections import FormParentSection
from Modules.Forms.form_patterns import FormParentPattern
from Modules.Forms.form_classifications import FormParentClassification
from Modules.Forms.form_experiment_admin import FormParentExAdmin
from Modules.Forms.form_designer_gui import FormParentDesigner

json_config = json.load(open('config.json', 'r'))
HOST = json_config["server"]["address"]     # The server's hostname or IP address
PORT = json_config["server"]["port"]        # The port used by the server


class WindowHome:
    def __init__(self, connection):
        #
        # Configuration of the window
        self.connection = connection
        self.role = 1
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.click_log_out)
        #w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        # self.window.geometry('%dx%d+0+0' % (1024, 778))
        #self.window.geometry('%dx%d+0+0' % (1500, 778))
        #self.window.geometry('%dx%d+0+0' % (w, h))
        # Place window on top left corner
        self.window.geometry('+%d+%d' % (0, 0))
        self.window.resizable(0, 0)
        self.window.title('Tool for experimenting')
        self.window.withdraw()
        self.create_login()
        self.show_login()

    def create_login(self):
        # Resources for the Forms
        self.tlevel_login = Toplevel(self.window)
        self.tlevel_login.protocol("WM_DELETE_WINDOW", self.click_log_out)
        self.tlevel_login.withdraw()
        frm_parent = LabelFrame(self.tlevel_login)
        lbl_title = Label(frm_parent, text='Login')
        lbl_title.config(fg=TEXT_COLOR, font=TITLE_FONT)
        lbl_title.grid(row=0, column=0, columnspan=3, pady=15, sticky=EW)
        lbl_role = Label(frm_parent, text='Role')
        lbl_role.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_role.grid(row=1, column=0, pady=10, padx=30, sticky=NW)
        lbl_username = Label(frm_parent, text='E-mail')
        lbl_username.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_username.grid(row=2, column=0, pady=10, padx=30, sticky=NW)
        lbl_passwd = Label(frm_parent, text='Password')
        lbl_passwd.config(fg=TEXT_COLOR, font=SUBTITLE2_FONT)
        lbl_passwd.grid(row=3, column=0, pady=10, padx=30, sticky=NW)
        self.cbx_role = Combobox(frm_parent, state="readonly", width=25)
        self.cbx_role['values'] = ['Administrator', 'Experimenter', 'Designer']
        self.cbx_role.grid(row=1, column=1, pady=10, padx=30, columnspan=2, sticky=NW)
        self.txt_email = Entry(frm_parent, width=25)
        self.txt_email.grid(row=2, column=1, pady=10, padx=30, columnspan=2, sticky=NW)
        self.txt_passwd = Entry(frm_parent, width=25, show="*")
        self.txt_passwd.grid(row=3, column=1, pady=10, padx=30, columnspan=2, sticky=NW)
        btn_access = Button(frm_parent, text='Login', command=self.click_login)
        btn_access.grid(row=4, column=1, padx=30, pady=15)
        btn_exit = Button(frm_parent, text='Exit', command=self.click_log_out)
        btn_exit.grid(row=4, column=2, padx=30, pady=15)
        frm_parent.grid(padx=10, pady=10)

    def show_login(self):
        self.tlevel_login.title('System access')
        self.tlevel_login.deiconify()
        self.tlevel_login.grab_set()

    def click_login(self):
        if len(self.txt_email.get()) != 0 and len(self.txt_passwd.get()) != 0 and len(
                self.cbx_role.get()) != 0:  # validate empty fileds in login form
            if self.cbx_role.get() == 'Experimenter':  # directive (action) changes in accordance of the role
                self.role = 1
                self.directive = Message(action=20, information=[self.txt_email.get(), 'login'])
            elif self.cbx_role.get() == 'Designer':
                self.role = 2
                self.directive = Message(action=25, information=[self.txt_email.get(), 'login'])
            elif self.cbx_role.get() == 'Administrator':
                self.role = 3
                self.directive = Message(action=15, information=[self.txt_email.get(), 'login'])
            self.connection = self.directive.send_directive(self.connection)
            if self.connection.message.action == 5:  # The user does not exist
                messagebox.showerror(parent=self.tlevel_login, title='E-mail',
                                     message=self.connection.message.information[0])
            else:  # block to validate the inserted password
                if self.role == 2:
                    self.current_designer = Designer(id=self.connection.message.information[0],
                                                     name=self.connection.message.information[1],
                                                     surname=self.connection.message.information[2],
                                                     user=self.connection.message.information[3],
                                                     password=self.connection.message.information[4],
                                                     connection=self.connection)
                    if self.current_designer.password == hashlib.sha1(self.txt_passwd.get().encode()).hexdigest():
                        self.access_system()
                    else:
                        messagebox.showerror(parent=self.tlevel_login, title='Password',
                                             message='The password you provided is wrong, retry')
                elif self.role == 1:
                    if self.connection.message.information[4] == hashlib.sha1(
                            self.txt_passwd.get().encode()).hexdigest():
                        self.access_system()
                    else:
                        messagebox.showerror(parent=self.tlevel_login, title='Password',
                                             message='The password you provided is wrong, retry')
                elif self.role == 3:
                    if self.connection.message.information[4] == hashlib.sha1(
                            self.txt_passwd.get().encode()).hexdigest():
                        self.access_system()
                    else:
                        messagebox.showerror(parent=self.tlevel_login, title='Password',
                                             message='The password you provided is wrong, retry')
        else:
            messagebox.showwarning(parent=self.tlevel_login, title='Missing information', message='Fill all the fields')

    def access_system(self):
        # Components (tool bar) will be shown depending on the role of the user
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)
        if self.role == 1:  # logged as experimenter
            administration_menu = Menu(menu_bar, tearoff=0)
            designers_menu = Menu(administration_menu, tearoff=0)
            designers_menu.add_command(label='Designers', command=self.click_designers)
            designers_menu.add_command(label='Designers groups', command=self.click_designers_groups)
            administration_menu.add_cascade(label='Designers', menu=designers_menu)
            patterns_menu = Menu(administration_menu, tearoff=0)
            patt_structure_menu = Menu(patterns_menu, tearoff=0)
            patt_structure_menu.add_command(label='Classifications', command=self.click_class)
            patt_structure_menu.add_command(label='Sections', command=self.click_sections)
            patt_structure_menu.add_command(label='Templates', command=self.click_templates)
            patterns_menu.add_cascade(label='Pattern structure', menu=patt_structure_menu)
            patterns_menu.add_command(label='Patterns', command=self.click_patterns)
            administration_menu.add_cascade(label='Patterns', menu=patterns_menu)
            administration_menu.add_command(label='Problems', command=self.click_problems)
            experiment_menu = Menu(administration_menu, tearoff=0)
            experiment_menu.add_command(label='Experiment administration', command=self.click_exp_admin)
            experiment_menu.add_command(label='Experiment configuration', command=self.click_config_ex_sc)
            menu_bar.add_cascade(label='Administration', menu=administration_menu)
            menu_bar.add_cascade(label='Experiment', menu=experiment_menu)

            # Configuration of the existing frames, one for each command in the menu bar
            self.frm_parent_designer = FormParentAED(self.window, 'Designer', connection)
            self.frm_parent_designers_group = FormParentDG(self.window, connection)
            self.frm_parent_template = FormParentTemplate(self.window, connection)
            self.frm_parent_class = FormParentClassification(self.window, connection)
            self.frm_parent_section = FormParentSection(self.window, connection)
            self.frm_parent_problem = FormParentProblem(self.window, connection)
            self.frm_parent_pattern = FormParentPattern(self.window, connection)
            self.frm_parent_exp_config = FormParentExConfig(self.window, connection)
            self.frm_parent_exp_admin = FormParentExAdmin(self.window, connection)
        elif self.role == 2:  # logged as designer
            self.frm_parent_designer_gui = FormParentDesigner(self.window, connection, self.current_designer)
            self.click_designer_gui()
        elif self.role == 3:  # logged as administrator
            administration_menu = Menu(menu_bar, tearoff=0)
            users_menu = Menu(administration_menu, tearoff=0)
            users_menu.add_command(label='Administrators', command=self.click_administrators)
            users_menu.add_command(label='Experimenters', command=self.click_experimenters)
            designers_menu = Menu(users_menu, tearoff=0)
            designers_menu.add_command(label='Designers', command=self.click_designers)
            designers_menu.add_command(label='Designers groups', command=self.click_designers_groups)
            users_menu.add_cascade(label='Designers', menu=designers_menu)
            administration_menu.add_cascade(label='Users', menu=users_menu)
            patterns_menu = Menu(administration_menu, tearoff=0)
            patt_structure_menu = Menu(patterns_menu, tearoff=0)
            patt_structure_menu.add_command(label='Classifications', command=self.click_class)
            patt_structure_menu.add_command(label='Sections', command=self.click_sections)
            patt_structure_menu.add_command(label='Templates', command=self.click_templates)
            patterns_menu.add_cascade(label='Pattern structure', menu=patt_structure_menu)
            patterns_menu.add_command(label='Patterns', command=self.click_patterns)
            administration_menu.add_cascade(label='Patterns', menu=patterns_menu)
            administration_menu.add_command(label='Problems', command=self.click_problems)
            experiment_menu = Menu(administration_menu, tearoff=0)
            experiment_menu.add_command(label='Experiment administration', command=self.click_exp_admin)
            experiment_menu.add_command(label='Experiment configuration', command=self.click_config_ex_sc)
            menu_bar.add_cascade(label='Administration', menu=administration_menu)
            menu_bar.add_cascade(label='Experiment', menu=experiment_menu)

            # Configuration of the existing frames, one for each command in the menu bar
            self.frm_parent_administrator = FormParentAED(self.window, 'Administrator', connection)
            self.frm_parent_experimenter = FormParentAED(self.window, 'Experimenter', connection)
            self.frm_parent_designer = FormParentAED(self.window, 'Designer', connection)
            self.frm_parent_designers_group = FormParentDG(self.window, connection)
            self.frm_parent_template = FormParentTemplate(self.window, connection)
            self.frm_parent_class = FormParentClassification(self.window, connection)
            self.frm_parent_section = FormParentSection(self.window, connection)
            self.frm_parent_problem = FormParentProblem(self.window, connection)
            self.frm_parent_pattern = FormParentPattern(self.window, connection)
            self.frm_parent_exp_config = FormParentExConfig(self.window, connection)
            self.frm_parent_exp_admin = FormParentExAdmin(self.window, connection)
        else:
            raise Exception('Error while trying login the system')
        menu_bar.add_command(label='Log out', command=self.click_log_out)
        self.tlevel_login.grab_release()
        self.tlevel_login.withdraw()
        self.window.deiconify()

    def click_experimenters(self):
        self.frm_parent_designer.hide_frm()
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_exp_config.hide_frm()
        self.frm_parent_exp_admin.hide_frm()
        self.frm_parent_experimenter.hide_frm()
        self.frm_parent_experimenter.show_frm()

    def click_designers(self):
        if self.role == 3:
            self.frm_parent_administrator.hide_frm()
            self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_exp_config.hide_frm()
        self.frm_parent_exp_admin.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_designer.show_frm()

    def click_administrators(self):
        self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_exp_config.hide_frm()
        self.frm_parent_exp_admin.hide_frm()
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_administrator.show_frm()

    def click_designers_groups(self):
        if self.role == 3:
            self.frm_parent_administrator.hide_frm()
            self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_exp_config.hide_frm()
        self.frm_parent_exp_admin.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_designers_group.show_frm()

    def click_templates(self):
        if self.role == 3:
            self.frm_parent_administrator.hide_frm()
            self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_exp_config.hide_frm()
        self.frm_parent_exp_admin.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_template.show_frm()

    def click_sections(self):
        if self.role == 3:
            self.frm_parent_administrator.hide_frm()
            self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_exp_config.hide_frm()
        self.frm_parent_exp_admin.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_section.show_frm()

    def click_class(self):
        if self.role == 3:
            self.frm_parent_administrator.hide_frm()
            self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_exp_config.hide_frm()
        self.frm_parent_exp_admin.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_class.show_frm()

    def click_patterns(self):
        if self.role == 3:
            self.frm_parent_administrator.hide_frm()
            self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_exp_config.hide_frm()
        self.frm_parent_exp_admin.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_pattern.show_frm()

    def click_problems(self):
        if self.role == 3:
            self.frm_parent_administrator.hide_frm()
            self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_exp_config.hide_frm()
        self.frm_parent_exp_admin.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_problem.show_frm()

    def click_config_ex_sc(self):
        if self.role == 3:
            self.frm_parent_administrator.hide_frm()
            self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_exp_admin.hide_frm()
        self.frm_parent_exp_config.hide_frm()
        self.frm_parent_exp_config.show_frm()

    def click_exp_admin(self):
        if self.role == 3:
            self.frm_parent_administrator.hide_frm()
            self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_exp_config.hide_frm()
        self.frm_parent_exp_admin.hide_frm()
        self.frm_parent_exp_admin.show_frm()

    def click_designer_gui(self):
        self.frm_parent_designer_gui.hide_frm()
        self.frm_parent_designer_gui.show_frm()

    def click_log_out(self):
        if self.role != 2:
            msg = Message(comment='close_connection')
            self.connection.create_message(msg)
            self.connection.send_message()
            self.connection.close_connection()
            shutil.rmtree('./Resources/temp/')
            os.mkdir('./Resources/temp/')
            self.window.destroy()
        else:
            # Cant log out if designer is running an experimental scenario
            try:
                if not self.frm_parent_designer_gui.frm_general.grid_info():
                    msg = Message(comment='close_connection')
                    self.connection.create_message(msg)
                    self.connection.send_message()
                    self.connection.close_connection()
                    shutil.rmtree('./Resources/temp/')
                    os.mkdir('./Resources/temp/')
                    self.window.destroy()
                else:
                    messagebox.showerror(parent=self.window, title='Can not exit',
                                         message='You must finish current experimental scenario to exit')
            except:
                msg = Message(comment='close_connection')
                self.connection.create_message(msg)
                self.connection.send_message()
                self.connection.close_connection()
                shutil.rmtree('./Resources/temp/')
                os.mkdir('./Resources/temp/')
                self.window.destroy()


if __name__ == '__main__':
    connection = Connection()
    try:
        connection.create_connection(HOST, PORT)
        app = WindowHome(connection)
        app.window.mainloop()
    except Exception as e:
        error = 'Error with the client: ' + str(e)
        print(error)
    finally:
        connection.close_connection()
