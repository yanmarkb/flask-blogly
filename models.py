from flask_sqlalchemy import SQLAlchemy  # Imports the SQLAlchemy module for working with databases
from datetime import datetime  # Import the datetime module for working with dates and times

db = SQLAlchemy()  # Create an instance of the SQLAlchemy class to interact with the database

class User(db.Model):  # Define a User class that represents a table in the database
    __tablename__ = "users"  # Set the name of the table in the database

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Defines a column for the user's ID
    first_name = db.Column(db.String(50), nullable=False)  # Defines a column for the user's first name
    last_name = db.Column(db.String(50), nullable=False)  # Defines a column for the user's last name
    image_url = db.Column(db.String(500), nullable=True)  # Defines a column for the user's image URL
    

class Post(db.Model):  # Define a Post class that represents a table in the database
    """Blog post."""

    __tablename__ = "posts"  # Set the name of the table in the database

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Define a column for the post's ID
    title = db.Column(db.Text, nullable=False)  # Define a column for the post's title
    content = db.Column(db.Text, nullable=False)  # Define a column for the post's content
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Define a column for the post's creation date and time
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Define a column for the user ID associated with the post

    user = db.relationship('User', backref='posts')  # Define a relationship between the Post and User classes
