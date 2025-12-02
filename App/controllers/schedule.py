from App.models import Schedule
from App.database import db
from App.controllers import *

def schedule_subscribe(resident):
    """
    Subscribes a resident to a schedule.
    """
    schedule = Schedule.query.first()
    
    if not schedule:
        raise ValueError("Schedule not found.")
    if resident in schedule.residents:
        raise ValueError("Resident is already subscribed to this schedule.")


    schedule.residents.append(resident)
    db.session.add(schedule)
    db.session.commit()
    return schedule

def schedule_unsubscribe(resident):
    """
    Unsubscribes a resident from a schedule.
    """
    schedule = Schedule.query.get(resident.scheduleId)
    
    if not schedule:
        raise ValueError("Schedule not found.")
        
    if resident not in schedule.residents:
        raise ValueError("Resident is not subscribed to this schedule.")

    schedule.residents.remove(resident)
    db.session.add(schedule)
    db.session.commit()
    return schedule

def schedule_notify_subscribers(message):
    """
    Notifies all subscribers of a schedule.
    """
    schedule = Schedule.query.first()

    if not schedule:
        raise ValueError("Schedule not found.")
    if not message:
        raise ValueError("Message content is required.")

    for resident in schedule.residents:
        resident_receive_notification(resident, message)
    return True