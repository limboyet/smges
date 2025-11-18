from flask import request, Blueprint, jsonify, render_template
from flask import current_app as app
from sqlalchemy.sql import func

from app.common.functions import check_access
from app.common.error_handling import InvalidLogin
from app.common.dbmodel import db, Contact, InstrumentRental, User
import jwt
import secrets
import bcrypt
import logging

contact_bp = Blueprint('contact_bp', __name__)

@contact_bp.route("/contact", methods=['GET'], defaults={'contact_id': None})
@contact_bp.route("/contact/<int:contact_id>/", methods=['GET'])
@check_access(resource="auth")
def get_contact(contact_id):
    return jsonify({'message': 'Solicitado ' + str(contact_id) }), 200

@contact_bp.route("/contact", methods=['POST'])
def post_contact():
    return jsonify({'message': 'Logged out successfully'}), 200

@contact_bp.route("/contact/<int:contact_id>", methods=['PUT'])
def put_contact(contact_id):
    return jsonify({'message': 'Logged out successfully'}), 200

@contact_bp.route("/contact/<int:contact_id>", methods=['PATCH'])
def patch_contact(contact_id):
    return jsonify({'message': 'Logged out successfully'}), 200

@contact_bp.route("/contact/<int:contact_id>", methods=['DELETE'])
def delete_contact(contact_id):
    return jsonify({'message': 'Logged out successfully'}), 200

@contact_bp.route("/contact/<int:contact_id>/rentals", methods=['GET'])
@check_access(resource="rentals")
def get_contact_rentals(contact_id):
    return jsonify({'message': 'Solicitado ' + str(contact_id) }), 200