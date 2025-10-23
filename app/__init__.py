from flask import Flask, jsonify

from app.auth.resources import auth_bp
from app.common.error_handling import ObjectNotFound, AppErrorBaseClass, BadObjectRequest, InvalidLogin, InvalidToken, DBConnection
from app.common.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config.from_prefixed_env()
    # Registra manejadores de errores personalizados
    register_error_handlers(app)
    app.register_blueprint(auth_bp)
    return app

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({'msg': 'Internal server error'}), 500
    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), 405
    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403
    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not Found error'}), 404
    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({'msg': str(e)}), 500
    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({'msg': str(e)}), 404
    @app.errorhandler(BadObjectRequest)
    def handle_bad_object_request_error(e):
        return jsonify({'msg': str(e)}), 400
    @app.errorhandler(InvalidLogin)
    def handle_invalid_login_error(e):
        return jsonify({'msg': str(e)}), 401
    @app.errorhandler(InvalidToken)
    def handle_invalid_token_error(e):
        return jsonify({'msg': str(e)}), 403
    @app.errorhandler(DBConnection)
    def handle_dbconnection_error(e):
        return jsonify({'msg': str(e)}), 500
