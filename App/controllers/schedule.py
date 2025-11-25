from App.models import Schedule, Resident
from App.database import db

def subscribe(schedule_id, resident):
    """
    Subscribes a resident to a schedule.
    """
    schedule = Schedule.query.get(schedule_id)
    
    if not schedule:
        raise ValueError("Schedule not found.")
    
    # Check if already subscribed (assuming relationship is loaded)
    if resident in schedule.residents:
        raise ValueError("Resident is already subscribed to this schedule.")

    # Call Model Method
    schedule.subscribe(resident)
    
    db.session.add(schedule)
    db.session.commit()
    return schedule

def unsubscribe(schedule_id, resident):
    """
    Unsubscribes a resident from a schedule.
    """
    schedule = Schedule.query.get(schedule_id)
    
    if not schedule:
        raise ValueError("Schedule not found.")
        
    if resident not in schedule.residents:
        raise ValueError("Resident is not subscribed to this schedule.")

    # Call Model Method
    schedule.unsubscribe(resident)
    
    db.session.add(schedule)
    db.session.commit()
    return schedule

def notify_subscribers(schedule_id, message):
    """
    Notifies all subscribers of a schedule.
    """
    schedule = Schedule.query.get(schedule_id)

    if not schedule:
        raise ValueError("Schedule not found.")
    
    if not message:
        raise ValueError("Message content is required.")

    # Call Model Method
    schedule.notify_subscribers(message)
    
    # Commit required to save any Notification objects created by the resident.update() calls
    db.session.commit()
    return True