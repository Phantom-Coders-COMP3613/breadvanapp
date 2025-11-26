from App.database import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    residents = db.relationship("Resident", backref="schedule", lazy=True)

    def subscribe(self, resident):
        self.residents.append(resident)

    def unsubscribe(self, resident):
        self.residents.remove(resident)

    def notify_subscribers(self, message):
        for resident in self.residents:
            resident.update()

