from src import db

class SensorDetails(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    sensor_name = db.Column(db.String, nullable=False)
    honeypot_running = db.Column(db.Integer, nullable=False)
    cpu_usage = db.Column(db.Float, nullable=False)
    cpu_frequency = db.Column(db.Float, nullable=False)
    cpu_count = db.Column(db.Integer, nullable=False)
    ram_total = db.Column(db.Float, nullable=False)
    ram_usage = db.Column(db.Float, nullable=False)
    ram_available = db.Column(db.Float, nullable=False)
    ram_percentage = db.Column(db.Float, nullable=False)
    swap_memory_total = db.Column(db.Float, nullable=False)
    swap_memory_usage = db.Column(db.Float, nullable=False)
    swap_memory_free = db.Column(db.Float, nullable=False)
    swap_memory_percentage = db.Column(db.Float, nullable=False)
    network_packet_received = db.Column(db.Integer, nullable=False)
    network_packet_sent = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)



