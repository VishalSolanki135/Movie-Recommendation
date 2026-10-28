class MovieController:
    # constructor of a class and it is used to initialize the class variables
    # it gets automatically called when an object of the class is created
    def __init__(self, movie_service): 
        self.movie_service = movie_service
    def search(self, query):
        return self.movie_service.search(query)
    def similar_movies(self, title):
        return self.movie_service.similarMovies(title)