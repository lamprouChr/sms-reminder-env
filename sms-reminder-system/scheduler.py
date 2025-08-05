from datetime import datetime, timedelta
from models import db, Appointment
from twilio.rest import Client
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_sms(name, phone):
    client.messages.create(
        to=phone,
        from_=TWILIO_PHONE,
        body=f"Reminder: You have an appointment tomorrow, {name}!"
    )

with app.app_context():
    tomorrow = datetime.now() + timedelta(days=1)
    start = datetime(tomorrow.year, tomorrow.month, tomorrow.day)
    end = start + timedelta(days=1)
    appointments = Appointment.query.filter(
        Appointment.appointment_time >= start,
        Appointment.appointment_time < end
    ).all()
    for appt in appointments:
        send_sms(appt.name, appt.phone)
