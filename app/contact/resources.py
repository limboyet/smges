from flask import request, Blueprint, jsonify, render_template
from flask import current_app as app
from sqlalchemy.sql import func

from app.common.functions import check_access
from app.common.error_handling import InvalidLogin
from app.common.dbmodel import db, Contact, InstrumentRental, User
import json
import logging

contact_bp = Blueprint('contact_bp', __name__)

@contact_bp.route("/contact", methods=['GET'], defaults={'contact_id': None})
@contact_bp.route("/contact/<int:contact_id>/", methods=['GET'])
@check_access(resource="auth")
def get_contact(contact_id):
    if contact_id is not None:
        contacts = Contact.query.filter_by(id=contact_id).all()
    else:
        contacts = Contact.query.all()

    output = {"msg": "List of contacts", "contacts": []}
    for c in contacts:
        tmpobject = { "id": c.id, "name": c.name, "surname1": c.surname1, "surname2": c.surname2}
        if c.id_type is not None:
            tmpobject['id_type'] = c.id_type
        if c.id_number is not None:
            tmpobject['id_number'] = c.id_number

        output["contacts"].append(tmpobject)
    return json.dumps(output)

@contact_bp.route("/contact", methods=['POST'])
@check_access(resource="auth")
def post_contact():
    return jsonify({'message': 'Logged out successfully'}), 200

@contact_bp.route("/contact/<int:contact_id>", methods=['PUT'])
@check_access(resource="auth")
def put_contact(contact_id):
    return jsonify({'message': 'Logged out successfully'}), 200

@contact_bp.route("/contact/<int:contact_id>", methods=['PATCH'])
@check_access(resource="auth")
def patch_contact(contact_id):
    return jsonify({'message': 'Logged out successfully'}), 200

@contact_bp.route("/contact/<int:contact_id>", methods=['DELETE'])
@check_access(resource="auth")
def delete_contact(contact_id):
    return jsonify({'message': 'Logged out successfully'}), 200

@contact_bp.route("/contact/<int:contact_id>/rentals", methods=['GET'])
@check_access(resource="rentals")
def get_contact_rentals(contact_id):
    return jsonify({'message': 'Solicitado ' + str(contact_id) }), 200