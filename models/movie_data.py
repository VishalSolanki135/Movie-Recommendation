class MovieData:
    def __init__(self, title=None, description=None):
        self.title = title
        self.description = description
    
    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description