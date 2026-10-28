class MovieMatch:
    def __init__(self, title=None, description=None, match=0.0):
        self.title = title
        self.description = description
        self.match = match

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    def getMatch(self):
        return self.match

    def setMatch(self, match):
        self.match = match