from flask import Flask, jsonify, render_template, request, url_for, redirect
from data_manager.json_data_manager import JSONDataManager
import requests

API_KEY = "d4ba49c2"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="

app = Flask(__name__)
data_manager = JSONDataManager('users.json')


@app.route('/')
def home():
    """
    Home page route.

    Returns:
        list: List of all movies in the database
    """
    # Create the movie_list
    movie_list = data_manager.create_movie_list()
    return render_template('movie_list.html', movies=movie_list)


@app.route('/users')
def list_users():
    """
    Route for listing all users.

    Returns:
        str: A rendered template with user data.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    """
    Route for displaying a user's movies.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: A rendered template with user and movie data.
    """
    user = data_manager.get_user_by_id(user_id)
    if user:
        movies = data_manager.get_user_movies(user_id)
        return render_template('user_movies.html', user=user, movies=movies, user_id=user_id), 201
    return "User not found"


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Route for adding a new user.

    Returns:
        str: A rendered template for adding a user or a redirect to the list of users.
    """
    if request.method == 'POST':
        name = request.form['name']
        if data_manager.add_user(name):
            return redirect(url_for('list_users'))
        return "User ID already exists"
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Route for adding a movie to a user's list.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: A rendered template for adding a movie or a redirect to the user's movie list.
    """
    user = data_manager.get_user_by_id(user_id)
    if user:
        if request.method == 'POST':
            name = request.form['name']
            director = request.form['director']
            year = int(request.form['year'])
            rating = float(request.form['rating'])
            poster = find_movie_in_api(name)["Poster"]
            data_manager.add_user_movie(
                str(user_id), name, director, year, rating, poster)
            return redirect(url_for('user_movies', user_id=user_id))
        return render_template('add_movie.html', user=user, user_id=user_id)
    return "User not found"


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Route for updating a movie in a user's list.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie to be updated.

    Returns:
        str: A rendered template for updating a movie or an error message if user or movie not found.
    """
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
                poster = request.form['poster']
                updated_movie = {
                    'name': name,
                    'director': director,
                    'year': year,
                    'rating': rating,
                    'poster': poster
                }
                data_manager.update_user_movie(
                    user_id, str(movie_id), updated_movie)
                return redirect(url_for('user_movies', user_id=user_id))
            return render_template('update_movie.html', user=user, movie=movie, user_id=user_id, movie_id=movie_id)
    return "User or movie not found"


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    """
    Route for deleting a movie from a user's list.

    Args:
        user_id (str): The ID of the user.
        movie_id (str): The ID of the movie to be deleted.

    Returns:
        str: A redirect to the user's movie list or an error message if user or movie not found.
    """
    user = data_manager.get_user_by_id(user_id)
    if user:
        movies = data_manager.get_user_movies(user_id)
        if movie_id in movies:
            data_manager.delete_user_movie(user_id, movie_id)
        return redirect(url_for('user_movies', user_id=user_id))
    return "User or movie not found"


def find_movie_in_api(title):
    """
    Retrieve movie info from the OMDB API.

    Args:
        title (str): The title of the movie to search for.

    Returns:
        dict: The movie data retrieved from the API as a dictionary.
    """
    try:
        response = requests.get(URL+title)
        response.raise_for_status()  # Raises an HTTPError for 4xx and 5xx status codes
        if response.status_code == requests.codes.ok:
            data = response.json()
            return data
    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Something went wrong: {err}"


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(502)
def bad_gateway(e):
    return render_template('502.html'), 502


@app.errorhandler(503)
def service_unavailable(e):
    return render_template('503.html'), 503


@app.errorhandler(504)
def gateway_timeout(e):
    return render_template('504.html'), 504


if __name__ == '__main__':
    app.run(debug=True)
