from flask import request, jsonify
from flask import current_app as app
from datetime import datetime

from app.common.error_handling import InvalidLogin, InvalidToken, DBConnection
from app.common.dbmodel import User,Session,db

import jwt
import MySQLdb

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------
def verify_token(request):
  token = request.headers.get('Authorization', '')
  if not token:
      raise InvalidLogin('Token not provided')
  token_parts = token.split(" ")
  if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
      raise InvalidToken('Invalid token format')
  token = token_parts[1]
  try:
      payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
      session_id=payload['session_id']
      username=payload['username']
      # db = db_connect()
      # c = db.cursor()
      # c.execute("""SELECT id, username, last_used FROM sessions WHERE id = %s and username = %s""", (session_id,username,))
      # if c.rowcount != 1:
      #   raise InvalidLogin('Authentication failed')
      # registro = c.fetchone()
      # db.close
      # if (datetime.now() - registro[2]).total_seconds() > app.config['SESSION_TIMEOUT']:
      #   db = db_connect()
      #   c = db.cursor()
      #   c.execute("""DELETE FROM sessions WHERE id = %s and username = %s""", (session_id,username,))
      #   db.close
      #   raise InvalidLogin('Session expired')
      return token
  except jwt.ExpiredSignatureError:
      raise InvalidToken('Token expired')
  except jwt.InvalidTokenError:
      raise InvalidToken('Invalid token')
  except Exception as e:
    print(e)
    raise e

def db_connect():
  try:
    db = MySQLdb.connect(
      host=app.config['DB_SERVER'],
      user=app.config['DB_USER'],
      password=app.config['DB_PASS'],
      database=app.config['DB_NAME']
    )
  except MySQLdb.Error as e:
    raise DBConnection('Database connection error')
  return db