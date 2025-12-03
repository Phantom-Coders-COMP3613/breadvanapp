from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user


from App.controllers import resident as resident_controller
from App.controllers import user as user_controller
from App.controllers import *



resident_views = Blueprint('resident_views', __name__)

@resident_views.route('/api/resident/stops', methods=['POST'])
@login_required('Resident')
def create_stop():
    data = request.get_json() or {}
    drive_id = data.get('drive_id')

    if not drive_id:
        return jsonify({'error': {'code': 'validation_error', 'message': 'drive_id required'}}), 422
    
    resident = current_user

    try: 
        stop = resident_controller.resident_request_stop(resident, drive_id)
        out = stop.get_json() if hasattr(stop, 'get_json') else stop
        return jsonify(out), 201

    except ValueError as e:
        return jsonify({'error': {'code': 'bad_request', 'message': str(e)}}), 404
    
@resident_views.route('/resident/stops/<int:stop_id>', methods=['DELETE'])
@login_required('Resident')
def delete_stop(stop_id):
    
    resident = current_user
    
    try:
        resident_controller.resident_cancel_stop(resident, stop_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': {'code': 'not_found', 'message': str(e)}}), 404

@resident_views.route('/api/resident/driver-stats', methods=['GET'])
@login_required(Resident)
def driver_stats():
    data = request.json
    driver = resident_view_driver_status(data['driver_id'])
    if not driver:
        return jsonify({'message': f'Error returning driver'}), 400
    return jsonify({'status': 'success', 'message': f'Driver returned successfully with ID: {driver.id}, Status: {driver.status}'}), 200
   

@resident_views.route('/api/resident/watch-schedule', methods=['POST'])
@login_required(Resident)
def watch_schedule():
   
    resident = current_user
    resident_controller.resident_watch_schedule(resident)
    return '', 204

@resident_views.route('/api/resident/unwatch-schedule', methods=['POST'])
@login_required(Resident)
def unwatch_schedule():
    
    resident = current_user
    resident_controller.resident_unwatch_schedule(resident)
    return '', 204

@resident_views.route('/api/resident/notifications', methods=['GET'])
@login_required(Resident)
def notifications():
    
    resident= resident_view_notifications(current_user)
    
    if not resident:
        return jsonify({'error': {'code': 'not_found', 'message': 'Resident not found'}}), 404
    return jsonify({'notifications': notifications}), 200
