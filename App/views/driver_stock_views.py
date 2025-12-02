from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.models import Driver, Item # Driver and Item models needed for context/relations
from App.controllers import driver as driver_controller # Controller functions for business logic

driver_stock_views = Blueprint('driver_stock_views', __name__, url_prefix='/api/driver')

def get_driver_or_403(user_id):
    """Fetches the Driver object for the authenticated user or returns None."""
    driver = Driver.query.get(user_id)

    if not driver: 
        return None
    return driver


@driver_stock_views.route('/stock', methods=['GET'])
@jwt_required()

def view_driver_stock_endpoint():
    """
    GET /api/driver/stock
    Endpoint to view the current stock carried by the authenticated driver.
    """
    driver = get_driver_or_403(current_user.id)

    if not driver:
        return jsonify({"error": "Unauthorized or user is not a driver"}), 403

    try:
        stocks = driver_controller.driver_view_stock(driver)
        
        stock_data = []
        for stock in stocks:
            item_name = stock.item.name if stock.item else 'Unknown Item'
            stock_data.append({
                'id': stock.id,
                'itemId': stock.itemId,
                'itemName': item_name,
                'quantity': stock.quantity
            })
        
        return jsonify(stock_data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve stock: {str(e)}"}), 500


@driver_stock_views.route('/stock', methods=['POST'])
@jwt_required()
def update_driver_stock_endpoint():
    """
    POST /api/driver/stock
    Endpoint to update the quantity of a specific item in the driver's stock.
    Requires itemId and quantity in the JSON body.
    """
    driver = get_driver_or_403(current_user.id)
    if not driver:
        return jsonify({"error": "Unauthorized or user is not a driver"}), 403

    data = request.get_json()
    item_id_raw = data.get('itemId')
    quantity_raw = data.get('quantity')

    if item_id_raw is None or quantity_raw is None:
        return jsonify({"error": "Missing itemId or quantity"}), 400
    
    try:
        item_id = int(item_id_raw)
        quantity = int(quantity_raw)
        if quantity < 0:
            return jsonify({"error": "Quantity cannot be negative"}), 400
    except ValueError:
        return jsonify({"error": "itemId and quantity must be valid integers"}), 400

    try:
        updated_stock = driver_controller.driver_update_stock(driver, item_id, quantity)
        
        stock_data = {
            'id': updated_stock.id,
            'itemId': updated_stock.itemId,
            'itemName': updated_stock.item.name if updated_stock.item else 'Unknown Item',
            'quantity': updated_stock.quantity
        }
        return jsonify(stock_data), 200
    except ValueError as e:

        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to update stock: {str(e)}"}), 500