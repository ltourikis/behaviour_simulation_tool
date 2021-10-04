import logging
import os
import sys
import random
import time
import platform

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# default wait time so that elements load
# might be overriden
WAIT_TIME = 10

# Configure logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


def realistic_sleep_timer_inbetween_actions():
    """
    	Wait 1 - 4 secs inbetween actions to make the simulation more realistic

    	:return:	s:		the sleep time
    """
    s = random.random()* 3 + 1
    logging.info(f"(Sleep Time inbetween actions to make the simulation more realistic)Sleep time = {s:.2f} secs")
    time.sleep(s)
    return s

def realistic_sleep_timer_inbetween_sessions():
	"""
		Wait 7 - 10 secs inbetween sessions to make the simulation more realistic

		:return:	s:		the sleep time
	"""
	s = random.random()* 3 + 7
	logging.info(f"(Sleep Time inbetween sessions to make the simulation more realistic)Sleep time = {s:.2f} secs")
	time.sleep(s)
	return s

def deal_with_popup(driver):
	"""
		Handles the cookies popup by clicking "I Agree"

		:return:    -1:			 in case no valid link is found
	"""
	try:
		logging.info("(google)Locating agree button")
		agree = WebDriverWait(driver, WAIT_TIME).until(
					EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Συμφωνώ")]'))
					)
		agree.click()
	except Exception as e:
		logging.info("(google)Error in: Locating agree button")
		logging.info("(google)Error description: " + str(e))
		logging.info("(google)Clicking agree button aborted..")
		return -1


def search_element(driver, search_query):
	""" 
		Function that searches for an element on google.

		The google search form is initially filled with the param:search_query.
		Then "Enter" is sent.
	
		:param:		search_query:		The query to be searched on google
		:return:	-1:					If any errors occured
		:return:	session_duration:	Time spent browing on the function
	"""
	try:
		logging.info("(google)Locating search form")
		form =  WebDriverWait(driver, WAIT_TIME).until(
			EC.presence_of_element_located((By.XPATH, '//input[@name="q"]'))
			)
		logging.info(f"(google)Filling search form with {search_query}")
		form.clear()
		form.send_keys(search_query)
		form.send_keys(Keys.ESCAPE)
		form.click()

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s1 = realistic_sleep_timer_inbetween_actions()

		form.send_keys(Keys.RETURN)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s2 = realistic_sleep_timer_inbetween_actions()

	except Exception as e:
		logging.info("(google)Error in: Searching element")
		logging.info("(google)Error description: " + str(e))
		logging.info("(google)Searching aborted..")
		return -1

	# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
	s3 = realistic_sleep_timer_inbetween_actions()

	session_duration = s1 + s2 + s3

	return session_duration



def google(duration_list, interarrivals_list, url=None):
	"""
		Handles the google browsing.

		The parameters interarrivals_list and duration_list are
		received as Strings, with their values separated by a comma.
		The function transforms them to float type lists.
		For example if "100, 20" is received, it is transformed to [100.0, 20.0].

		The two lists should have the same length.

		The param:duration_list holds the list with values that represents the total time 
		that will be spent on google on each senario.

		Inbetween the restarting of the senarios there is "break" time that lasts 
		as much as the value taken from the param:interarrivals_list each time accordingly.
		
		############################################################

		The url param is not used. It's there because the wrapper function that 
		calls the facebook function as well as other functions,on some occassions 
		might need a url param.
		Not the best implementation and will be fixed.

		############################################################

		Initially the google_search_queries.txt is opened and the search queries 
		are stored on the l[] list.		

		############################################################


		Inbetween steps that are supposedly made by human user sleep timers of
		1-4 seconds are initiated so that the simulation is more realistic.

		The browsing sequence is:
		1.deal with pop-up (if possible)
		2.search a query
		3.sleep 7-10 seconds
		4.repeat steps 4-5 until duration is over

		:param: 	duration_list:			String with the duration of each session.
		:param: 	interarrivals_list:		String with the break duration inbetween sessions.
		:param:		url:					Not being used. Set to none

	"""
	duration_list = [float(s) for s in duration_list.split(',')]
	interarrivals_list = [float(s) for s in interarrivals_list.split(',')]
	logging.info("Setting up google browsing..")
	logging.info(f"  --duration_list(secs): {duration_list}")
	logging.info(f"  --interarrivals_list(secs): {interarrivals_list}")

	# Open the google_search_queries.txt that contains possible search queries
	try:
		logging.info("(google)Opening file: google_search_queries.txt")
		file = open(os.path.join(sys.path[0], "profile_functions/google/google_search_queries.txt"), "r")

	except Exception as e:
		logging.info("(google)Could not open/read file: google_search_queries.txt")
		return -1

	# Create a list with the search queries and close the file
	logging.info("(google)Creating search queries list")
	l = []
	for search_query in file: 
		l.append(search_query.rstrip())
	file.close() 

	# Start the browsing sessions
	for duration, interarrival in zip(duration_list, interarrivals_list):

		if "Linux" in platform.platform():
			driver = webdriver.Firefox()
			logging.info("Operating System Linux detected")
			logging.info("Using Firefox as browser")
		else:
			driver = webdriver.Chrome()
			logging.info("Operating System Windows detected")
			logging.info("Using Chrome as browser")

		logging.info("Opening website: google.com")
		driver.get("https://www.google.com/")
		
		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s1 = realistic_sleep_timer_inbetween_actions()

		deal_with_popup(driver)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s2 = realistic_sleep_timer_inbetween_actions()

		# update the remaining duration after the initial steps and their sleep time
		duration = duration - s1 - s2

		# Boolean variable so that after the first browsing session and onwards
		# a .back() is initiated. This way the senario won't arrive on a "dead-end"
		# page e.g. pdf, and always clickable links will be present
		first_time_in_loop = True

		while duration > 0:

			if not first_time_in_loop:
				logging.info(f"(google) Returning on home page...")
				driver.back()
				time.sleep(2)

			# select a random search query to search
			session_duration = search_element(driver, random.choice(l))
			logging.info(f"(google)Ending Mode:browsing after {session_duration:.2f} secs")

			s2 = realistic_sleep_timer_inbetween_sessions()

			# update the duration variable by subtracting the time spent on the application
			# and another 2 seconds that is roughly the time spent waiting on loading 
			# elements on google
			duration = duration - session_duration - s2 - 2

			# Set the variable to false so that on the next loop a .back() is initiated
			first_time_in_loop = False
		
		driver.quit()

		logging.info(f"(google)Time sleeping until next initiation of senario: {interarrival} secs")
		time.sleep(interarrival)
	logging.info("(google)Browsing ended successfully.")

