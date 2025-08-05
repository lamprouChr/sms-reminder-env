from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=True)
