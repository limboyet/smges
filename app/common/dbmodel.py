from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
# from flask import current_app as app
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate

import uuid
from enum import Enum

# from app import db
db = SQLAlchemy()
migrate = Migrate()

# ---------------- Helper classes ----------------
# from sqlalchemy.ext.declarative import DeclarativeMeta
# import json

# ---------------- Database Models ----------------
# ---------------- Relation tables ----------------
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    user_id = db.Column(db.String(20), db.ForeignKey('appuser.username'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)

class RolesPermissions(db.Model):
    __tablename__ = 'roles_permissions'
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)

class InstrumentRental(db.Model):
    __tablename__ = 'rental'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instrument.id'), primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    startdate = db.Column(db.DateTime(), nullable=False)
    enddate = db.Column(db.DateTime())

# ---------------- Resources tables ----------------
class Session(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('appuser.username'))
    start = db.Column(db.DateTime())
    last_used = db.Column(db.DateTime())

    # Relationships
    # one-to-many
    user = db.relationship('User', back_populates='sessions')

class User(db.Model):
    __tablename__ = 'appuser'
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, default=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)

    # Relationships
    # many-to-many
    roles = db.relationship('Role', secondary=RolesUsers.__table__, back_populates='users')
    # one-to-many
    sessions = db.relationship('Session', back_populates='user')
    # one-to-one
    contact = db.relationship('Contact', back_populates='user')
    
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80))

    # Relationships
    # many-to-many
    users = db.relationship('User', secondary=RolesUsers.__table__, back_populates='roles')
    permissions = db.relationship('Permission', secondary=RolesPermissions.__table__, back_populates='roles')

class PermissionEnum(Enum):
    Create = "C", "CREATE"
    Read = "R", "READ"
    Update = "U", "UPDATE"
    Delete = "D", "DELETE"

class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    module = db.Column(db.String(80))
    permission = db.Column(db.Enum(PermissionEnum))
    UniqueConstraint(module, permission, name="permission_constraint_01")

    # Relationships
    # many-to-may
    roles = db.relationship('Role', secondary=RolesPermissions.__table__, back_populates='permissions')

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    surname1 = db.Column(db.String(50))
    surname2 = db.Column(db.String(50))
    email = db.Column(db.String(255))
    id_type = db.Column(db.String(50))
    id_number = db.Column(db.String(50))

    # Relationships
    # one-to-one
    user = db.relationship('User', uselist=False, back_populates='contact')
    # one-to-many
    rentals = db.relationship('Instrument', secondary=InstrumentRental.__table__, back_populates='rentals')

class InstrumentType(db.Model):
    __tablename__ = 'instrumentType'
    id = db.Column(db.String(50), primary_key=True)

class Instrument(db.Model):
    __tablename__ = 'instrument'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    type = db.Column(db.String(50), db.ForeignKey('instrumentType.id'), nullable=False)
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    serial = db.Column(db.String(50))
    active = db.Column(db.Boolean(), nullable=False, default=True)
    startdate = db.Column(db.DateTime(), nullable=False)
    enddate = db.Column(db.DateTime())
    # Relationship with InstrumentRental
    rentals = db.relationship('Contact', secondary=InstrumentRental.__table__, back_populates='rentals')
