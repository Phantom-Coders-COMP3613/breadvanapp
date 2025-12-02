from App.models import *
from App.database import db

def create_area(name):
    area = Area(name=name)
    db.session.add(area)
    db.session.commit()
    return area

def create_street(area_id, name):
    area = Area.query.get(area_id)
    if not area:
        raise ValueError("Invalid area ID.")
    street = Street(name=name, areaId=area_id)
    db.session.add(street)
    db.session.commit()
    return street

def create_item(name, price):
    item = Item(name=name, price=price)
    db.session.add(item)
    db.session.commit()
    return item

def create_schedule():
    schedule = Schedule()
    db.session.add(schedule)
    db.session.commit()
    return schedule