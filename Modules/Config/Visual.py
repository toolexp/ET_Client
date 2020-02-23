"""
File where constant variables are set, so they can be used from any file of the project. The constants are set in
function of the main configuration file (config.json) that is editable. The constants are mainly about visual components
such as titles, subtitles and labels fonts (size, kind, color)
"""

import json

json_config = json.load(open('config.json', 'r'))

# Constants associated with fonts
TITLE_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['title'])
SUBTITLE_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['subtitle'])
SUBTITLE2_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['subtitle_two'])
LABEL_GUI_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['subtitle_two'])
LABEL_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['text'])
TEXT_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['text'])
NOTE_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['note'])
TEXT_COLOR = json_config["visual_font"]['color']['sky_blue']

# Constants associated with elements' background color
ENABLED_COLOR = 'white'
DISABLED_COLOR = '#F0F0F0'
