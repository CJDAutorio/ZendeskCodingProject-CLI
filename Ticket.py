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
