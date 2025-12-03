from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers import *



resident_views = Blueprint('resident_views', __name__)

@resident_views.route('/api/resident/stops', methods=['POST'])
@login_required(Resident)
def create_stop():
    data = request.json
    drive_id = data['drive_id']

    resident = current_user
    stop = resident_request_stop(resident, drive_id)
    if not stop:
        return jsonify({'message': f'Error creating stop'}), 400
    return jsonify({'status': 'success', 'message': f'Stop created successfully with ID: {stop.id}'}), 200

    
@resident_views.route('/api/resident/stops/<int:drive_id>', methods=['DELETE'])
@login_required(Resident)
def delete_stop(drive_id):
    
    resident = current_user
    
    stop = resident_cancel_stop(resident, drive_id)
    if not stop:
        return jsonify({'message': f'Error deleting stop'}), 400
    return jsonify({'status': 'success', 'message': f'Stop ID:{stop.id} for Drive ID:{drive_id} made by Resident ID:{resident.id} deleted successfully'}), 200

@resident_views.route('/api/resident/driver-status', methods=['GET'])
@login_required(Resident)
def driver_stats():
    data = request.json
    driver = resident_view_driver_status(data['driver_id'])
    if not driver:
        return jsonify({'message': f'Error returning driver'}), 400
    
    area = Area.query.get(driver.areaId)
    street = Street.query.get(driver.streetId)
    if area:
        return jsonify({'status': 'success', 'message': f'Driver returned successfully with ID: {driver.id}, Status: {driver.status}, Area: {area.name}'}), 200
    elif area and street:
            return jsonify({'status': 'success', 'message': f'Driver returned successfully with ID: {driver.id}, Status: {driver.status}, Street: {street.name}, Area: {area.name}'}), 200
    return jsonify({'status': 'success', 'message': f'Driver returned successfully with ID: {driver.id}, Status: {driver.status}'}), 200

@resident_views.route('/api/resident/watch-schedule', methods=['POST'])
@login_required(Resident)
def watch_schedule():
   
    resident = current_user
    schedule = resident_watch_schedule(resident)
    if resident in schedule.residents:
        return jsonify({'status': 'success', 'message': f'Resident ID: {resident.id} successfully subscribed!'}), 200
    return jsonify({'message': f'Error subscribing resident'}), 400

@resident_views.route('/api/resident/unwatch-schedule', methods=['POST'])
@login_required(Resident)
def unwatch_schedule():
    
    resident = current_user
    schedule = resident_unwatch_schedule(resident)
    if resident not in schedule.residents:
        return jsonify({'status': 'success', 'message': f'Resident ID: {resident.id} successfully unsubscribed!'}), 200
    return jsonify({'message': f'Error unsubscribing resident'}), 400

@resident_views.route('/api/resident/inbox', methods=['GET'])
@login_required(Resident)
def notifications():
    
    inbox = resident_view_inbox(current_user)
    total = len(inbox or [])
    
    if not inbox:
        return jsonify({'message': f'No notifications'}), 400
    items = [d.get_json() if hasattr(d, 'get_json') else d for d in (inbox or [])]
    return jsonify({'Notifications:': items, 'total': total}), 200
