from flask import Flask, jsonify
from app.auth.resources import auth_bp
from app.common.error_handling import *
from app.common.config import Config
from app.common.dbmodel import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config.from_prefixed_env()
    # Configuramos DB e inicializamos la BD
    if 'DB_TYPE' in app.config.keys():
        app.config['SQLALCHEMY_DATABASE_URI']= app.config['DB_TYPE'] + "+" + app.config['DB_DRIVER'] + "://" + app.config['DB_USER'] + ":" + app.config['DB_PASS'] + "@" + app.config['DB_SERVER'] + ":" + str(app.config['DB_PORT']) + "/" + app.config['DB_NAME']
    db.init_app(app)
    migrate.init_app(app, db)

    # with app.app_context():
    #   new_contact = Contact(name='Administrator', surname1='', surname2='', email='admin@example.org')
    #   bytes = '1234'.encode('utf-8')
    #   salt = bcrypt.gensalt()
    #   new_user = User(username='admin', password=bcrypt.hashpw(bytes, salt), active=True, contact_id=1)
    #   db.session.add(new_contact)
    #   db.session.add(new_user)
    #   db.session.commit()

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
    @app.errorhandler(NoAuthorizationError)
    def handle_invalid_token_error(e):
        return jsonify({'msg': str(e)}), 401

