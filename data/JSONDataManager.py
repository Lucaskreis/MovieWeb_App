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
            return data[user_id]["movies"]
        else:
            return None

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
#colocar a ultima function no data_manager
#Implementar update, add, delete

