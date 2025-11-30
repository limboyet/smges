from flask import request, Blueprint, jsonify, url_for
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
    try:
        if contact_id is not None:
            contacts = Contact.query.filter_by(id=contact_id).order_by(Contact.id.asc()).all()
        else:
            contacts = Contact.query.order_by(Contact.id.asc()).all()

        output = {"msg": "List of contacts", "contacts": []}
        for c in contacts:
            new_contact = { "id": c.id, "name": c.name, "surname1": c.surname1, "surname2": c.surname2}
            if c.id_type is not None:
                new_contact['id_type'] = c.id_type
            if c.id_number is not None:
                new_contact['id_number'] = c.id_number
            new_contact['uri'] = url_for('contact_bp.get_contact', contact_id=c.id, _external=True)
            new_contact["rentals"] = []
            new_contact["membressy"] = []
            for r in c.rentals:
                new_rental = { "id": r.id, "active": r.active, "uri": url_for('rental_bp.get_rental', rental_id=r.id, _external=True) }
                new_contact["rentals"].append(new_rental)
            if len(new_contact["rentals"]) == 0:
                new_contact.pop('rentals', None)
            for m in c.membressy:
                new_membressy = { "id": m.id, "type": m.member_type.value[1], "active": m.active, "uri": "tobedetermined" }
                new_contact["membressy"].append(new_membressy)
            if len(new_contact["membressy"]) == 0:
                new_contact.pop('membressy', None)
            output["contacts"].append(new_contact)
        return json.dumps(output)
    except Exception as e:
        app.logger.error(e)
        raise e

@contact_bp.route("/contact", methods=['POST'])
@check_access()
def post_contact():
    # new_contact = "uri": url_for('rental_bp.get_rental', rental_id=r.id, _external=True) }
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
