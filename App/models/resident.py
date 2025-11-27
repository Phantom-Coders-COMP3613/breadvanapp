from datetime import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import JSON

from App.database import db
from .user import User
from .driver import Driver
from .stop import Stop
from .notifications import Notification
from .schedule import Schedule

class Resident(User):

    __tablename__ = "resident"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable = False)
    streetId = db.Column(db.Integer,db.ForeignKey('street.id'),nullable=False)
    scheduleid = db.Column(db.Integer,db.ForeignKey('schedule.id'),nullable=False)
    houseNumber = db.Column(db.Integer, nullable=False)
    

    area = db.relationship("Area", backref='residents')
    street = db.relationship("Street", backref='residents')
    stops = db.relationship('Stop', backref='resident')
    notifications = db.relationship("Notification", backref="resident")

    __mapper_args__ = {
        "polymorphic_identity": "Resident",
    }

    def __init__(self, username, password, areaId, streetId, driverId, houseNumber,scheduleid):
        super().__init__(username, password)
        self.areaId = areaId
        self.streetId = streetId
        self.driverId = driverId
        self.houseNumber = houseNumber
        self.scheduleid = scheduleid

    def get_json(self):
        user_json = super().get_json()
        user_json['areaId'] = self.areaId
        user_json['streetId'] = self.streetId
        user_json['houseNumber'] = self.houseNumber
        return user_json

    def request_stop(self, driveId):
        try:
            new_stop = Stop(driveId=driveId, residentId=self.id)
            db.session.add(new_stop)
            db.session.commit()
            return (new_stop)
        except Exception:
            db.session.rollback()
            return None

    def cancel_stop(self, stopId):
        stop = Stop.query.get(stopId)
        if stop:
            db.session.delete(stop)
            db.session.commit()
        return

    def view_driver_stats(self, driverId):
        driver = Driver.query.get(driverId)
        return driver
    
    def update(self, message):
      print(f'{self.name}: received {message}')
      self.notification.append(Notification(message))
      db.session.add(self)
      db.session.commit()

    def watch_schedule(self,scheduleId):
        schedule= Schedule.query.get(scheduleId)
        if schedule:
            schedule.subscribe(self)
        
    def unwatch_schedule(self,scheduleId):
        schedule= Schedule.query.get(scheduleId)
        if schedule:
            schedule.unsubscribe(self)
