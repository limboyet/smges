from flask import request, Blueprint, jsonify, url_for
from flask import current_app as app
from sqlalchemy.sql import func

from app.common.functions import check_access
from app.common.error_handling import InvalidLogin
from app.common.dbmodel import InstrumentRental
import json
import logging

rental_bp = Blueprint('rental_bp', __name__)

@rental_bp.route("/rental", methods=['GET'], defaults={'rental_id': None})
@rental_bp.route("/rental/<int:rental_id>/", methods=['GET'])
@check_access()
def get_rental(rental_id):
    try:
        if rental_id is not None:
            rentals = InstrumentRental.query.filter_by(id=rental_id).all()
        else:
            rentals = InstrumentRental.query.all()

        output = {"msg": "List of rentals", "rentals": []}
        return json.dumps(output)
    except Exception as e:
        app.logger.error(e)
        raise e

@rental_bp.route("/rental", methods=['POST'])
@check_access()
def post_rental():
    return jsonify({'message': 'Logged out successfully'}), 200

@rental_bp.route("/rental/<int:rental_id>", methods=['PUT'])
@check_access()
def put_rental(rental_id):
    return jsonify({'message': 'Logged out successfully'}), 200

@rental_bp.route("/rental/<int:rental_id>", methods=['PATCH'])
@check_access()
def patch_rental(rental_id):
    return jsonify({'message': 'Logged out successfully'}), 200

@rental_bp.route("/rental/<int:rental_id>", methods=['DELETE'])
@check_access()
def delete_rental(rental_id):
    return jsonify({'message': 'Logged out successfully'}), 200

@rental_bp.route("/rental/<int:rental_id>/rentals", methods=['GET'])
@check_access()
def get_rental_rentals(rental_id):
    return jsonify({'message': 'Solicitado ' + str(rental_id) }), 200