from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token # Make sure this is imported

auth_views = Blueprint('auth_views', __name__)

@auth_views.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    try:
        user = user.verify_user(username, password)
    except Exception:
        return jsonify({'error': 'Authentication service unavailable'}), 500

    if user:

        additional_claims = {'role': user.role} 
        
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200
    
    return jsonify({'error': 'Invalid username or password'}), 401