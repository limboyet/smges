from flask import request, Blueprint, jsonify, render_template
from flask import current_app as app
from flask_login import LoginManager, login_user, logout_user, current_user
from sqlalchemy.sql import func

from app.common.functions import verify_token, db_connect
from app.common.error_handling import InvalidLogin
from app.common.dbmodel import User,Session,db
import jwt
import secrets
import bcrypt

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/auth/login", methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            raise InvalidLogin('Both username and password are required')
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                session_id = secrets.token_urlsafe(64)
                token = jwt.encode({'username': username, 'session_id': session_id}, app.config['SECRET_KEY'], algorithm='HS256')
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
def logout():
    token_valid = verify_token(request)
    payload = jwt.decode(token_valid, app.config['SECRET_KEY'], algorithms=['HS256'])
    session_id=payload['session_id']
    username=payload['username']
    Session.query.filter_by(id=session_id).delete()
    db.session.commit()
    return jsonify({'message': 'Logged out successfully'}), 200
