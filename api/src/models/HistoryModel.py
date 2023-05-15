from src import db

class History(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    honeypot_sensor_id = db.Column(db.Integer, db.ForeignKey('honeypot_sensor.id'), nullable=False)
    sensor_status = db.Column(db.String, nullable=False)
    honeypot_status = db.Column(db.String, nullable=False)
    status_code_id = db.Column(db.Integer, db.ForeignKey('status_code.id'), nullable=False)
    started_at = db.Column(db.DateTime(timezone=True), nullable=True)
    stopped_at = db.Column(db.DateTime(timezone=True), nullable=True)
    peak_memory_usage_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)