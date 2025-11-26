from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token # Make sure this is imported

auth_views = Blueprint('auth_views', __name__)

@auth_views.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    user = user_controller.verify_user(username, password) 

    if user:

        additional_claims = {'role': user.role} 
        
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200
    
    return jsonify({'error': 'Invalid username or password'}), 401