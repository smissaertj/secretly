from app import db
import os
from sqlalchemy.dialects.postgresql import JSON

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64))
    text = db.Column(db.String(256))
    passwd_hash = db.Column(db.String(64))

    def __init__(self):
        self.uuid = os.random(24).hex()

    def __repr__(self):
        return f'<id {self.id}'