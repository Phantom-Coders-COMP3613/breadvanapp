from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.views.auth import auth_views
from App.controllers import driver as driver_controller
from App.controllers import user as user_controller
from App.views import user as user_views
from App.controllers import *

driver_views = Blueprint('driver_views', __name__, url_prefix='/api/driver')


@driver_views.route('/me', methods=['GET'])
@jwt_required()
@login_required(Driver)
def me():
    return jsonify({'id': current_user.id}), 200


@driver_views.route('/api/driver/drives', methods=['GET'])
@jwt_required()
@login_required(Driver)
def list_drives():
    params = request.args
    page = int(params.get('page', 1))
    page_size = int(params.get('page_size', 20))
    
    
    driver = current_user
    drives = driver_controller.driver_view_drives(driver)

    total = len(drives or [])
    start = (page - 1) * page_size
    
    items = [d.get_json() if hasattr(d, 'get_json') else d for d in (drives or [])[start:start+page_size]]
    return jsonify({'items': items, 'page': page, 'total': total}), 200


@driver_views.route('/api/driver/drives', methods=['POST'])
@jwt_required()
@login_required(Driver)
def create_drive():
    data = request.get_json() or {}

    required= ['street_id', 'date', 'time']
    missing= [f for f in required if f not in data.get(f)]
    if missing:
        return jsonify({
            'error': {
                'code': 'validation_error', 
                'message': f'Missing required fields: {", ".join(missing)}'
            }
        }), 422
    
    driver = current_user
    drive = driver_controller.driver_schedule_drive(driver, data.get('area_id'),data.get('street_id'), data.get('date'), data.get('time'))
    

    out = drive.get_json() if hasattr(drive, 'get_json') else drive
    return jsonify(out), 201

@driver_views.route('/driver/drives', methods=['POST'])
@jwt_required()
@role_required('Driver')
def create_drive_alt():
    return create_drive()
    
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
    results = driver_controller.driver_end_drive(current_user)
    return jsonify({'id': getattr(results, 'id', drive_id), 'status': 'ended'}), 200


@driver_views.route('/drives/<int:drive_id>/cancel', methods=['POST'])
@jwt_required()
@login_required(Driver)
def cancel_drive(drive_id):
    driver_controller.driver_cancel_drive(current_user, drive_id)
    return jsonify({'id': drive_id, 'status': 'cancelled'}), 200


@driver_views.route('/drives/<int:drive_id>/requested-stops', methods=['GET'])
@jwt_required()
@login_required(Driver)
def requested_stops(drive_id):
    stops = driver_controller.driver_view_requested_stops(current_user, drive_id)
    items = [s.get_json() if hasattr(s, 'get_json') else s for s in (stops or [])]
    return jsonify({'items': items}), 200
