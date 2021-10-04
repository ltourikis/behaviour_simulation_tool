import sys
import os
import logging
import json

import numpy as np

from profiles_collection import profiles

# Configure logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

def sequence_that_sums(duration, sessions):
	"""
		Creates a sequence of random numbers that has param:sessions length 
		and param:duration sum.

		The function call np.ones(sessions) return a list of Dirac's with sessions length.
		For example np.ones(5) returns [1. 1. 1. 1. 1.]

		The size parameter controls how many lists will be created.
		The return value is a list of the aforementioned lists.
		We need just one and thus we select the one created with the [0] 
		at the end of the expression.

		The dirichlet is multiplied by @duration so that it sums up to duration.
		If not the sum would be 1.


	"""
	return duration * np.random.dirichlet(np.ones(sessions), size=1)[0]

def config_quick_profile():
	"""
		Handles the config file for the quick profile.

		Firstly, the quick_profile_config.json is handled and the profile
		info is fetched.

		Then the info is passed in the profiles dictionary located in 
		the profiles_collection.py
	"""
	# Open the quick_profile_config.json
	try:
		file = open(os.path.join(sys.path[0], "quick_profile_config.json"), "r")

	except Exception as e:
		logging.info("Could not open/read file: quick_profile_config.json")
		return -1

	# Create a json with the configuration and close the file
	config = json.load(file)
	file.close() 

	for app in config["apps"]:
		
		total_sessions_duration = config["apps"][app]["total_sessions_duration"]
		total_interarrivals_duration = config["apps"][app]["total_interarrivals_duration"]
		sessions = config["apps"][app]["sessions"]

		# sequence_that_sums returns a list. The API needs a string though
		# and thus we convert the initial list to the duration_string. 
		# Same with the interarrivals sequence.
		duration_list = sequence_that_sums(total_sessions_duration, sessions).round(decimals=2)
		duration_string = ','.join(map(str, duration_list))

		interarrivals_list = sequence_that_sums(total_interarrivals_duration, sessions).round(decimals=2)
		interarrivals_string = ','.join(map(str, interarrivals_list))
		
		profiles["Quick_Profile"]["applications"][app]["duration_list"] = duration_string
		profiles["Quick_Profile"]["applications"][app]["interarrivals_list"] = interarrivals_string

	profiles["Quick_Profile"]["persona"]["enabled"] = config["persona"]["enabled"]
	profiles["Quick_Profile"]["asklipios_LIS"]["enabled"] = config["asklipios_LIS"]["enabled"]
	profiles["Quick_Profile"]["total_duration"] = config["total_duration"]
	profiles["Quick_Profile"]["time_remaining"] = config["total_duration"]



if __name__ == "__main__":
	config_quick_profile()
	print(profiles)
