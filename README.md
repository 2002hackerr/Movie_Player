# Movie Player Program

This Python program allows you to manage a collection of directors and their movies, with the added functionality of fetching data from IMDb. It offers various operations, including adding, updating, deleting, and listing directors and their movies, as well as playing movies and fetching data from IMDb. The program stores its data in a JSON file for persistent storage between sessions.

## Features

- **Manage Directors**: Add, update, delete, and list directors.
- **Manage Movies**: Add, update, delete, and list movies associated with directors.
- **IMDb Integration**: Fetch movie and director details directly from IMDb.
- **Data Persistence**: All data is stored in a `movies_data.json` file for later use.
- **Play Movie**: Simulate playing a movie by printing its title and director.

## IMDb Integration Key Features

The Movie Player offers seamless integration with IMDb using the IMDbPY library, allowing you to fetch up-to-date information about movies and directors directly from IMDb:

1. **Fetch Director's Filmography**: Search for a director by name and retrieve their entire filmography of directed movies.
2. **Fetch Movie Details**: Search for a movie by title and retrieve detailed information, including:
   - Movie title
   - Runtime
   - IMDb rating
   - Director's name
   - IMDb URL link to the movie
3. **Automatic Data Formatting**: Data fetched from IMDb is automatically formatted into a readable JSON format for easy understanding and optional saving.
4. **Error Handling**: Handles errors such as missing data on IMDb or network issues and logs them for debugging.
5. **Optional Data Saving**: Results can be optionally saved to a file (`imdb_results.json`) for future reference.
6. **Flexible Search**: Supports both director-based and movie-based searches from IMDb.

## Requirements

To run the program, you need:

- Python 3.x
- IMDbPY library

## Installation

1. **Clone the repository** or download the script file.
2. Install the necessary dependencies:

    ```bash
    pip install imdbpy
    ```

3. Make sure that Python 3 is installed on your system. You can check this by running:

    ```bash
    python --version
    ```

## How to Run the Program

1. Navigate to the directory where the script is located.
2. Run the program using Python:

    ```bash
    python movie_player.py
    ```

3. The program will start with a menu offering various options.

## Usage

Once the program is running, you can use the menu to interact with the Movie Player. Below are the available options:

### Menu Options:

1. **List Directors**: Lists all the directors currently stored in the database.
2. **Add Director**: Adds a new director by specifying the director's name.
3. **Update Director**: Updates the name of an existing director.
4. **Delete Director**: Removes a director and all associated movies from the database.
5. **List Movies**: Lists all the movies under a specified director.
6. **Add Movie**: Adds a movie to a specific director's collection.
7. **Update Movie**: Updates an existing movie's title and runtime.
8. **Delete Movie**: Deletes a movie from a director's collection.
9. **Play Movie**: Simulates playing a movie by printing its title and director.
10. **Fetch Data from IMDb**: Fetches data from IMDb for a specific director or movie, and optionally saves it to a file.
11. **Exit**: Exits the program.

### Example Commands:

- To **add a director**:  
  Select option `2` and enter the director's name.

- To **add a movie**:  
  Select option `6`, enter the director's name, movie title, and runtime.

- To **fetch movie details from IMDb**:  
  Select option `10`, choose `Fetch by Movie`, and enter the movie title.

## Data Storage

All data is stored in a file named `movies_data.json` in the same directory as the script. This file is automatically created the first time the program runs and is used to save directors and movies for future sessions.

## Logging

Errors and important events are logged in `app.log`, which is also stored in the same directory.

## IMDb Integration

The program uses the IMDbPY library to fetch data from IMDb. You can retrieve information about directors or movies, such as filmography, runtime, rating, and more. The data can also be saved to a file (`imdb_results.json`).

## Error Handling

Common issues such as invalid JSON, missing directors or movies, and IMDb fetch errors are handled gracefully and logged into `app.log`.

## Contributing

If you'd like to contribute to the program, feel free to fork the repository and submit a pull request.

## License

This project is open source and available under the MIT License.
