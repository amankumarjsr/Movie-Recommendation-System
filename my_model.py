import pickle
import requests


class model:
    def __init__(self):
        self.movies = pickle.load(open("movie_list.pkl", "rb"))
        self.similarity = pickle.load(open("similarity.pkl", "rb"))

    # --- fetching the poster image for the recommended movies
    def fetch_poster(self, movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=a8e6a37659062d28e92b8a5ff3ece6f8&language=en-US".format(
            movie_id
        )
        data = requests.get(url)
        data = data.json()
        poster_path = data["poster_path"]
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path

    def recommend(self, movie):
        index = self.movies[self.movies["title"] == movie].index[0]
        distances = sorted(
            list(enumerate(self.similarity[index])), reverse=True, key=lambda x: x[1]
        )
        recommended_movie_names = []
        recommended_movie_posters = []
        movie_codes = []
        model1 = model()
        for i in distances[1:6]:
            # fetch the movie poster
            movie_id = self.movies.iloc[i[0]].id
            recommended_movie_posters.append(model1.fetch_poster(movie_id))
            recommended_movie_names.append(self.movies.iloc[i[0]].title)
            movie_codes.append(movie_id)
        return recommended_movie_names, recommended_movie_posters, movie_codes
