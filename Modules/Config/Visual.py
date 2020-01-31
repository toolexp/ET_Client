import json

json_config = json.load(open('config.json', 'r'))
TITLE_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['title'])
SUBTITLE_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['subtitle'])
SUBTITLE2_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['subtitle_two'])
LABEL_GUI_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['subtitle_two'])
LABEL_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['text'])
TEXT_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['text'])
NOTE_FONT = (json_config["visual_font"]["type"], json_config["visual_font"]["size"]['note'])
TEXT_COLOR = json_config["visual_font"]['color']['sky_blue']
ENABLED_COLOR = 'white'
DISABLED_COLOR = '#F0F0F0'
