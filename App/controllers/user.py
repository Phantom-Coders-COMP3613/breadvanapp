from App.models import *
from App.database import db

def create_resident(username, password, area_id, street_id, house_number):
    newresident = Resident(username=username, password=password, areaId=area_id, streetId=street_id, houseNumber=house_number, scheduleId=1)
    try:
        db.session.add(newresident)
        db.session.commit()
        return newresident
    except Exception as e:
        db.session.rollback()
        print(f"Error creating resident: {e}")
        return None

def create_driver(username, password):
    newdriver = Driver(username=username, password=password, status="Offline", areaId=None, streetId=None)
    try:
        db.session.add(newdriver)
        db.session.commit()
        return newdriver
    except Exception as e:
        db.session.rollback()
        print(f"Error creating driver: {e}")
        return None

def user_login(username, password):
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    if user and user.check_password(password):
        user.logged_in = True
        if isinstance(user, Driver):
            user.status = "Available"
        db.session.commit()
        return user
    raise ValueError("Invalid username or password.")

def user_logout(user):
    user.logged_in = False
    if isinstance(user, Driver):
        user.status = "Offline"
    db.session.commit()
    return user

def user_view_drives():
    drives = Drive.query.all()
    return [d for d in drives if d.status in ("Upcoming", "In Progress")]

def user_view_stock(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return None
    # Return all stock entries for this driver
    stocks = DriverStock.query.filter_by(driverId=driver_id).all()
    return stocks