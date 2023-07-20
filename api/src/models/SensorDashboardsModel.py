from src import db

class SensorDashboards(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    dashboard_id = db.Column(db.String, nullable=False)
    dashboard_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False)