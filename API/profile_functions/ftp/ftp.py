import ftplib
import time
import os
import yaml

# get config variables
with open(os.path.join((os.path.sep).join(os.path.realpath(__file__).split(os.path.sep)[:-1]), "config.yml"), "r") as ymlfile:
    config = yaml.safe_load(ymlfile)

hostname = str(config['server']['hostname'])
port = int(config['server']['port'])
user = str(config['client']['user'])
passwd = str(config['client']['passwd'])

def ftp_client(hostname, port, user=None, passwd=None):
    try:
        # Connect to server
        print("Initiating session with the following info: \n")
        print(f"Hostname: {hostname}\nPort: {port}\nUser: {user}\nPassword: {passwd}")
        session = ftplib.FTP()

        # Print the welcome message.
        # print(session.getwelcome())

        # Login
        print("Connecting...")
        session.connect(hostname, port)
        print("Logging in...")
        session.login(user=user, passwd=passwd)

        # The dir() method produces a directory listing and adds the data to the list.
        # files = []
        # session.dir(files.append)
        # print(files)

        # Get welcome
        print(f"Welcome message: {session.getwelcome()}")
        # Get the working directory
        print(f"Current working directory is: {session.pwd()}")
        

        # # File to download
        # file_orig = 'README.MIRRORS'

        # # # File to upload
        ftp_folder = os.path.dirname(os.path.realpath(__file__))
        file = open(os.path.join(ftp_folder, 'gotcha.png'), 'rb')
        # Send file
        print('Uploading file...\n')
        session.storbinary('STOR gotcha.png', file)     
        file.close()                                 

        # close session
        print('Quiting FTP session...\n')
        session.quit()

    except ftplib.all_errors as e:
        print('FTP error:', e)

def ftp_loop(hostname=hostname, port=port, user=user, passwd=passwd):
    while True:
        print(f"Attempting to connect to {hostname} ...")
        ftp_client(hostname=hostname, port=port, user=user, passwd=passwd)
        # ftp_client()
        time.sleep(5)

if __name__ == '__main__':
    ftp_loop()
 
