from App.database import db
from App.models import *
from .admin import *
from .user import *
from .driver import *
from .resident import *

def initialize():
    db.drop_all()
    db.create_all()

    create_area("St. Augustine")
    create_area("Curepe")

    create_street(1, "Warner Street")
    create_street(2, "Gordon Street")

    create_schedule()

    resident1 = create_resident('Resident1', 'Resident1pass', 1, 15, 123, 1)
    resident2 = create_resident('Resident2', 'Resident2pass', 2, 27, 422, 1)
    resident_watch_schedule(1, resident1)

    driver1 = create_driver('Driver1', 'Driver1pass', "Offline", 1, 15)
    driver2 = create_driver('Driver2', 'Driver2pass', "Available", 2, 27)

    create_item("Cake", 5.00)
    create_item("Raisin Bread", 12.00)
    create_item("Hops Bread", 20.00)

    driver_schedule_drive(driver1, 1, 15, "2025-12-31", "10:00")
    driver_schedule_drive(driver2, 2, 27, "2026-01-06", "09:00")

    resident_request_stop(resident1, 1)
    resident_request_stop(resident2, 2)
