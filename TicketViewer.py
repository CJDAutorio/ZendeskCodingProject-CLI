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
    def __init__(self, requesterID, assigneeID, subject, description, tags, createdAt, updatedAt, priority, status, ticketID):
        self.requesterID = requesterID
        self.assigneeID = assigneeID
        self.subject = subject
        self.description = description
        self.tags = tags
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.priority = priority
        self.status = status
        self.ticketID = ticketID

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

    def get_createdAt(self):
        return self.createdAt

    def get_updatedAt(self):
        return self.updatedAt

    def get_priority(self):
        return self.priority

    def get_status(self):
        return self.status

    def get_ticketID(self):
        return self.ticketID


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
                                   data["tickets"][t]["tags"],
                                   data["tickets"][t]["created_at"],
                                   data["tickets"][t]["updated_at"],
                                   data["tickets"][t]["priority"],
                                   data["tickets"][t]["status"],
                                   data["tickets"][t]["id"]))


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


def ticket_view(ticketIndex):
    global ticketsArray
    ticket = ticketsArray[ticketIndex]
    print("\n*** Ticket View ***")
    print("ID: " + str(ticket.get_ticketID()).ljust(10) + "Priority: " + str(ticket.get_priority()))
    print("Requester ID: " + str(ticket.get_requesterID()).ljust(20) + "Assignee ID: " + str(ticket.get_assigneeID()))
    print("Subject: " + ticket.get_subject().ljust(80) + "Tags: " + str(ticket.get_tags()))
    print("\nDescription:\n" + ticket.get_description() + "\n")
    print("Created at: " + str(ticket.get_createdAt()).ljust(30) + "Updated at: " + str(ticket.get_updatedAt()))
    input("\nPress enter to return to the ticket list.")


# Controls ticket list view
def ticket_list_control():
    userInput = ""
    currentPage = 1

    print("\nLoading ticket list...\n")

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
              "'q':\tPrevious page\n"
              "'e':\tNext page\n"
              "'s':\tOpen ticket at specified number (seen in 'Ticket No.' column)\n"
              "'exit':\tExits the program\n")

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
        elif userInput.lower() == "s":
            print("Ticket number:")
            selectTicketNumber = input()
            if 0 < int(selectTicketNumber) < len(ticketsArray) + 1:
                ticket_view(int(selectTicketNumber) - 1)
            else:
                print("Error: Invalid ticket number!")
        # Exit
        elif userInput.lower() == "exit":
            print("Thank you for using my ticket viewer. Exiting...")
            exit()
        else:
            print("Error: Invalid input!")

        print("\nLoading ticket list...\n")


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
