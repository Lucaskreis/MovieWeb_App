from flask import Flask, render_template
from data.JSONDataManager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('data/data.json')


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    if movies is None:
        return "User not found"
    return render_template('user_movies.html', user_id=user_id, movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
