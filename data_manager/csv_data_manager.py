import csv
from data_manager_interface import DataManagerInterface


class CSVDataManager(DataManagerInterface):
    def __init__(self, filename) -> None:
        self.filename = filename

    def get_all_users(self):
        users = {}
        with open(self.filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = int(row["user_id"])
                if user_id not in users:
                    users[user_id] = {
                        "name": row["name"],
                        "movies": {}
                    }
                movies = users[user_id]["movies"]
                movie_id = int(row["movie_id"])
                movie = {
                    "name": row["movie_name"],
                    "director": row["director"],
                    "year": int(row["year"]),
                    "rating": float(row["rating"])
                }
                movies[movie_id] = movie
        return users

    def save_db(self, users):
        with open(self.filename, "w", newline="") as csvfile:
            fieldnames = ["user_id", "name", "movie_id",
                          "movie_name", "director", "year", "rating"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user_id, user_data in users.items():
                name = user_data["name"]
                movies = user_data["movies"]
                for movie_id, movie in movies.items():
                    writer.writerow({
                        "user_id": user_id,
                        "name": name,
                        "movie_id": movie_id,
                        "movie_name": movie["name"],
                        "director": movie["director"],
                        "year": movie["year"],
                        "rating": movie["rating"]
                    })

    def get_user_movies(self, user_id):
        users = self.get_all_users()
        return users.get(user_id, {}).get("movies", {})

    def add_user_movie(self, user_id, name, director, year, rating):
        users = self.get_all_users()
        user = users.get(user_id, {})
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
        users[user_id] = user

        self.save_db(users)

        return movies

    def delete_user_movie(self, user_id, movie_id):
        users = self.get_all_users()
        user = users.get(user_id, {})
        movies = user.get("movies", {})

        if movie_id in movies:
            del movies[movie_id]
            user["movies"] = movies
            users[user_id] = user
            self.save_db(users)
            return True

        return False

    def update_user_movie(self, user_id, movie_id, updated_movie):
        users = self.get_all_users()
        user = users.get(user_id, {})
        movies = user.get("movies", {})

        if movie_id in movies:
            movies[movie_id].update(updated_movie)
            user["movies"] = movies
            users[user_id] = user
            self.save_db(users)
            return True

        return False

    def get_movie_details(self, movie_id):
        users = self.get_all_users()
        for user_data in users.values():
            movies = user_data.get("movies", {})
            movie = movies.get(movie_id)
            if movie:
                return movie
        return None

    def get_users_with_movie(self, movie_id):
        users = self.get_all_users()
        user_list = []
        for user_id, user_data in users.items():
            movies = user_data.get("movies", {})
            if movie_id in movies:
                user_list.append(user_id)
        return user_list

    def get_users_by_name(self, name):
        users = self.get_all_users()
        user_list = []
        for user_id, user_data in users.items():
            if user_data.get("name") == name:
                user_list.append(user_id)
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
        return users.get(user_id)
