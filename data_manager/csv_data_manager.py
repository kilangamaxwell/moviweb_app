import csv
import json
from data_manager.data_manager_interface import DataManagerInterface


class CSVDataManager(DataManagerInterface):
    """A data manager that interacts with a CSV file."""

    def __init__(self, filename):
        """
        Initialize the CSVDataManager.

        Args:
            filename (str): The filename of the CSV file.
        """
        self.filename = filename

    def get_all_users(self):
        """
        Retrieve all users from the CSV file.

        Returns:
            list: A list of dictionaries representing the users.
        """
        try:
            with open(self.filename, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                users = [row for row in reader]
            return users
        except FileNotFoundError:
            return []  # Return an empty list if the file is not found
        except csv.Error as e:
            # Return the specific CSV error message
            return f"CSV Error: {str(e)}"

    def save_db(self, data):
        """
        Save the data to the CSV file.

        Args:
            data (list): The data to be saved.

        Returns:
            bool: True if the data was saved successfully, False otherwise.
        """
        try:
            with open(self.filename, "w", newline="") as csvfile:
                fieldnames = data[0].keys() if data else []
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
                return True
        except IOError:
            return False  # Return False if there is an IO error while saving the data

    def get_user_movies(self, user_id):
        """
        Retrieve the movies of a specific user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: A dictionary representing the movies of the user.
        """
        try:
            users = self.get_all_users()
            for user in users:
                if user["id"] == user_id:
                    return user.get("movies", {})
            return {}
        except KeyError:
            return f"KeyError: User ID {user_id} not found"

    def add_user_movie(self, user_id, name, director, year, rating, poster):
        """
        Add a movie to a user's list of movies.

        Args:
            user_id (str): The ID of the user.
            name (str): The name of the movie.
            director (str): The director of the movie.
            year (str): The year of the movie.
            rating (str): The rating of the movie.
            poster (str): The url to the movie's poster

        Returns:
            list: The updated list of movies for the user.
        """
        try:
            users = self.get_all_users()
            for user in users:
                if user["id"] == user_id:
                    movies = user.get("movies", [])
                    movie_id = max([int(movie["id"])
                                    for movie in movies], default=0) + 1
                    movie = {
                        "id": str(movie_id),
                        "name": name,
                        "director": director,
                        "year": year,
                        "rating": rating,
                        'poster': poster
                    }
                    movies.append(movie)
                    user["movies"] = movies
                    self.save_db(users)
                    return movies
            return []
        except KeyError:
            return f"KeyError: User ID {user_id} not found"

    def delete_user_movie(self, user_id, movie_id):
        """
        Delete a movie from a user's list of movies.

        Args:
            user_id (str): The ID of the user.
            movie_id (str): The ID of the movie to be deleted.

        Returns:
            bool: True if the movie was deleted successfully, False otherwise.
        """
        try:
            users = self.get_all_users()
            for user in users:
                if user["id"] == user_id:
                    movies = user.get("movies", [])
                    for movie in movies:
                        if movie["id"] == movie_id:
                            movies.remove(movie)
                            self.save_db(users)
                            return True
            return False
        except KeyError:
            return f"KeyError: User ID {user_id} not found"

    def update_user_movie(self, user_id, movie_id, updated_movie):
        """
        Update a movie in a user's list of movies.

        Args:
            user_id (str): The ID of the user.
            movie_id (str): The ID of the movie to be updated.
            updated_movie (dict): The updated movie information.

        Returns:
            bool: True if the movie was updated successfully, False otherwise.
        """
        try:
            users = self.get_all_users()
            for user in users:
                if user["id"] == user_id:
                    movies = user.get("movies", [])
                    for movie in movies:
                        if movie["id"] == movie_id:
                            movie.update(updated_movie)
                            self.save_db(users)
                            return True
            return False
        except KeyError:
            return f"KeyError: User ID {user_id} not found"

    def get_movie_details(self, movie_id):
        """
        Retrieve the details of a specific movie.

        Args:
            movie_id (str): The ID of the movie.

        Returns:
            dict: A dictionary representing the movie details.
        """
        try:
            users = self.get_all_users()
            for user in users:
                movies = user.get("movies", [])
                for movie in movies:
                    if movie["id"] == movie_id:
                        return movie
            return None
        except KeyError:
            return f"KeyError: Movie ID {movie_id} not found"

    def get_users_with_movie(self, movie_id):
        """
        Retrieve a list of user IDs that have a specific movie.

        Args:
            movie_id (str): The ID of the movie.

        Returns:
            list: A list of user IDs.
        """
        try:
            users = self.get_all_users()
            user_list = []
            for user in users:
                movies = user.get("movies", [])
                for movie in movies:
                    if movie["id"] == movie_id:
                        user_list.append(int(user["id"]))
            return user_list
        except KeyError:
            return f"KeyError: Movie ID {movie_id} not found"

    def get_users_by_name(self, name):
        """
        Retrieve a list of user IDs that have a specific name.

        Args:
            name (str): The name to search for.

        Returns:
            list: A list of user IDs.
        """
        try:
            users = self.get_all_users()
            user_list = []
            for user in users:
                if user.get("name") == name:
                    user_list.append(int(user["id"]))
            return user_list
        except KeyError:
            return f"KeyError: Name {name} not found"

    def get_top_rated_movies(self, n):
        """
        Retrieve the top-rated movies.

        Args:
            n (int): The number of movies to retrieve.

        Returns:
            list: A list of top-rated movies.
        """
        try:
            users = self.get_all_users()
            all_movies = []
            for user in users:
                movies = user.get("movies", [])
                all_movies.extend(movies)

            top_rated_movies = sorted(
                all_movies, key=lambda x: x["rating"], reverse=True)[:n]
            return top_rated_movies
        except KeyError:
            return "KeyError: Error retrieving top-rated movies"

    def get_movie_count_per_year(self):
        """
        Retrieve the movie count per year.

        Returns:
            dict: A dictionary with movie counts per year.
        """
        try:
            users = self.get_all_users()
            movie_count_per_year = {}
            for user in users:
                movies = user.get("movies", [])
                for movie in movies:
                    year = movie.get("year")
                    if year in movie_count_per_year:
                        movie_count_per_year[year] += 1
                    else:
                        movie_count_per_year[year] = 1
            return movie_count_per_year
        except KeyError:
            return "KeyError: Error retrieving movie count per year"

    def get_user_by_id(self, user_id):
        """
        Retrieve a user by ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: A dictionary representing the user.
        """
        try:
            users = self.get_all_users()
            for user in users:
                if user["id"] == user_id:
                    return user
            return None
        except KeyError:
            return f"KeyError: User ID {user_id} not found"

    def add_user(self, name):
        """
        Add a new user.

        Args:
            name (str): The name of the user.

        Returns:
            bool: True if the user was added successfully, False otherwise.
        """
        try:
            users = self.get_all_users()
            user_id = max([int(user["id"]) for user in users], default=0) + 1
            new_user = {
                "id": str(user_id),
                "name": name,
                "movies": []
            }
            users.append(new_user)
            self.save_db(users)
            return True
        except KeyError:
            return f"KeyError: Error adding user"

    def create_movie_list(self):
        """
        Create a list of movies based on the provided JSON data.


        Returns:
            list: A list of dictionaries representing movies, with each dictionary
                containing movie details such as ID, name, director, year, rating,
                and the user's name.
        """
        movie_list = []
        users = self.get_all_users()
        for user in users:
            user_id = user['id']
            name = user['name']
            movies = user.get('movies', [])
            for movie in movies:
                movie_id = movie['id']
                movie = {
                    'name': movie['name'],
                    'director': movie['director'],
                    'year': int(movie['year']),
                    'rating': float(movie['rating']),
                    'poster': movie['poster']
                }
                if movie not in movie_list:
                    movie_list.append(movie)

        return movie_list
