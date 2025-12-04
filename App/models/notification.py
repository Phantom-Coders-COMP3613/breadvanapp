from datetime import datetime
from App.database import db

class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    residentId = db.Column(db.Integer, db.ForeignKey('resident.id'))
    message = db.Column(db.String(500), nullable=False)

    def __init__(self,message):
        self.message = message
        
    def get_json(self):
       return {
           'notificationId': self.id,
            'residentId': self.residentId,
            'message': self.message,
       }

    def __repr__(self):
        return f'Resident {self.residentId} received notification!\n {self.message}'
    
    