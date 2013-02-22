import random
import re

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


def slugify(s):
    s = s.lower()
    s = s.replace(' ', '_')
    s = s.replace('-', '_')
    s = s.replace('/', '_')
    s = s.replace('.', '_')
    s = re.sub('\W', '', s)
    s = s.replace('_', ' ')
    s = re.sub('\s+', ' ', s)
    s = s.strip()
    s = s.replace(' ', '-')
    return s


def consume(s):
    s = slugify(s)
    s = s.split('-')

    for i, w in enumerate(s):
        w1 = s[i]
        w2 = s[i + 1] if i + 1 < len(s) else None
        w3 = s[i + 2] if i + 2 < len(s) else None

        if i == 0:
            add_link(None, w1, w2)

        if w2 is not None:
            add_link(w1, w2, w3)


def produce(w=None):
    s = []

    w1, w2 = get_first()
    s.append(w1)
    s.append(w2)

    w3 = True
    while w3:
        w3 = get_next(w1, w2)

        if w3 is not None:
            s.append(w3)

        w1 = w2
        w2 = w3

    return ' '.join(s)
