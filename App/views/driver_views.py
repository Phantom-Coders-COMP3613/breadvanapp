from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.views.auth import auth_views
from App.views import user as user_views
from App.controllers import *

driver_views = Blueprint('driver_views', __name__)


@driver_views.route('/me', methods=['GET'])
@jwt_required()
@login_required(Driver)
def me():
    return jsonify({'id': current_user.id}), 200


@driver_views.route('/api/driver/drives', methods=['POST'])
@jwt_required()
@login_required(Driver)
def create_drive():
    data = request.json

    driver = current_user

    drive = driver_schedule_drive(driver, data['area_id'],data['street_id'], data['date'], data['time'])

    if not drive:
        return jsonify({'message': f'Error scheduling drive'}), 400
    return jsonify({'status': 'success', 'message': f'Drive scheduled successfully with ID: {drive.id}'}), 200


@driver_views.route('/api/driver/drives/<int:driveId>/start', methods=['POST'])
@jwt_required()
@login_required(Driver)
def start_drive(driveId):
    drive= driver_start_drive(current_user, driveId)
    if not drive:
        return jsonify({'message': f'Error starting drive'}), 400
    return jsonify({'status': 'success', 'message': f'Drive started successfully with ID: {driveId}'}), 200


@driver_views.route('/api/driver/drives/<int:driveId>/end', methods=['POST'])
@jwt_required()
@login_required(Driver)
def end_drive(driveId):
    drive = driver_end_drive(current_user)
    if not drive:
        return jsonify({'message': f'Error ending drive'}), 400
    return jsonify({'status': 'success', 'message': f'Drive ended successfully with ID: {driveId}'}), 200


@driver_views.route('/api/driver/drives/<int:driveId>/cancel', methods=['POST'])
@jwt_required()
@login_required(Driver)
def cancel_drive(driveId):
    drive = driver_cancel_drive(current_user, driveId)
    if not drive:
        return jsonify({'message': f'Error cancelling drive'}), 400
    return jsonify({'status': 'success', 'message': f'Drive cancelled successfully with ID: {drive.id}'}), 200



@driver_views.route('/api/driver/drives/<int:driveId>/requested-stops', methods=['GET'])
@jwt_required()
@login_required(Driver)
def requested_stops(driveId):
    stops = driver_view_requested_stops(current_user, driveId)
    items = [s.get_json() if hasattr(s, 'get_json') else s for s in (stops or [])]
    return jsonify({'stops': items}), 200

@driver_views.route('/api/driver/update-stock', methods=['PUT'])
@jwt_required()
@login_required(Driver)
def update_driver_stock():
    data = request.json

    updated_stock = driver_update_stock(current_user, data['item_id'], data['quantity'])
    if not updated_stock:
        return jsonify({'message': f'Error creating or updating stock'}), 400
    return jsonify({'message': f'Stock created or updated successfully with ID: {updated_stock.id}'}), 200
