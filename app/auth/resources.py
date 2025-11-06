from flask import request, Blueprint, jsonify, render_template
from flask import current_app as app
from flask_login import LoginManager, login_user, logout_user, current_user

from app.common.functions import verify_token, db_connect
from app.common.error_handling import InvalidLogin
from app.common.dbmodel import User
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
    return jsonify({'token': token}), 200
  except Exception as e:
    print(e)
    raise e
      # db = db_connect()
      # c = db.cursor()
      # c.execute("""SELECT username, password_hash FROM users WHERE username = %s""", (username,))
      # if c.rowcount != 1:
      #   raise InvalidLogin('Authentication failed')
      # registro = c.fetchone()
      # if bcrypt.checkpw(password.encode(), registro[1].encode()):
      #   session_id = secrets.token_urlsafe(64)
      #   token = jwt.encode({'username': username, 'session_id': session_id}, app.config['SECRET_KEY'], algorithm='HS256')
      # else:
      #   raise InvalidLogin('Authentication failed')
      # #Register session
      # try:
      #   c.execute("""insert into sessions(id, username, start, last_used) values (%s,%s,now(),now())""", (session_id,username,)  )
      #   db.commit()
      # except Exception as e:
      #   db.rollback()
      #   raise e
      # db.close()
      # return jsonify({'token': token}), 200

@auth_bp.route("/auth/logout", methods=['POST'])
def logout():
  token_valid = verify_token(request)
  payload = jwt.decode(token_valid, app.config['SECRET_KEY'], algorithms=['HS256'])
  session_id=payload['session_id']
  username=payload['username']
  db = db_connect()
  c = db.cursor()
  try:
    c.execute("""DELETE FROM sessions WHERE id = %s and username = %s""", (session_id,username,))
    db.commit()
  except Exception as e:
    db.rollback()
    raise e
  db.close()
  return jsonify({'message': 'Logged out successfully'}), 200

# # Signin route for user login
@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    msg = ""
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
    #     if user:
    #         if user.password == request.form['password']:
    #             login_user(user)
    #             return redirect(url_for('index'))
    #         else:
    #             msg = "Wrong password"
    #     else:
    #         msg = "User doesn't exist"
    #     return render_template(msg)
    return jsonify({'MSG': msg}), 200