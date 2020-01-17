from datetime import datetime
import logging
import json

from marshmallow import fields, Schema

from nl.carcharging.models.base import Base, Session
from . import db


class RfidModel(Base):
    __tablename__ = 'rfid'

    rfid = db.Column(db.String(100), primary_key=True)
    enabled = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    last_used_at = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    vehicle_make = db.Column(db.String(100))
    vehicle_model = db.Column(db.String(100))
    get_odometer = db.Column(db.Boolean)
    license_plate = db.Column(db.String(20))
    valid_from = db.Column(db.DateTime)
    valid_until = db.Column(db.DateTime)

    api_access_token = db.Column(db.String(100))
    api_token_type = db.Column(db.String(100))
    api_created_at = db.Column(db.String(100))
    api_expires_in = db.Column(db.String(100))
    api_refresh_token = db.Column(db.String(100))

    def __init__(self):
        self.logger = logging.getLogger('nl.carcharging.models.RfidModel')
        self.logger.debug('Initializing RfidModel without data')


    def set(self, data):
        for key in data:
            setattr(self, key, data.get(key))
        self.allow = data.get('allow', False)
        self.created_at = data.get('created_at', datetime.now())
        self.modified_at = data.get('last_used_at', datetime.now())

    def save(self):
        session = Session()
        session.add(self)
        session.commit()

    def delete(self):
        session = Session()
        session.delete(self)
        session.commit()

    @staticmethod
    def get_all():
        session = Session()
        return session.query(RfidModel).all()

    @staticmethod
    def get_one(rfid):
        session = Session()
        return session.query(RfidModel)\
            .filter(RfidModel.rfid == str(rfid)).first()

    def __repr(self):
        return '<id {}>'.format(self.rfid)

    def to_str(self):
        return ({
                "rfid": str(self.rfid),
                "enabled": self.enabled,
                "created_at": (str(self.created_at.strftime("%d/%m/%Y, %H:%M:%S")) if self.created_at is not None else None),
                "last_used_at": (str(self.last_used_at.strftime("%d/%m/%Y, %H:%M:%S")) if self.last_used_at is not None else None),
                "name": str(self.name),
                "vehicle_make": str(self.vehicle_make),
                "vehicle_model": str(self.vehicle_model),
                "get_odometer": str(self.get_odometer),
                "license_plate": str(self.license_plate),
                "valid_from": (str(self.valid_from.strftime("%d/%m/%Y, %H:%M:%S")) if self.valid_from is not None else None),
                "valid_until": (str(self.valid_until.strftime("%d/%m/%Y, %H:%M:%S")) if self.valid_until is not None else None),
                "api_access_token": str(self.api_access_token),
                "api_token_type": str(self.api_token_type),
                "api_created_at": str(self.api_created_at),
                "api_expires_in": str(self.api_expires_in),
                "api_refresh_token": str(self.api_refresh_token)
            }
        )

class RfidSchema(Schema):
    """
    Rfid Schema
    """
    rfid = fields.Str(required=True)
    allow = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    last_used = fields.DateTime(dump_only=True)
    name = fields.Str(required=True)
    vehicle = fields.Str(required=True)
    license_plate = fields.Str(required=True)
    valid_from = fields.DateTime(dump_only=True)
    valid_until = fields.DateTime(dump_only=True)