import textwrap
import threading
import time
import datetime
from tkinter import Label, Toplevel
import pandas as pd


def verify_ip(ip):
    """
    Verifies that the format of an IP address is correct

    :param ip: ip address
    :type ip: str
    :return: success or not depending on the validation
    :rtype: bool
    """
    try:
        digits = ip.split('.')
        for item in digits:
            if not item.isdigit():
                return False
            if int(item) > 255:
                return False
    except:
        return False
    return True


def verify_port(port):
    """
    Verifies that the format of a port number is correct (range)

    :param port: port number
    :type port: int
    :return: success or not depending on the validation
    :rtype: bool
    """
    if 1023 < int(port) <= 65535:
            return True
    return False


def summarize_text(string, lenght=90):
    if len(string) > lenght / 6:
        return string[:int(lenght / 6) - 3] + '...'
    else:
        return string


def wrap_text(string, lenght=90):
    return '\n'.join(textwrap.wrap(string, lenght))


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def get_mean_value(df=None):
    # First obtain the fourth metric (selection efficiency) and replace in the selected patterns column
    df['m4'] = df.apply(lambda row: row['m4']/row['m3'] if row['m4'] is not None else None, axis=1)
    df_designers = df[['id', 'variable']]
    df_designers = df_designers.append(pd.DataFrame({'id': None, 'variable': 'AVERAGE'}, index=[0]),
                                       ignore_index=True)
    df.drop(columns=['id', 'variable'], inplace=True)
    df_mean = df.mean(axis=0, skipna=True)
    df = df.append(df_mean, ignore_index=True)
    df = df.round(decimals=3)
    df = df_designers.join(df)
    df.fillna('X', inplace=True)
    return df


class Category:
    def __init__(self, id=0, name='', classification_id=0):
        self.id = id
        self.name = name
        self.classification_id = classification_id


class Classification:
    def __init__(self, id=0, name='', categories=None):
        if categories is None:
            categories = []
        self.id = id
        self.name = name
        self.categories = categories


class CreateToolTip(object):
    """
    Create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                      background='white', relief='solid', borderwidth=1,
                      font=("arial", "8", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


class Designer:
    def __init__(self, id=0, name='', surname='', user='', password='', current_group='control', connection=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.user = user
        self.password = password
        self.current_group = current_group
        self.connection = connection
        if self.connection is not None:
            self.retrieve_components()

    def retrieve_components(self):
        if self.id == 0:
            self.directive = Message(action=25, information=[self.id])
            self.connection = self.directive.send_directive(self.connection)
            self.name = self.connection.message.information[0]
            self.surname = self.connection.message.information[1]
            self.user = self.connection.message.information[2]
            self.password = self.connection.message.information[3]

    def get_current_role(self, id_exp_sc):
        # Get role for current experimental scenario (control or experimental)
        self.directive = Message(action=85, information=[self.id, id_exp_sc])
        self.connection = self.directive.send_directive(self.connection)
        self.current_group = self.connection.message.information[0]


class Experiment:
    def __init__(self, id=0, name='', description='', design_type=0, state='', creation_date='', execution_date='',
                 finished_date=''):
        self.id = id
        self.name = name
        self.description = description
        self.design_type = design_type
        self.state = state
        self.creation_date = creation_date
        self.execution_date = execution_date
        self.finished_date = finished_date


class ExperimentalSC:
    def __init__(self, id=0, title='', description='', access_code='', state='', availability=True,
                 id_experiment=None, experiment=None, id_description_diagram=None, description_diagram=None,
                 control_group=None, experimental_group=None, cgroup_patterns=None, egroup_patterns=None,
                 problems=None, connection=None, info_designers=None):
        self.id = id
        self.title = title
        self.description = description
        self.access_code = access_code
        self.state = state
        self.availability = availability
        self.id_experiment = id_experiment
        self.id_description_diagram = id_description_diagram
        self.experiment = experiment
        self.description_diagram = description_diagram
        self.info_designers = info_designers
        if experimental_group is None:
            self.experimental_group = []
        if control_group is None:
            self.control_group = []
        if egroup_patterns is None:
            self.egroup_patterns = []
        if cgroup_patterns is None:
            self.cgroup_patterns = []
        if problems is None:
            self.problems = []
        self.connection = connection
        if self.connection is not None:
            self.retrieve_components()

    def retrieve_components(self):
        # Retrieve experiment
        if self.id_experiment is not None and self.experiment is None:
            self.directive = Message(action=95, information=[self.id_experiment])
            self.connection = self.directive.send_directive(self.connection)
            self.experiment = Experiment(id=self.id_experiment, name=self.connection.message.information[0],
                                         description=self.connection.message.information[1],
                                         design_type=int(self.connection.message.information[2]),
                                         state=self.connection.message.information[3])
        # Retrieve description diagram
        if self.id_description_diagram is not None and self.description_diagram is None:
            self.directive = Message(action=65, information=[self.id_description_diagram])
            self.connection = self.directive.send_directive(self.connection)
            self.description_diagram = File()
            self.description_diagram.write_file(name=self.connection.message.information[0],
                                                file_bytes=self.connection.message.information[1])

    def retrieve_designers_groups(self):
        self.directive = Message(action=27, information=[self.id])
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information[0]:  # Here are designers of experimental group
            elements = item.split('¥')
            self.experimental_group.append(Designer(id=int(elements[0]), name=elements[1], surname=elements[2],
                                                    user=elements[3]))
        for item in self.connection.message.information[1]:  # Here are designers of control group
            elements = item.split('¥')
            self.control_group.append(Designer(id=int(elements[0]), name=elements[1], surname=elements[2],
                                               user=elements[3]))

    def retrieve_patterns_groups(self, av_patterns):
        self.directive = Message(action=87, information=[self.id])
        self.connection = self.directive.send_directive(self.connection)
        for item in self.connection.message.information[0]:  # Here are patterns of experimental group
            current_id = int(item.split('¥')[0])
            for pattern in av_patterns:
                if pattern.id == current_id:
                    self.egroup_patterns.append(pattern)
                    break

        for item in self.connection.message.information[1]:  # Here are patterns of control group
            current_id = int(item.split('¥')[0])
            for pattern in av_patterns:
                if pattern.id == current_id:
                    self.cgroup_patterns.append(pattern)
                    break

    def retrieve_problems(self, av_patterns):
        self.directive = Message(action=52, information=[self.id])
        self.connection = self.directive.send_directive(self.connection)
        self.problems = []
        for item in self.connection.message.information[0]:  # Here are problems of experimental scenario
            elements = item.split('¥')
            self.problems.append(Problem(id=int(elements[0]), brief_description=elements[1], description=elements[2],
                                         id_solution=elements[3], connection=self.connection, av_patterns=av_patterns))


class File:
    def __init__(self, name='', file=None, file_bytes=None, filename=None, image=None):
        self.name = name
        self.file = file
        self.file_bytes = file_bytes
        self.filename = filename
        self.image = image

    def read_file(self, filename):
        self.filename = filename
        self.file = open(self.filename, 'rb')
        self.file_bytes = self.file.read()
        self.name = self.file.name.split('/')[-1]

    def write_file(self, name, file_bytes):
        self.name = name
        self.file_bytes = file_bytes
        path = './Resources/temp/'
        self.filename = path + name
        self.file = open(self.filename, 'wb')
        self.file.write(self.file_bytes)
        self.file.close()

    def write_permanent_file(self, name, file_bytes, path):
        self.name = name
        self.file_bytes = file_bytes
        self.filename = path + '/' + name
        self.file = open(self.filename, 'wb')
        self.file.write(self.file_bytes)
        self.file.close()


class Measurement:
    def __init__(self, id=0, value=0, acquisition_start_date=None, acquisition_end_date=datetime.datetime.now(),
                 id_metric=None, id_designer=None, id_problem=None, metric=None, designer=None, problem=None,
                 connection=None):
        self.id = id
        self.value = value
        self.acquisition_start_date = acquisition_start_date
        self.acquisition_end_date = acquisition_end_date
        self.id_metric = id_metric
        self.id_designer = id_designer
        self.id_problem = id_problem
        self.metric = metric
        self.designer = designer
        self.problem = problem
        self.connection = connection


class Message:
    """
    A class used to represent the message that is exchanged between server and client. This message is like the
    communication protocol handled by both endpoints of the communication. A message object has attributes:

    :param action: number that indicates an specific action.
    When message is sent from server to client, possible options for this parameters are:
        - 2: means that the requested action by the client was completed successfully
        - 5: means that the requested action by the client was not completed
        - 6: means that the requested action by the client was completed but with a warning
    When message is sent from client to server, possible options are listed in ET_Server project >
    Modules.Config.protocol
    :type action: int
    :param comment: additional information that may be useful for any of the endpoints
    :type comment: str
    :param information: list of parameters with important information associated with the action of the message
    :type information: list
    """

    def __init__(self, action=0, comment='', information=None):
        """
        Constructor of the class
        """
        if information is None:
            information = []
        self.action = action
        self.comment = comment
        self.information = information

    def send_directive(self, connection):
        """
        In this function the client exchanges information with the server (sends message and waits to receive response
        from the server)

        :param connection: active connection object with the server
        :type connection: Modules.Config.Connection.Connection
        :return connection: active connection object with server an with new changes (new message)
        :rtype connection: Modules.Config.Connection.Connection
        """
        connection.create_message(self)
        connection.send_message()
        connection.receive_message()
        return connection


class Pattern:
    def __init__(self, id=0, template=None, sections=None, main_sections=None):
        if main_sections is None:
            main_sections = []
        if sections is None:
            sections = []
        self.id = id
        self.template = template
        self.sections = sections
        self.main_sections = main_sections

    def get_main_sections(self):
        contents = []
        for item in self.main_sections:
            contents.append(item.content)
        current_length = len(contents)
        for index in range(0, 3 - current_length):
            contents.append('')
        return contents

    def get_joined_main_s(self):
        return ' '.join(self.get_main_sections())

    @staticmethod
    def get_available_patterns(connection):
        # Retrieve list of patterns from DB
        directive = Message(action=42, information=[])
        connection = directive.send_directive(connection)
        patterns_db = connection.message.information
        # Retrieving content of each pattern form DB
        patterns = []
        for item in patterns_db:
            id_pattern = item.split('¥')[0]
            id_template = item.split('¥')[1]
            directive = Message(action=40, information=[int(id_template)])
            connection = directive.send_directive(connection)
            template_aux = Template(int(id_template), connection.message.information[0],
                                    connection.message.information[1])
            sections = connection.message.information[2]
            current_sections = []
            current_m_sections = []
            for item2 in sections:
                elements = item2.split('¥')
                directive = Message(action=47, information=[int(id_pattern), int(elements[0])])
                connection = directive.send_directive(connection)
                elements_content = connection.message.information[0].split('¥')
                section_aux = Section(temp_section_id=int(elements[0]), template_id=int(elements[1]),
                                      section_id=int(elements[2]), name=elements[3], description=elements[4],
                                      data_type=elements[5], position=int(elements[6]), mandatory=elements[7],
                                      main=elements[8], classification_id=elements[9],
                                      pattern_section_id=int(elements_content[0]), diagram_id=elements_content[4],
                                      category_id=elements_content[5], content=elements_content[1])
                if section_aux.main == '✓':
                    current_m_sections.append(section_aux)
                current_sections.append(section_aux)
            pattern_aux = Pattern(id=int(id_pattern), template=template_aux, sections=current_sections,
                                  main_sections=current_m_sections)
            patterns.append(pattern_aux)
        return patterns

    @staticmethod
    def get_patterns(connection, patterns_db):
        # Retrieving content of each pattern form DB
        patterns = []
        for item in patterns_db:
            id_pattern = item.split('¥')[0]
            id_template = item.split('¥')[1]
            directive = Message(action=40, information=[int(id_template)])
            connection = directive.send_directive(connection)
            template_aux = Template(int(id_template), connection.message.information[0],
                                    connection.message.information[1])
            sections = connection.message.information[2]
            current_sections = []
            current_m_sections = []
            for item2 in sections:
                elements = item2.split('¥')
                directive = Message(action=47, information=[int(id_pattern), int(elements[0])])
                connection = directive.send_directive(connection)
                elements_content = connection.message.information[0].split('¥')
                section_aux = Section(temp_section_id=int(elements[0]), template_id=int(elements[1]),
                                      section_id=int(elements[2]), name=elements[3], description=elements[4],
                                      data_type=elements[5], position=int(elements[6]), mandatory=elements[7],
                                      main=elements[8], classification_id=elements[9],
                                      pattern_section_id=int(elements_content[0]), diagram_id=elements_content[4],
                                      category_id=elements_content[5], content=elements_content[1])
                if section_aux.main == '✓':
                    current_m_sections.append(section_aux)
                current_sections.append(section_aux)
            pattern_aux = Pattern(id=int(id_pattern), template=template_aux, sections=current_sections,
                                  main_sections=current_m_sections)
            patterns.append(pattern_aux)
        return patterns


class Problem:
    id_visual = 0

    def __init__(self, id=0, brief_description='', description='', id_solution=None, solution=None,
                 connection=None, av_patterns=None):
        self.id = id
        Problem.id_visual += 1
        self.id_visual = Problem.id_visual
        self.brief_description = brief_description
        self.description = description
        self.id_solution = id_solution
        if solution is None:
            self.solution = Solution()
        if av_patterns is None:
            av_patterns = []
        self.connection = connection
        if self.connection is not None:
            self.retrieve_components(av_patterns)

    def retrieve_components(self, av_patterns):
        if self.id_solution is not None:
            self.directive = Message(action=60, information=[self.id_solution])
            self.connection = self.directive.send_directive(self.connection)
            self.solution = Solution(id=self.id_solution, annotations=self.connection.message.information[0],
                                     diagram_id=self.connection.message.information[1],
                                     patterns_id=self.connection.message.information[2], connection=self.connection)
            current_ids = []
            for item in self.solution.patterns_id:
                current_id = int(item.split('¥')[0])
                current_ids.append(current_id)
                for pattern in av_patterns:
                    if pattern.id == current_id:
                        self.solution.patterns.append(pattern)
                        break
            self.solution.patterns_id = current_ids


class Section:
    def __init__(self, temp_section_id=0, template_id=0, section_id=0, name='', description='', data_type='',
                 position=0, mandatory='✓', main='', classification_id=0, pattern_section_id=0, diagram_id=0,
                 category_id=0, content='', file=None, category=None):
        self.temp_section_id = temp_section_id
        self.template_id = template_id
        self.section_id = section_id
        self.name = name
        self.description = description
        self.data_type = data_type
        self.position = position
        self.mandatory = mandatory
        self.main = main
        if classification_id != 'None':
            self.classification_id = int(classification_id)
        else:
            self.classification_id = 0
        if diagram_id != 'None':
            self.diagram_id = int(diagram_id)
        else:
            self.diagram_id = 0
        if category_id != 'None':
            self.category_id = int(category_id)
        else:
            self.category_id = 0
        self.pattern_section_id = pattern_section_id
        self.content = content
        self.file = file
        self.category = category

    def get_mandatory_bool(self):
        if self.mandatory == '✓':
            return True
        else:
            return False


class Solution:
    def __init__(self, id=0, annotations='', patterns=None, patterns_id=None, diagram=None, diagram_id=0,
                 connection=None):
        if patterns is None:
            patterns = []
        if patterns_id is None:
            patterns_id = []
        self.id = id
        self.annotations = annotations
        self.patterns = patterns
        self.patterns_id = patterns_id
        self.diagram = diagram
        self.diagram_id = diagram_id
        self.connection = connection
        if self.connection is not None:
            self.retrieve_components()

    def retrieve_components(self):
        # Retrieve diagram for the solution
        if self.diagram_id is not None:
            self.directive = Message(action=65, information=[self.diagram_id])
            self.connection = self.directive.send_directive(self.connection)
            self.diagram = File()
            self.diagram.write_file(name=self.connection.message.information[0],
                                    file_bytes=self.connection.message.information[1])


class Template:
    def __init__(self, id=0, name='', description='', sections=None):
        if sections is None:
            sections = []
        self.id = id
        self.name = name
        self.description = description
        self.sections = sections


class TimerClass:
    def __init__(self):
        self.running_thread = threading.Thread(target=self.count, daemon=True)
        self.seconds = 0
        self.stop_var = False

    def begin(self):
        self.running_thread.start()

    def count(self):
        while True:
            time.sleep(1)
            self.seconds += 1
            if self.stop_var:
                break

    def stop(self):
        self.stop_var = True
