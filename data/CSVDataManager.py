import csv
from .data_manager import DataManagerInterface


class CSVDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        users = []
        with open(self.filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                users.append(row)
        return users

    def get_user_movies(self, user_id):
        users = self.get_all_users()
        for user in users:
            if user['id'] == user_id:
                return user, user["movies"]
        return None, None

    def list_all_users(self):
        users = self.get_all_users()
        users_list = []
        for user in users:
            user_info = {"id": user["id"], "name": user["name"]}
            users_list.append(user_info)
        return users_list

    def delete_user(self, user_id):
        users = self.get_all_users()
        updated_users = [user for user in users if user['id'] != user_id]
        with open(self.filename, 'w', newline='') as csvfile:
            fieldnames = ['id', 'name', 'movies']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user in updated_users:
                writer.writerow(user)

    # Implement other methods (update_movie, add_user, etc.) similarly
