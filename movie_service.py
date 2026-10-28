import math
from pathlib import Path

from models.movie import Movie
from models.movie_data import MovieData
from models.movie_match import MovieMatch

class MovieService:
    def __init__(self, embedding_model, json_mapper):
        self.embedding_model = embedding_model
        self.json_mapper = json_mapper
        self.moviesEmbedding = []
    
    def initializeMovies(self):
        resource = (
            Path(__file__).resolve().parent
            / "resources"
            / "movies.json"
        )

        input_stream = resource.open("r", encoding="utf-8")

        movie_data_list = [
            MovieData(movie_data["title"], movie_data["description"])
            for movie_data in self.json_mapper.load(input_stream)
        ]

        for movie_data in movie_data_list:
            embedding = self.embedding_model.embed(
                movie_data.getDescription()
            )

            movie = Movie(
                movie_data.getTitle(),
                movie_data.getDescription(),
                embedding
            )

            self.moviesEmbedding.append(movie)
        
        input_stream.close()

        print(
            str(len(self.moviesEmbedding))
            + " movies loaded with embeddings."
        )

    def search(self, query):
        user_query_embedding = self.embedding_model.embed(query)

        matches = []

        for movie in self.moviesEmbedding:
            similarity = self.cosineSimilarity(
                user_query_embedding,
                movie.getEmbedding()
            )

            match = MovieMatch(
                movie.getTitle(),
                movie.getDescription(),
                similarity
            )

            matches.append(match)
        
        self.sortBySimilarity(matches)

        return self.topKMatches(matches, 3)
    
    def similarMovies(self, title):
        selected_movie = self.findMovie(title)
        matches = []

        for movie in self.moviesEmbedding:
            if movie.getTitle().lower() == title.lower():
                continue
            similarity = self.cosineSimilarity(
                selected_movie.getEmbedding(),
                movie.getEmbedding()
            )

            match = MovieMatch(
                movie.getTitle(),
                movie.getDescription(),
                similarity
            )

            matches.append(match)
        
        self.sortBySimilarity(matches)
        return self.topKMatches(matches, 3)
    
    def findMovie(self, title):
        for movie in self.moviesEmbedding:
            if movie.getTitle().lower() == title.lower():
                return movie
        raise ValueError(f"Movie not found: {title}")
    
    def cosineSimilarity(self, a, b):
        dot_product = 0.0
        norm_a = 0.0
        norm_b = 0.0

        for i in range(len(a)):
            dot_product += a[i] * b[i]
            norm_a += a[i] * a[i]
            norm_b += b[i] * b[i]
        
        if(norm_a == 0 or norm_b == 0):
            return 0.0
        
        return dot_product / (math.sqrt(norm_a) * math.sqrt(norm_b))
    
    def sortBySimilarity(self, matches):
        matches.sort(key=lambda movie:movie.getMatch(), reverse=True)
    
    def topKMatches(self, matches, limit):
        top_matches = []
        number_of_matches = min(limit, len(matches))

        for i in range(number_of_matches):
            top_matches.append(matches[i])
        
        return top_matches
