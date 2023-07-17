# Project Title

MovieWeb App

## Description

The MovieWeb App is a Flask-based web application that allows users to manage their movie collection. Users can view a list of movies, add new movies, update existing movies, and delete movies from their collection. The application retrieves movie data from the OMDB API.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/movieweb-app.git
   ```

2. Navigate to the project directory:

   ```
   cd movieweb-app
   ```

3. Create a virtual environment:

   ```
   python -m venv venv
   ```

4. Activate the virtual environment:

   - For Windows:
     ```
     venv\Scripts\activate
     ```
   - For macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

6. Set up the database:

   - Make sure you have SQLite installed on your system.
   - Create a new SQLite database file named `database.db`.

7. Run the application:

   ```
   python app.py
   ```

8. Open your web browser and navigate to `http://localhost:5000` to access the MovieWeb App.

## Usage

- Home Page: Displays a list of all movies in the database.
- User Listing: Shows all registered users.
- User Movies: Displays the movies associated with a specific user.
- Add User: Allows the addition of a new user.
- Add Movie: Lets users add a new movie to their collection.
- Update Movie: Allows users to update information about a movie.
- Delete Movie: Enables users to delete a movie from their collection.

## API Integration

The application integrates with the OMDB API to retrieve movie data. It uses an API key to access the OMDB API. The base URL for the API is `http://www.omdbapi.com/`.

## Credits

The MovieWeb App is developed by Robert Maxwell(https://github.com/krmaxwell88).

## Future Modifications

User Authentication and User Profiles will be added to the project in future updates.
