from App.database import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    residents = db.relationship("Resident", backref="schedule", lazy=True)