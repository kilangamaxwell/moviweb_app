from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user_movie(self, user_id, name, director, year, rating):
        pass

    @abstractmethod
    def delete_user_movie(self, user_id, movie_id):
        pass

    @abstractmethod
    def update_user_movie(self, user_id, movie_id, updated_movie):
        pass

    @abstractmethod
    def get_movie_details(self, movie_id):
        pass

    @abstractmethod
    def get_users_with_movie(self, movie_id):
        pass

    @abstractmethod
    def get_users_by_name(self, name):
        pass

    @abstractmethod
    def get_top_rated_movies(self, n):
        pass

    @abstractmethod
    def get_movie_count_per_year(self):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def add_user(self, name):
        pass
