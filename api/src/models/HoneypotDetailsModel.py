from src import db
# import enum

# class HoneypotDetailEnum(enum.Enum):
#     sleeping = "sleeping"
#     not_running = "not running"
#     running = "running"

class HoneypotDetails(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    honeypot_sensor_id = db.Column(db.Integer, db.ForeignKey('honeypot_sensor.id'), nullable=False)
    sensor_name = db.Column(db.String, nullable=False)
    honeypot_name = db.Column(db.String, nullable=False)
    # state = db.Column(db.Enum(name='honeypotdetail_state_enum', values_callable=(e.value for e in HoneypotDetailEnum)), nullable=False)
    state = db.Column(db.String, nullable=False)
    virtual_memory = db.Column(db.Float, nullable=False)
    resident_memory = db.Column(db.Float, nullable=False)
    text_memory = db.Column(db.Float, nullable=False)
    data_memory = db.Column(db.Float, nullable=False)
    virtual_memory_percentage = db.Column(db.Float, nullable=False)
    resident_memory_percentage = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)

