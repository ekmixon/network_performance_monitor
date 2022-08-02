#!/usr/bin/env python3
# This file is part of the Network Performance Monitor which is released under the GNU General Public License v3.0
# See the file LICENSE for full license details.

import sys
import os
import getopt
import logging
import json
import util

APP_PATH="/opt/netperf"
SETTINGS_FILE = f"{APP_PATH}/config/netperf.json"

def log_level_switcher(log_level_txt):
	log_levels = {
		"CRITICAL" : logging.INFO,
		"ERROR" : logging.ERROR,
		"WARNING": logging.WARNING,
		"INFO": logging.INFO,
		"DEBUG": logging.DEBUG
	}
	return log_levels.get(log_level_txt, logging.NOTSET)


class netperf_settings:

	settings_json = None

	def save_settings(self):
		with open(SETTINGS_FILE,"w") as sf:
			settings_json_string = json.dumps(self.settings_json,indent=4)
			sf.truncate()
			sf.write(settings_json_string)
			sf.close()

	def __init__(self):
		with open(SETTINGS_FILE) as sf:
			self.settings_json = json.load(sf)

	def get_data_root(self):
		if "data_root" in self.settings_json:
			return str(self.settings_json["data_root"])
		else:
			return None

	def get_db_filename(self):
		if "data_root" not in self.settings_json:
			return None
		client_id = util.get_client_id()
		return f'{self.settings_json["data_root"].rstrip("/")}/{client_id}/database/{client_id}.db'

	def get_db_path(self):
		if "data_root" not in self.settings_json:
			return None
		client_id = util.get_client_id()
		return f'{self.settings_json["data_root"].rstrip("/")}/{client_id}/database'

	def get_report_path(self):
		if "data_root" not in self.settings_json:
			return None
		client_id = util.get_client_id()
		return f'{self.settings_json["data_root"].rstrip("/")}/{client_id}/reports'

	def get_db_write_queue_name(self):
		return (
			str(self.settings_json["db_write_queue"])
			if "db_write_queue" in self.settings_json
			else "/netperf.db"
		)

	def get_log_filename(self):
		return (
			f'{self.settings_json["data_root"].rstrip("/")}/log/netperf.log'
			if "data_root" in self.settings_json
			else "/mnt/usb_storage/netperf/log/netperf.log"
		)

	def get_log_path(self):
		if "data_root" in self.settings_json:
			return f'{self.settings_json["data_root"].rstrip("/")}/log'
		else:
			return "/mnt/usb_storage/netperf/log"

	def get_speedtest_enforce_quota(self):
		if "speedtest" in self.settings_json:
			speedtest_settings = self.settings_json["speedtest"]
			if "enforce_quota" in speedtest_settings:
				return speedtest_settings["enforce_quota"]
			else:
				return None

	def get_data_usage_quota_GB(self):
		if "speedtest" in self.settings_json:
			speedtest_settings = self.settings_json["speedtest"]
			if "data_usage_quota_GB" in speedtest_settings:
				return speedtest_settings["data_usage_quota_GB"]
			else:
				return None

	def get_logger_format(self):
		logger_format="%(asctime)s %(name)s %(levelname)s:%(message)s"
		if "logging" in self.settings_json:
			log_settings = self.settings_json["logging"]
			if "logger_format" in log_settings:
				logger_format = log_settings["logger_format"]
		return logger_format


	def get_log_level(self):
		log_level=logging.NOTSET
		if "logging" in self.settings_json:
			log_settings = self.settings_json["logging"]
			if "log_level" in log_settings:
				log_level = log_level_switcher(log_settings["log_level"])
		return log_level

	def set_data_usage_quota_GB(self,data_usage_quota_GB):
		self.settings_json["speedtest"]["data_usage_quota_GB"] = data_usage_quota_GB
		self.save_settings()

	def set_speedtest_enforce_quota(self,flag):
		self.settings_json["speedtest"]["enforce_quota"] = flag
		self.save_settings()

	def set_data_root(self,path):
		self.settings_json["data_root"] = path.rstrip("/")
		self.save_settings()

	def set_log_level(self,log_level):
		if "logging" in self.settings_json:
			log_settings = self.settings_json["logging"]
			if "log_level" in log_settings:
				log_settings["log_level"] = log_level
		self.save_settings()

	def get_dashboard_enabled(self):
		return (
			self.settings_json["dashboard"].get("enabled", False)
			if "dashboard" in self.settings_json
			else False
		)

	def get_dashboard_queue_name(self):
		return (
			self.settings_json["dashboard"].get("queue_name", None)
			if "dashboard" in self.settings_json
			else None
		)

	def set_dashboard_enabled(self,value):
		self.settings_json["dashboard"]["enabled"] = value
		self.save_settings()

	def set_bandwidth_monitor_enabled(self,value):
		self.settings_json["bandwidth_monitor"]["enabled"] = value
		self.save_settings()

	def set_speedtest_client(self, value):
		self.settings_json["speedtest"]["client"] = value
		self.save_settings()

	def get_speedtest_client(self):
		return (
			self.settings_json["speedtest"].get("client", None)
			if "speedtest" in self.settings_json
			else None
		)

	def set_speedtest_server_id(self,server_id):
		if "speedtest" in self.settings_json:
			speedtest_settings = self.settings_json["speedtest"]
			speedtest_settings["server_id"] = None if server_id == "None" else server_id
		self.save_settings()

	def get_speedtest_server_id(self):
		return (
			self.settings_json["speedtest"].get("server_id", None)
			if "speedtest" in self.settings_json
			else None
		)

def main():
	log_levels = {'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'}
	ns = netperf_settings()
	unixOptions = 'g:s:v'
	gnuOptions = ['get=', 'set=', 'value=']
	try:
		options, remainder = getopt.getopt(sys.argv[1:], unixOptions, gnuOptions)
	except getopt.error as err:
		#output error, and return with an error code
		print(err)
		sys.exit(2)

	action = ""
	setting = ""
	value = ""
	for opt, arg in options:
		if opt in ('-g', '--get'):
			action = "get"
			setting = arg
		elif opt in ('-s', '--set'):
			action = "set"
			setting = arg
		elif opt in ('-v', '--value'):
			value = arg

	if action == "get":
		if setting == "db_filename":
			print (ns.get_db_filename())
		elif setting == "log_filename":
			print (ns.get_log_filename())
		elif setting == "data_root":
			print (ns.get_data_root())
		elif setting == "report_path":
			print (ns.get_report_path())
		else:
			if setting == "speedtest_server_id":
				print (ns.get_speedtest_server_id())
			else:
				if setting == "speedtest_client":
					print (ns.get_speedtest_client())

	elif action == "set":
		if setting == "data_usage_quota_GB":
			val_error=False
			if value == "":
				val_error = True
			try:
				data_usage_quota_GB = int(value)
			except ValueError:
				val_error = True
			if val_error or data_usage_quota_GB < 0:
				print ("data_usage_quota_GB value must be a positive integer.")
				sys.exit(0)
			else:
				ns.set_data_usage_quota_GB(data_usage_quota_GB)
		else:
			if setting == "enforce_quota":
				value_error = False
				if value.lower() == "true":
					flag = True
				else:
					if value.lower() == "false":
						flag = False
					else:
						value_error = True
				if value_error:
					print ("enforce_quota value must be True or False")
				else:
					ns.set_speedtest_enforce_quota(flag)
			else:
				if setting == "data_root":
					if os.path.isdir(value):
						ns.set_data_root(value)
					else:
						print("Invalid path.")
				else:
					if setting == "log_level":
						if value in log_levels:
							ns.set_log_level(value)
						else:
							print("Invalid log level")
					else:
						if setting == "dashboard_enabled":
							if value.lower() == "true":
								ns.set_dashboard_enabled(True)
							else:
								if value.lower() == "false":
									ns.set_dashboard_enabled(False)
								else:
									print ("dashboard_enabled value must be True or False")
						else:
							if setting == "bwmonitor_enabled":
								if value.lower() == "true":
									ns.set_bandwidth_monitor_enabled(True)
								else:
									if value.lower() == "false":
										ns.set_bandwidth_monitor_enabled(False)
									else:
										print ("bwmonitor_enabled value must be True or False")
							else:
								if setting == "speedtest_client":
									if value.lower() == "ookla":
										ns.set_speedtest_client("ookla")
									else:
										if value.lower() == "speedtest-cli":
											ns.set_speedtest_client("speedtest-cli")
										else:
											print ("speedtest_client value must be 'speedtest-cli' or 'ookla'")
								else:
									if setting == "speedtest_server_id":
										if value == "":
											print ("speedtest_server_id setting requires a value")

										else:
											ns.set_speedtest_server_id(value)
if __name__ == "__main__":
	main()
