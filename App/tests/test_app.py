import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date, time

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class ResidentUnitTests(unittest.TestCase):

    def test_new_resident(self):
        resident = Resident("john", "johnpass", 1,2,123,1)
        assert resident.username == "john"
        assert resident.password != "johnpass"
        assert resident.areaId == 1
        assert resident.streetId == 2
        assert resident.houseNumber == 123
        assert resident.scheduleId == 1

    def test_resident_getJSON(self):
        resident = Resident("john", "johnpass", 1, 2, 123,1)
        resident_json = resident.get_json()
        self.assertDictEqual(resident_json, {"id":None, "username":"john", "areaId":1, "streetId":2, "houseNumber":123, "scheduleId":1})

class DriverUnitTests(unittest.TestCase):

    def test_new_driver(self):
        driver = Driver("steve", "stevepass", "Busy", 2, 12)
        assert driver.username == "steve"
        assert driver.password != "stevepass"
        assert driver.status == "Busy"
        assert driver.areaId == 2
        assert driver.streetId == 12

    def test_driver_getJSON(self):
        driver = Driver("steve", "stevepass", "Busy", 2, 12)
        driver_json = driver.get_json()
        self.assertDictEqual(driver_json, {"id":None, "username":"steve", "status":"Busy", "areaId":2, "streetId":12})

class AreaUnitTests(unittest.TestCase):

    def test_new_area(self):
        area = Area("Sangre Grande")
        assert area.name == "Sangre Grande"

    def test_area_getJSON(self):
        area = Area("Sangre Grande")
        area_json = area.get_json()
        self.assertDictEqual(area_json, {"id":None, "name":"Sangre Grande"})

class StreetUnitTests(unittest.TestCase):

    def test_new_street(self):
        street = Street("Picton Road", 8)
        assert street.name == "Picton Road"
        assert street.areaId == 8

    def test_street_getJSON(self):
        street = Street("Picton Road", 8)
        street_json = street.get_json()
        self.assertDictEqual(street_json, {"id":None, "name":"Picton Road", "areaId":8})

class DriveUnitTests(unittest.TestCase):

    def test_new_drive(self):
        drive = Drive(78, 2, 12, date(2025, 11, 8), time(11, 30), "Upcoming")
        assert drive.driverId == 78
        assert drive.areaId == 2
        assert drive.streetId == 12
        assert drive.date == date(2025, 11, 8)
        assert drive.time == time(11, 30)
        assert drive.status == "Upcoming"

    def test_drive_getJSON(self):
        drive = Drive(78, 2, 12, date(2025, 11, 8), time(11, 30), "Upcoming")
        drive_json = drive.get_json()
        self.assertDictEqual(drive_json, {"id":None, "driverId":78, "areaId":2, "streetId":12, "date":"2025-11-08", "time":"11:30:00", "status":"Upcoming"})

class StopUnitTests(unittest.TestCase):

    def test_new_stop(self):
        stop = Stop(1, 2)
        assert stop.driveId == 1
        assert stop.residentId == 2

    def test_stop_getJSON(self):
        stop = Stop(1, 2)
        stop_json = stop.get_json()
        self.assertDictEqual(stop_json, {"id":None, "driveId":1, "residentId":2})

class ItemUnitTests(unittest.TestCase):

    def test_new_item(self):
        item = Item("Whole-Grain Bread", 19.50)
        assert item.name == "Whole-Grain Bread"
        assert item.price == 19.50

    def test_item_getJSON(self):
        item = Item("Whole-Grain Bread", 19.50)
        item_json = item.get_json()
        self.assertDictEqual(item_json, {"id":None, "name":"Whole-Grain Bread", "price":19.50})

class DriverStockUnitTests(unittest.TestCase):

    def test_new_driverStock(self):
        driverStock = DriverStock(1, 2, 30)
        assert driverStock.driverId == 1
        assert driverStock.itemId == 2
        assert driverStock.quantity == 30

    def test_driverStock_getJSON(self):
        driverStock = DriverStock(1, 2, 30)
        driverStock_json = driverStock.get_json()
        self.assertDictEqual(driverStock_json, {"id":None, "driverId":1, "itemId":2, "quantity":30})

class NotificationUnitTests(unittest.TestCase):

    def test_new_notification(self):
        notification=Notification(1,"I have arrived")
        assert notification.residentId == 1
        assert notification.message == "I have arrived"
        

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    db.create_all()    
    yield app.test_client()
    db.drop_all()

class ResidentsIntegrationTests(unittest.TestCase):
    
    def setUp(self):
        self.area = create_area("St. Augustine")
        self.street = create_street(self.area.id, "Warner Street")
        self.driver = create_driver("driver1", "pass")
        self.resident = create_resident("john", "johnpass", self.area.id, self.street.id, 123)
        self.drive = driver_schedule_drive(self.driver,self.area.id, self.street.id, "2025-12-25", "11:30")
        self.item = Item("Whole-Grain Bread", 19.50)


    def test_request_stop(self):

        stop = resident_request_stop(self.resident, self.drive.id)
        self.assertIsNotNone(stop)

    def test_cancel_stop(self):
        stop = resident_request_stop(self.resident, self.drive.id)
        resident_cancel_stop(self.resident, self.stop.id)
        self.assertIsNone(Stop.query.filter_by(id=self.stop.id).first())

    def test_view_driver_status(self):
        driver = resident_view_driver_status(self.resident, self.driver.id)
        self.assertIsNotNone(driver)

    def test_view_stock(self):
        driver_update_stock(self.driver, self.item.id, 30)
        stock = resident_view_stock(self.resident, self.driver.id) # type: ignore
        self.assertIsNotNone(stock)

    def test_update(self):
        message = "Truck delayed by 30 minutes."
        initial_count = len(Notification.query.all())
        self.resident.receive_notification(message)
        new_count = len(Notification.query.all())
        self.assertEqual(new_count, initial_count + 1)
        self.assertEqual(self.resident.notification[-1].message, message)

    def test_watch_schedule(self):
        schedule = Schedule.query.get(self.resident.scheduleid)
        initial_count = len(schedule.residents)
        self.resident.watch_schedule(schedule.id)
        self.assertEqual(len(schedule.residents), initial_count + 1)
        self.assertIn(self.resident, schedule.residents)

    def test_unwatch_schedule(self):
         schedule = Schedule.query.get(self.resident.scheduleid)
         self.resident.watch_schedule(schedule.id)
         self.assertIn(self.resident, schedule.residents)
         self.resident.unwatch_schedule(schedule.id)
         self.assertNotIn(self.resident, schedule.residents)

    def test_view_notifications(self):
        message1 = "Drive scheduled for tomorrow."
        message2 = "New item added to stock."
        notif1 = Notification(message=message1, residentId=self.resident.id)
        notif2 = Notification(message=message2, residentId=self.resident.id)
        db.session.add_all([notif1, notif2])
        db.session.commit()
        notifications = resident_view_notifications(self.resident) # type: ignore
        self.assertEqual(len(notifications), 2)
        self.assertEqual(notifications[0].message, message1)
        self.assertEqual(notifications[1].message, message2)

    def test_receive_notification(self):
        message = "Truck delayed by 30 minutes."
        initial_count = len(Notification.query.all())
        resident_receive_notification(self.resident, message)
        new_count = len(Notification.query.all())
        self.assertEqual(new_count, initial_count + 1)
        self.assertEqual(self.resident.notifications[-1].message, message)

class DriversIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.area = Area("St. Augustine")
        self.street = Street(self.area.id, "Warner Street")
        self.driver = Driver("driver1", "pass","Available", self.area.id,self.street.id)
        self.resident = Resident("john", "johnpass", self.area.id, self.street.id, 123,1)
        self.drive = Drive(self.driver, self.area.id, self.street.id, "2025-12-25", "11:30", "Upcoming")
        self.stop = Stop(self.drive.id,self.resident.id)
        self.item = Item("Whole-Grain Bread", 19.50)

    def test_schedule_drive(self):
        drive = driver_schedule_drive(self.driver, self.area.id, self.street.id, "2025-12-25", "09:00")
        self.assertIsNotNone(drive)

    def test_cancel_drive(self):
        drive = driver_schedule_drive(self.driver, self.area.id, self.street.id, "2025-12-25", "08:15")
        driver_cancel_drive(self.driver, drive.id)
        assert drive.status == "Cancelled"

    def test_view_drives(self):
        drives = driver_view_drives(self.driver) # type: ignore
        self.assertIsNotNone(drives)

    def test_start_drive(self):
        driver_start_drive(self.driver, self.drive.id)
        drive = Drive.query.filter_by(id=self.drive.id).first()
        assert self.drive.status == "In Progress"
        assert self.driver.status == "Busy"

    def test_end_drive(self):
        driver_start_drive(self.driver, self.drive.id)
        driver_end_drive(self.driver)
        drive = Drive.query.filter_by(id=self.drive.id).first()
        assert self.drive.status == "Completed"
        assert self.driver.status == "Available"

    def test_view_requested_stops(self):
        stops = driver_view_requested_stops(self.driver, self.drive.id)
        self.assertIsNotNone(stops)
    
    def test_update_stock(self):
        newquantity = 30
        driver_update_stock(self.driver, self.item.id, newquantity)
        stock = DriverStock.query.filter_by(driverId=self.driver.id, itemId=self.item.id).first()
        assert stock.quantity == newquantity

    def test_view_stock(self):
        stock = driver_view_stock(self.driver)
        self.assertIsNotNone(stock)
