from App.models import *
from App.database import db
# All resident-related business logic will be moved here as functions

def resident_request_stop(resident, drive_id):
    drives = Drive.query.filter_by(areaId=resident.areaId, streetId=resident.streetId, status="Upcoming").all()
    existing_stop = Stop.query.filter_by(driveId=drive_id, residentId=resident.id).first()
    if not any(d.id == drive_id for d in drives) or not existing_stop:
        return None

    new_stop = Stop(driveId=drive_id, residentId=resident.id)
    db.session.add(new_stop)
    db.session.commit()
    return new_stop

def resident_cancel_stop(resident, drive_id):
    stop = Stop.query.filter_by(driveId=drive_id, residentId=resident.id).first()
    if not stop:
        return None
    db.session.delete(stop)
    db.session.commit()
    return stop

def resident_view_driver_stats(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return None
    return driver

def resident_view_stock(driver_id):
    driver = Driver.query.get(driver_id)
    stocks =  DriverStock.query.filter_by(driverId=driver_id).all()
    if not driver or not stocks:
        return None
    return stocks

def resident_watch_schedule(resident, scheduleId):
    schedule= Schedule.query.get(scheduleId)
    if not schedule:
        return None
    return schedule.subscribe(resident)

def resident_unwatch_schedule(resident,scheduleId):
    schedule= Schedule.query.get(scheduleId)
    if not schedule:
        return None
    return schedule.unsubscribe(resident)

def resident_view_notifications(resident):
    return Notification.query.filter_by(residentId=resident.id).all()

def resident_receive_notification(resident, message):
    resident.notifications.append(Notification(message=message, residentId=resident.id))
    db.session.add(resident)
    db.session.commit()
    return resident.notifications[-1]