from datetime import datetime
from App.database import db

class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    residentId = db.Column(db.Integer, db.ForeignKey('resident.id'))
    message = db.Column(db.String(255), nullable=False)

    def __init__(self,message):
        self.message = message

    def __repr__(self):
        return f'<Resident received notification!\n {self.message}>'
    
    