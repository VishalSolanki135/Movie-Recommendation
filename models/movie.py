class Movie:
    def __init__(self, title=None, description=None, embedding=None):
        self.title = title
        self.description = description
        self.embedding = embedding
    
    def getTitle(self):
        return self.title
    def setTitle(self, title):
        self.title = title
    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description

    def getEmbedding(self):
        return self.embedding

    def setEmbedding(self, embedding):
        self.embedding = embedding