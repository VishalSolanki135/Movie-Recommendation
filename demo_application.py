import json

from movie_controller import MovieController
from movie_service import MovieService

class DemoApplication:
    # static method doesn't need any self or cls argument because it doesnt modify or alter any data of instance or class. 
    # It organize related utility functions inside a class without creating objects
    @staticmethod
    def main(embedding_model):
        json_mapper = json
        movieService = MovieService(embedding_model, json_mapper)
        movieService.initializeMovies()
        return MovieController(movieService)