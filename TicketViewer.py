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
    ticketsArray.clear()
    # Creates Ticket objects with the data from the tickets table in the data response
    for t in range(len(data["tickets"])):
        ticketsArray.append(Ticket(data["tickets"][t]["requester_id"],
                                   data["tickets"][t]["assignee_id"],
                                   data["tickets"][t]["subject"],
                                   data["tickets"][t]["description"],
                                   data["tickets"][t]["tags"]))


# Prints table of current tickets (ticket numbers start at i + 1)
def print_ticket_table():
    global ticketsArray

    # Prints head of table
    print("Ticket No.".ljust(16) + "Requester ID".ljust(20) + "Assignee ID".ljust(20) + "Subject".ljust(
        80) + "Tags".ljust(20))
    print("-------------".ljust(16) +
          "-----------------".ljust(20) +
          "-----------------".ljust(20) +
          "----------------------------------------------------------------------------".ljust(80) +
          "----------------------------------".ljust(20))

    # Prints information in tickets in a table format
    for i in range(len(ticketsArray)):
        print(str(i + 1).ljust(16) +
              str(ticketsArray[i].get_requesterID()).ljust(20) +
              str(ticketsArray[i].get_assigneeID()).ljust(20) +
              str(ticketsArray[i].get_subject()).ljust(80) +
              str(ticketsArray[i].get_tags()).ljust(20))


# Controls ticket list view
def ticket_list_control():
    userInput = ""
    currentPage = 1

    # HTTP get request
    responseParameters = {"per_page": "25", "page": currentPage}
    response = requests.get(url, auth=(username, apiToken), params=responseParameters)

    while userInput != "exit":
        print("\n**** Tickets for user: " + config.get("USERINFORMATION", "Username") + " ****\n"
              "Current page: " + str(currentPage))

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print("Status:", response.status_code, "Problem with the request, config file may have errors. If needed, "
                                                   "you can delete the config.ini file and run the program again to "
                                                   "generate a new config.ini. Exiting.")
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()

        populate_ticket_array(data)

        print_ticket_table()

        print("\nControls:\n"
              "'q':\t\t\t\tPrevious page\n"
              "'e':\t\t\t\tNext page\n"
              "Any number 1-25:\tOpen ticket at specified number (seen in 'Ticket No.' column\n"
              "'exit':\t\t\t\tExits the program\n")

        userInput = input()
        # Previous page
        if userInput.lower() == "q":
            if data["previous_page"] is not None:
                # Decrements page number
                currentPage -= 1
                responseParametersUpdate = {"page": currentPage}
                responseParameters.update(responseParametersUpdate)
                # Updates response
                response = requests.get(url, auth=(username, apiToken), params=responseParameters)
            else:
                print("Error: No previous page!")
        # Next page
        elif userInput.lower() == "e":
            if data["next_page"] is not None:
                # Increments page number
                currentPage += 1
                responseParametersUpdate = {"page": currentPage}
                responseParameters.update(responseParametersUpdate)
                # Updates response
                response = requests.get(url, auth=(username, apiToken), params=responseParameters)
            else:
                print("Error: No next page!")
        # Select a ticket
        elif isinstance(userInput, int) and 0 < userInput < len(data):
            print("PLACEHOLDER FOR TICKET SELECTION FUNCTION")
        # Exit
        elif userInput == "exit":
            print("Thank you for using my ticket viewer. Exiting...")
            exit()
        else:
            print("Error: Invalid input!")


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

    ticket_list_control()


# Runs main function
main()
