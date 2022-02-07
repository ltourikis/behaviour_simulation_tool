import ftplib
hostname = '10.10.2.62'
port = 31001
user = 'edge'
passwd = 'edge'

# Connect to ftp1.at.proftpd.org
session = ftplib.FTP()

# Print the welcome message.
# print(session.getwelcome())

# Login
session.connect(hostname, port)
session.login(user=user, passwd=passwd)
wdir = session.pwd()
print(wdir)