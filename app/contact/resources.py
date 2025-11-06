from flask import request, Blueprint, jsonify
from flask import current_app as app

from app.common.functions import verify_token, db_connect
from app.common.error_handling import InvalidLogin, ObjectNotFound
import jwt
import secrets
import bcrypt
import MySQLdb

person_bp = Blueprint('person_bp', __name__)

@person_bp.route("/person")
def login():
  try:
      username = request.json.get('username')
      password = request.json.get('password')
      if username is None or password is None:
        raise InvalidLogin('Both username and password are required')
      db = db_connect()
      c = db.cursor()
      c.execute("""SELECT username, password_hash FROM users WHERE username = %s""", (username,))
      if c.rowcount != 1:
        raise InvalidLogin('Authentication failed')
      registro = c.fetchone()
      if bcrypt.checkpw(password.encode(), registro[1].encode()):
        session_id = secrets.token_urlsafe(64)
        token = jwt.encode({'username': username, 'session_id': session_id}, app.config['SECRET_KEY'], algorithm='HS256')
      else:
        raise InvalidLogin('Authentication failed')
      #Register session
      try:
        c.execute("""insert into sessions(id, username, start, last_used) values (%s,%s,now(),now())""", (session_id,username,)  )
        print("Llego")
        db.commit()
      except Exception as e:
        db.rollback()
        raise e
      db.close()
      return jsonify({'token': token}), 200
  except Exception as e:
    print(e)
    raise e

