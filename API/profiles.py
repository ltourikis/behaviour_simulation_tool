"""
This is the profiles module and supports  ReST actions for the
profiles collection
"""

# System modules
from datetime import datetime
from multiprocessing import Process
import psutil
import time
import threading
import os
import platform
import logging
import glob

# 3rd party modules
from flask import abort, make_response, current_app

# profiles data
from profiles_collection import profiles

# module that configures the quick profile 
# according to the config.txt file
from quick_profile import config_quick_profile



def get_timestamp():
    """
        Returns timestamp. For Logging purposes.

        Format: Year - Month - Day Hour:Minute:Seconds  
    """
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def create_serialazable_data(profile):
    """
        Creates json with the profile info that the API makes public
        when sent as response to a GET request.

        Part of the profile info like process ID is left out, as there is 
        no reason to be public.

        :param:     profile:    json that has all the profile info to be processed
        :return:    s_data:     the json modified and ready to be sent as response to GET
                                requests by the API
    """
    s_data = {
        "profile_name" : profile["profile_name"],
        "status" : profile["status"],
        "duration": profile["total_duration"],
        "started_running" : profile["started_running"],
        "time_remaining": profile["time_remaining"],
        "request_body": profile["request_body"],
        "asklipios_LIS": profile["asklipios_LIS"]["status"],
        "persona": profile["persona"]["status"],
        "applications": {
            "google" : {
                "status": profile["applications"]["google"]["status"]
            },
            "youtube": {
                "status": profile["applications"]["youtube"]["status"]
            },
            "facebook": {
                "status": profile["applications"]["facebook"]["status"]
            },
            "outlook": {
                "status": profile["applications"]["outlook"]["status"]
            },
            "promitheus": {
                "status": profile["applications"]["promitheus"]["status"]
            },
            "galinos": {
                "status": profile["applications"]["galinos"]["status"]
            },
            "apografi_http": {
                "status": profile["applications"]["apografi_http"]["status"]
            },
            "gsis": {
                "status": profile["applications"]["gsis"]["status"]
            },
            "idika": {
                "status": profile["applications"]["idika"]["status"]
            },
            "ebaby": {
                "status": profile["applications"]["ebaby"]["status"]
            },
            "eopyy": {
                "status": profile["applications"]["eopyy"]["status"]
            },
            "e_prescription": {
                "status": profile["applications"]["e_prescription"]["status"]
            },
            "diavgeia": {
                "status": profile["applications"]["diavgeia"]["status"]
            },
            "e_services": {
                "status": profile["applications"]["e_services"]["status"]
            },
            "dypethessaly": {
                "status": profile["applications"]["dypethessaly"]["status"]
            }
        }
    }
    return s_data

def terminate_all_processes(profile_name):
    """
        Terminates all the applications initiated by the API and the processes 
        they spawned.

        The function is called by the stop_profile() function.

        Firstly the applications are terminated and then asklipios/LIS and the persona.
        After each termination the profiles dictionary is updated accordingly.

        The condition for an app to be terminated is that the corresponding
        "status" attribute in the profiles dictionary has the value: "running".
        Child processes are terminated recursively and then followed by the termination of
        the parent process.

        IMPORTANT: For the persona termination a temporary kill_persona.txt is being
        created in order to store the PIDs of the processes spawned. When the session is 
        either terminated via the API or the timeout funcionality the PIDs are being 
        fetched, stored in a list and the file deleted. 
        This is a workaround to handle the PIDs spawned out of the flask framework
        and has been tested both in windows and linux environments.

    """
    # terminate the applications running and the processes they spawned
    if "Linux" in platform.platform():
        logging.info("(Terminating apps)Operating System Linux detected")
        for app in profiles[profile_name]["applications"].keys():
            if profiles[profile_name]["applications"][app]["status"] == "running":
                parent = psutil.Process(profiles[profile_name]["applications"][app]["PID"].pid)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()

            profiles[profile_name]["applications"][app]["status"] = "not running"
            profiles[profile_name]["applications"][app]["PID"] = None
            profiles[profile_name]["applications"][app]["duration_list"] = None
            profiles[profile_name]["applications"][app]["interarrivals_list"] = None

    else:
        logging.info("(Terminating apps)Operating System Windows detected")
        try:
            for app in profiles[profile_name]["applications"].keys():
                if profiles[profile_name]["applications"][app]["status"] == "running":
                    parent = psutil.Process(profiles[profile_name]["applications"][app]["PID"].pid)
                    for child in parent.children(recursive=True):
                        child.kill()
                    parent.kill() 

                profiles[profile_name]["applications"][app]["status"] = "not running"
                profiles[profile_name]["applications"][app]["PID"] = None
                profiles[profile_name]["applications"][app]["duration_list"] = None
                profiles[profile_name]["applications"][app]["interarrivals_list"] = None


        except Exception as e:
            logging.info("Some processes are already dead")
            logging.info("Windows handling the issue..") 

    profiles[profile_name]["applications"][app]["status"] = "not running"
    profiles[profile_name]["applications"][app]["PID"] = None
    profiles[profile_name]["applications"][app]["duration_list"] = None
    profiles[profile_name]["applications"][app]["interarrivals_list"] = None

    # terminate asklipios_LIS
    if profiles[profile_name]["asklipios_LIS"]["PID"] != None:
        parent = psutil.Process(profiles[profile_name]["asklipios_LIS"]["PID"].pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()

        profiles[profile_name]["asklipios_LIS"]["PID"] = None
        profiles[profile_name]["asklipios_LIS"]["status"] = "not running"

    # terminate persona
    if profiles[profile_name]["persona"]["PID"] != None:
    
        try:
            file = open("kill_persona.txt", "r")
            p_list = file.readlines()
            file.close()
            os.remove("kill_persona.txt")

        except Exception as e:
            print("Could not open/create file: kill_persona.txt")
            return -1

        for p in p_list:
            os.kill(int(p.rstrip("\n")), 9)

        if "Linux" in platform.platform():
            parent = psutil.Process(profiles[profile_name]["persona"]["PID"].pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
            logging.info("(persona)Operating System Linux detected")
        else:
            logging.info("(persona)Operating System Windows detected")

        if "Linux" in platform.platform():
            for file in glob.glob('persona/sphinxuser_*.json'):
                if file != 'persona/sphinxuser_0000.json':
                    os.remove(file)
        else:
            for file in glob.glob('persona/sphinxuser_*'):
                if file != 'persona/sphinxuser_0000':
                    os.remove(file)

        profiles[profile_name]["persona"]["PID"] = None
        profiles[profile_name]["persona"]["status"] = "not running"

def timeout(app, profile_name, total_duration):
    """
        Initiates the stop_profile function after the timer runs out

        To simplify things the timer is a while loop decrementing the total_duration
        parameter.

        If the profile has been already stopped (via the stop profile functionality 
        of the API, a simple GET request) the timer is stopped.

        :param:         app:                the flask app
        :param:         profile_name:       name of the profile to be stopped  
        :param:         total_duration:     time in seconds before the profile timeout   
    """
    with app.app_context():
        while total_duration:
            time.sleep(1)
            total_duration -= 1
            profiles[profile_name]["time_remaining"] = total_duration

            if profiles[profile_name]["status"] == "not running":
                profiles[profile_name]["time_remaining"] = None
                logging.info("Timer stopped!")
                return 0
   
        try:
            stop_profile(profile_name)
            logging.info(f"Profile {profile_name}: timeout triggered")
        except Exception as e:
            logging.info(f"Error with timeout function. Error: {e}")



def read_profile(profile_name):
    """
        This function responds to a GET request for /api/profiles/{profile_name}
        with the matching profile from the profiles dict.

        Before the profile is returned the create_serialazable_data function
        reprocesses the profile dict to keep private part of the data (PIDs etc)

        If the profile is not found 404 and an according message is returned.

        :param      profile_name:    name of the profile to find
        :return:    profile returned after being processed by the 
                    create_serialazable_data function.
        :return:    404 on error
    """
    if profile_name in profiles:
        profile = profiles[profile_name]

    else:
        abort(
            404, f"Profile {profile_name} not found"
        )

    return create_serialazable_data(profile)


def read_all():
    """
        This function responds to a GET request for /api/profiles
        with the list of all available profiles

        :return:        all the profiles returned in alphabetical order after 
                        being processed by the create_serialazable_data function.
    """
    return [create_serialazable_data(profiles[key]) for key in sorted(profiles.keys())]


def start_custom_profile(body):

    """
        This function responds to a POST request for /api/profiles/start_custom_profile
        with the initiation of the given custom profile.

        The custom profile info is provided via the API.

        ###############################################################################

        Example of input for the API:

        {
            "asklipios_LIS": {
                "enabled": false
            },
            "persona": {
                "enabled": false
            },
            "apps": {
                "facebook": {
                    "duration_list": "20, 53",
                    "interarrivals_list": "2,2"
                },
                "youtube": {
                    "duration_list": "20, 5",
                    "interarrivals_list": "2,2"
                },
                "apografi_http": {
                    "duration_list": "20, 5",
                    "interarrivals_list": "2,2"
                }
            },
            "total_duration": 300
        }

        Example of input with no apps initiated:

        {
            "asklipios_LIS": {
                "enabled": true
            },
            "persona": {
                "enabled": false
            },
            "apps": {
                
            },
            "total_duration": 50
        }

        ###############################################################################

        --total_duration is in SECONDS!

        --duration_list and interarrivals_list must be of string type 
          with the showcased format eg: "20, 5"
          The 2 lists must also have the same length.

        --ATTENTION! "asklipios_LIS" and "persona" attributes with their "enabled"
        attribute, as well "apps" and "total_duration" must ALWAYS be present!

        --"enabled" can be true or false (NO "" present!)
    
        ###############################################################################

        Asklipios/LIS and persona are configured via their config files:
        --asklipios_LIS/LIS_config.txt
        --persona/persona_config.txt

        ###############################################################################

        :param :     body:              input passed via the API
        :return:     200 on success 
        :return:     400 on error "Profile {profile_name} already running"
        :return:     500 on all other errors 
    """
    profile_name = "Custom_Profile"

    if profiles[profile_name]["status"] == "running":
        abort(
                400, f"Profile {profile_name} already running"
            )

    profiles[profile_name]["request_body"] = body
    profiles[profile_name]["status"] = "running"
    profiles[profile_name]["total_duration"] = body["total_duration"]
    profiles[profile_name]["time_remaining"] = body["total_duration"]
    profiles[profile_name]["started_running"] = get_timestamp()

    app = current_app._get_current_object()
    t = threading.Thread(target=timeout, args=(app, profile_name, body['total_duration']))
    t.start()

    for app in body["apps"].keys():
        try:
            p = Process(target=profiles[profile_name]["applications"][app]["function"], 
                       args=(body["apps"][app]["duration_list"], 
                            body["apps"][app]["interarrivals_list"],
                            profiles[profile_name]["applications"][app]["url"])
                       )
            p.start()

            profiles[profile_name]["applications"][app]["status"] = "running"
            profiles[profile_name]["applications"][app]["PID"] = p
            profiles[profile_name]["applications"][app]["duration_list"] = body["apps"][app]["duration_list"]
            profiles[profile_name]["applications"][app]["interarrivals_list"] = body["apps"][app]["interarrivals_list"]

        except Exception as e:
            stop_profile(profile_name)
            abort(
                500, f"Profile {profile_name} coudn't start: {e}. Error with process: {profiles[profile_name]['applications'][app]}."
            )
            
    if body["asklipios_LIS"]["enabled"]:
        try:
            p = Process(target=profiles[profile_name]["asklipios_LIS"]["function"],
                        args=() )
            p.start()

            profiles[profile_name]["asklipios_LIS"]["PID"] = p
            profiles[profile_name]["asklipios_LIS"]["status"] = "running"
        except Exception as e:
            stop_profile(profile_name)
            abort(
                500, f"Profile {profile_name} coudn't start: {e}. Error with asklipios_LIS"
            )

    if body["persona"]["enabled"]:
        try:
            p = Process(target=profiles[profile_name]["persona"]["function"],
                        args=() )
            p.start()

            profiles[profile_name]["persona"]["PID"] = p
            profiles[profile_name]["persona"]["status"] = "running"
        except Exception as e:
            stop_profile(profile_name)
            abort(
                500, f"Profile {profile_name} coudn't start: {e}. Error with persona"
            )

    return make_response(
            f"{profile_name} successfully created with duration: {body['total_duration']}", 200
            )


def start_quick_profile():

    """
        This function responds to a GET request for /api/profiles/start_quick_profile
        with the initiation of the given  quick profile

        ###############################################################################
        ATTENTION! To configure the Quick Profile make appropriate changes in
        the quick_profile_config.json

        --For Asklipios/LIS and persona set "enabled" to true or false. No "" needed!!

        --To NOT use an app set it's "sessions" to 0.

        --To use an app set number of sessions as an integer.
          Set the TOTAL duration time of all the sessions.
          Set the TOTAL duration time duration of all the interarrivals.

        --total_duration is in SECONDS! total_duration sets a timeout timer that when
          ends terminates all processes.

        ###############################################################################
        :param:      profile_name:      name of the profile to start
        :return:     200 on success 
        :return:     400 on error "Profile {profile_name} already running"
        :return:     500 on all other errors 
    """
    profile_name = "Quick_Profile"

    if profiles[profile_name]["status"] == "running":
        abort(
                400, f"Profile {profile_name} already running"
            )

    config_quick_profile()

    profiles[profile_name]["status"] = "running"
    profiles[profile_name]["started_running"] = get_timestamp()

    app = current_app._get_current_object()
    t = threading.Thread(target=timeout, args=(app, profile_name, profiles[profile_name]["total_duration"]))
    t.start()

    for app in profiles[profile_name]["applications"].keys():
        try:
            if profiles[profile_name]["applications"][app]["duration_list"] != '':
                p = Process(target=profiles[profile_name]["applications"][app]["function"], 
                           args=(profiles[profile_name]["applications"][app]["duration_list"], 
                                profiles[profile_name]["applications"][app]["interarrivals_list"],
                                profiles[profile_name]["applications"][app]["url"])
                           )
                p.start()

                profiles[profile_name]["applications"][app]["status"] = "running"
                profiles[profile_name]["applications"][app]["PID"] = p

        except Exception as e:
            stop_profile(profile_name)
            abort(
                500, f"Profile {profile_name} coudn't start: {e}. Error with process: {profiles[profile_name]['applications'][app]}."
            )
            
    if profiles[profile_name]["asklipios_LIS"]["enabled"]:
        try:
            p = Process(target=profiles[profile_name]["asklipios_LIS"]["function"],
                        args=() )
            p.start()

            profiles[profile_name]["asklipios_LIS"]["PID"] = p
            profiles[profile_name]["asklipios_LIS"]["status"] = "running"
        except Exception as e:
            stop_profile(profile_name)
            abort(
                500, f"Profile {profile_name} coudn't start: {e}. Error with asklipios_LIS"
            )

    if profiles[profile_name]["persona"]["enabled"]:
        try:
            p = Process(target=profiles[profile_name]["persona"]["function"],
                        args=() )
            p.start()

            profiles[profile_name]["persona"]["PID"] = p
            profiles[profile_name]["persona"]["status"] = "running"
        except Exception as e:
            stop_profile(profile_name)
            abort(
                500, f"Profile {profile_name} coudn't start: {e}. Error with persona"
            )

    return make_response(
            f"{profile_name} successfully created with duration: {profiles[profile_name]['total_duration']}", 200
            )

def stop_profile(profile_name):
    """
        This function responds to a GET request for /api/profiles/{profile_name}/stop
        with the termination of the given profile.

        :param:         profile_name:       name of the profile to be terminated
        :return:        200 on success
        :return:        400 on error profile doesn't exist or profile already stopped.
    """
    if profile_name not in profiles.keys():
        abort(
                400, f"Profile {profile_name} doesn't exist."
            )
    elif profiles[profile_name]["status"] == "not running":
        abort(
                400, f"Profile {profile_name}  is already stopped."
            )
    else:
        terminate_all_processes(profile_name)

    profiles[profile_name]["status"] = "not running"
    profiles[profile_name]["total_duration"] = None
    profiles[profile_name]["started_running"] = None
    profiles[profile_name]["request_body"] = None
    profiles[profile_name]["time_remaining"] = None

    logging.info(f"Profile {profile_name} ended")

    return make_response(
            f"{profile_name} successfully stopped", 200
            )
