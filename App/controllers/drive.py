from App.models import *

def driver_view_drives(driver):
    return Drive.query.filter(Drive.driverId==driver.id, Drive.status.in_(["Upcoming", "In Progress"])).all()