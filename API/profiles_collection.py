from profile_functions.youtube.youtube import youtube
from profile_functions.facebook.facebook import facebook
from profile_functions.google.google import google
from profile_functions.outlook.outlook import outlook
from profile_functions.generic_browsing.generic_browsing import generic_browsing
from asklipios_LIS.asklipios_LIS import asklipios_LIS
from persona.persona import persona

"""
    Dictionary containing the profiles

    Two profiles are available as of right now:
        - Custom Profile
        - Quick_Profile

    Both support the persona and the asklipios/LIS functionalities
    as well as various applications.
    
    This dictionary is handled by the API and acts as a mini database.
    Values should NOT be changed manually unless a new application/feature is 
    supported!
"""

profiles = {
    "Custom_Profile": {
        "profile_name": "Custom_Profile",
        "status": "not running",
        "total_duration": None,
        "time_remaining": None,
        "started_running": None,
        "request_body": None,
        "persona": {
            "function": persona,
            "PID": None,
            "status": "not running"
        },
        "asklipios_LIS": {
            "function": asklipios_LIS,
            "PID": None,
            "status": "not running"
        },
        "applications": {
            "google": {
                "function": google,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": None
            },
            "youtube": {
                "function": youtube,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": None
            },
            "outlook": {
                "function": outlook,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": None
            },
            "galinos": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.galinos.gr/"
            },
            "promitheus": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "http://www.eprocurement.gov.gr"
            },
            "facebook": {
                "function": facebook,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": None
            },
            "apografi_http": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "http://apografi.gov.gr/"            
            },
            "gsis": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.gsis.gr"            
            },
            "idika": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.idika.gr"            
            }, 
            "ebaby": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://ebaby.ypes.gr/"            
            },
            "eopyy": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.eopyy.gov.gr"            
            },
            "e_prescription": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.e-prescription.gr"            
            },
            "diavgeia": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.diavgeia.gov.gr"            
            },
            "e_services": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://eservices.yeka.gr/"            
            },
            "dypethessaly": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.dypethessaly.gr"            
            }
        }
    },
    "Quick_Profile": {
        "profile_name": "Quick_Profile",
        "status": "not running",
        "total_duration": None,
        "time_remaining": None,
        "started_running": None,
        "request_body": None,
        "persona": {
            "enabled": False,
            "function": persona,
            "PID": None,
            "status": "not running"
        },
        "asklipios_LIS": {
            "enabled": False,
            "function": asklipios_LIS,
            "PID": None,
            "status": "not running"
        },
        "applications": {
            "google": {
                "function": google,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": None
            },
            "youtube": {
                "function": youtube,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": None
            },
            "outlook": {
                "function": outlook,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": None
            },
            "galinos": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.galinos.gr/"
            },
            "promitheus": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "http://www.eprocurement.gov.gr"
            },
            "facebook": {
                "function": facebook,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": None
            },
            "apografi_http": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "http://apografi.gov.gr/"            
            },
            "gsis": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.gsis.gr"            
            },
            "idika": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.idika.gr"            
            }, 
            "ebaby": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://ebaby.ypes.gr/"            
            },
            "eopyy": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.eopyy.gov.gr"            
            },
            "e_prescription": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.e-prescription.gr"            
            },
            "diavgeia": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.diavgeia.gov.gr"            
            },
            "e_services": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://eservices.yeka.gr/"            
            },
            "dypethessaly": {
                "function": generic_browsing,
                "PID": None,
                "status": "not running",
                "duration_list": None,
                "interarrivals_list": None,
                "url": "https://www.dypethessaly.gr"            
            },
        }
    }
}
