from app import db
from datetime import datetime
import os
# from sqlalchemy.dialects.postgresql import JSON

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64))
    message = db.Column(db.String())
    passwd_hash = db.Column(db.String(128))
    create_date = db.Column(db.Date)
    read_date = db.Column(db.Date)
    is_read = db.Column(db.Boolean, default=False)

    def __init__(self, message_txt, passwd_hash):
        self.uuid = os.urandom(24).hex()
        self.message = message_txt
        self.passwd_hash = passwd_hash
        self.create_date = datetime.now().strftime('%Y-%m-%d')

    def addToDB(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<id {self.id}>'