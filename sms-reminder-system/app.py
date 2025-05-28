from flask import Flask, request, render_template, redirect, url_for

from datetime import datetime
from models import db, Appointment
from dotenv import load_dotenv
import os
from flask_migrate import Migrate  # Add this import
from twilio.rest import Client

load_dotenv()
#fsdfd
app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")
if database_url is None:
    print("DATABASE_URL: None, using local SQLite fallback")
    database_url = "sqlite:///appointments.db"
else:
    print(f"DATABASE_URL: {database_url}")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)  # Initialize migration support here

TEMPLATE = """
<h2>Add Appointment</h2>
<form method="POST">
  Name: <input name="name"><br>
  Phone: <input name="phone"><br>
  Appointment: <input type="datetime-local" name="appointment"><br>
  <button type="submit">Add</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        appointment_time = datetime.strptime(request.form["appointment"], "%Y-%m-%dT%H:%M")
        db.session.add(Appointment(name=name, phone=phone, appointment_time=appointment_time))
        db.session.commit()
        return redirect(url_for("home"))

    appointments = Appointment.query.all()
    return render_template("add_appointment.html", appointments=appointments)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)
