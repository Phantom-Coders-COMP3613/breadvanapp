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

    
@resident_views.route('/api/resident/stops/<int:driveId>', methods=['DELETE'])
@login_required(Resident)
def delete_stop(driveId):
    
    resident = current_user
    
    stop = resident_cancel_stop(resident, driveId)
    if not stop:
        return jsonify({'message': f'Error deleting stop'}), 400
    return jsonify({'status': 'success', 'message': f'Stop deleted successfully'}), 200

@resident_views.route('/api/resident/driver-status/<int:driverId>', methods=['GET'])
@login_required(Resident)
def driver_stats(driverId):
    driver = resident_view_driver_status(driverId)
    if not driver:
        return jsonify({'message': f'Error returning driver'}), 400
    stats = [driver.get_json() if hasattr(driver, 'get_json') else driver]
    return jsonify({"stats": stats}), 200

@resident_views.route('/api/resident/watch-schedule', methods=['POST'])
@login_required(Resident)
def watch_schedule():
   
    resident = current_user
    schedule = resident_watch_schedule(resident)
    if resident in schedule.residents:
        return jsonify({'status': 'success', 'message': f'Resident ID: {resident.id} successfully subscribed!'}), 200
    return jsonify({'message': f'Error watching schedule'}), 400

@resident_views.route('/api/resident/unwatch-schedule', methods=['POST'])
@login_required(Resident)
def unwatch_schedule():
    
    resident = current_user
    schedule = resident_unwatch_schedule(resident)
    if resident not in schedule.residents:
        return jsonify({'status': 'success', 'message': f'Resident ID: {resident.id} successfully unsubscribed!'}), 200
    return jsonify({'message': f'Error unwatching schedule'}), 400

@resident_views.route('/api/resident/inbox', methods=['GET'])
@login_required(Resident)
def notifications():
    
    inbox = resident_view_inbox(current_user)
    total = len(inbox or [])
    
    if not inbox:
        return jsonify({'message': f'No notifications'}), 400
    items = [d.get_json() if hasattr(d, 'get_json') else d for d in (inbox or [])]
    return jsonify({'notifications': items, 'total': total}), 200
