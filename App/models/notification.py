from datetime import datetime
from App.database import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    residentId = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    resident= db.relationship("Resident", backref='notifications')
       
    def __init__(self, residentId, message):
        self.residentId = residentId
        self.message = message

    def mark_as_read(self):
        self.is_read = True
        db.session.commit()

    def __repr__(self):
        return f'<Notification {self.id} for User {self.residentId}>'
    
    