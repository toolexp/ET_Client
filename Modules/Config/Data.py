import textwrap
from datetime import time
from tkinter import Toplevel, Label


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


class DesignersGroup:
    def __init__(self, id=0, name='', description=''):
        self.id = id
        self.name = name
        self.description = description


class Template:
    def __init__(self, id=0, name='', description=''):
        self.id = id
        self.name = name
        self.description = description


class Pattern:
    def __init__(self, id=0, template=None, sections=None):
        if sections is None:
            sections = []
        self.id = id
        self.template = template
        self.sections = sections

    def get_content_name(self):
        return self.sections[0].content

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
            directive = Message(action=77, information=[template_aux.id])
            connection = directive.send_directive(connection)
            sections = connection.message.information
            current_sections = []
            for item2 in sections:
                elements = item2.split('¥')
                directive = Message(action=47, information=[int(id_pattern), int(elements[0])])
                connection = directive.send_directive(connection)
                elements_content = connection.message.information[0].split('¥')
                section_aux = Section(temp_section_id=int(elements[0]), template_id=int(elements[1]),
                                      section_id=int(elements[2]), name=elements[3], description=elements[4],
                                      data_type=elements[5], position=int(elements[6]), mandatory=elements[7],
                                      classification_id=elements[8], pattern_section_id=int(elements_content[0]),
                                      diagram_id=elements_content[4], category_id=elements_content[5],
                                      content=elements_content[1])
                current_sections.append(section_aux)
            pattern_aux = Pattern(id=int(id_pattern), template=template_aux, sections=current_sections)
            patterns.append(pattern_aux)
        return patterns


class Section:
    def __init__(self, temp_section_id=0, template_id=0, section_id=0, name='', description='', data_type='',
                 position=0,
                 mandatory='✓', classification_id=0, pattern_section_id=0, diagram_id=0, category_id=0, content='',
                 file=None, category=None):
        self.temp_section_id = temp_section_id
        self.template_id = template_id
        self.section_id = section_id
        self.name = name
        self.description = description
        self.data_type = data_type
        self.position = position
        self.mandatory = mandatory
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


class Category:
    def __init__(self, id=0, name='', classification_id=0):
        self.id = id
        self.name = name
        self.classification_id = classification_id


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


class Problem:
    def __init__(self, id=0, name='', description='', id_solution=None, connection=None):
        self.id = id
        self.name = name
        self.description = description
        if id_solution is not None:
            self.directive = Message(action=60, information=[id_solution])
            self.connection = self.directive.send_directive(connection)
            elements = self.connection.message.information
            solution = Solution(id=id_solution, annotations=elements[0], patterns_id=elements[2],
                                diagram_id=int(elements[1]))
            self.solution = solution
        else:
            self.solution = id_solution


class Solution:
    def __init__(self, id=0, annotations='', patterns_id=None, diagram_id=0):
        if patterns_id is None:
            patterns_id = []
        self.id = id
        self.annotations = annotations
        self.patterns_id = patterns_id
        self.diagram_id = diagram_id


class ExperimentalSC:
    def __init__(self, id=0, name='', description='', access_code='', start_time=time(0, 0, 0), end_time=time(0, 0, 0),
                 scenario_availability=True, scenario_lock=False, experiment=None, id_control_group=None,
                 id_experimental_group=None):
        self.id = id
        self.name = name
        self.description = description
        self.access_code = access_code
        self.start_time = start_time
        self.end_time = end_time
        self.scenario_availability = scenario_availability
        self.scenario_lock = scenario_lock
        self.experiment = experiment
        self.id_control_group = id_control_group
        self.id_experimental_group = id_experimental_group


class ScenarioComponent:
    id_counter = 0

    def __init__(self, id_problem=0, id_patterns_cgroup=None, id_patterns_egroup=None):
        if id_patterns_egroup is None:
            id_patterns_egroup = []
        if id_patterns_cgroup is None:
            id_patterns_cgroup = []
        self.id_counter += 1
        self.id = self.id_counter
        self.id_problem = id_problem
        self.id_patterns_egroup = id_patterns_egroup
        self.id_patterns_cgroup = id_patterns_cgroup


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


def wrap_text(string, lenght=90):
    return '\n'.join(textwrap.wrap(string, lenght))
