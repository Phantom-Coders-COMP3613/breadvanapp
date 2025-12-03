from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_resident,
    create_driver
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/api/resident', methods=['POST'])
def create_resident_api():
    data = request.json
    resident = create_resident(data['username'], data['password'], data['area_id'], data['street_id'], data['house_number'])
    if resident:
        return jsonify({'message': f'Resident created successfully with ID: {resident.id}'}), 201
    return jsonify({'error': 'Failed to create resident'}), 400

@user_views.route('/api/driver', methods=['POST'])
def create_driver_api():
    data = request.json
    driver = create_driver(data['username'], data['password'])
    if driver:
        return jsonify({'message': f'Driver created successfully with ID: {driver.id}'}), 201
    return jsonify({'error': 'Failed to create driver'}), 400

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')