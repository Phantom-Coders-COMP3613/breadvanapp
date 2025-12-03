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
        return jsonify({'message': f'Error creating drive'}), 400
    return jsonify({'status': 'success', 'message': f'Drive created successfully with ID: {drive.id}'}), 200


@driver_views.route('/api/driver/drives/<int:drive_id>/start', methods=['POST'])
@jwt_required()
@login_required(Driver)
def start_drive(drive_id):
        try:
            driver= driver_controller.driver_start_drive(current_user, drive_id)
            if not driver:
                return jsonify({
                    "error": {
                    "code": "not_found",
                    "message": "Drive does not exist"
                    }
        }), 404
    
            return jsonify({'id': drive_id, 'status': 'started'}), 200
        except ValueError as e:  # Catch controller errors
            return jsonify({'error': {'code': 'not_found', 'message': str(e)}}), 404
        except Exception as e:
            return jsonify({'error': {'code': 'internal_error', 'message': str(e)}}), 500


@driver_views.route('/drives/<int:drive_id>/end', methods=['POST'])
@jwt_required()
@login_required(Driver)
def end_drive(drive_id):
    results = driver_end_drive(current_user)
    return jsonify({'id': getattr(results, 'id', drive_id), 'status': 'ended'}), 200


@driver_views.route('/api/driver/drives/<int:drive_id>/cancel', methods=['POST'])
@jwt_required()
@login_required(Driver)
def cancel_drive(drive_id):
    drive = driver_cancel_drive(current_user, drive_id)
    if not drive:
        return jsonify({'message': f'Error cancelling drive'}), 400
    return jsonify({'status': 'success', 'message': f'Drive cancelled successfully with ID: {drive.id}'}), 200



@driver_views.route('/api/driver/drives/<int:drive_id>/requested-stops', methods=['GET'])
@jwt_required()
@login_required(Driver)
def requested_stops(drive_id):
    stops = driver_view_requested_stops(current_user, drive_id)
    items = [s.get_json() if hasattr(s, 'get_json') else s for s in (stops or [])]
    return jsonify({'Stops': items}), 200
