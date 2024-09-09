import json
import imdb
import logging
import os

# Set up logging
logging.basicConfig(filename='app.log', level=logging.ERROR)

# IMDb instance
ia = imdb.IMDb()

# Class Definitions
class Movie:
    def __init__(self, title, runtime):
        self.title = title
        self.runtime = runtime

    def to_dict(self):
        return {
            'title': self.title,
            'runtime': self.runtime
        }


class Director:
    def __init__(self, name):
        self.name = name
        self.movies = []

    def add_movie(self, movie):
        self.movies.append(movie)

    def remove_movie(self, title):
        self.movies = [movie for movie in self.movies if movie.title != title]

    def to_dict(self):
        return {
            'name': self.name,
            'movies': [movie.to_dict() for movie in self.movies]
        }


class MoviePlayer:
    def __init__(self, data_file='movies_data.json'):
        self.directors = []
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    # Ensure data is a dictionary with 'directors' key
                    if isinstance(data, dict) and 'directors' in data:
                        for director_data in data['directors']:
                            director = Director(director_data['name'])
                            for movie_data in director_data['movies']:
                                movie = Movie(movie_data['title'], movie_data['runtime'])
                                director.add_movie(movie)
                            self.directors.append(director)
                    else:
                        print("Error: Data format is incorrect.")
                        logging.error("Error: Data format is incorrect.")
            else:
                print("No data file found. Starting with an empty database.")
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")
            logging.error(f"Error reading JSON file: {e}")

    def save_data(self):
        data = {'directors': [director.to_dict() for director in self.directors]}
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def list_directors(self):
        if not self.directors:
            print("No directors found.")
        for idx, director in enumerate(self.directors, 1):
            print(f"{idx}. {director.name}")

    def add_director(self, name):
        self.directors.append(Director(name))
        self.save_data()
        print(f"Director '{name}' added.")

    def update_director(self, old_name, new_name):
        for director in self.directors:
            if director.name == old_name:
                director.name = new_name
                self.save_data()
                print(f"Director '{old_name}' updated to '{new_name}'.")
                return
        print(f"Director '{old_name}' not found.")

    def delete_director(self, name):
        self.directors = [director for director in self.directors if director.name != name]
        self.save_data()
        print(f"Director '{name}' and all associated movies deleted.")

    def list_movies(self, director_name):
        for director in self.directors:
            if director.name == director_name:
                if not director.movies:
                    print(f"No movies found for director '{director_name}'.")
                for idx, movie in enumerate(director.movies, 1):
                    print(f"{idx}. {movie.title} ({movie.runtime})")
                return
        print(f"Director '{director_name}' not found.")

    def add_movie(self, director_name, movie_title, runtime):
        for director in self.directors:
            if director.name == director_name:
                director.add_movie(Movie(movie_title, runtime))
                self.save_data()
                print(f"Movie '{movie_title}' added under director '{director_name}'.")
                return
        print(f"Director '{director_name}' not found.")

    def update_movie(self, director_name, old_title, new_title, new_runtime):
        for director in self.directors:
            if director.name == director_name:
                for movie in director.movies:
                    if movie.title == old_title:
                        movie.title = new_title
                        movie.runtime = new_runtime
                        self.save_data()
                        print(f"Movie '{old_title}' updated to '{new_title}' ({new_runtime}).")
                        return
        print(f"Movie '{old_title}' under director '{director_name}' not found.")

    def delete_movie(self, director_name, title):
        for director in self.directors:
            if director.name == director_name:
                director.remove_movie(title)
                self.save_data()
                print(f"Movie '{title}' deleted from director '{director_name}'.")
                return
        print(f"Movie '{title}' under director '{director_name}' not found.")

    def play_movie(self, director_name, title):
        for director in self.directors:
            if director.name == director_name:
                for movie in director.movies:
                    if movie.title == title:
                        print(f"Now Playing: '{title}' directed by {director_name}.")
                        return
        print(f"Movie '{title}' under director '{director_name}' not found.")

    def fetch_data_from_imdb(self, director_name=None, movie_title=None, save_to_file=False):
        results = []
        try:
            if director_name:
                search_results = ia.search_person(director_name)
                if search_results:
                    director = search_results[0]
                    person = ia.get_person(director.personID, info='filmography')
                    movies = [movie['title'] for movie in person.get('filmography', {}).get('director', [])]
                    results.append({"type": "director", "name": director_name, "movies": movies})
                else:
                    results.append({"type": "director", "name": director_name, "error": "Not found on IMDb."})

            if movie_title:
                search_results = ia.search_movie(movie_title)
                if search_results:
                    movie = search_results[0]
                    movie_info = ia.get_movie(movie.movieID)

                    title = movie_info.get('title', 'Unknown')
                    runtime = movie_info.get('runtimes', ['Unknown'])[0]
                    rating = movie_info.get('rating', 'N/A')
                    imdb_url = f"https://www.imdb.com/title/tt{movie.movieID}/"

                    directors = [director['name'] for director in movie_info.get('directors', [])]
                    director_name = directors[0] if directors else 'Unknown'

                    results.append({
                        "type": "movie",
                        "title": title,
                        "runtime": runtime,
                        "rating": rating,
                        "director": director_name,
                        "imdb_url": imdb_url
                    })
                else:
                    results.append({"type": "movie", "title": movie_title, "error": "Not found on IMDb."})

        except Exception as e:
            results.append({"error": f"An error occurred: {e}"})
            logging.error(f"An error occurred while fetching data from IMDb: {e}")

        if save_to_file:
            with open('imdb_results.json', 'a') as file:
                for result in results:
                    file.write(json.dumps(result) + "\n")
            print("Results appended to 'imdb_results.json'.")

        for result in results:
            print(json.dumps(result, indent=4))

    def menu(self):
        while True:
            print("\nMovie Player Menu:")
            print("1. List Directors")
            print("2. Add Director")
            print("3. Update Director")
            print("4. Delete Director")
            print("5. List Movies")
            print("6. Add Movie")
            print("7. Update Movie")
            print("8. Delete Movie")
            print("9. Play Movie")
            print("10. Fetch Data from IMDb")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.list_directors()
            elif choice == '2':
                name = input("Enter director name: ")
                self.add_director(name)
            elif choice == '3':
                old_name = input("Enter current director name: ")
                new_name = input("Enter new director name: ")
                self.update_director(old_name, new_name)
            elif choice == '4':
                name = input("Enter director name to delete: ")
                self.delete_director(name)
            elif choice == '5':
                director_name = input("Enter director name to list movies: ")
                self.list_movies(director_name)
            elif choice == '6':
                director_name = input("Enter director name: ")
                movie_title = input("Enter movie title: ")
                runtime = input("Enter movie runtime (e.g., '120 minutes'): ")
                self.add_movie(director_name, movie_title, runtime)
            elif choice == '7':
                director_name = input("Enter director name: ")
                old_title = input("Enter current movie title: ")
                new_title = input("Enter new movie title: ")
                new_runtime = input("Enter new runtime (e.g., '120 minutes'): ")
                self.update_movie(director_name, old_title, new_title, new_runtime)
            elif choice == '8':
                director_name = input("Enter director name: ")
                title = input("Enter movie title to delete: ")
                self.delete_movie(director_name, title)
            elif choice == '9':
                director_name = input("Enter director name: ")
                title = input("Enter movie title to play: ")
                self.play_movie(director_name, title)
            elif choice == '10':
                fetch_type = input("Fetch by (1) Director or (2) Movie: ")
                if fetch_type == '1':
                    director_name = input("Enter director name: ")
                    self.fetch_data_from_imdb(director_name=director_name, save_to_file=True)
                elif fetch_type == '2':
                    movie_title = input("Enter movie title: ")
                    self.fetch_data_from_imdb(movie_title=movie_title, save_to_file=True)
                else:
                    print("Invalid choice. Please try again.")
                    logging.warning("User entered an invalid fetch type.")
            elif choice == '0':
                print("Exiting Movie Player.")
                break
            else:
                print("Invalid choice. Please try again.")
                logging.warning("User entered an invalid menu choice.")


# Main Execution
if __name__ == '__main__':
    player = MoviePlayer()
    player.menu()
