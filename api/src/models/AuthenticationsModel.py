from src import db

class Authentications(db.Model):
    token = db.Column(db.Text, primary_key=True, nullable=False)
