from flask import request, Blueprint, jsonify
from flask import current_app as app
from sqlalchemy.sql import func, and_, or_

from app.common.functions import verify_token, decode_token
from app.common.error_handling import InvalidLogin,NoAuthorizationError, BadObjectRequest
from app.common.dbmodel import User,Session,db
import jwt
import secrets
import bcrypt
import json

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/auth/login", methods=['POST'])
def auth_login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            raise InvalidLogin('Both username and password are required')
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                session_id = secrets.token_urlsafe(64)
                token = jwt.encode({'username': username, 'session_id': session_id}, app.config['SECRET_KEY'], algorithm=app.config['JWT_ALGORITHM'])
                # login_user(user)
            else:
                raise InvalidLogin('Authentication failed')
        else:
            raise InvalidLogin('Authentication failed')
        session = Session(id = session_id, user_id = username, start = func.now(), last_used = func.now())
        db.session.add(session)
        db.session.commit()
        return jsonify({'token': token}), 200
    except Exception as e:
        print(e)
        raise e

@auth_bp.route("/auth/logout", methods=['POST'])
def auth_logout():
    try:
        token = verify_token()
        payload = decode_token(token)
        username=payload['username']
        app.logger.debug(str(request.url_rule) + ': Start user ' + username + ' logout with valid token')
        session_id=payload['session_id']
        Session.query.filter_by(id=session_id).delete()
        db.session.commit()
        app.logger.debug(str(request.url_rule) + ': User ' + username + ' session removed')
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        app.logger.error(e)
        raise e

@auth_bp.route("/auth/session", methods=['GET'], defaults={'session_id': None})
@auth_bp.route("/auth/session/<string:session_id>/", methods=['GET'])
def auth_sessions(session_id):
    try:
        token = verify_token()
        payload = decode_token(token)
        username=payload['username']
        app.logger.debug(str(request.url_rule) + ': Start user ' + username + ' session query with valid token')
        user = User.query.filter_by(username=username).first()
        if user.is_admin:
            if session_id is not None:
                sessions = Session.query.filter_by(id=session_id).all()
            else:
                sessions = Session.query.all()
        else:
            if session_id is not None:
                sessions = Session.query.filter(and_(Session.id==session_id, Session.user_id==username)).all()
            else:
                sessions = Session.query.filter_by(user_id=username).all()                                
        output = {"msg": "List of sessions", "sessions": []}
        for s in sessions:
            output["sessions"].append({ "id": s.id, "user": s.user_id, "start": str(s.start)})

        return json.dumps(output)
    except Exception as e:
        app.logger.error(e)
        raise e

@auth_bp.route("/auth/session/<string:session_id>/", methods=['DELETE'])
def auth_delete_session(session_id):
    try:
        if session_id is None:
            msg = f"Session id cannot be null"
            raise BadObjectRequest(msg)
        token = verify_token()
        payload = decode_token(token)
        username=payload['username']
        user = User.query.filter_by(username=username).first()
        session = Session.query.filter_by(id=session_id).first()
        if user.is_admin or session.user_id == username:
            Session.query.filter_by(id=session_id).delete()
            db.session.commit()
        else:
            msg = f"User {payload['username']} is not allowed to delete session"
            app.logger.error(msg)
            raise NoAuthorizationError(msg)
        output = {"msg": f"Session {session_id} deleted"}
        return json.dumps(output)
    except Exception as e:
        app.logger.error(e)
        raise e
