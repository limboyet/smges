from flask import Flask, jsonify
from app.auth.resources import auth_bp
from app.contact.resources import contact_bp
from app.common.error_handling import *
from app.common.config import Config
from app.common.dbmodel import *

import logging

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config())
    app.config.from_prefixed_env()
    # Configuramos DB e inicializamos la BD
    if 'DB_TYPE' in app.config.keys():
        app.config['SQLALCHEMY_DATABASE_URI']= app.config['DB_TYPE'] + "+" + app.config['DB_DRIVER'] + "://" + app.config['DB_USER'] + ":" + app.config['DB_PASS'] + "@" + app.config['DB_SERVER'] + ":" + str(app.config['DB_PORT']) + "/" + app.config['DB_NAME']
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        try:
            init_db()
            app.logger.debug("Inicialización completada")
        except Exception as e:
            app.logger.error(e)

  # Registra manejadores de errores personalizados
    register_error_handlers(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(contact_bp)
    logging.basicConfig(level=app.config['LOG_LEVEL'])
    logger = logging.getLogger(__name__)

    # logger.setLevel(logging.DEBUG)
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

def init_db():
    import bcrypt

    user = Contact.query.first()
    if user:
        return
    new_contact = Contact(name='Administrator', surname1='', surname2='', email='admin@example.org')
    bytes = '1234'.encode('utf-8')
    salt = bcrypt.gensalt()
    new_user = User(username='admin', password=bcrypt.hashpw(bytes, salt), active=True, is_admin=True, contact_id=1)
    new_role = Role(name='admin',description='Administrador')
    db.session.add_all([new_contact, new_user, new_role])
    db.session.commit()
    new_user_role = RolesUsers(user_id='admin',role_id=1)
    db.session.add(new_user_role)
    new_permission = Permission(module='all',permission=PermissionEnum.Create)
    db.session.add(new_permission)
    new_permission2 = Permission(module='all',permission=PermissionEnum.Read)
    db.session.add(new_permission2)
    new_permission3 = Permission(module='all',permission=PermissionEnum.Update)
    db.session.add(new_permission3)
    new_permission4 = Permission(module='all',permission=PermissionEnum.Delete)
    db.session.add(new_permission4)
    db.session.commit()
    new_rpermission = RolesPermissions(role_id=1, permission_id=1)
    db.session.add(new_rpermission)
    new_rpermission2 = RolesPermissions(role_id=1, permission_id=2)
    db.session.add(new_rpermission2)
    new_rpermission3 = RolesPermissions(role_id=1, permission_id=3)
    db.session.add(new_rpermission3)
    new_rpermission4 = RolesPermissions(role_id=1, permission_id=4)
    db.session.add(new_rpermission4)
    db.session.commit()
