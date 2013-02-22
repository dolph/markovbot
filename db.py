import random

import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy.ext import declarative


engine = sql.create_engine('sqlite:///markov.db', echo=False)
Session = orm.sessionmaker(bind=engine)
Base = declarative.declarative_base()


class Link(Base):
    __tablename__ = 'links'

    id = sql.Column(sql.Integer, primary_key=True)
    word1 = sql.Column(sql.String, index=True)
    word2 = sql.Column(sql.String, index=True)
    word3 = sql.Column(sql.String)


Base.metadata.create_all(engine)


def reset():
    session = Session()
    session.query(Link).delete()
    session.commit()


def add_link(w1, w2, w3):
    session = Session()
    ref = Link(word1=w1, word2=w2, word3=w3)
    session.add(ref)
    session.commit()


def list_first():
    session = Session()
    refs = session.query(Link).filter_by(word1=None).all()
    return [(ref.word2, ref.word3) for ref in refs]


def get_first(*args):
    words = list_first(*args)
    random.shuffle(words)
    return words.pop()


def list_next(w1, w2):
    session = Session()
    refs = session.query(Link).filter_by(word1=w1, word2=w2).all()
    return [ref.word3 for ref in refs]


def get_next(*args):
    words = list_next(*args)
    random.shuffle(words)
    return words.pop()
