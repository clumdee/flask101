from flask_sqlalchemy import SQLAlchemy


# define SQLAlchemy object
db = SQLAlchemy()

# create a model (table) for users
class Users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email