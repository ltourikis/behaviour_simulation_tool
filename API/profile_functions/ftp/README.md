# FTP hijacking

    python3 ftp_sniffer.py

This script activates a sniffer waiting for ftp credentials towards the port defined in config.yml. The interface is also selected there. After credentials are captured a connection is attempted automatically against the ftp server. using ftp.py from the parent directory. The scripts then terminates.

Please take care of possible sudo permissions required for sniffing. In order to maintain venv packages with sudo try the following:
    
    sudo path/to/venv/bin/python ftp_sniffer.py

The requirements here are additive to the root folders' requirements.