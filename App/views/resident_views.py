from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from App.api.security import role_required, current_user_id
from App.controllers import resident as resident_controller
from App.controllers import user as user_controller

resident_views = Blueprint('resident_views', __name__)


@resident_views.route('/api/resident/me', methods=['GET'])
@jwt_required()
@role_required('Resident')
def me():
    uid = current_user_id()
    return jsonify({'id': uid}), 200


@resident_views.route('/api/resident/stops', methods=['POST'])
@jwt_required()
@role_required('Resident')
def create_stop():
    data = request.get_json() or {}
    drive_id = data.get('drive_id')
    if not drive_id:
        return jsonify({'error': {'code': 'validation_error', 'message': 'drive_id required'}}), 422
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    stop = resident_controller.resident_request_stop(resident, drive_id)
    out = stop.get_json() if hasattr(stop, 'get_json') else stop
    return jsonify(out), 201


@resident_views.route('/api/resident/stops/<int:stop_id>', methods=['DELETE'])
@jwt_required()
@role_required('Resident')
def delete_stop(stop_id):
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    resident_controller.resident_cancel_stop(resident, stop_id)
    return '', 204


@resident_views.route('/api/resident/inbox', methods=['GET'])
@jwt_required()
@role_required('Resident')
def inbox():
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    items = resident_controller.resident_view_inbox(resident)
    items = [i.get_json() if hasattr(i, 'get_json') else i for i in (items or [])]
    return jsonify({'items': items}), 200


@resident_views.route('/api/resident/driver-stats', methods=['GET'])
@jwt_required()
@role_required('Resident')
def driver_stats():
    params = request.args
    driver_id = params.get('driver_id')
    if not driver_id:
        return jsonify({'error': {'code': 'validation_error', 'message': 'driver_id is required'}}), 422
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    try:
        stats = resident_controller.resident_view_driver_stats(resident, int(driver_id))
    except ValueError as e:
        return jsonify({'error': {'code': 'not_found', 'message': str(e)}}), 404
    return jsonify({'stats': stats}), 200

@resident_views.route('/api/resident/watch-schedule', methods=['POST'])
@jwt_required()
@role_required('Resident')
def watch_schedule():
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    resident_controller.resident_watch_schedule(resident)
    return '', 204

@resident_views.route('/api/resident/unwatch-schedule', methods=['POST'])
@jwt_required()
@role_required('Resident')
def unwatch_schedule():
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    resident_controller.resident_unwatch_schedule(resident)
    return '', 204

@resident_views.route('/api/resident/notify', methods=['POST'])
@jwt_required()
@role_required('Resident')
def notify():
    data = request.get_json() or {}
    message = data.get('message')
    if not message:
        return jsonify({'error': {'code': 'validation_error', 'message': 'message is required'}}), 422
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    resident_controller.resident_update(resident, message)
    return '', 204

@resident_views.route('/api/resident/notifications', methods=['GET'])
@jwt_required()
@role_required('Resident')
def notifications():
    uid = current_user_id()
    resident = user_controller.get_user(uid)
    notifications = resident_controller.resident_view_notifications(resident)
    notifications = [n.get_json() if hasattr(n, 'get_json') else n for n in (notifications or [])]
    return jsonify({'notifications': notifications}), 200