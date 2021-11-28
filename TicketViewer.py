import requests
import configparser
from os.path import exists
import json

# Global parameters
config = configparser.ConfigParser()
url = ""
username = ""
apiToken = ""
ticketsArray = []


# Ticket class to easily store individual Ticket information
class Ticket:
    def __init__(self, requesterID, assigneeID, subject, description, tags):
        self.requesterID = requesterID
        self.assigneeID = assigneeID
        self.subject = subject
        self.description = description
        self.tags = tags

    def get_requesterID(self):
        return self.requesterID

    def get_assigneeID(self):
        return self.assigneeID

    def get_subject(self):
        return self.subject

    def get_description(self):
        return self.description

    def get_tags(self):
        return self.tags


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


# Populates global array with Ticket objects
def populate_ticket_array(data):
    global ticketsArray
    # Creates Ticket objects with the data from the tickets table in the data response
    for t in range(len(data["tickets"])):
        ticketsArray.append(Ticket(data["tickets"][t]["requester_id"],
                                   data["tickets"][t]["assignee_id"],
                                   data["tickets"][t]["subject"],
                                   data["tickets"][t]["description"],
                                   data["tickets"][t]["tags"]))


# Functionality for controlling ticket table view
def print_ticket_table():
    print("Tickets for user: " + config.get("USERINFORMATION", "Username"))


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
        print('Status:', response.status_code, 'Problem with the request, config file may have errors. If needed, '
                                               'you can delete the config.ini file and run the program again to '
                                               'generate a new config.ini. Exiting.')
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()

    populate_ticket_array(data)

    print_ticket_table()


# Runs main function
main()
