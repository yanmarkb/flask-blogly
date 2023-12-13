
"""Blogly application."""

from flask import Flask, render_template, request, redirect, url_for  # Importing the Flask class, render_template function, and request object.

from models import db, User, Post  # Importing the db and User classes from the models module.

app = Flask(__name__)  # Creating an instance of the Flask class.

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


@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def new_post(user_id):
    """Show form to add a post for that user and handle form submission."""
    user = User.query.get_or_404(user_id)  # Get the user with the given user_id from the database.
    if request.method == 'POST':  # Check if the request method is POST.
        title = request.form['title']  # Get the value of the 'title' field from the form.
        content = request.form['content']  # Get the value of the 'content' field from the form.
        post = Post(title=title, content=content, user_id=user_id)  # Create a new Post object with the given title, content, and user_id.
        db.session.add(post)  # Add the post to the database session.
        db.session.commit()  # Commit the changes to the database.
        return redirect(url_for('user_detail', user_id=user_id))  # Redirect to the 'user_detail' route for the user.

    return render_template('new_post.html', user=user)  # Render the 'new_post.html' template with the user data.

@app.route('/posts/<int:post_id>', methods=['GET'])
def post_detail(post_id):
    """Show a post and buttons to edit and delete the post."""
    post = Post.query.get_or_404(post_id)  # Get the post with the given post_id from the database.
    user = User.query.get_or_404(post.user_id)  # Get the user associated with the post.
    return render_template('post_detail.html', post=post, user=user)  # Render the 'post_detail.html' template with the post and user data.

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    """Show form to edit a post and handle form submission."""
    post = Post.query.get_or_404(post_id)  # Get the post with the given post_id from the database.
    user = User.query.get_or_404(post.user_id)  # Get the user associated with the post.

    if request.method == 'POST':  # Check if the request method is POST.
        post.title = request.form['title']  # Update the post's title with the value from the form.
        post.content = request.form['content']  # Update the post's content with the value from the form.
        db.session.commit()  # Commit the changes to the database.
        return redirect(url_for('post_detail', post_id=post_id, user=user))  # Redirect to the 'post_detail' route for the post.

    return render_template('edit_post.html', post=post, user=user)  # Render the 'edit_post.html' template with the post and user data.

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete a post."""
    post = Post.query.get_or_404(post_id)  # Get the post with the given post_id from the database.
    db.session.delete(post)  # Delete the post from the database.
    db.session.commit()  # Commit the changes to the database.
    return redirect(url_for('user_detail', user_id=post.user_id))  # Redirect to the 'user_detail' route for the user.

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application in debug mode.


