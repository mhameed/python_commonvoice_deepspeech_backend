import uuid
from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy import UniqueConstraint

class Sentence(db.Model):
    id = db.Column(db.String(192), primary_key=True)
    language = db.Column(db.String(7), nullable=False, default='en')
    text = db.Column(db.String(255), nullable=False, unique=True)
    clips = relationship("Clip", back_populates="sentence")

    def __init__(self, *args, **kwargs):
        super(Sentence, self).__init__()
        self.id = kwargs.get('id', uuid.uuid4().hex)
        if not self.id.startswith('t-'):
            self.id = 't-' + self.id
        self.text = kwargs.get('text')
        self.language = kwargs.get('language')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<sentence('%s', '%s', '%s')>" % (self.id, self.language, self.text)

    def to_dict(self):
        return {'id':self.id, 'language':self.language, 'text':self.text}

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()


class Clip(db.Model):
    id = db.Column(db.String(192), primary_key=True)
    sentence_id = db.Column(db.String(192), ForeignKey('sentence.id'))
    sentence = relationship("Sentence", back_populates="clips")
    positiveVotes = db.Column(db.Integer)
    negativeVotes = db.Column(db.Integer)
    data = db.Column(db.LargeBinary)

    def __init__(self, *args, **kwargs):
        super(Clip, self).__init__()
        self.id = kwargs.get('id', uuid.uuid4().hex)
        if not self.id.startswith('a-'):
            self.id = 'a-' + self.id
        self.sentence_id = kwargs.get('sentence_id')
        self.positiveVotes = 0
        self.negativeVotes = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<clip('%s', '%s', %d, %d)>" % (self.id, self.sentence_id, self.positiveVotes, self.negativeVotes)

    def to_dict(self):
        return {'id':self.id, 'sentence_id':self.sentence_id, 'positive':self.positiveVotes, 'negative':self.negativeVotes}

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

class Unrecognized(db.Model):
    id = db.Column(db.String(192), primary_key=True)

    def __init__(self, *args, **kwargs):
        super(Unrecognized, self).__init__()
        self.id = kwargs.get('id', uuid.uuid4().hex)
        if not self.id.startswith('u-'):
            self.id = 'u-' + self.id

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<unrecognized('%s',)>" % self.id

    def to_dict(self):
        return {'id':self.id}

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

# vim: sw=4 ts=4 sts=4 expandtab
