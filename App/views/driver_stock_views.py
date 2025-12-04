from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.models import Driver, Item # Driver and Item models needed for context/relations
from App.controllers import *

driver_stock_views = Blueprint('driver_stock_views', __name__)

def get_driver_or_403(user_id):
    """Fetches the Driver object for the authenticated user or returns None."""
    driver = Driver.query.get(user_id)

    if not driver: 
        return None
    return driver


@driver_stock_views.route('/api/stocks/<int:driverId>', methods=['GET'])
def view_driver_stock_endpoint(driverId):
    stock = user_view_stock(driverId)
    total = len(stock or [])
    
    if not stock:
        return jsonify({'message': f'No stock'}), 400
    items = [d.get_json() if hasattr(d, 'get_json') else d for d in (stock or [])]
    return jsonify({'stocks': items, 'total': total}), 200
