from App.database import db
from datetime import datetime
from .user import User
from .drive import Drive
from .street import Street


class Driver(User):
    __tablename__ = "driver"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    streetId = db.Column(db.Integer, db.ForeignKey('street.id'))

    area = db.relationship("Area", backref="drivers")
    street = db.relationship("Street", backref="drivers")

    __mapper_args__ = {
        "polymorphic_identity": "Driver",
    }

    def __init__(self, username, password, status, areaId, streetId):
        super().__init__(username, password)
        self.status = status
        self.areaId = areaId
        self.streetId = streetId

    def get_json(self):
        user_json = super().get_json()
        user_json['status'] = self.status
        user_json['areaId'] = self.areaId
        user_json['streetId'] = self.streetId
        return user_json

    def login(self, password):
        if super().login(password):
            self.areaId = 0
            self.streetId = 0
            self.status = "Available"
            db.session.commit()
            return True
        return False

    def logout(self):
        super().logout()
        self.status = "Offline"
        db.session.commit()