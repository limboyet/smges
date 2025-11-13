from flask import request
from flask import current_app as app
from datetime import datetime
from sqlalchemy import and_

from app.common.error_handling import InvalidLogin, InvalidToken, NoAuthorizationError
from app.common.dbmodel import RolesUsers,Session,db

import jwt
import logging

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------
def decode_token(token):
    return jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

def verify_token():
    token = request.headers.get('Authorization', '')
    if not token:
        raise InvalidLogin('Token not provided')
    token_parts = token.split(" ")
    if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
        raise InvalidToken('Invalid token format')
    token = token_parts[1]
    try:
        payload = decode_token(token)
        session_id=payload['session_id']
        username=payload['username']
        session = Session.query.filter(and_(Session.user_id == username, Session.id == session_id)).first()
        if not session:
            raise InvalidLogin('Invalid Session')
        if (datetime.now() - session.last_used).total_seconds() > app.config['SESSION_TIMEOUT']:
            logging.info('Usuario ' + username + ': Sesión expirada')
            db.session.delete(session)
            db.session.commit()
            raise InvalidLogin('Session expired')
        return token
    except jwt.ExpiredSignatureError:
        raise InvalidToken('Token expired')
    except jwt.InvalidTokenError:
        raise InvalidToken('Invalid token')
    except Exception as e:
        logging.error(e)
        raise e

# @check_access decorator function
def check_access(roles = []):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            # calling @jwt_required()
            payload = decode_token(verify_token())
            user_roles = RolesUsers.query.filter_by(user_id=payload['username']).all()
            if "all" in roles:
                return f(*args, **kwargs)
            for role in roles:
                if role in user_roles:
                    logging.debug("check_access: User " + payload['username'] + " is authorized by role " + role)
                    return f(*args, **kwargs)
            # logging.error("check_access: User " + payload['username'] + " not authorized to access " + request.query_string)
            logging.error("url=" + str(request.url_rule) + " User " + payload['username'] + " is not allowed.")
            raise NoAuthorizationError("User " + payload['username'] + " is not allowed.")
        return decorator_function
    return decorator
