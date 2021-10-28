## Setup

### 1. Run the following command on your desired directory:
    git clone https://github.com/ltourikis/behaviour_simulation_tool 
			
### 2. Install python (version 3.6.9 or later)
	
### 3.Install the necessary python modules contained in the requirements.txt
#### On a windows pc run:
    pip install -r requirements.txt
#### On a linux distro run:
    pip3 install -r requirements.txt

### 4.Install the latest versions of Firefox and Chrome Browsers
	 
### 5.Download the corresponding drivers of the aforementioned browsers (chromedriver and geckodriver) on a directory that is included in the PATH enviromental variable.
	   
### 6.Set the IP and port that the server is listening to, by modifying the following line in the config final line API/server_config.json
    "HOST": "0.0.0.0"
	   		
### 7.Start the server.
#### On a windows pc run:
    python API/server.py
	   		 
#### On a linux distro run:
    python3 API/server.py
