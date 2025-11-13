from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
# from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import uuid

# from app import db
db = SQLAlchemy()
migrate = Migrate()

# # ---------------- Association Table for User Roles ----------------
# roles_users = db.Table('roles_users',
#     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
# )

# ---------------- Database Models ----------------
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    user_id = db.Column(db.String(20), db.ForeignKey('appuser.username'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)

class RolesPermissions(db.Model):
    __tablename__ = 'roles_permissions'
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)

class Session(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('appuser.username'))
    start = db.Column(db.DateTime())
    last_used = db.Column(db.DateTime())

class User(db.Model, UserMixin):
    __tablename__ = 'appuser'
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, default=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)

    # Relationship with roles
    roles = db.relationship('RolesUsers', backref='User', lazy=True, cascade='all, delete-orphan')
    sessions = db.relationship('Session', backref='User', lazy=True, cascade='all, delete-orphan')

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('RolesUsers', backref='Role', lazy=True, cascade='all, delete-orphan')

class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    roles = db.relationship('RolesPermissions', backref='Permission', lazy=True, cascade='all, delete-orphan')

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    surname1 = db.Column(db.String(50))
    surname2 = db.Column(db.String(50))
    email = db.Column(db.String(255))
    # Relationship with roles
    roles = db.relationship('User', backref='Contact', lazy=True, cascade='all, delete-orphan')
