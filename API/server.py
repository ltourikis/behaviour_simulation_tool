"""
Main module of the server file
"""

import os
import sys
import logging
import json

# 3rd party modules
import connexion

# configure logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")


# Open the server_config.json that contains the host IP
try:
    
    file = open(os.path.join(sys.path[0], "server_config.json"), "r")

except Exception as e:
    logging.info("Could not open/read file: server_config")
    sys.exit(-1)

config = json.load(file)
file.close()

host = config["HOST"]
logging.info(f"HOST IP = {host}")

# create the application instance
app = connexion.App(__name__, specification_dir="./")

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger.yml")

if __name__ == "__main__":
    app.run(host=host,debug=True)

