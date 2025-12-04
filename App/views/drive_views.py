from flask import Blueprint, request, jsonify
from App.controllers import *

drive_views = Blueprint('common_views', __name__)


@drive_views.route('/api/drives', methods=['GET'])
def list_drives():
    drives = user_view_drives()
    total = len(drives or [])
    
    if not drives:
        return jsonify({'message': f'No drives'}), 400
    items = [d.get_json() if hasattr(d, 'get_json') else d for d in (drives or [])]
    return jsonify({'drives': items, 'total': total}), 200

