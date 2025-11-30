from App.models import *

def view_stock(driver_id):
    driver = Driver.query.get(driver_id)
    stocks =  DriverStock.query.filter_by(driverId=driver_id).all()
    if not driver or not stocks:
        return None
    return stocks