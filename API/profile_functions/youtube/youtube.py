import logging
import os
import time
import random
import platform
import datetime

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

def youtube_sign_in(driver, email, password):
	"""
		Handles the sign in popup.

		**Google has currently disabled the aforementioned popup.**

		Fills the username form and then "enter" is sent.
		Fills the password form and then "enter" is sent.

		If the popup is not located, an error is logged and the browsing 
		procedure continues.

		:param:		username: 			The username of the user 
    	:param:		password:			The password of the user 
    	:return:	0:					If any errors occurs
    	:return:	session_duration:	Time spent browing on the function
	"""
	try:
		logging.info("(youtube)Locating Sign In screen")
		button = WebDriverWait(driver, WAIT_TIME).until(
		EC.presence_of_all_elements_located((By.XPATH, "//tp-yt-paper-button[@id = 'button'][@aria-label = 'Sign in']"))
		)
		button[1].click()

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s1 = realistic_sleep_timer_inbetween_actions()

		logging.info("(youtube)Clicked Sing In button succesfully")
	except Exception as e:
		logging.info("(youtube)Error in: Signing in")
		logging.info("(youtube)Error description: " + str(e))
		logging.info("(youtube)Signing in aborted..")
		return 0

	try:
		logging.info("(youtube)Locating email form")
		email_form = WebDriverWait(driver, WAIT_TIME).until(
		EC.presence_of_element_located((By.ID, "identifierId"))
		)
		logging.info("(youtube)Filling email form")
		email_form.send_keys(email)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s2 = realistic_sleep_timer_inbetween_actions()

		email_form.send_keys(Keys.RETURN)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s3 = realistic_sleep_timer_inbetween_actions()

	except Exception as e:
		logging.info("(youtube)Error in: Locating or filling email form")
		logging.info("(youtube)Error description: " + str(e))
		logging.info("(youtube)Signing in aborted..")
		return 0

	try:
		logging.info("(youtube)Locating password form")
		password_form = WebDriverWait(driver, WAIT_TIME).until(
		EC.presence_of_element_located((By.XPATH, "//input[@type = 'password'][@aria-label = 'Enter your password']"))
		)
		logging.info("(youtube)Filling password form")
		password_form.send_keys(password)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s4 = realistic_sleep_timer_inbetween_actions()

		password_form.send_keys(Keys.RETURN)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s5 = realistic_sleep_timer_inbetween_actions()

	except Exception as e:
		logging.info("(youtube)Error in: Locating or filling password form")
		logging.info("(youtube)Error description: " + str(e))
		logging.info("(youtube)Signing in aborted..")
		return 0

	session_duration = s1 + s2 + s3 + s4 + s5


def pick_a_random_video(driver):
	"""
		Selects a random video on a given youtube page.

		Initially a list of all the elements with id 'video-titles' is created 
		and then filtered by the is_displayed() method.
		Then a random video from the list is selected.
		
		:return:	-1:			If any errors occurs
	"""
	try:
		logging.info("(youtube)Creating video list")
		videos = driver.find_elements_by_id('video-title')
		valid_links = [link for link in videos if link.is_displayed()]
	except Exception as e:
		logging.info("(youtube)Error in: Creating video list")
		logging.info("(youtube)Error description: " + str(e))
		return -1

	try:
		logging.info("(youtube)Clicking on random video")
		random.choice(valid_links).click()
	except Exception as e:
		logging.info("(youtube)Error in: Clicking on video")
		logging.info("(youtube)Error description: " + str(e))
		logging.info("(youtube)Clicking on random video aborted..")
		return -1

def google_cookies_fullscreen(driver):
	"""
		Handles the cookies popup.

		Once the cookies popup appears the "I agree" button is selected.

    	:return:	-1:			If any errors occurs
	"""
	try:
		logging.info("(youtube)Locating Google Cookies screen")
		i_agree = WebDriverWait(driver, WAIT_TIME).until(
		EC.presence_of_all_elements_located((By.XPATH, '//tp-yt-paper-button[@id="button"]'))
		)
		logging.info('(youtube)Clicking I Agree button')
		i_agree[6].click()
	except Exception as e:
		logging.info("(youtube)Error in: google_cookies_fullscreen()")
		logging.info("(youtube)Error description: " + str(e))
		logging.info("(youtube)Clicking Google Cookies aborted..")
		return -1

def get_duration(driver):
	"""
		Gets the total duration of the video and returns it. Also handles ads.

		When the "skip_ads" button appears it is clicked.
		One video may have more than one ads, so we check on a while loop
		until the "skip adds" is not present in the page.

		That means all ads are handled.

		:return:	0:						If any errors occurs
		:return:	duration_in_seconds:	Duration of the video in seconds
	"""
	# initial 10 seconds sleep time so that skip ads button appears
	# dodging the ads timer actually..
	time.sleep(10)

	try:
		while len(driver.find_elements_by_xpath("//button [@class = 'ytp-ad-skip-button ytp-button']"))>0:
			# if skip ads button is present click it 
			driver.find_element_by_xpath("//button [@class = 'ytp-ad-skip-button ytp-button']").click()
			logging.info("(youtube)Skipped ads successfully..")
			# wait for 7 seconds and search again..
			time.sleep(7)
	except Exception as e:
		logging.info("(youtube)Error in: handling ads..")
		logging.info("(youtube)Error description: " + str(e))

	logging.info("(youtube)Fetching video duration..")
	try:
		duration = driver.find_element_by_xpath("//span[@class = 'ytp-time-duration']").get_attribute("innerText")

	except Exception as e:
		logging.info("(youtube)Error in: Obtaining the length of the video in raw format")
		logging.info("(youtube)Error description: " + str(e))
		logging.info("(youtube)Fetching duration aborted..")
		return 0

	try:
		# Obtain the length of the video in seconds
		x = time.strptime(duration, '%M:%S')

		duration_in_seconds = datetime.timedelta(minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
		logging.info(f"(youtube)Duration of video is {duration_in_seconds} seconds")
	except Exception as e:
		logging.info("(youtube)Error in: Obtaining the length of the video in seconds")
		logging.info("(youtube)Error description: " + str(e))
		logging.info("(youtube)Fetching duration aborted..")
		return 0

	return duration_in_seconds

def youtube(duration_list, interarrivals_list, url):
	"""
		Handles the youtube browsing.

		The parameters interarrivals_list and duration_list are
		received as Strings, with their values separated by a comma.
		The function transforms them to float type lists.
		For example if "100, 20" is received, it is transformed to [100.0, 20.0].

		The two lists must have the same length.

		The param:duration_list holds the list with values that represents the total time 
		that will be spent on facebook on each senario.

		Inbetween the restarting of the senarios there is "break" time that lasts 
		as much as the value taken form the param:interarrivals_list each time accordingly.
		
		############################################################
		
		The url param is not used. It's there because the wrapper function that 
		calls the facebook function as well as other functions,on some occassions 
		might need a url param.
		Not the best implementation and will be fixed.

		############################################################

		In between each action that represents a real human action there is a wait time
		so that the simulation is closer to human behaviour. 
		
		############################################################

		The password and email of the user are stored on a .env file for
		safety reasons.
		The .env file should have entries as follows:

		EMAIL="xxxx@xxx.xxx"
		PASSWORD="xxxxxxxxx"

		############################################################

		The browsing sequence is:
		1.accept cookies (if possible)
		2.sign in (if possible)
		3.watch a random video
		4.skip ads (if possible)
		5.repeat steps 3-4 until the duration is over

		:param: 	duration_list:			String with the duration of each session.
		:param: 	interarrivals_list:		String with the break duration inbetween sessions.
		:param:		url:					Not being used. Set to none

	"""
	duration_list = [float(s) for s in duration_list.split(',')]
	interarrivals_list = [float(s) for s in interarrivals_list.split(',')]
	logging.info("Setting up youtube browsing..")
	logging.info(f"  --duration_list(secs): {duration_list}")
	logging.info(f"  --interarrivals_list(secs): {interarrivals_list}")

	for duration, interarrival in zip(duration_list, interarrivals_list):

		# Sign in to youtube
		load_dotenv()
		password = os.environ.get('PASSWORD_YOUTUBE')
		email = os.environ.get('EMAIL_YOUTUBE')

		logging.info("Opening website: youtube.com")
		if "Linux" in platform.platform():
			driver = webdriver.Firefox()
			logging.info("Operating System Linux detected")
			logging.info("Using Firefox as browser")
		else:
			driver = webdriver.Chrome()
			logging.info("Operating System Windows detected")
			logging.info("Using Chrome as browser")
		driver.get("https://www.youtube.com/")

		google_cookies_fullscreen(driver)

		# Wait 1 - 4 secs inbetween actions to make the simulation more realistic
		s1 = realistic_sleep_timer_inbetween_actions()

		s2 = youtube_sign_in(driver, email, password)

		duration = duration - s1 - s2
		
		# Start watching videos. 
		logging.info("(youtube)Mode: Browsing on random trending video")
		logging.info(f"(youtube) About to watch videos for {duration:.2f} seconds")

		while duration > 0:
			driver.get('https://www.youtube.com/feed/trending')

			pick_a_random_video(driver)

			random_video_duration = get_duration(driver)

			if random_video_duration > duration:

				# If the video about to be watched is bigger than the remaining duration
				# of the session, then the video will be stopped when the duration timer 
				# expires. 
				logging.info(f"(youtube)Watching video for {duration:.2f} secs(video will be interrupted!)")
				time.sleep(duration)
				logging.info(f"(youtube)Watching video is interrupted, end of duration")
				
				# duration is set to zero so that the loop breaks and the app moves on to the 
				# next senario
				duration = 0

			else:
				logging.info(f"(youtube)Watching video for {random_video_duration} secs")
				time.sleep(random_video_duration)
				logging.info(f"(youtube)Watched whole video successfully. Moving on to next video..")
				duration -= random_video_duration
		
		driver.quit()

		logging.info(f"(youtube)Time sleeping until next initiation of senario: {interarrival} secs")
		time.sleep(interarrival)
	logging.info("(youtube)Browsing ended successfully.")

if __name__ == "__main__":
	youtube("30,300", "2,2", None)