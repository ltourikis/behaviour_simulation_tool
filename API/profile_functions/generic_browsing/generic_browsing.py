# Contains the functions that handle the browsing for any url

import random
import time
import logging
import platform

from selenium import webdriver

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

def click_on_valid_link(driver, elements, url):
	""" 
		Clicks on a random link in browsing mode.

		Each time 10 attempts are tolerated of trying to locate a valid link.
		The links are contained in the param:elements.
		For each failed attempt a new link is selected.
		If 10 attempts are made and no valid link is found the process is aborted
		and the error code -1 is returned
		
		:param:		url:			the url of the site visited.Used for logging
									purposes only
		:param:		elements:    	list of "clickable" elements found on a page
    	:return:    -1:			 	in case no valid link is found
	"""

	cnt = 0
	while True:
		try:
			random.choice(elements).click()
			logging.info(f"({url})Clicked on link successfully")
			break
		except Exception as e:
			logging.info(f"({url})Error clicking on link: " + str(e))
			logging.info(f"({url})Trying another link")

			# 10 trials of clicking a links on the current page are tolerated
			# For each failed attempt a new link is selected
			cnt += 1
			if cnt < 10:
				continue
			else:
				logging.info(f"({url})10 trials made, aborting..")
				return -1

def get_clickable_elements(driver, url):
	"""
		Locates all the @href elements on a page and returns them.

		If no @href elements are located -1 is returned (that is highly unlucky
		to happen on any given fb page though). 
		Note that the @href elements might not be trully clickable.
		Thus a first filter is applied on the elements via the .is_displayed() method.

		:param:		url:		the url of the site visited.Used for logging
								purposes only
    	:return:	elements: 	If the procedure was successful 
    	:return:	-1:  		If any error occured    
	"""
	# Sleeping 4 seconds for page to load all elements
	time.sleep(4)

	# Fetch clickable elements
	elements = driver.find_elements_by_xpath("//a[@href]")
	logging.info(f"({url})Links found: {len(elements)}")

	# Check whether elements could be determined (empty list)
	if not elements:
		logging.info(f"({url})click_on_stuff() error: No elements found")
		return -1

	# Filtering all links that are not active (eg generated by JS)
	try:
		valid_elements = [element for element in elements if element.is_displayed()]	
	except Exception as e:
		logging.info(f"({url})click_on_stuff() error: is_displayed() exception: " + str(e))
		return -1
	return elements

def click_on_stuff(driver, url):
	"""
		Wrapper function for the click_on_valid_lick() function.
		
		Firstly the clickable elements (links) are brought via the 
		get_clickable_elements() function.

		Then a click is made on a random element via the click_on_valid_lick() function
		and a sleep is initiated in order to make the simulation more realistic

		:param:		url:				the url of the site visited.Used for logging
										purposes only		
		:return:	session_duration:	time spent browing on the function	 
	"""
	elements = get_clickable_elements(driver, url)
	click_on_valid_link(driver, elements, url)

	# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
	session_duration = realistic_sleep_timer_inbetween_actions()

	return session_duration



def generic_browsing(duration_list, interarrivals_list, url):
	"""
		Handles the browsing of any given url.

		The param:url contains the url of the website that will be visited.

		The parameters interarrivals_list and duration_list are
		received as Strings, with their values separated by a comma.
		The function transforms them to float type lists.
		For example if "100, 20" is received, it is transformed to [100.0, 20.0].

		The param:duration_list holds the list with values that represents the total time 
		that will be spent on param:url on each senario.

		Inbetween the restarting of the senarios there is "break" time that lasts 
		as much as the value taken from the param:interarrivals_list each time accordingly.

		The two lists should have the same length.
		
		Inbetween steps that are supposedly made by human user sleep timers of
		1-4 seconds are initiated so that the simulation is more realistic.

		:param: 	duration_list:			String with the duration of each session.
		:param: 	interarrivals_list:		String with the break duration inbetween sessions.
		:param:		url:					String of the url that will be visited

	"""

	duration_list = [float(s) for s in duration_list.split(',')]
	interarrivals_list = [float(s) for s in interarrivals_list.split(',')]

	logging.info(f"Seting up {url} browsing..")
	logging.info(f"  --duration_list(secs): {duration_list}")
	logging.info(f"  --interarrivals_list(secs): {interarrivals_list}")

	for duration, interarrival in zip(duration_list, interarrivals_list):

		logging.info(f"Opening website: {url}")
		if "Linux" in platform.platform():
			driver = webdriver.Firefox()
			logging.info("Operating System Linux detected")
			logging.info("Using Firefox as browser")
		else:
			driver = webdriver.Chrome()
			logging.info("Operating System Windows detected")
			logging.info("Using Chrome as browser")

		driver.get(url)
		logging.info(f"({url})Browsing")		

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s1 = realistic_sleep_timer_inbetween_actions()

		# update the remaining duration after the initial steps and their sleep time
		duration -= s1

		# Boolean variable so that after the first browsing session and onwards
		# a .back() is initiated. This way the senario won't arrive on a "dead-end"
		# page e.g. pdf, and always clickable links will be present
		first_time_in_loop = True

		while duration > 0:
			
			if not first_time_in_loop:
					logging.info(f"({url})Returning on home page...")
					driver.back()
					time.sleep(2)

			session_duration = click_on_stuff(driver, url)
			logging.info(f"({url})Ending Mode:browsing after {session_duration:.2f} secs")

			s2 = realistic_sleep_timer_inbetween_sessions()

			# Set the variable to false so that on the next loop a .back() is initiated
			first_time_in_loop = False

			# update the duration variable by subtracting the time spent on the application
			# and another 10 seconds that is roughly the time spent waiting on loading 
			# elements and websites
			duration = duration - session_duration - s2 - 10

		driver.quit()

		logging.info(f"({url})Time sleeping until next initiation of senario: {interarrival} secs")
		time.sleep(interarrival)
	logging.info(f"({url})Browsing ended successfully.")

if __name__ == "__main__":
	generic_browsing("30, 60", "2,2", "https://www.galinos.gr/")