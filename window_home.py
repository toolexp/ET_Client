from tkinter import ttk
from tkinter import Tk, Menu
from Modules.Config.Connection import Connection
from Modules.Config.Data import Message
from Modules.Forms.form_AED import FormParentAED
from Modules.Forms.form_designers_groups import FormParentDG
from Modules.Forms.form_experimental_scenarios import FormParentExSC
from Modules.Forms.form_problems import FormParentProblem
from Modules.Forms.form_templates import FormParentTemplate
from Modules.Forms.form_sections import FormParentSection
from Modules.Forms.form_patterns import FormParentPattern
from Modules.Forms.form_classifications import FormParentClassification

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65450        # The port used by the server


class WindowHome:
    def __init__(self, connection):
        #
        # Configuration of the window
        self.connection = connection
        self.window = Tk()
        self.window.title('Tool for experimenting')
        #w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        #self.window.geometry('%dx%d+0+0' % (1024, 778))
        self.window.geometry('%dx%d+0+0' % (1500, 778))
        #self.window.geometry('%dx%d+0+0' % (w, h))
        self.window.resizable(0, 0)

        # Configuration of the top Menu bar
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)
        administration_menu = Menu(menu_bar)
        users_menu = Menu(administration_menu)
        users_menu.add_command(label='Administrators', command=self.click_administrators)
        users_menu.add_command(label='Experimenters', command=self.click_experimenters)
        users_menu.add_command(label='Designers', command=self.click_designers)
        administration_menu.add_cascade(label='Users', menu=users_menu)
        administration_menu.add_command(label='Designers groups', command=self.click_designers_groups)
        template_menu = Menu(administration_menu)
        template_menu.add_command(label='Classifications', command=self.click_class)
        template_menu.add_command(label='Sections', command=self.click_sections)
        template_menu.add_command(label='Templates', command=self.click_templates)
        administration_menu.add_cascade(label='Pattern structure', menu=template_menu)
        administration_menu.add_command(label='Patterns', command=self.click_patterns)
        administration_menu.add_command(label='Problems', command=self.click_problems)
        experiment_menu = Menu(administration_menu)
        experiment_menu.add_command(label='Experiment administration')
        experiment_menu.add_command(label='Experiment configuration', command=self.click_config_ex_sc)
        administration_menu.add_cascade(label='Experiment', menu=experiment_menu)
        menu_bar.add_cascade(label='Administration', menu=administration_menu)
        menu_bar.add_command(label='Log out', command=self.click_log_out)

        # Configuration of the existing frames, one for each command in the menu bar
        self.frm_parent_administrator = FormParentAED(self.window, 'Administrator', connection)
        self.frm_parent_experimenter = FormParentAED(self.window, 'Experimenter', connection)
        self.frm_parent_designer = FormParentAED(self.window, 'Designer', connection)
        self.frm_parent_designers_group = FormParentDG(self.window, connection)
        self.frm_parent_template = FormParentTemplate(self.window, connection)
        self.frm_parent_class = FormParentClassification(self.window, connection)
        self.frm_parent_section = FormParentSection(self.window, connection)
        self.frm_parent_problem = FormParentProblem(self.window,connection)
        self.frm_parent_pattern = FormParentPattern(self.window, connection)
        self.frm_parent_ex_sc = FormParentExSC(self.window, connection)

    def click_experimenters(self):
        self.frm_parent_designer.hide_frm()
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_ex_sc.hide_frm()
        self.frm_parent_experimenter.hide_frm()
        self.frm_parent_experimenter.show_frm()

    def click_designers(self):
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_ex_sc.hide_frm()
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
        self.frm_parent_ex_sc.hide_frm()
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_administrator.show_frm()

    def click_designers_groups(self):
        self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_ex_sc.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_designers_group.show_frm()

    def click_templates(self):
        self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_ex_sc.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_template.show_frm()

    def click_sections(self):
        self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_ex_sc.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_section.show_frm()

    def click_class(self):
        self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_ex_sc.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_class.show_frm()

    def click_patterns(self):
        self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_ex_sc.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_pattern.show_frm()

    def click_problems(self):
        self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_ex_sc.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_problem.show_frm()

    def click_config_ex_sc(self):
        self.frm_parent_experimenter.hide_frm()
        self.frm_parent_designer.hide_frm()
        self.frm_parent_administrator.hide_frm()
        self.frm_parent_designers_group.hide_frm()
        self.frm_parent_template.hide_frm()
        self.frm_parent_section.hide_frm()
        self.frm_parent_pattern.hide_frm()
        self.frm_parent_class.hide_frm()
        self.frm_parent_problem.hide_frm()
        self.frm_parent_ex_sc.hide_frm()
        self.frm_parent_ex_sc.show_frm()


    def click_log_out(self):
        msg = Message(comment='close_connection')
        self.connection.create_message(msg)
        self.connection.send_message()
        self.connection.close_connection()
        self.window.destroy()

if __name__=='__main__':
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