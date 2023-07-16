import json
from data_manager.data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    """A data manager that interacts with a JSON file."""

    def __init__(self, filename) -> None:
        """
        Initialize the JSONDataManager.

        Args:
            filename (str): The filename of the JSON file.
        """
        self.filename = filename

    def get_all_users(self):
        """
        Retrieve all users from the JSON file.

        Returns:
            dict: A dictionary representing the users.
        """
        try:
            with open(self.filename, "r") as jfile:
                users = json.load(jfile)
            return users
        except FileNotFoundError:
            # Handle the exception when the file is not found
            return {"Error: File Not Found"}
        except json.JSONDecodeError:
            # Handle the exception when there is an error decoding JSON data
            return {"JSONDecodeError: An error occurred while reading the file."}

    def save_db(self, data):
        """
        Save the data to the JSON file.

        Args:
            data (dict): The data to be saved.

        Returns:
            bool: True if the data was saved successfully, False otherwise.
        """
        try:
            with open(self.filename, "w") as jfile:
                json.dump(data, jfile, indent=4)
                return True
        except IOError:
            # Handle the exception when there is an IO error while saving the data
            return {"IOError: An error occurred while writing to the file."}

    def get_user_movies(self, user_id):
        """
        Retrieve the movies of a specific user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: A dictionary representing the movies of the user.
        """
        users = self.get_all_users()
        return users.get(str(user_id), {}).get("movies", {})

    def add_user_movie(self, user_id, name, director, year, rating, poster):
        """
        Add a movie to a user's list of movies.

        Args:
            user_id (str): The ID of the user.
            name (str): The name of the movie.
            director (str): The director of the movie.
            year (str): The year of the movie.
            rating (str): The rating of the movie.
            poster (str): The url to the movie's poster from OMDB

        Returns:
            dict: The updated list of movies for the user.
        """
        try:
            users = self.get_all_users()
            user = users.get(str(user_id), {})
            movies = user.get("movies", {})

            movie_id = max(
                map(lambda item: (int(item[0])), movies.keys()), default=0) + 1
            movie = {
                'name': name,
                'director': director,
                'year': year,
                'rating': rating,
                'poster': poster
            }
            movies[movie_id] = movie

            user["movies"] = movies
            users[str(user_id)] = user

            self.save_db(users)

            return movies
        except KeyError:
            # Handle the exception when the specified key is not found
            return {"KeyError: Key not found in the dictionary."}

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
            user = users.get(str(user_id), {})
            movies = user.get("movies", {})

            if str(movie_id) in movies:
                del movies[str(movie_id)]
                user["movies"] = movies
                users[str(user_id)] = user
                self.save_db(users)
                return True

            return False
        except KeyError:
            # Handle the exception when the specified key is not found
            print("KeyError: Key not found in the dictionary.")
            return False

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
            user = users.get(str(user_id), {})
            movies = user.get("movies", {})

            if str(movie_id) in movies:
                movies[str(movie_id)].update(updated_movie)
                user["movies"] = movies
                users[str(user_id)] = user
                self.save_db(users)
                return True

            return False
        except KeyError:
            # Handle the exception when the specified key is not found
            print("KeyError: Key not present in the dictionary.")
            return False

    def get_movie_details(self, movie_id):
        """
        Retrieve the details of a specific movie.

        Args:
            movie_id (str): The ID of the movie.

        Returns:
            dict: A dictionary representing the movie details.
        """
        users = self.get_all_users()
        for user_data in users.values():
            movies = user_data.get("movies", {})
            movie = movies.get(str(movie_id))
            if movie:
                return movie
        return None

    def get_users_with_movie(self, movie_id):
        """
        Retrieve a list of user IDs that have a specific movie.

        Args:
            movie_id (str): The ID of the movie.

        Returns:
            list: A list of user IDs.
        """
        users = self.get_all_users()
        user_list = []
        for user_id, user_data in users.items():
            movies = user_data.get("movies", {})
            if str(movie_id) in movies:
                user_list.append(int(user_id))
        return user_list

    def get_users_by_name(self, name):
        """
        Retrieve a list of user IDs that have a specific name.

        Args:
            name (str): The name of the user.

        Returns:
            list: A list of user IDs.
        """
        users = self.get_all_users()
        user_list = []
        for user_id, user_data in users.items():
            if user_data.get("name") == name:
                user_list.append(int(user_id))
        return user_list

    def get_top_rated_movies(self, n):
        """
        Retrieve the top-rated movies.

        Args:
            n (int): The number of movies to retrieve.

        Returns:
            list: A list of top-rated movies.
        """
        users = self.get_all_users()
        all_movies = []
        for user_data in users.values():
            movies = user_data.get("movies", {})
            all_movies.extend(movies.values())

        top_rated_movies = sorted(
            all_movies, key=lambda x: x["rating"], reverse=True)[:n]
        return top_rated_movies

    def get_movie_count_per_year(self):
        """
        Retrieve the movie count per year.

        Returns:
            dict: A dictionary with movie counts per year.
        """
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
        """
        Retrieve a user by ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            dict: A dictionary representing the user.
        """
        users = self.get_all_users()
        return users.get(str(user_id))

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
            user_id = max(map(lambda item: int(item),
                          users.keys()), default=0) + 1
            users[str(user_id)] = {
                "name": name,
                "movies": {}
            }
            self.save_db(users)
            return True
        except KeyError:
            # Handle the exception when the specified key is not found
            print("KeyError: Key not present in the dictionary.")
            return False

    def create_movie_list(self):
        """
        Create a list of movies based on the provided JSON data.

        Args:
            json_data (dict): The JSON data containing user and movie information.

        Returns:
            list: A list of dictionaries representing movies, with each dictionary
                containing movie details such as ID, name, director, year, rating,
                and the user's name.
        """
        movie_list = []
        movies_db = self.get_all_users()
        for user_id, user_data in movies_db.items():
            name = user_data['name']
            movies = user_data['movies']
            for movie_id, movie_data in movies.items():
                movie = {
                    'name': movie_data['name'],
                    'director': movie_data['director'],
                    'year': movie_data['year'],
                    'rating': movie_data['rating'],
                    'poster': movie_data['poster']
                }
                if movie not in movie_list:
                    movie_list.append(movie)
        return movie_list
