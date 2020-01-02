import textwrap
import threading
import time
import datetime
from tkinter import Toplevel, Label


def verify_ip(ip):
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
    if not port.isdigit():
        return False
    else:
        return True


def wrap_text(string, lenght=90):
    return '\n'.join(textwrap.wrap(string, lenght))


class Category:
    def __init__(self, id=0, name='', classification_id=0):
        self.id = id
        self.name = name
        self.classification_id = classification_id


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
                 problems=None, connection=None):
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


class Measurement:
    def __init__(self, id=0, value='', date=datetime.datetime.now(), id_metric=None, id_designer=None,
                 id_problem=None, metric=None, designer=None, scenario_comp=None, connection=None):
        self.id = id
        self.value = value
        self.date = date
        self.id_metric = id_metric
        self.id_designer = id_designer
        self.id_problem = id_problem
        self.metric = metric
        self.designer = designer
        self.scenario_comp = scenario_comp
        self.connection = connection
        '''if self.connection is not None:
            self.retrieve_components()'''

    '''def retrieve_components(self):
        if self.id_metric is not None:
            self.directive = Message(action=95, information=[self.id_metric])
            self.connection = self.directive.send_directive(self.connection)
            self.metric = Metric(id=self.id_metric, name=self.connection.message.information[0],
                                 description=self.connection.message.information[1])
        if self.id_designer is not None:
            self.directive = Message(action=30, information=[self.id_designer])
            self.connection = self.directive.send_directive(self.connection)
            self.control_group = Designer(id=self.id_designer, name=self.connection.message.information[0],
                                                description=self.connection.message.information[1])
        if self.id_scenario_comp is not None:
            self.directive = Message(action=30, information=[self.id_experimental_group])
            self.connection = self.directive.send_directive(self.connection)
            self.experimental_group = DesignersGroup(id=self.id_experimental_group,
                                                     name=self.connection.message.information[0],
                                                     description=self.connection.message.information[1])'''


class Message:

    def __init__(self, action=0, comment='', information=None):
        if information is None:
            information = []
        self.action = action
        self.comment = comment
        self.information = information

    def send_directive(self, connection):
        connection.create_message(self)
        connection.send_message()
        connection.receive_message()
        return connection


class Pattern:
    def __init__(self, id=0, template=None, sections=None, main_section=None):
        if sections is None:
            sections = []
        self.id = id
        self.template = template
        self.sections = sections
        self.main_section = main_section

    def get_main_section(self):
        return self.main_section.content

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
            current_m_section = None
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
                    current_m_section = section_aux
                current_sections.append(section_aux)
            pattern_aux = Pattern(id=int(id_pattern), template=template_aux, sections=current_sections,
                                  main_section=current_m_section)
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
            current_m_section = None
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
                    current_m_section = section_aux
                current_sections.append(section_aux)
            pattern_aux = Pattern(id=int(id_pattern), template=template_aux, sections=current_sections,
                                  main_section=current_m_section)
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
                                     diagram_id=int(self.connection.message.information[1]),
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
        if self.diagram_id != 0:
            self.directive = Message(action=65, information=[self.diagram_id])
            self.connection = self.directive.send_directive(self.connection)
            self.diagram = File()
            self.diagram.write_file(name=self.connection.message.information[0],
                                    file_bytes=self.connection.message.information[1])


class Template:
    def __init__(self, id=0, name='', description=''):
        self.id = id
        self.name = name
        self.description = description


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
