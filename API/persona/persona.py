import logging
import json
import sys
import os
import subprocess
import platform

# configure logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

def create_users(number_of_users, variability_amount_list, period_list):

    # read the template sphinxuser_0000.json
    try:
        file = open(os.path.join(sys.path[0], "persona/sphinxuser_0000.json"), "r")

    except Exception as e:
        logging.info("Could not open/read file: sphinxuser_0000.json")
        return -1

    template = json.load(file)
    file.close()

    user_list = []

    #print(range(number_of_users), variability_amount_list, period_list)
    for (user, va, p) in zip(range(number_of_users), variability_amount_list, period_list):
        name = password = template['user']['username'][:-4] + str(f"{(user + 1):04d}")
        file_name = name + ".json"

        user_list.append(file_name)

        try:
            file = open("persona/" + file_name, "w")

        except Exception as e:
            logging.info(f"Could not open/create file: {file_name}")
            return -1

        template['user']['username'] = name
        template['user']['password'] = password
        template['variability_amount'] = str(va)
        template['period'] = str(p)
        
        json.dump(template, file)
        file.close()

    return user_list

def run_the_scripts(user_list):
    p_list =[]

    try:
        for user in user_list:
            if "Linux" in platform.platform():
                bashCommand = f"python3 persona/personsim_v2.py persona/settings_sphinx.json persona/{user}"
                logging.info("Operating System Linux detected")
            else:
                bashCommand = f"python persona/personsim_v2.py persona/settings_sphinx.json persona/{user}"
                logging.info("Operating System Windows detected")
                
            process = subprocess.Popen(bashCommand.split())
            p_list.append(process)
            logging.info(f"(persona)Running: {bashCommand}")

        logging.info("(persona)Initiated the simulations successfully")
    except Exception as e:
        logging.info(f"(persona)Problem creating {user}")
        logging.info(e)
        return -1

    return p_list

def persona():

    # delete if it exists from previous session. 
    # (keeping the directory clean)

    if os.path.exists("kill_persona.txt"):
        os.remove("kill_persona.txt")
        logging.info("(persona) Deleted old file: kill_persona.txt")

    # read the configuration
    try:
        file = open(os.path.join(sys.path[0], "persona/persona_config.json"), "r")
        #file = open(os.path.join(sys.path[0], "persona_config.txt"), "r")

    except Exception as e:
        logging.info("Could not open/read file: persona_config.json")
        return -1

    config = json.load(file)
    file.close()

    number_of_users = config["number_of_users"]
    logging.info(f"(persona)Number of users created {number_of_users}")

    variability_list = config["variability_list"]
    logging.info(f"(persona)Variability amount list: {variability_list}")
    
    period_list = config["period_list"]
    logging.info(f"(persona)Period list: {period_list}")

    # Create the users
    logging.info("(persona)Creating users..")
    user_list = create_users(number_of_users, variability_list, period_list)

    # Run the persona_sim.py 
    p_list = run_the_scripts(user_list)

    try:
        file = open("kill_persona.txt", "w")
        for p in p_list:
            file.write(str(p.pid)+ "\n")

        file.close()

    except Exception as e:
        logging.info(f"Could not open/create file: kill_persona.txt")
        return -1

if __name__ == '__main__':
    persona()
