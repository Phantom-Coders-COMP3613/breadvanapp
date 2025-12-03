from flask import Blueprint, request, jsonify
from App.controllers import *

common_views = Blueprint('common_views', __name__)


@common_views.route('/api/drives', methods=['GET'])
def list_drives():
    params = request.args
    page = int(params.get('page', 1))
    page_size = int(params.get('page_size', 20))

    drives = user_view_drives()

    total = len(drives or [])
    start = (page - 1) * page_size
    
    items = [d.get_json() if hasattr(d, 'get_json') else d for d in (drives or [])[start:start+page_size]]
    return jsonify({'Drives:': items, 'page': page, 'total': total}), 200

