from flask import Flask, render_template, request, redirect, url_for
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
    user, movies = data_manager.get_user_movies(user_id)
    if movies is None:
        return "User not found"
    return render_template('user_movies.html', user=user, movies=movies, id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_user_name = request.form['username']
        data_manager.add_user(new_user_name)  # Implement this method in JSONDataManager
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/add_movie/<user_id>', methods=['GET', 'POST'])
def add_movie(user_id):
    user, _ = data_manager.get_user_movies(user_id)
    if user is None:
        return "User not found"

    if request.method == 'POST':
        movie_title = request.form['movie_title']
        data_manager.add_movie_to_user(user_id, movie_title)  # Implement this method in JSONDataManager
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html', user=user)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user, movies = data_manager.get_user_movies(user_id)

    if user is None:
        return "User not found"

    movie_to_update = next((movie for movie in movies if movie["id"] == int(movie_id)), None)

    if movie_to_update is None:
        return "Movie not found"

    if request.method == 'POST':
        new_movie_title = request.form['movie_title']
        data_manager.update_movie(user_id, movie_id, new_movie_title)
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', user=user, movie=movie_to_update)


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    user, _ = data_manager.get_user_movies(user_id)

    if user is None:
        return "User not found"

    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)
