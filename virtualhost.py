#!/usr/bin/python

import os
import sys
import argparse
import configparser
import utils


def do_create_httpd(options):
	config_path = options['system']['httpd_config_path']
	content = utils.get_config_content(config_path)
	content = get_prepared_content(content, options, 'httpd')
	
	httpd_path = options['system']['httpd_path']
	file_name = options['httpd']['site_name'] + '.conf'
	full_file_path = httpd_path + file_name
	
	utils.create_file(full_file_path, content)
	
	utils.success_msg("Httpd File was Created.")

def do_create_nginx(options):
	if not utils.is_true('create_nginx', options['nginx']):
		return False;
	
	config_path = options['system']['nginx_config_path']
	content = utils.get_config_content(config_path)
	content = get_prepared_content(content, options, 'nginx')
	
	httpd_path = options['system']['nginx_path']
	file_name = options['nginx']['site_name'] + '.conf'
	full_file_path = httpd_path + file_name
	
	utils.create_file(full_file_path, content)
	utils.success_msg("Nginx File was Created.")

def do_create_site(options):
	if not utils.is_true('create_test_folder', options['default']):
		return False
	
	if not os.path.isdir(options['default']['site_path']):
		utils.error_msg('Path to Folder Site Not Found')
		return False
	
	site_folder_path = options['default']['site_path'] + options['default']['site_name']
	
	if os.path.isdir(site_folder_path):
		utils.error_msg('Site Folder is Exist')
		return False
		
	os.makedirs(site_folder_path)
	
	template_path = options['system']['template_page_path']
	content = utils.get_config_content(template_path)
	
	site_folder_path = site_folder_path + "/index.html"
	utils.create_file(site_folder_path, content)
	
	utils.success_msg("Site Folder was Created.")
	

def do_create_hosts(options):
	if not utils.is_true('add_hosts', options['default']):
		return False
		
	file_hosts_path = options['system']['file_hosts_path']
	if not os.path.isfile(file_hosts_path):
		raise Exception('File Hosts Not Found')
	
	host_ip = options['system']['hosts_ip']
	string = "\n" + host_ip + " " + options['default']['site_name']
	#add conditions if record exists
	file = open(file_hosts_path, 'a')
	file.write(string)
	file.close()
	
	utils.success_msg("Record in Hosts was Added.")

def get_config():
	config = configparser.ConfigParser()
	config.read('config.ini')
	
	return config;

def get_prepared_content(content, options, key_opt):

	for key in options[key_opt]:
		reserve_key = '{$.' + key.upper() + '}'
		if options[key_opt][key]:
			content = content.replace(reserve_key, options[key_opt][key])
	
	return content
	
def get_prepared_arguments(arguments):
	arguments = vars(arguments)
	for key in arguments:
		if arguments[key] is None:
			arguments = utils.remove_dict(arguments, key)
	return arguments

def get_options(arguments, config):
	default_configs  = dict(config.items('DEFAULT'))
	configs_https    = dict(config.items('HTTPD'))
	configs_nginx    = dict(config.items('NGINX'))
	configs_system   = dict(config.items('SYSTEM'))
	
	arguments = arguments.items()
	
	options = {
		'default': dict(default_configs.items() + arguments),
		'httpd'  : dict(default_configs.items() + configs_https.items() + arguments),
		'nginx'  : dict(default_configs.items() + configs_nginx.items() + arguments),
		'system' : dict(default_configs.items() + configs_system.items() + arguments)
	} 
	
	return options;

def do_create_virtual_host(arguments):
	arguments = get_prepared_arguments(arguments)
	config = get_config()
	
	options = get_options(arguments, config)


	do_create_httpd(options)
	do_create_nginx(options)
	do_create_hosts(options)
	do_create_site(options)


def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("site_name")
	parser.add_argument('-i', '--info')
	parser.add_argument('-a', '--add_hosts')
	return parser

def __init():
	parser = create_parser()
	arguments = parser.parse_args(sys.argv[1:])
	do_create_virtual_host(arguments)


if __name__ == "__main__":
	try:
		__init()
	except Exception as e:
		utils.error_msg(str(e))
    

