import json

json_config = json.load(open('config.json', 'r'))
TITLE_FONT = (json_config['font_type'], json_config['font_size']['title'])
SUBTITLE_FONT = (json_config['font_type'], json_config['font_size']['subtitle'])
SUBTITLE2_FONT = (json_config['font_type'], json_config['font_size']['subtitle_two'])
LABEL_GUI_FONT = (json_config['font_type'], json_config['font_size']['subtitle_two'])
LABEL_FONT = (json_config['font_type'], json_config['font_size']['text'])
TEXT_FONT = (json_config['font_type'], json_config['font_size']['text'])
NOTE_FONT = (json_config['font_type'], json_config['font_size']['note'])
TEXT_COLOR = json_config['color']['sky_blue']

#TEXT_COLOR = "#1B5070"