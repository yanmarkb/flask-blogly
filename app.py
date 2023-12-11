
"""Blogly application.""" 

from flask import Flask, render_template, request, redirect, url_for 

from models import db, User  # Importing the db and User classes from the models module.

app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'  # Configuring the database URI.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disabling modification tracking.

app.config['SQLALCHEMY_ECHO'] = True  # Enabling SQL query logging.

db.init_app(app)  # Initializing the database with the Flask application.

@app.before_first_request  # A decorator that runs the decorated function before the first request to the application.
def create_tables():
    db.create_all()  # Creating all the database tables.

@app.route('/')  # A decorator that maps the root URL to the decorated function.
def home():
    return redirect(url_for('users'))  # Redirecting to the 'users' route.

@app.route('/users')  # A decorator that maps the '/users' URL to the decorated function.
def users():
    users = User.query.all()  # Querying all the users from the database.
    return render_template('users.html', users=users)  # Rendering the 'users.html' template with the users data.

@app.route('/users/new', methods=['GET', 'POST'])  # A decorator that maps the '/users/new' URL to the decorated function.
def new_user():
    if request.method == 'POST':  # Checking if the request method is POST.
        user = User(
            first_name=request.form['first_name'],  # Getting the value of the 'first_name' field from the form.
            last_name=request.form['last_name'],  # Getting the value of the 'last_name' field from the form.
            image_url=request.form['image_url'] or None  # Getting the value of the 'image_url' field from the form, or None if it's empty.
        )
        db.session.add(user)  # Adding the user to the database session.
        db.session.commit()  # Committing the changes to the database.
        return redirect(url_for('users'))  # Redirecting to the 'users' route.
    else:
        return render_template('new_user.html')  # Rendering the 'new_user.html' template.

@app.route('/users/<int:user_id>')  # A decorator that maps the '/users/<user_id>' URL to the decorated function.
def user_detail(user_id):
    user = User.query.get_or_404(user_id)  # Querying the user with the given user_id from the database.
    return render_template('user_detail.html', user=user)  # Rendering the 'user_detail.html' template with the user data.

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])  # A decorator that maps the '/users/<user_id>/edit' URL to the decorated function.
def edit_user(user_id):
    user = User.query.get_or_404(user_id)  # Querying the user with the given user_id from the database.
    if request.method == 'POST':  # Checking if the request method is POST.
        user.first_name = request.form['first_name']  # Updating the user's first name with the value from the form.
        user.last_name = request.form['last_name']  # Updating the user's last name with the value from the form.
        user.image_url = request.form['image_url'] or None  # Updating the user's image URL with the value from the form, or None if it's empty.
        db.session.commit()  # Committing the changes to the database.
        return redirect(url_for('users'))  # Redirecting to the 'users' route.
    else:
        return render_template('edit_user.html', user=user)  # Rendering the 'edit_user.html' template with the user data.

@app.route('/users/<int:user_id>/delete', methods=['POST'])  # A decorator that maps the '/users/<user_id>/delete' URL to the decorated function.
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()  # Deleting the user with the given user_id from the database.
    db.session.commit()  # Committing the changes to the database.
    return redirect(url_for('users'))  # Redirecting to the 'users' route.

if __name__ == '__main__':
    app.run(debug=True)  # Running the Flask application in debug mode.
