from datetime import datetime
from flaskr import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<User id={id} user_name={user_name!r}>'.format(
                id=self.id, user_name=self.user_name)

class QAmenu(db.Model):
    __tablename__ = 'qamenu'
    id = db.Column(db.Integer, primary_key=True)
    qa_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<QAmenu id={id} qa_name={qa_name!r}>'.format(
                id=self.id, qa_name=self.qa_name)

def init():
    db.create_all()
