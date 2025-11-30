from App.models import *
from App.database import db

def create_resident(username, password, area_id, street_id, schedule_id, house_number):
    newresident = Resident(username=username, password=password, areaId=area_id, streetId=street_id, scheduleId=schedule_id, houseNumber=house_number)
    try:
        db.session.add(newresident)
        db.session.commit()
        return newresident
    except Exception as e:
        db.session.rollback()
        print(f"Error creating resident: {e}")
        return None

def create_driver(username, password, area_id, street_id, status):
    newdriver = Driver(username=username, password=password, areaId=area_id, streetId=street_id, status=status)
    try:
        db.session.add(newdriver)
        db.session.commit()
        return newdriver
    except Exception as e:
        db.session.rollback()
        print(f"Error creating driver: {e}")
        return None