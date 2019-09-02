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

    def __init__(self, name='', template='', text_sections=None, file_sections=None, text_content=None,
                 file_content=None):
        if file_content is None:
            file_content = []
        if text_content is None:
            text_content = []
        if file_sections is None:
            file_sections = []
        if text_sections is None:
            text_sections = []
        self.name = name
        self.template = template
        self.text_sections = text_sections
        self.file_sections = file_sections
        self.text_content = text_content
        self.file_content = file_content


class Section:

    def __init__(self, index=None, data_type=None, section=None):
        self.index = index
        self.data_type = data_type
        self.section = section


class File:

    def __init__(self, name='', file=None, file_bytes=None, filename=None):
        self.name = name
        self.file = file
        self.file_bytes = file_bytes
        self.filename = filename

    def read_file(self, filename):
        self.filename = filename
        self.file = open(self.filename, 'rb')
        self.file_bytes = self.file.read()
        self.name = self.file.name.split('/')[-1]
