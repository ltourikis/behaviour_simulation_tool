import time
import random
import sys
import logging
import os
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains

from dotenv import load_dotenv

# configure logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

def timer_between_next_session(t):
    """
        Timer that is initiated inbetween the restart of sessions of Asklipios/LIS

        :param:     t:      sleep time in SECONDS
    """
    secs = t 
    logging.info(f"Wait time inbetween sessions {t} seconds")
    time.sleep(2) # insert secs here when done testing

def timer_between_asklipios_LIS(t):
    """
        After asklipios senario is over a certain amount of time should pass
        before the commition of the exams through LIS. 

        :param:     t:      sleep time in SECONDS
    """
    secs = t 
    logging.info(f"Wait time inbetween asklipios and LIS {t} seconds")
    time.sleep(2)   # insert secs here when done testing

def realistic_sleep_timer():
    """
        Wait 1 - 4 secs inbetween actions that simulate human interactions
        to make the simulation more realistic.
    """
    s = random.random()* 3 + 1
    logging.info(f"(Sleep Time inbetween actions)Sleep time = {s:.2f} secs")
    time.sleep(s)

def login(driver):
    """
        Handles the sign in for Asklipios.

        ATTENTION! A .env file needs to be present in the directory
        with entries like the following:
            
            PASSWORD="xxxxx" 
            USERNAME="loukas" 
    """
    try:
        time.sleep(2)
        logging.info("(Asklipios)Locating Είσοδος..")
        driver.switch_to.frame(driver.find_element_by_name("STARTPAGE"))
        entry = driver.find_element_by_xpath('//a[contains(text(), "Είσοδος")]')
        entry.click()

        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("CONTENTS"))

        load_dotenv()
        password = os.environ.get('PASSWORD_LIS')
        username = os.environ.get('USERNAME_LIS')

        logging.info("(Asklipios)Locating userid form..")
        name = driver.find_element_by_id("userid")
        name.send_keys(username)

        realistic_sleep_timer()

        logging.info("(Asklipios)Locating password form..")
        psswrd = driver.find_element_by_id("keyword")
        psswrd.send_keys(password)

        realistic_sleep_timer()

        logging.info("(Asklipios)Clicking continue")
        continue_button = driver.find_element_by_id("btnLogin")
        continue_button.click()
          
        realistic_sleep_timer()
    except Exception as e:
        logging.info(f"(Asklipios)Exiting login() with error {e}")

def click_pathologiki(driver):
    """
        Clicks ΠΑΘΟΛΟΓΙΚΗ button after logging in asklipios.
    """
    try:
        time.sleep(1)
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("CONTENTS"))

        logging.info("(Asklipios)Locating ΠΑΘΟΛΟΓΙΚΗ button..")
        pathologiki = driver.find_element_by_xpath('//a[@class = "ward-dep-link"]')
        pathologiki.click()
        
        realistic_sleep_timer()
    except Exception as e:
        logging.info(f"(Asklipios)Exiting click_pathologiki() with error {e}")

def eisagogi_asthenous(driver):
    """
        Commits a new patient from Λίστα Αναμονή
    """
    try:
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("CONTENTS"))

        try:
            # try to locate any new patient in Λίστα Αναμονή.
            # if at least one is found commit him, else continue
            logging.info("(Asklipios)Locating Λίστα Αναμονή..")
            queue = driver.find_elements_by_xpath('//a[contains(@href, "javascript:assignWaiting")]')
            patient = random.choice(queue)
            patient.click()
            logging.info("(Asklipios)Patient successfully fetched from Λίστα Αναμονή")

        except Exception as no_patients_waiting:
            logging.info("(Asklipios)No patient found in Λίστα Αναμονή")
            return -1
        
        realistic_sleep_timer()
        main_window = driver.window_handles[0]
        patient_window = driver.window_handles[1]
        driver.switch_to_window(patient_window)
        try:
            logging.info("(Asklipios)Locating bed buttton to insert new patient")
            beds = driver.find_elements_by_xpath('//img[@alt = "Κλικ για πλήρωση κλίνης"]')
            bed = random.choice(beds)
            bed.click()
            logging.info("(Asklipios)Bed successfully found and selected")
            driver.switch_to_window(main_window)
        except Exception as no_available_beds:
            logging.info("(Asklipios)Can't find free bed. Exiting..")
            return -1

        realistic_sleep_timer()
        
    except Exception as e:
        logging.info(f"(Asklipios)Exiting eisagogi_asthenous() with error {e}")

def blue_bottle(driver, epeigon_probability):
    """
       Handles new exams functionality for a random patient

       Procedure starts from clicking the "blue bottle" icon right after the name
       of a patient. If no "blue bottles" are found an error is thrown, and an corresponding
       message that there are no available patients.

       If blue bottle is clicked successfully a doctor is selected, then "Νέα Παραγγελία",
       then the two "+" expand crosses, then "Επιλέξτε". 

       The next step of the senario is to click on "Επείγον" or not, by generating a random
       number and then comparing it with the param:epeigon_probability.

       Then "Ενημέρωση" is selected, followed by "Επιβεβαίωση", "Εκτύπωση παραπεμπτικών" which
       pop-ups a new tab, and finally "Κλείσιμο".

       The function returns the number of the blue bottle (by order of appearance on screen) 
       that was clicked so that on a later stage the senario can return on the same patient 
       and verify that the results are ready for viewing.

       Also returns the number needed by LIS in order to commit the exams (fills the
       Εισαγωγή Εντολής form).

       :param:      epeigon_probability:        chance that the "Επείγον" is selected
       :return:     precious_number:            will be used by LIS to commit exams
       :return:     no_of_random_bottle:        number of blue bottle by order of 
                                                appearance

    """
    try:
        time.sleep(1)
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("CONTENTS"))

        try:
            logging.info("(Asklipios)Locating blue bottles..")
            bottles = driver.find_elements_by_xpath('//img[@alt = "Εργαστηριακές εξετάσεις"]')
            len_of_bottles_list = len(bottles)
            no_of_random_bottle = random.randint(0,len_of_bottles_list-1)
            bottle = bottles[no_of_random_bottle]
            bottle.click()
            logging.info(f"(Asklipios)No of bottle selected = {no_of_random_bottle+1}")
        except Exception as no_blue_bottles:
            logging.info("Can't find any blue bottles. Please insert patients.")
            logging.info("Exiting..")
            return -1

        realistic_sleep_timer()
        logging.info("(Asklipios)Selecting Doctor")
        select = Select(driver.find_element_by_name('doctor'))
        select.select_by_visible_text('ΑΝΑΣΤΑΣΙΟΥ ΑΛΕΞΑΝΔΡΟΣ (21096500596)')

        logging.info("(Asklipios)Clicking Νέα Παραγγελία")
        submit = driver.find_element_by_xpath('//input[@value = "Νέα Παραγγελία"]')
        submit.click()

        realistic_sleep_timer()

        logging.info("(Asklipios)Clicking on first +")  
        crosses = driver.find_elements_by_xpath('//div[@class = "hitarea expandable-hitarea"]')
        crosses[0].click()
        time.sleep(0.5)
        logging.info("(Asklipios)Clicking on second +")
        crosses[1].click()

        realistic_sleep_timer()

        logging.info("(Asklipios)Clicking Επιλέξτε")
        epilexte = driver.find_element_by_xpath('//label[@for = "checkbox-11_1_49"]')
        epilexte.click()

        realistic_sleep_timer()

        r = random.random()
        if r < epeigon_probability:
            logging.info("(Asklipios)Clicking Επείγον")
            epeigon = driver.find_element_by_xpath('//label[@for = "ucheckbox-11_1_49"]')
            epeigon.click()
            realistic_sleep_timer()
            
        logging.info("(Asklipios)Clicking Ενημέρωση")
        enimerosi = driver.find_element_by_id('gotoorder')
        enimerosi.click()
          
        realistic_sleep_timer()

        logging.info("(Asklipios)Clicking Επιβεβαίωση")
        epiveveosi = driver.find_element_by_xpath('//input[@value = "Επιβεβαίωση"]')
        epiveveosi.click()

        realistic_sleep_timer()

        logging.info("(Asklipios)Clicking Εκτύπωση παραπεμπτικών")
        ektiposi_parape = driver.find_element_by_xpath('//input[@value = "Εκτύπωση παραπεμπτικών"]')
        ektiposi_parape.click()

        realistic_sleep_timer()

        logging.info("(Asklipios)Handling popup tab")
        popup_tab = driver.window_handles[1]
        driver.switch_to_window(popup_tab)
        driver.close()

        realistic_sleep_timer()

        logging.info("(Asklipios)Clicking kleisimo")
        driver.switch_to_window(driver.window_handles[0])
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("CONTENTS"))
        close = driver.find_element_by_id('escape_link')
        close.click()

        realistic_sleep_timer()

        logging.info("(Asklipios)Locating number for LIS")
        l = driver.find_elements_by_xpath('//font[@color = "#000033"]')
        precious_number = l[0].text
        precious_number = int(precious_number.partition('/')[2])
        logging.info(f"(Asklipios)Number is {precious_number}")

        return (precious_number, no_of_random_bottle)
        
    except Exception as e:
        print(e)
        
def loginLIS(driver):
    """
        Sign in to LIS

        ATTENTION! A .env file needs to be present in the directory
        with entries like the following:
            
            PASSWORD="xxxxx" 
            USERNAME="loukas" 
    """
    try:
        load_dotenv()
        password = os.environ.get('PASSWORD_LIS')
        username = os.environ.get('USERNAME_LIS')

        logging.info("(LIS)Locating name form..")
        name = driver.find_element_by_name('username')
        name.send_keys(username)

        realistic_sleep_timer()  

        logging.info("(LIS)Locating password form..")
        psswrd = driver.find_element_by_name('password')
        psswrd.send_keys(password)

        realistic_sleep_timer()  

        logging.info("(LIS)Locating submit button..")
        submit = driver.find_element_by_xpath('//button[@value = "login"]')
        submit.click()

        realistic_sleep_timer()

        logging.info("(LIS)Locating ΒΙΟΧΗΜΙΚΟ button..")
        bioximiko = driver.find_element_by_xpath('//button[@value = "11"]')
        bioximiko.click()

        realistic_sleep_timer()
        
    except Exception as e:
        logging.info(f"(LIS)Exiting loginLIS() with error {e}")

def commit_exams_LIS(driver, num):
    """
        Handles the commit of exams in LIS

        :param:     num:        value produced in Asklipios and necessary for
                                the success of the whole commit exams senario
    """
    try:
        logging.info("(LIS)Locating Εισαγωγή Εντολής button..")
        eisagogi_edolis = driver.find_element_by_xpath('//span[contains(text(), "Εισαγωγή Εντολής")]')
        eisagogi_edolis.click()

        realistic_sleep_timer()

        logging.info("(LIS)Locating Εισαγωγή Εντολής form..")
        forms = driver.find_elements_by_xpath('//div[@class = "col-md-6"]/input')
        forms[1].send_keys(num)
          
        realistic_sleep_timer()

        logging.info("(LIS)Locating Εισαγωγή button..")
        eisagogi = driver.find_elements_by_xpath('//button[@class = "btn btn-primary"]')
        eisagogi[1].click()

        realistic_sleep_timer()

        try:
            # check if a windows popups. if not the particular ordered is already submitted
            # normally that should never happen, unless number of order is given manually 
            popup_tab = driver.window_handles[2]
            driver.switch_to_window(popup_tab)
            driver.close()
            realistic_sleep_timer()
        except Exception as e:
            logging.info("(LIS)Order already been submited")
        
        driver.switch_to_window(driver.window_handles[1])
        logging.info("(LIS)Clicking escape to return to main window")
        forms[1].send_keys(Keys.ESCAPE)
        time.sleep(3)

        logging.info("(LIS)Locating patient orders..")
        orders = driver.find_elements_by_xpath('//div[@class = "media-body order-row"]')
        action = ActionChains(driver)
        logging.info("(LIS)Double clicking on the latest order")
        action.double_click(orders[0]).perform()
          
        realistic_sleep_timer()
        
    except Exception as e:
        logging.info(f"(LIS)Exiting commit_exams_LIS() with error {e}")
        
def handle_exams(driver, normal_values_probability):
    """
        Fills the detail forms of the exams about to be commited

        Has the capability to fill the results form with either values within the normal
        range but also outside the normal range

        :param:     normal_values_probability:      chance the values filled on exam results
                                                    form to be within the normal range
    """
    try:
        # click egekrimeno
        logging.info("(LIS)Clicking εγκεκριμενο")
        check_boxes = driver.find_elements_by_xpath('//input[@type = "checkbox"]')
        egekrimeno = check_boxes[2]
        egekrimeno.click()
          
        realistic_sleep_timer()

        # fetch normal values
        logging.info("(LIS)Fetching normal values..")
        tds = driver.find_elements_by_xpath('//tr[@class = "test-highlight test-group-7 selected changed"]/td')
        normal_values_string = tds[8].text
        normal_values_list = normal_values_string.partition('-')
        lower_value, upper_value = int(normal_values_list[0]), int(normal_values_list[2])
        
        normal_value = (lower_value + upper_value)//2
        abnormal_value = upper_value + 1
        
        # fill apotelesma
        logging.info("(LIS)Locating αποτελεσμα form")
        apotelesma_form = driver.find_element_by_xpath('//input[@class = "inline-edit result"]')
        apotelesma_form.clear()

        r = random.random()
        if r < normal_values_probability:
            logging.info("(LIS)Normal values are selected")
            apotelesma_form.send_keys(normal_value)
        else:
            logging.info("(LIS)Abnormal values are selected")
            apotelesma_form.send_keys(abnormal_value)

        realistic_sleep_timer()

        # click apothikeusi
        logging.info("(LIS)Locating Αποθήκευση")
        apothikeusi = driver.find_element_by_xpath('//button[@title = "Αποθήκευση"]')
        apothikeusi.click()

        realistic_sleep_timer()

        #click apostoli apotelesmatos
        logging.info("(LIS)Clicking Αποστολή Αποτελέσματος")
        apostoli_a = driver.find_element_by_xpath('//button[@title = "Αποστολή Αποτελέσματος"]')
        apostoli_a.click()

        realistic_sleep_timer()
        
    except Exception as e:
        logging.info(f"(LIS)Exiting handle_exams() with error {e}")

def check_for_the_result_in_asklipios(driver, no_of_random_bottle):
    """
        Checks for the result in Asklipios.

        The check is repeated every two minutes for a total of ten minutes. If the
        results are not updated on Asklipios the procedure is aborted..

        In case they are found they are printed

        :param:     no_of_random_bottle:        used so that the check is made on the 
                                                patient for whom the test was issued
    """
    driver.switch_to_window(driver.window_handles[0])
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name("CONTENTS"))

    time.sleep(2)    
    tds = driver.find_elements_by_xpath('//tr[@bgcolor = "#efefef"]/td')

    logging.info("(Asklipios)Results are not back yet.. Waiting for 2 minutes")
    for i in range(5):
        time.sleep(120)
        close = driver.find_element_by_id('escape_link')
        close.click()

        time.sleep(2)

        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element_by_name("CONTENTS"))
        bottles = driver.find_elements_by_xpath('//img[@alt = "Εργαστηριακές εξετάσεις"]')
        bottle = bottles[no_of_random_bottle]
        bottle.click()
        time.sleep(2)
        
        tds = driver.find_elements_by_xpath('//tr[@bgcolor = "#efefef"]/td')
        if "Αποτέλεσμα" not in tds[7].text:
            logging.info("(Asklipios)Results are not back yet.. Waiting for 2 minutes")
        else:
            logging.info("(Asklipios)Results are back")
            logging.info("(Asklipios)Clicking Εκτύπωση LIS")
            print_LIS = driver.find_element_by_xpath('//img[@alt = "Εκτύπωση LIS"]')
            print_LIS.click()

            realistic_sleep_timer()
        
            return 0
    logging.info("(Asklipios)coudn't find results after 10 mins.. Exiting..")
    return -1
        
def asklipios_LIS():
    """
        Handles the Asklipios and LIS senarios

        ###################################################

        Firtsly the configuration is handled via the LIS_config.json The contents of 
        the file are the following:

        {
            "LIS": "http://10.10.2.118:9999/",
            "asklipios": "http://10.10.2.103:51001/",
            "asklipios_only": true,
            "time_between_sessions": 10,
            "time_between_asklipios_LIS": 10,
            "epigon_probability": 0.5,
            "normal_values_probability": 0.5
        }

        If "asklipios_only" is set on true, then the browsing sequence won't go into
        the LIS part. Instead it will loop the Asklipios part until it is stopped.

        "LIS" is filled with the according IP that the service is running on.
        Similarly "asklipios" is filled with the according IP that the service 
        is running on.

        "Time_between_sessions" and "time_between_asklipios_LIS" are filled with a positive 
        integer value that represents MINUTES. These values are used on the according functions 
        and handle the sleep time inbetween sessions and the sleep time after the completion 
        of the senario of Asklipios and before the start of LIS. 

        Epigon_probability is the chance "Επείγον" to be selected when new exams
        are issued for a patient on Asklipios.

        Normal_values_probability is the chance that the results of the issued exams 
        are within the normal range.

        ###################################################

        The password and username used for signing in Asklipios & LIS are stored 
        on a .env file for safety reasons.
        The .env file should have entries as follows:

        USERNAME="XXXXXXXX"
        PASSWORD="xxxxxxxxx"

        ###################################################

        The browsing sequence is:
        
        A. Initial Steps in Asklipios
            1.Sign in to Asklipios
            2.Select ΠΑΘΟΛΟΓΙΚΗ
        B. Commit new patient in Asklipios
            3.Try to locate any new patient in Λίστα Αναμονής.
              If no new patients are available continue with step 6
            4.Try to locate a free bed for the new patient
              If there is no free bed continue with step 6
            5.Commit the new patient in the available bed
        C. Create new exams for a patient in Asklipios
            6.Locate the available blue bottles icons and select one randomly
              If no new bottles are available continue with step 27
            7.Select a doctor
            8.Select Νέα Παραγγελία
            9.Click on the two "+" icons to expand the menus
           10.Click on Επιλέξτε
           11.Possibility to select "Επείγον"
           12.Click Ενημέρωση
           13.Click Επιβεβαίωση
           14.Click Εκτύπωση παραπεμπτικών
           15.Close Asklipios
        D. Initial Steps in LIS
           16.If Asklipios_only is selected go to step 1 
              ELSE  Sign in to LIS
           17.Select ΒΙΟΧΗΜΙΚΟ
        C. Handle and Commit Exams in LIS
           18.Select Εισαγωγή Εντολής and type a no of Order and then "Enter"
           19.Return to main window  
           20.Double click on the latest order
           21.Select Εγκεκριμένο
           22.Chance to fill the results form with results within normal range
              Chance to fill the results form with values out of the normal range
           23.Select Αποθήκευση
           24.Select Αποστολή Αποτελέσματος
        D. Check for results back in Asklipios
           25.Check every two minutes and for a total of 10 minutes if the results
              are back. If after 10 minutes the results are not back continue with step 27
           26.Select Εκτύπωση LIS
        E. Finish the senario
           27.Exit the applications
        F. Repeat the senario until the profile stops
           28.Go to step 1         
       
    """
    try:
        file = open(os.path.join(sys.path[0], "asklipios_LIS/LIS_config.json"), "r")

    except Exception as e:
        logging.info("Could not open/read file: LIS_config.json")
        return -1
    config = json.load(file)
    file.close()

    asklipios_ip = config["asklipios"]
    logging.info(f"Asklipios ip = {asklipios_ip}")

    LIS_ip = config["LIS"]
    logging.info(f"LIS ip = {LIS_ip}")
    
    time_between_sessions = config["time_between_sessions"]
    logging.info(f"Time between sessions imported from config: {time_between_sessions} seconds")

    time_between_asklipios_LIS = config["time_between_asklipios_LIS"]
    logging.info(f"Time between Asklipios and LIS imported from config: {time_between_asklipios_LIS} seconds")

    epigon_probability = config["epigon_probability"]
    logging.info(f"Epigon probability imported from config: {epigon_probability*100}%")

    normal_values_probability = config["normal_values_probability"]
    logging.info(f"Normal values probability imported from config: {normal_values_probability*100}%")

    # Congiguration that makes the script to NOT enter LIS.
    # Initiates Asklipios Simulation only
    asklipios_only = config["asklipios_only"]
    mode  = "Asklipios&LIS"
    if asklipios_only:
        mode = "Asklipios_only"
    logging.info(f"Mode enabled: {mode}")

    
    while True:
        logging.info("New session initiated")
        #########ASKLIPIOS########
        
        logging.info("Starting (Asklipios)")
        driver = webdriver.Chrome()
        driver.get(asklipios_ip)

        login(driver)
        click_pathologiki(driver)
        eisagogi_asthenous(driver)
        (precious_number, bottle) = blue_bottle(driver, epigon_probability)

        # Skip LIS if asklipios_only is configured
        if asklipios_only:
            timer_between_next_session(time_between_sessions)
            driver.quit()
            time.sleep(3)
            continue

        timer_between_asklipios_LIS(time_between_asklipios_LIS)
        ###########LIS############

        logging.info("Starting (LIS)")
        driver.execute_script("window.open('');")
        driver.switch_to_window(driver.window_handles[1])
        driver.get(LIS_ip)
        loginLIS(driver)
        commit_exams_LIS(driver, precious_number)
        handle_exams(driver, normal_values_probability)

        driver.close()
        time.sleep(3)

        #########ASKLIPIOS########
        logging.info("Returning to Asklipios and checking if the results are back..")
        check_for_the_result_in_asklipios(driver, bottle)
        time.sleep(2)
        driver.quit()

        timer_between_next_session(time_between_sessions)
    
if __name__ == "__main__":
    asklipios_LIS()
