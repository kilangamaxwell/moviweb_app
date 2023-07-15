from flask import Flask, jsonify, render_template, request, url_for, redirect
from data_manager.json_data_manager import JSONDataManager
import requests

API_KEY = "d4ba49c2"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="

app = Flask(__name__)
data_manager = JSONDataManager('users.json')


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)
    if user:
        movies = data_manager.get_user_movies(user_id)
        return render_template('user_movies.html', user=user, movies=movies, user_id=user_id), 201
    return "User not found"


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        if data_manager.add_user(name):
            return redirect(url_for('list_users'))
        return "User ID already exists"
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    user = data_manager.get_user_by_id(user_id)
    if user:
        if request.method == 'POST':
            name = request.form['name']
            director = request.form['director']
            year = int(request.form['year'])
            rating = float(request.form['rating'])
            data_manager.add_user_movie(
                str(user_id), name, director, year, rating)
            return redirect(url_for('user_movies', user_id=user_id))
        return render_template('add_movie.html', user=user, user_id=user_id)
    return "User not found"


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user = data_manager.get_user_by_id(user_id)
    if user:
        movies = data_manager.get_user_movies(user_id)
        if str(movie_id) in movies:
            db_movie = movies[str(movie_id)]
            title = db_movie["name"]
            movie = find_movie_in_api(title)
            if request.method == 'POST':
                name = request.form['name']
                director = request.form['director']
                year = int(request.form['year'])
                rating = float(request.form['rating'])
                updated_movie = {
                    'name': name,
                    'director': director,
                    'year': year,
                    'rating': rating
                }
                data_manager.update_user_movie(
                    user_id, str(movie_id), updated_movie)
                return redirect(url_for('user_movies', user_id=user_id))
            return render_template('update_movie.html', user=user, movie=movie, user_id=user_id, movie_id=movie_id)
    return "User or movie not found"


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    user = data_manager.get_user_by_id(user_id)
    if user:
        movies = data_manager.get_user_movies(user_id)
        if movie_id in movies:
            data_manager.delete_user_movie(user_id, movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    return "User or movie not found"


def find_movie_in_api(title):
    """Retrieve movie info from the OMDB API.

    Args:
        title (str): The title of the movie to search for.

    Returns:
        dict: The movie data retrieved from the API as a dictionary.
    """
    response = requests.get(URL+title)
    try:
        response = requests.get(URL+title)
        response.raise_for_status()  # Raises an HTTPError for 4xx and 5xx status codes
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
    if response.status_code == requests.codes.ok:
        data = response.json()
    return data


if __name__ == '__main__':
    app.run(debug=True)
