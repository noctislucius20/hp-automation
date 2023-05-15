from src import db

class HoneypotSensor(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    honeypot_id = db.Column(db.Integer, db.ForeignKey("honeypots.id"), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensors.id"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False)
