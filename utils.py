#!/usr/bin/python

TEXT_COLOR_RED = '\033[91m'
TEXT_COLOR_GREEN = '\033[92m'
TEXT_COLOR_YELLOW = '\033[93m'
TEXT_COLOR_BLUE = '\033[94m'
TEXT_COLOR_MAGENTA = '\033[95m'
TEXT_COLOR_CYAN = '\033[96m'
TEXT_COLOT_WHITE = '\033[97m'
TEXT_COLOR_GREY = '\033[90m'
TEXT_COLOR_BLACK = '\033[30m'
TEXT_STYLE_BOLD = '\033[1m'
TEXT_STYLE_ITALIC = '\033[3m'
TEXT_STYLE_UNDERLINE = '\033[4m'
TEXT_END = '\033[0m'

def success_msg(msg):
	print(color_text(msg, TEXT_COLOR_GREEN))

def error_msg(msg):
	print(color_text(msg, TEXT_COLOR_RED))

def color_text(text, color):
    return color + text + TEXT_END

def get_config_content(path):	
	data_file = open(path)
	content = data_file.read()
	data_file.close()
	
	return content

def create_file(path, content):
	file = open(path, 'w')
	file.write(content)
	file.close()

def remove_dict(dct, key):
   copy = dct.copy()
   del copy[key]
   return copy

def str2bool(value):
	return value.lower() in ("yes", "true", "t", "1")

def is_true(key, options):
	return key in options.keys() and str2bool(options[key])
	

