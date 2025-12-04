from App.database import db
from App.models import *
from .admin import create_area, create_street, create_item, create_schedule
from .user import create_resident, create_driver
from .driver import driver_schedule_drive, driver_update_stock
from .resident import resident_watch_schedule, resident_request_stop

def initialize():
    db.drop_all()
    db.create_all()

    create_area("St. Augustine")
    create_area("Curepe")

    create_street(1, "Warner Street")
    create_street(2, "Gordon Street")

    create_schedule()

    resident1 = create_resident('Resident1', 'Resident1pass', 1, 1, 123)
    resident2 = create_resident('Resident2', 'Resident2pass', 2, 2, 422)
    resident_watch_schedule(resident1)

    driver1 = create_driver('Driver1', 'Driver1pass')
    driver2 = create_driver('Driver2', 'Driver2pass')

    create_item("Cake", 5.00)
    create_item("Raisin Bread", 12.00)
    create_item("Hops Bread", 20.00)

    driver_update_stock(driver1, 1, 15)
    driver_update_stock(driver2, 2, 10)
    driver_update_stock(driver1, 3, 20)

    driver_schedule_drive(driver1, 1, 1, "2026-01-14", "10:00")
    driver_schedule_drive(driver2, 2, 2, "2026-01-06", "09:00")

    resident_request_stop(resident2, 2)
