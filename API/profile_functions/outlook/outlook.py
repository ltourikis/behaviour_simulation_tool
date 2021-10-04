import time
import random
import string
import os
import logging
import platform

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

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

def realistic_sleep_timer_for_writing_an_email():
	"""
		Wait 20 - 30 secs for the procedure of typing an email
		to make the simulation more realistic

		:return:	s:		the sleep time
	"""
	s = random.random()* 10 + 20
	logging.info(f"(Sleep Time for Typing an Email)Sleep time = {s:.2f} secs")
	time.sleep(s)
	return s

def outlook_sign_in(driver, email, password):
	"""
		Handles the signing in on outlook.

		Fills the email and password forms with the passed params:email, password.

		:param:		email:					Email to sign in with
		:param:		password:				Password to sign in with
		:returns:	-1:						In case of any error
		:return: 	session_duration:		Time spent while on the function
	"""
	try:
		logging.info("(outlook)Locating Sign In button")
		if "Linux" in platform.platform():
			sign_in = WebDriverWait(driver, WAIT_TIME).until(
			EC.presence_of_element_located((By.XPATH, f"//a[contains(text(),'Sign in')]"))
			)	
		else:
			sign_in = WebDriverWait(driver, WAIT_TIME).until(
			EC.presence_of_element_located((By.XPATH, f"//a[contains(text(),'Είσοδος')]"))
			)
		sign_in.click()

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s1 = realistic_sleep_timer_inbetween_actions()

		logging.info("(outlook)Sign in button clicked successfully")

	except Exception as e:
		logging.info("(outlook)Error in: Signing in")
		logging.info("(outlook)Error description: " + str(e))
		logging.info("(outlook)Signing in aborted..")
		return -1

	try:
		logging.info("(outlook)Locating email form")
		email_form = WebDriverWait(driver, WAIT_TIME).until(
		EC.presence_of_element_located((By.XPATH, "//input[@type = 'email']"))
		)
		logging.info("(outlook)Filling email form")
		email_form.clear()
		email_form.send_keys(email)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s2 = realistic_sleep_timer_inbetween_actions()

		email_form.send_keys(Keys.RETURN)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s3 = realistic_sleep_timer_inbetween_actions()

	except Exception as e:
		logging.info("(outlook)Error in: Locating or filling email form")
		logging.info("(outlook)Error description: " + str(e))
		logging.info("(outlook)Signing in aborted..")
		return -1

	try:
		logging.info("(outlook)Locating password form")
		pass_form = WebDriverWait(driver, WAIT_TIME).until(
		EC.presence_of_element_located((By.XPATH, "//input[@type = 'password']"))
		)
		logging.info("(outlook)Filling password form")
		pass_form.send_keys(password)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s4= realistic_sleep_timer_inbetween_actions()

		pass_form.send_keys(Keys.RETURN)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s5 = realistic_sleep_timer_inbetween_actions()

	except Exception as e:
		logging.info("(outlook)Error in: Locating or filling password form")
		logging.info("(outlook)Error description: " + str(e))
		logging.info("(outlook)Signing in aborted..")
		return -1

	session_duration = s1 + s2 + s3 + s4 + s5

	return session_duration

def stay_signed_in(driver):
	"""
		Handles the "stay signed in pop up" and clicks "No".

		:returns:		-1:		in case of any error
	"""
	try:
		logging.info("(outlook)Locating stay signed in pop-up")
		logging.info("(outlook)Locating no button")
		no_button = WebDriverWait(driver, WAIT_TIME).until(
		EC.presence_of_element_located((By.ID, "idBtn_Back"))
		)

		no_button.click()
	except Exception as e:
		logging.info("(outlook)Error in: Locating stay signed in pop-up")
		logging.info("(outlook)Clicking no aborted..")
		return -1

def click_inbox(driver):
	"""
		Clicks the inbox button on the home page of outlook.

		:returns:		-1:		in case of any error
	"""
	try:
		logging.info("(outlook)Locating inbox button")
		inbox = WebDriverWait(driver, WAIT_TIME).until(
		EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Inbox')]"))
		)
		inbox.click()
		logging.info("(outlook)Inbox button clicked succesfully")
	except Exception as e:
		logging.info("(outlook)Error in: Clicking inbox")
		logging.info("(outlook)Error description: " + str(e))
		logging.info("(outlook)Clicking inbox aborted..")
		return -1

def get_emails(driver):
	"""
		Creates a list with all the available emails in inbox.

		:returns:		emails:		list with all the emails in inbox
		:returns:		-1:			in case of any error
	"""
	try:
		logging.info("(outlook)Locating message list element")
		message_list = WebDriverWait(driver, WAIT_TIME).until(
		EC.presence_of_element_located((By.XPATH, "//div[@aria-label = 'Message list']"))
		)
		logging.info("(outlook)Creating message list")
		emails = message_list.find_elements_by_xpath("//div[@data-convid]")
		logging.info("(outlook)Message list created successfully")

	except Exception as e:
		logging.info("(outlook)Error in: Getting emails")
		logging.info("(outlook)Error description: " + str(e))
		logging.info("(outlook)Getting emails aborted..")
		return -1
	return emails

def new_email(driver, receiver):
	"""
		Creates a new email and the sends it to the param:receiver.

		The email body is 1000 random ascii characters
		The email subject is 10 randim ascii characters

		:param:		receiver:				Email adress of the receiver
		:return:	-1:						In case of any error
		:return: 	session_duration:		Time spent while on the function
	"""
	letters = string.ascii_letters
	try:
		logging.info("(outlook)Locating new email button")
		new_message = WebDriverWait(driver, WAIT_TIME).until(
		EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'New message')]"))
		)
		new_message.click()
		logging.info("(outlook)New message button clicked successfully")

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s1 = realistic_sleep_timer_inbetween_actions()

		logging.info("(outlook)Locating 'To' form")
		to = WebDriverWait(driver, WAIT_TIME).until(
				EC.presence_of_element_located((By.XPATH, "//input[@aria-label='To']"))
		)
		logging.info("(outlook)Filling 'To' form")
		to.send_keys(receiver)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s2 = realistic_sleep_timer_inbetween_actions()

		logging.info("(outlook)Locating subject form")
		subject = driver.find_element_by_xpath("//input[@aria-label = 'Add a subject']")
		logging.info("(outlook)Filling subject form")
		subject.send_keys(''.join(random.choice(letters) for i in range(10)))

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s3 = realistic_sleep_timer_inbetween_actions()

		logging.info("(outlook)Locating message form")
		message = driver.find_element_by_xpath("//div[@aria-label = 'Message body']")
		logging.info("(outlook)Filling message form")
		message.send_keys(''.join(random.choice(letters) for i in range(1000)))

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s4 = realistic_sleep_timer_for_writing_an_email()

		logging.info("(outlook)Locating send button")
		send = driver.find_element_by_xpath("//button[@aria-label = 'Send']")
		send.click()
		logging.info("(outlook)Send button clicked successfully")

	except Exception as e:
		logging.info("(outlook)Error in: Creating new email")
		logging.info("(outlook)Error description: " + str(e))
		logging.info("(outlook)Creating new email aborted..")
		return -1

	session_duration = s1 + s2 + s3 + s4

	return session_duration

def browse_emails(driver):
	"""
		Browse the emails in inbox 

		:return: 	session_duration:		Time spent while on the function
	"""
	click_inbox(driver)

	# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
	s1 = realistic_sleep_timer_inbetween_actions()

	emails = get_emails(driver)

	random.choice(emails).click()

	# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
	s2 = realistic_sleep_timer_inbetween_actions()

	session_duration = s1 + s2

	return session_duration


def outlook(duration_list, interarrivals_list, url=None):
	"""
		Handles the outlook sessions.

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
		The password and email of the user and the address of the receiver
		are stored on a .env file for safety reasons.
		The .env file should have entries as follows:

		OUTLOOK_EMAIL="xxxx@xxx.xxx"
		OUTLOOK_PASSWORD1="xxxxxxxxx"
		RECEIVER_EMAIL="xxxx@xxx.xxx"

		############################################################

		The session sequence is:
		1.sign in
		2.handle the "stay singed in?" pop-up (if possible)
		3.50% chance to browse on random emails in inbox and 50% time
		  to send a new email
		4.repeat step 3 until the duration is over

		:param: 	duration_list:			String with the duration of each session.
		:param: 	interarrivals_list:		String with the break duration inbetween sessions.
		:param:		url:					Not being used. Set to none

	"""
	# Make the received strings into lists that contain float type numbers.
	duration_list = [float(s) for s in duration_list.split(',')]
	interarrivals_list = [float(s) for s in interarrivals_list.split(',')]
	logging.info("Setting up outlook browsing..")
	logging.info(f"  --duration_list(secs): {duration_list}")
	logging.info(f"  --interarrivals_list(secs): {interarrivals_list}")

	load_dotenv()
	password = os.environ.get('OUTLOOK_PASSWORD')
	email = os.environ.get('OUTLOOK_EMAIL')
	receiver = os.environ.get('RECEIVER_EMAIL')

	for duration, interarrival in zip(duration_list, interarrivals_list):
		# Log in to outlook
		logging.info("Opening website: outlook.com")
		if "Linux" in platform.platform():
			driver = webdriver.Firefox()
			logging.info("Operating System Linux detected")
			logging.info("Using Firefox as browser")
		else:
			driver = webdriver.Chrome()
			logging.info("Operating System Windows detected")
			logging.info("Using Chrome as browser")
		driver.get("https://outlook.live.com/owa/")

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s1 = realistic_sleep_timer_inbetween_actions()

		s2 = outlook_sign_in(driver, email, password)

		stay_signed_in(driver)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s3 = realistic_sleep_timer_inbetween_actions()

		duration = duration - s1 - s2 - s3

		while duration > 0:
			#50-50 to browse or send a message
			if random.random() < 0.5:
				logging.info(f"(outlook)Mode:Browsing emails")
				session_duration = browse_emails(driver)
				logging.info(f"(outlook)Ending session(Mode:browsing emails) after {session_duration:.2f} secs")
				
				s4 = realistic_sleep_timer_inbetween_sessions()
			else:
				logging.info(f"(outlook)Mode:Sending email")
				session_duration = new_email(driver, receiver)
				logging.info(f"(outlook)Ending session(Mode:sending email) after {session_duration:.2f} secs")
				
				s4 = realistic_sleep_timer_inbetween_sessions()
			duration = duration - session_duration - s4 - 10
	
		driver.quit()

		logging.info(f"(outlook)Time sleeping until next initiation of senario: {interarrival} secs")
		time.sleep(interarrival)
	logging.info("(outlook)Session ended successfully.")

if __name__ == "__main__":
	outlook("15, 20", "2, 2")