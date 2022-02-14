from app import db, getRandomString
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy import UniqueConstraint

class Sentence(db.Model):
    id = db.Column(db.String(192), primary_key=True)
    language = db.Column(db.String(7), nullable=False, default='en')
    user = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(100))
    clips = relationship("Clip", back_populates="sentence")

    def __init__(self, *args, **kwargs):
        super(Sentence, self).__init__()
        self.id = kwargs.get('id', getRandomString(prefix='Sentence'))
        if not self.id.startswith('Sentence'):
            self.id = 'Sentence' + self.id
        self.text = kwargs.get('text')
        self.language = kwargs.get('language')
        self.user = kwargs.get('user')
        self.source = kwargs.get('source', '')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<sentence('%s', '%s', '%s', '%s', '%s')>" % (self.id, self.language, self.user, self.text, self.source)

    def to_dict(self):
        return {'id':self.id, 'language':self.language, 'text':self.text, 'source':self.source, 'user':self.user}

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
    language = db.Column(db.String(7), nullable=False, default='en')
    user = db.Column(db.String(20), nullable=False)
    positiveVotes = db.Column(db.Integer)
    negativeVotes = db.Column(db.Integer)
    data = db.Column(db.LargeBinary(length=(2**32)-1))
    dataset_version = db.Column(db.String(7), nullable=False, default='next')
    dataset_type = db.Column(db.String(7), nullable=False, default='none')

    def __init__(self, *args, **kwargs):
        super(Clip, self).__init__()
        self.id = kwargs.get('id', getRandomString('Clip'))
        if not self.id.startswith('Clip'):
            self.id = 'Clip' + self.id
        self.sentence_id = kwargs.get('sentence_id')
        self.user = kwargs.get('user')
        self.language = kwargs.get('language')
        self.positiveVotes = 0
        self.negativeVotes = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<clip('%s', '%s', '%s', '%s', %d, %d)>" % (self.id, self.sentence_id, self.language, self.user, self.positiveVotes, self.negativeVotes)

    def to_dict(self):
        return {'id':self.id, 'sentence_id':self.sentence_id, 'positive':self.positiveVotes, 'negative':self.negativeVotes, 'language':self.language, 'user':self.user}

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

class Unrecognized(db.Model):
    id = db.Column(db.String(192), primary_key=True)
    language = db.Column(db.String(7), nullable=False, default='en')
    user = db.Column(db.String(20), nullable=False)
    data = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, *args, **kwargs):
        super(Unrecognized, self).__init__()
        self.id = kwargs.get('id', getRandomString('Unrecognized'))
        if not self.id.startswith('Unrecognized'):
            self.id = 'Unrecognized' + self.id
        self.user = kwargs.get('user')
        self.language = kwargs.get('language')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<unrecognized('%s', '%s', '%s')>" % (self.id, self.language, self.user)

    def to_dict(self):
        return {'id':self.id, 'language':self.language, 'user':self.user}

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

# vim: sw=4 ts=4 sts=4 expandtab
