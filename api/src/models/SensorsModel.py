from src import db

class Sensors(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ip_address = db.Column(db.String, nullable=False)
    ip_gateway = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False)
