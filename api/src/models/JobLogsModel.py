from src import db

class JobLogs(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    job_id = db.Column(db.Integer, nullable=False)
    job_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)