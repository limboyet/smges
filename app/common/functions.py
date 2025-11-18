from flask import request
from flask import current_app as app
from datetime import datetime
from sqlalchemy import and_, or_
from functools import wraps

from app.common.error_handling import InvalidLogin, InvalidToken, NoAuthorizationError
from app.common.dbmodel import RolesUsers, Session, db, User, PermissionEnum

import jwt

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
            app.logger.info('Usuario ' + username + ': Sesión expirada')
            db.session.delete(session)
            db.session.commit()
            raise InvalidLogin('Session expired')
        return token
    except jwt.ExpiredSignatureError:
        raise InvalidToken('Token expired')
    except jwt.InvalidTokenError:
        raise InvalidToken('Invalid token')
    except Exception as e:
        app.logger.error(e)
        raise e

# @check_access decorator function
def check_access(resource = None):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            # calling @jwt_required()
            payload = decode_token(verify_token())
            if resource is None:
                app.logger.error(str(request.url_rule).split('/')[1])
                module = str(request.url_rule).split('/')[1]
            else:
                module = resource
            match request.method: 
                case "GET":
                    permission = PermissionEnum.Read.value[0]
                case "POST":
                    permission = PermissionEnum.Create.value[0]
                case "PUT" | "PATCH":
                    permission = PermissionEnum.Update.value[0]
                case "DELETE":
                    permission = PermissionEnum.Delete.value[0]

            app.logger.debug("check permission " + permission + " for module: " + module)
            user = User.query.filter_by(username=payload['username']).first()
            app.logger.debug(user.roles)
            allowed_perm = False
            app.logger.error("Entor2")

            for role in user.roles:
                for perm in role.permissions:
                    if (perm.module == module or perm.module == 'all') and perm.permission.value[0] == permission:
                        allowed_perm =True
            if not allowed_perm:
                msg = "User " + payload['username'] + " is not allowed to " + permission + " on " + module
                app.logger.error(msg)
                raise NoAuthorizationError(msg)
            app.logger.debug("User " + payload['username'] + " is allowed to " + permission + " on " + module)
            return f(*args, **kwargs)
        return decorator_function
    return decorator
