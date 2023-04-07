from src import db

class Authentications(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    token = db.Column(db.Text, nullable=False)
