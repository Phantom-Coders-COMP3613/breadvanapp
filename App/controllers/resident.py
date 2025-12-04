from App.models import *
from App.database import db
# All resident-related business logic will be moved here as functions

def resident_request_stop(resident, drive_id):
    drives = Drive.query.filter_by(areaId=resident.areaId, streetId=resident.streetId, status="Upcoming").all()
    existing_stop = Stop.query.filter_by(driveId=drive_id, residentId=resident.id).first()
    if not any(d.id == drive_id for d in drives) or existing_stop:
        return None

    new_stop = Stop(driveId=drive_id, residentId=resident.id)
    db.session.add(new_stop)
    db.session.commit()
    return new_stop

def resident_cancel_stop(resident, drive_id):
    stop = Stop.query.filter_by(driveId=drive_id, residentId=resident.id).first()
    #if not stop:
    #   return None
    db.session.delete(stop)
    db.session.commit()
    return stop

def resident_view_driver_status(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return None
    return driver

def resident_watch_schedule(resident):
    from .schedule import schedule_subscribe
    return schedule_subscribe(resident)

def resident_unwatch_schedule(resident):
    from .schedule import schedule_unsubscribe
    return schedule_unsubscribe(resident)

def resident_view_inbox(resident):
    return resident.notifications

def resident_receive_notification(resident, message):
    notification = Notification(message=message)
    resident.notifications.append(notification)
    db.session.add_all([resident, notification])
    db.session.commit()
    return resident.notifications[-1]