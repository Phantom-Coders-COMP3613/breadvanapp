from App.models import *
from App.database import db
from datetime import datetime, timedelta
from .schedule import schedule_notify_subscribers

# All driver-related business logic will be moved here as functions

def driver_schedule_drive(driver, area_id, street_id, date_str, time_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        raise ValueError("Invalid date or time format. Use YYYY-MM-DD and HH:MM.")
    scheduled_datetime = datetime.combine(date, time)
    now = datetime.now() 
    if scheduled_datetime < now:
        raise ValueError("Cannot schedule a drive in the past.")
    
    sixty_days_later = now + timedelta(days=60)


    if scheduled_datetime > sixty_days_later:
        raise ValueError("Cannot schedule a drive more than 60 days in advance.")
    
    
    existing_drive = Drive.query.filter_by(areaId=area_id, streetId=street_id, date=date).first()
    if existing_drive:
        raise ValueError(f"A drive for this street is already scheduled on {date_str}.")
    
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.strptime(time_str, "%H:%M").time()
    except Exception:
        print("Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.")
        return

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
        db.session.commit()
        return (new_drive)
    return None

def driver_cancel_drive(driver, drive_id):
    drive = Drive.query.get(drive_id)

    if not drive or drive.driverId != driver.id:
        raise ValueError("Drive not found or does not belong to this driver.")

    drive.status = "Cancelled"

    street = Street.query.get(drive.streetId)
    if street and street.residents:
        drive = Drive.query.get(drive_id)
        if drive:
            drive.status = "Cancelled"
            message = f"CANCELLED>> Drive {drive.id} by Driver {driver.id} on {drive.date} at {drive.time}"
            schedule_notify_subscribers(message)
            db.session.commit()
        return None

def driver_start_drive(driver, drive_id):
    current_drive = Drive.query.filter_by(driverId=driver.id, status="In Progress").first()
    if current_drive:
        raise ValueError(f"You are already on drive {current_drive.id}.")
    drive = Drive.query.filter_by(driverId=driver.id, id=drive_id, status="Upcoming").first()
    if not drive:
        raise ValueError("Drive not found or cannot be started.")      
    
    driver.status = "Busy"
    driver.areaId = drive.areaId
    driver.streetId = drive.streetId
    
    drive.status = "In Progress"
    
    db.session.commit()
    return driver.start_drive(drive_id)

def driver_end_drive(driver):
    current_drive = Drive.query.filter_by(driverId=driver.id, status="In Progress").first()
    if not current_drive:
        raise ValueError("No drive in progress.")
    
    driver.status = "Available"
    current_drive.status = "Completed"
    
    db.session.commit()
        
    return current_drive


def driver_view_requested_stops(driver, drive_id):
    stops = driver.view_requested_stops(drive_id)
    if not stops:
        return []
    return stops

def driver_update_stock(driver, item_id, quantity):
    item =  Item.query.get(item_id)
    if not item:
        raise ValueError("Invalid item ID.")
    stock =  DriverStock.query.filter_by(driverId=driver.id, itemId=item_id).first()
    if stock:
        stock.quantity = quantity
    else:
        stock = DriverStock(driverId=driver.id, itemId=item_id, quantity=quantity)
        db.session.add(stock)
    db.session.commit()
    return stock

def driver_view_stock(driver):
    stocks = DriverStock.query.filter_by(driverId=driver.id).all() 
    return stocks
    
    
    
