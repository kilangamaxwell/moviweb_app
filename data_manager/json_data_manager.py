from data_manager_interface import DataManagerInterface
import json


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename) -> None:
        self.filename = filename

    def get_all_users(self):
        with open(self.filename, "r") as jfile:
            users = json.load(jfile)
        return users

    def save_db(self, data):
        with open(self.filename, "w") as jfile:
            json.dump(data, jfile, indent=4)

    def get_user_movies(self, user_id):
        users = self.get_all_users()
        return users.get(str(user_id), {}).get("movies", {})

    def add_user_movie(self, user_id, name, director, year, rating):
        users = self.get_all_users()
        user = users.get(str(user_id), {})
        movies = user.get("movies", {})

        movie_id = max(movies.keys(), default=0) + 1
        movie = {
            'name': name,
            'director': director,
            'year': year,
            'rating': rating
        }
        movies[movie_id] = movie

        user["movies"] = movies
        users[str(user_id)] = user

        self.save_db(users)

        return movies

    def delete_user_movie(self, user_id, movie_id):
        users = self.get_all_users()
        user = users.get(str(user_id), {})
        movies = user.get("movies", {})

        if str(movie_id) in movies:
            del movies[str(movie_id)]
            user["movies"] = movies
            users[str(user_id)] = user
            self.save_db(users)
            return True

        return False

    def update_user_movie(self, user_id, movie_id, updated_movie):
        users = self.get_all_users()
        user = users.get(str(user_id), {})
        movies = user.get("movies", {})

        if str(movie_id) in movies:
            movies[str(movie_id)].update(updated_movie)
            user["movies"] = movies
            users[str(user_id)] = user
            self.save_db(users)
            return True

        return False

    def get_movie_details(self, movie_id):
        users = self.get_all_users()
        for user_data in users.values():
            movies = user_data.get("movies", {})
            movie = movies.get(str(movie_id))
            if movie:
                return movie
        return None

    def get_users_with_movie(self, movie_id):
        users = self.get_all_users()
        user_list = []
        for user_id, user_data in users.items():
            movies = user_data.get("movies", {})
            if str(movie_id) in movies:
                user_list.append(int(user_id))
        return user_list

    def get_users_by_name(self, name):
        users = self.get_all_users()
        user_list = []
        for user_id, user_data in users.items():
            if user_data.get("name") == name:
                user_list.append(int(user_id))
        return user_list

    def get_top_rated_movies(self, n):
        users = self.get_all_users()
        all_movies = []
        for user_data in users.values():
            movies = user_data.get("movies", {})
            all_movies.extend(movies.values())

        top_rated_movies = sorted(
            all_movies, key=lambda x: x["rating"], reverse=True)[:n]
        return top_rated_movies

    def get_movie_count_per_year(self):
        users = self.get_all_users()
        movie_count_per_year = {}
        for user_data in users.values():
            movies = user_data.get("movies", {})
            for movie in movies.values():
                year = movie.get("year")
                if year in movie_count_per_year:
                    movie_count_per_year[year] += 1
                else:
                    movie_count_per_year[year] = 1
        return movie_count_per_year

    def get_user_by_id(self, user_id):
        users = self.get_all_users()
        return users.get(str(user_id))
