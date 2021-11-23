import requests
import configparser
from os.path import exists

# Global parameters
url = "https://zccstudents9591.zendesk.com/api/v2/groups.json"
username = ""
apiToken = ""


# Create config file
def create_config():
    config = configparser.ConfigParser()
    config["USERINFORMATION"] = {
        "Username": "",
        "API Token": ""
    }
    with open("config.ini", "w") as configfile:
        config.write(configfile)


# Main function of program
def main():
    # Check if ini file exists. If not, create ini file
    if not exists("config.ini"):
        create_config()
        print("Config file not found! Config file has been created at program root. Please enter your information"
              "into the file config.ini and relaunch the program.")


# Runs main function
main()
