from App.models import *
from App.database import db
from datetime import datetime, timedelta
from .schedule import schedule_notify_subscribers

# All driver-related business logic is moved here as functions

def driver_schedule_drive(driver, area_id, street_id, date_str, time_str):
    """
    Schedules a new drive and notifies subscribers via the Schedule mechanism.
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return None

    scheduled_datetime = datetime.combine(date, time)
    now = datetime.now()

    if scheduled_datetime < now:
        return None

    sixty_days_later = now + timedelta(days=60)
    if scheduled_datetime > sixty_days_later:
        return None

    existing_drive = Drive.query.filter_by(areaId=area_id, streetId=street_id, date=date, status="Upcoming").first()
    if existing_drive:
        return None

    new_drive = Drive(driverId=driver.id, areaId=area_id,streetId=street_id,date=date,time=time,status="Upcoming")
    db.session.add(new_drive)
    db.session.commit()

    message = f"SCHEDULED>> Drive {new_drive.id} by Driver {driver.id} on {date} at {time}\n"
    message += "Items in Stock:\n"

    driverStock = DriverStock.query.filter_by(driverId=driver.id).all()
    if driverStock:
        for stock in driverStock:
            item = stock.item
            message += f"- {item.get_json()} (Quantity: {stock.quantity})\n"

    schedule_notify_subscribers(message)
    return (new_drive)
    

def driver_cancel_drive(driver, drive_id):
    """
    Cancels an upcoming drive.
    (Logic moved and integrated from Driver.cancel_drive)
    """
    drive = Drive.query.get(drive_id)

    if not drive or drive.driverId != driver.id or drive.status == "Cancelled":
        return None

    drive.status = "Cancelled"

    street = Street.query.get(drive.streetId)
    if street and street.residents:
        drive = Drive.query.get(drive_id)
        if drive:
            drive.status = "Cancelled"
            message = f"CANCELLED>> Drive {drive.id} by Driver {driver.id} on {drive.date} at {drive.time}"
            schedule_notify_subscribers(message)
            db.session.commit()
        return drive

def driver_start_drive(driver, drive_id):
    """
    Starts an upcoming drive, setting driver and drive status to 'Busy' and 'In Progress'.
    """
    current_drive = Drive.query.filter_by(driverId=driver.id, status="In Progress").first()
    if current_drive:
        return None

    drive = Drive.query.filter_by(driverId=driver.id, id=drive_id, status="Upcoming").first()
    if not drive:
        return None

    # Update driver state
    driver.status = "Busy"
    driver.areaId = drive.areaId
    driver.streetId = drive.streetId


    drive.status = "In Progress"
    db.session.commit()
    return drive


def driver_end_drive(driver):
    """
    Ends the current 'In Progress' drive, setting driver status to 'Available' and drive status to 'Completed'.
    """
    current_drive = Drive.query.filter_by(driverId=driver.id, status="In Progress").first()
    if not current_drive:
        return None

    driver.status = "Available"
    current_drive.status = "Completed"

    db.session.commit()

    return current_drive


def driver_view_requested_stops(driver, drive_id):
    """
    Views the requested stops for a specific drive.

    """
    drive = Drive.query.get(drive_id)
    
    if not drive or drive.driverId != driver.id:
        return []

    return drive.stops


def driver_update_stock(driver, item_id, quantity):
    """
    Updates or creates a driver's stock quantity for a specific item.
    """
    item = Item.query.get(item_id)
    if not item:
        return None
    stock = DriverStock.query.filter_by(driverId=driver.id, itemId=item_id).first()
    if stock:
        stock.quantity = quantity
    else:
        stock = DriverStock(driverId=driver.id, itemId=item_id, quantity=quantity)
        db.session.add(stock)
    db.session.commit()
    return stock
