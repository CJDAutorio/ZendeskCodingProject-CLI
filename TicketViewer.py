import requests
import configparser
from os.path import exists
import json

# Global parameters
config = configparser.ConfigParser()
url = ""
username = ""
apiToken = ""


# Reads config file
def read_config():
    config.read("config.ini")
    global url, username, apiToken
    url = config.get("USERINFORMATION", "URL")
    username = config.get("USERINFORMATION", "Username") + "/token"
    apiToken = config.get("USERINFORMATION", "API Token")


# Create config file
def create_config():
    config["USERINFORMATION"] = {
        "URL": "",
        "Username": "",
        "API Token": ""
    }
    with open("config.ini", "w") as configfile:
        config.write(configfile)


# Main function of program
def main():
    # If no config file exists, create config.ini and end program. Else, read config and continue
    if not exists("config.ini"):
        create_config()
        print("Config file not found! Config file has been created at program root. Please enter your information"
              "into the file config.ini and relaunch the program.")
        exit()
    else:
        read_config()

    # HTTP get request
    response = requests.get(url, auth=(username, apiToken))

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()


# Runs main function
main()
