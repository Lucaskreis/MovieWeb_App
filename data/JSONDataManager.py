import json
from .data_manager import DataManagerInterface


# trocar o nome do arquivo e cuidar o caminho dos diretórios

class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        with open(self.filename, "r") as file_obj:
            data = json.loads(file_obj.read())
            return data

    def get_user_movies(self, user_id):
        data = self.get_all_users()
        if user_id in data:
            return data[user_id]["name"], data[user_id]["movies"]
        else:
            return None, None

    def list_all_users(self):
        data = self.get_all_users()
        users_list = []

        for user_id, user_data in data.items():
            user_info = {
                "id": user_id,
                "name": user_data["name"]
            }
            users_list.append(user_info)

        return users_list

    def add_user(self,username):
        data = self.get_all_users()

        # Generate a new user ID that is unique
        highest_id = max(map(int, data.keys()), default=0)
        new_user_id = str(highest_id + 1)
        while new_user_id in data:
            highest_id += 1
            new_user_id = str(highest_id)

        new_user = {
            "name": username,
            "movies": []
        }

        data[new_user_id] = new_user

        with open(self.filename, "w") as file_obj:
            json.dump(data, file_obj, indent=4)

    def add_movie_to_user(self, user_id, movie_data):
        data = self.get_all_users()

        if user_id in data:
            new_movie_id = self.generate_unique_id(data[user_id]["movies"])
            new_movie = {
                "id": new_movie_id,
                "title": movie_data["Title"],
                "poster": movie_data["Poster"],
                "rating": movie_data["imdbRating"],
                "year": movie_data["Year"]
            }
            data[user_id]["movies"].append(new_movie)

            with open(self.filename, "w") as file_obj:
                json.dump(data, file_obj, indent=4)
        else:
            raise ValueError("User not found")

    def generate_unique_id(self, existing_movies):
        highest_id = max(map(lambda movie: movie["id"], existing_movies), default=0)
        new_id = highest_id + 1

        while any(movie["id"] == new_id for movie in existing_movies):
            new_id += 1

        return new_id
    #voltar nessa funcao de gerar id

    def update_movie(self, user_id, movie_id, updated_movie):
        data = self.get_all_users()

        if user_id in data:
            movies = data[user_id]["movies"]
            for movie in movies:
                if movie["id"] == int(movie_id):
                    movie.update(updated_movie)
                    break

            with open(self.filename, "w") as file_obj:
                json.dump(data, file_obj, indent=4)
        else:
            raise ValueError("User not found")

    def delete_user(self, user_id):
        data = self.get_all_users()

        if user_id in data:
            del data[user_id]

            with open(self.filename, "w") as file_obj:
                json.dump(data, file_obj, indent=4)
        else:
            raise ValueError("User not found")


    def delete_movie(self, user_id, movie_id):
        data = self.get_all_users()

        if user_id in data:
            movies = data[user_id]["movies"]
            movie_to_delete = next((movie for movie in movies if movie["id"] == int(movie_id)), None)

            if movie_to_delete:
                movies.remove(movie_to_delete)

                with open(self.filename, "w") as file_obj:
                    json.dump(data, file_obj, indent=4)
            else:
                raise ValueError("Movie not found")
        else:
            raise ValueError("User not found")