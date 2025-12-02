from datetime import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import JSON

from App.database import db
from .user import User
from .driver import Driver
from .stop import Stop
from .notification import Notification
from .schedule import Schedule

class Resident(User):

    __tablename__ = "resident"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    streetId = db.Column(db.Integer,db.ForeignKey('street.id'),nullable=False)
    scheduleId = db.Column(db.Integer,db.ForeignKey('schedule.id'),nullable=False)
    houseNumber = db.Column(db.Integer, nullable=False)

    area = db.relationship("Area", backref='residents')
    street = db.relationship("Street", backref='residents')
    stops = db.relationship('Stop', backref='resident')
    notifications = db.relationship("Notification", backref="resident")

    __mapper_args__ = {
        "polymorphic_identity": "Resident",
    }

    def __init__(self, username, password, areaId, streetId, houseNumber, scheduleId):
        super().__init__(username, password)
        self.areaId = areaId
        self.streetId = streetId
        self.houseNumber = houseNumber
        self.scheduleId = scheduleId

    def get_json(self):
        user_json = super().get_json()
        user_json['areaId'] = self.areaId
        user_json['streetId'] = self.streetId
        user_json['houseNumber'] = self.houseNumber
        user_json['scheduleId'] = self.scheduleId
        return user_json
